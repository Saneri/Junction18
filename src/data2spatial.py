import numpy as np


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
        self.pos = np.zeros(m_data.length, 3)
        self.rotation = np.eye(3)
        self.velocity = np.zeros(m_data.length, 3)
        self.ang = np.zeros(m_data.length, 3)

    def _evaluate(self, dt, d):
        dpos = self.velocity[self.ind] + dt * d.dv
        dv = self.acceleration[self.ind]
        return Derivative(dpos, dv)

    def take_step(self, acceleration, velocity, pos, dt):
        der = Derivative(velocity, acceleration)
        a = self._evaluate(0, der)
        b = self._evaluate(0.5*dt, a)
        c = self._evaluate(0.5*dt, b)
        d = self._evaluate(dt, c)

        dxdt = 1/6 * (a.dpos + 2 * (b.dpos + c.dpos) + d.dpos)
        dvdt = 1/6 * (a.dv + 2 * (b.dv + c.dv) + d.dv)

        position = pos + dxdt * self.dt
        velocity = velocity + dvdt * self.dt

        return position, velocity

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

    def update_postition(self, pos, velocity, index):
        R_inv = np.linalg.inv(self.rotation)
        self.pos[index] = R_inv.dot(pos)
        self.velocity[index] = R_inv.dot(velocity)

    def convert_to_spatial_coordinates(self):
        for i in range(self.m_data.length-1):
            acc = self.m_data.acc[i, :]
            ang_vel = self.m_data.ang_vel[i, :]
            dt = self.m_data.timestamps[i+1] - self.m_data.timestamps[i]
            pos, vel = self.take_step(acc, self.velocity, self.pos, dt)
            self.update_rotation(ang_vel, i)
            self.update_postition(pos, vel, i)
