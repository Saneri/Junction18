import numpy as np
import csv


class SpatialConverter(object):
    ''''Class used to convert accele '''
    def __init__(self, m_data):
        '''Initialize class'''
        self.m_data = m_data  # mesured data as a structure
        # data saved to lists as {data: x, timestamp: t}
        self.p = np.zeros(m_data, length, 3)
        self.t = np.array(m.timestamps)

        self.v = np.zeros(1, 3)
        self.a = np.zeros(1, 3)
        self.x_curr = 0
        self.y_curr = 0
        self.z_curr = 0
        self.ind_curr = 0

    def find_start_point(self, silence_time):
        self.m_data = 

    def update_postition(self):
        # s = self.v*t + 1/2 * self.a
        raise NotImplementedError

    def convert_to_spatial_coordinates(self):
        for i in range(self.m_data.length):
            self.
        raise NotImplementedError

