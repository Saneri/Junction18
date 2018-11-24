import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MesasureData(object):
    def __init__(self, data):
        self.acc = data
        self.length = data.shape[0]
        self.ang_vel = None
        self.dt = 0.1


class Derivative(object):

    def __init__(self, dpos, dv):
        self.dpos = dpos
        self.dv = dv


class SpatialConverter(object):
    '''
    Class used to convert acceleration and angular velocity to spatial
    coordinates.
    '''
    def __init__(self, m_data):
        '''Initialize class'''
        self.m_data = m_data  # measured data (acceleration and angular velocity)
        self.m_data.acc[:] = self.m_data.acc[:] - np.mean(self.m_data.acc[0:50, :], axis=0)

        self.pos = np.zeros((m_data.length, 3))
        self.rotation = np.eye(3)
        self.velocity = np.zeros((m_data.length, 3))
        self.velocity[0, :] = np.array([0, 1, 0])
        self.ang = np.zeros((m_data.length, 3))

    def _x_r(self, angle):
        a = angle*np.pi/180
        return np.array([[1, 0, 0],
                        [0, np.cos(a), -np.sin(a)],
                        [0, np.sin(a), np.cos(a)]])

    def _y_r(self, angle):
        a = angle*np.pi/180
        return np.array([[np.cos(a), 0, np.sin(a)],
                        [0, 1, 0],
                        [-np.sin(a), 0, np.cos(a)]])

    def _z_r(self, angle):
        a = angle*np.pi/180
        return np.array([[np.cos(a), -np.sin(angle), 0],
                        [np.sin(angle), np.cos(a), 0],
                        [0, 0, 1]])

    def update_rotation(self, ang_vel, index):
        x = self.angle[index, 0]
        y = self.angle[index, 0]
        z = self.angle[index, 0]
        self.rotation = self._x_r(x).dot(self._y_r(y)).dot(self._z_r(z))

    def update_position(self, pos, velocity, index):
        # R_inv = np.linalg.inv(self.rotation)
        # self.pos[index] = R_inv.dot(pos)
        # self.velocity[index] = R_inv.dot(velocity)
        self.pos[index] = pos
        self.velocity[index] = velocity

    def _evaluate(self, vel, acc, dt, d):
        dpos = vel + dt * d.dv
        dv = acc
        return Derivative(dpos, dv)

    def take_step(self, acceleration, velocity, pos, dt):
        der = Derivative(velocity, acceleration)
        a = self._evaluate(velocity, acceleration, 0, der)
        b = self._evaluate(velocity, acceleration, 0.5*dt, a)
        c = self._evaluate(velocity, acceleration, 0.5*dt, b)
        d = self._evaluate(velocity, acceleration, dt, c)

        dxdt = 1/6 * (a.dpos + 2 * (b.dpos + c.dpos) + d.dpos)
        dvdt = 1/6 * (a.dv + 2 * (b.dv + c.dv) + d.dv)

        position = pos + dxdt * self.m_data.dt
        velocity = velocity + dvdt * self.m_data.dt

        return position, velocity

    def convert_to_spatial_coordinates(self):
        for i in range(self.m_data.length-1):
            # ang_vel = self.m_data.ang_vel[i]
            # dt = self.m_data.timestamps[i + 1] - self.m_data.timestamps[i]
            dt = self.m_data.dt
            pos, vel = self.take_step(
                self.m_data.acc[i], self.velocity[i], self.pos[i], dt)
            # self.update_rotation(ang_vel, i)
            self.update_position(pos, vel, i+1)


if __name__ == '__main__':
    # df = pd.read_csv('acceleration.csv')
    # data = df.values[:, 0:3]
    # m_data = MesasureData(data)
    # c = SpatialConverter(m_data)
    # c.convert_to_spatial_coordinates()
    # print(c.pos)
    # fig, (ax1, ax2) = plt.subplots(2, 1)
    # ax1.plot(c.pos)
    # ax2.plot(m_data.acc)
    # plt.legend(['x', 'y', 'z'])
    # import pdb
    # pdb.set_trace()
    # plt.show()
    # # c = SpatialConverter()

    Ax = [-np.cos(x) for x in range(100)]
    Ay = [-np.sin(x) for x in range(100)]
    Az = [0 for x in range(100)]
<<<<<<< HEAD
    A = np.array([Ax, Ay, Az]).tranpose
    m_data = MesasureData(A)
=======
    A = np.array([Ax, Ay, Az])
    m_data = MesasureData(A.transpose())
>>>>>>> 2c572441438755da51ebd1f44e6d6d252e351e00

    c = SpatialConverter(m_data)
    c.convert_to_spatial_coordinates()
    plt.plot(c.pos)
    plt.show()
