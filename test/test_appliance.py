import numpy as np

from tsorb.Appliance import Appliance


def test_appliance():

    apps = [Appliance] * 10
    for i in range(10):
        if np.random.random() < 0.5:
            act_occ_dependent = False
        else:
            act_occ_dependent = True
        b = Appliance(
            "app_" + str(i),
            "app_" + str(i),
            "type_name_" + str(i),
            "profile_" + str(1),
            np.random.random(),
            10 * np.random.random(),
            50 * np.random.random(),
            1000 * np.random.random(),
            100 * np.random.random(),
            50 * np.random.random(),
            0.03 * np.random.random(),
            100000000 * np.random.random(),
            act_occ_dependent,
            np.random.random(),
            0.8 * np.random.random(),
            0.1,
        )
        apps[i] = b

    for app in apps:
        print(app)
        app.set_ownership()
        if app.owned:
            print("owned")
        else:
            print("not owned")
