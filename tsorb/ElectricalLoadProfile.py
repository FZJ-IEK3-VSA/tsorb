from tsorb.utils.InputData import DataExchangeCsv
from tsorb.OccupancyModel import OccupancyModel
from tsorb.LoadModel import AppliancesModel
from tsorb.LoadModel import LightingModel
import numpy as np
import pandas as pd


class ElectricalLoadProfile(object):
    def __init__(
        self,
        data_ex=None,
        residents=2,
        random_app_seed_per_run=True,
        pre_setup=False,
        weather_data=None,
        resolved_load=False,
        get_hot_water=False,
        freq="60min",
        resample_mean=False,
    ):
        """
        Initializes an Electrical LoadProfile Model with the given Data.
        -----------------------------------------------------------------------
        Parameters:
            data_ex: DataExchange Object, optional (default= None)
                An Object to Exchange Data between the different Submodels used
                used to build th Electrical Load
            residents: int, optional (default = 2)
                Number of residents living in the Household
            random_app_per_run: int, optional (default=True)
                If set the setting of the Appliances owned in the household
                will be seeded. (Same "random" distribution for each
                Initilization with this seed)
            pre_setup: string, optional (default=False)
                If set to a directory Path as a string, a pre chosen setup for
                the Appliance distribution in the household will be
            weather_data: pd.DataFrame, optional (default=None)
                A time indexed pandas dataframe containing weather data with
                the GHI as a column.
            resolved_load: boolean, default: False
                If activated the load model does not only return the total
                load, instead it gives the load profile for each appliance.
            freq: str, default: 60min
                Frequency in which the resulting profile shall get returned.
            get_hot_water: bool, optional (default=False)
                If set, an extra hot water profile is created independent
                from the electricity load of the other devices.
            resample_mean: bool, optional (default=False)
                Decides if the time series get averaged or not for resampling.
        -----------------------------------------------------------------------
        """
        # Initalize DataExchange Object to Exchange data between Models
        if data_ex is None:
            self._data_ex = DataExchangeCsv()
        else:
            self._data_ex = data_ex

        self.resolved_load = resolved_load
        self.get_hot_water = get_hot_water
        self.freq = freq
        self.resample_mean = resample_mean

        if residents > 5:
            raise ValueError('maximum number of "residents" is 5')
        # init related OccupancyModel, LightingModel, AppliancesModel
        self.occ_model = OccupancyModel(self._data_ex, residents, four_states=True)
        self.lig_model = LightingModel(self._data_ex, self.occ_model, weather_data)
        self.app_model = AppliancesModel(
            self._data_ex,
            self.occ_model,
            random_app_seed_per_run,
            pre_setup,
            get_hot_water=self.get_hot_water,
        )

        self._run_for_year = True

    def run(self, year, day_of_week, day_in_year):
        """
        Runs an Electrical Load Profile Object for the given year and type of
        day (weekday or weekend)
        -----------------------------------------------------------------------
        Parameters:
            year: int, required
                Set the year in which the Electrical Profile will take place
            day_of_week: str, required
                String either it is a weekday "wd" or weekend "we"
            day_in_year: int, required
                numerical day in year counted from 01.01.xxxx counted as 1. 
                Is generated automatically when run in full year calculations
        -----------------------------------------------------------------------
        Returns:
            Saves the total electricity consumption in the given Electrical
            Load Profile, the total heat gain and the occupancy behavior
        """
        # Start the Occupancy Model needed by the following Models
        self.occ_model.run(day_of_week)
        # Run LightingModel and fetch total Consumption for one day (1440 mins)
        self.lig_model.run(year, day_of_week, day_in_year)
        # Run AppModel and fetch total Consumption for one day (1440 mins)
        self.app_model.run(year, day_of_week, day_in_year)
        # Combine App+Lig Consumption to the daily total Consumption
        self.total_consumption = (
            self.app_model.total_consumption + self.lig_model.total_consumption
        )

        if self.get_hot_water:
            self.total_hot_water = self.app_model.total_hot_water

        self.total_heat_gain = (
            self.app_model.total_heat_gain + self.lig_model.total_heat_gain
        )

    def set_seed(self, seed):
        """
        Sets the seed for the random number generation
        :param seed:
        """
        np.random.seed(seed)

    def run_for_year(self, year):
        """
        Repetetively starts the run function for an Electrical Load Profile for
        each day in the chosen year. It will automatically start the run for
        each working/weekend day in the different months.
        -----------------------------------------------------------------------
        Parameters:
            year: int, required
                Set the year in which the Calculation should take place
        -----------------------------------------------------------------------
        Returns:
            totalLoad: numpy array
                Numpy array with the yearly electrical energy demand with a 
                minutewise resolution.
        """

        days = pd.date_range(
            start=str(year), end=str(int(year) + 1), freq="D", tz="Europe/Berlin"
        )[:-1]

        number_days_in_year = len(days)
        # build an empty numpy array to later save the total_consumption
        self.total_load = np.empty(1440 * number_days_in_year, dtype=float)
        self.app_heat_gain = np.empty(1440 * number_days_in_year, dtype=float)
        self.occ_active = np.empty(144 * number_days_in_year, dtype=float)
        self.occ_not_active = np.empty(144 * number_days_in_year, dtype=float)
        if self.get_hot_water:
            self.hotWater = np.empty(1440 * number_days_in_year, dtype=float)

        self.light = np.empty(1440 * number_days_in_year, dtype=float)  # Test Lighting

        # coefficients for seasonal correction
        z = [
            -2.46333771e-10,
            2.09410267e-07,
            -4.91019666e-05,
            1.99475890e-03,
            1.13989689e00,
        ]

        # coefficients for correction of hot water demand
        cor_hotwater = 0.7

        if self.resolved_load:
            appload = np.empty(
                [len(self.app_model.loads), 1440 * number_days_in_year], dtype=float
            )
            app_names = [load.get_key for load in self.app_model.loads]

        # Loop through every day in the chosen year
        for ii, day in enumerate(days):
            # Differentiate between weekday or weekendday
            if day.dayofweek in (5, 6):
                day_of_week = "we"
            else:
                day_of_week = "wd"

            # calculate dynamic factor for seasonal correction
            f = sum(coeff * (day.dayofyear ** pot) for pot, coeff in enumerate(z[::-1]))

            # start the run function for the given day
            self.run(year, day_of_week, day_in_year=ii + 1)
            # Save the total_consumption in the totalLoad
            self.total_load[1440 * ii : 1440 * (ii + 1)] = self.total_consumption * f
            self.app_heat_gain[1440 * ii : 1440 * (ii + 1)] = self.total_heat_gain * f
            if self.get_hot_water:
                self.hotWater[1440 * ii : 1440 * (ii + 1)] = (
                    self.total_hot_water * cor_hotwater
                )
            self.occ_active[144 * ii : 144 * (ii + 1)] = self.occ_model.occ_activity
            self.occ_not_active[
                144 * ii : 144 * (ii + 1)
            ] = self.occ_model.occ_no_activity

            #
            if self.resolved_load:
                for iii, load in enumerate(self.app_model.loads):
                    appload[iii][1440 * ii : 1440 * (ii + 1)] = load.consumption * f

            self.light[1440 * ii : 1440 * (ii + 1)] = (
                self.lig_model.total_consumption * f
            )

        self._run_for_year = year

        if self.resolved_load:
            self.load_resolved = pd.DataFrame(
                appload.T,
                index=pd.date_range(
                    start=pd.datetime(year, 1, 1),
                    periods=len(self.total_load),
                    freq="1min",
                ),
                columns=app_names,
            )

            self.load_resolved["LIGHTS"] = self.light

            return self.load_resolved

        else:
            return self.total_load

    def get_rescheduled_profiles(self, year):
        """
        Gets the relevant profiles (total load, appHeatGain, occActive,
        occNotActive), reschedules them to the frequencies and returns them
        as pandas.DataFrame
        """
        if not self._run_for_year == year:
            self.run_for_year(year)

        if self.resolved_load:
            if self.resample_mean:
                return self.load_resolved.resample(self.freq).mean()
            else:
                return self.load_resolved.resample(self.freq).pad()
        else:
            index_1 = pd.date_range(
                start=pd.datetime(year, 1, 1), periods=len(self.total_load), freq="1min"
            )
            index_10 = pd.date_range(
                start=pd.datetime(year, 1, 1), periods=len(self.occ_active), freq="10min"
            )

            profiles = pd.DataFrame([])

            if self.resample_mean:
                profiles["Load"] = (
                    pd.Series(self.total_load, index=index_1).resample(self.freq).mean()
                )
                profiles["AppHeatGain"] = (
                    pd.Series(self.app_heat_gain, index=index_1)
                    .resample(self.freq)
                    .mean()
                )
                profiles["OccActive"] = (
                    pd.Series(self.occ_active, index=index_10)
                    .astype(int)
                    .resample(self.freq)
                    .mean()
                )
                profiles["OccNotActive"] = (
                    pd.Series(self.occ_not_active, index=index_10)
                    .astype(int)
                    .resample(self.freq)
                    .mean()
                )
            else:
                profiles["Load"] = (
                    pd.Series(self.total_load, index=index_1).resample(self.freq).pad()
                )
                profiles["AppHeatGain"] = (
                    pd.Series(self.app_heat_gain, index=index_1).resample(self.freq).pad()
                )
                profiles["OccActive"] = (
                    pd.Series(self.occ_active, index=index_10)
                    .astype(int)
                    .resample(self.freq)
                    .pad()
                )
                profiles["OccNotActive"] = (
                    pd.Series(self.occ_not_active, index=index_10)
                    .astype(int)
                    .resample(self.freq)
                    .pad()
                )

            if self.get_hot_water:
                profiles["HotWater"] = (
                    pd.Series(self.hotWater, index=index_1).resample(self.freq).pad()
                )

            return profiles
