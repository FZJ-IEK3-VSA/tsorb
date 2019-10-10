import time

from tsorb.utils.InputData import DataExchangeCsv
from tsorb.ElectricalLoadProfile import ElectricalLoadProfile

def test_simple():

    starttime = time.time()

    # init the data object
    data_ex_main = DataExchangeCsv()

    # init the profile generator
    elp = ElectricalLoadProfile(
            data_ex=data_ex_main,
            residents=4,)

    # get the profile
    results = elp.get_rescheduled_profiles(2010)

    print("Profile generation took " + str(time.time() - starttime))

    # ToDo get the results for a fixed seed and check the values
