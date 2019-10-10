import numpy as np
from tsorb.Load import Load


class Bulb(Load):
    def __init__(self, key, rating):
        super(Bulb, self).__init__(key.upper())
        self.rating = rating

        # This calibration scalar is used to calibrate the model to so that it provides
        # a particular average output over a large number of runs.
        self._calibration = 0.008

        # weight how likely a switch on event for this particular bulb is
        # a value of about 0.3 produces a switch on event
        self.weight = -1 * np.log(np.random.random()) * self._calibration
        self.switched_on_time_series = np.zeros(1440)
        # ratio how much of the light is transformed to heat
        self.heat_gain = 0.97

    def __str__(self):
        return "Key: {0}, Rating: {1}, Weight: {2}".format(
            self._key, self.rating, self.weight
        )

    def switch_on(self, minute):
        """
        Turns on the bulb in a one minute time interval and stores the rating in the consumption array
        :param minute:
        """
        if 0 <= minute < self.consumption.size:
            self.consumption[minute] = self.rating
            self.switched_on_time_series[minute] = 1
