from tsorb.utils.InputData import DataExchangeCsv
from tsorb.OccupancyModel import OccupancyModel


def test_occupancy():

    data_ex_main = DataExchangeCsv()
    occ_model = OccupancyModel(data_ex_main, 1, True)
    occ_model.set_seed(1)
    occ_model.run("wd")
