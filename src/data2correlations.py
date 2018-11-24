import csv2data
import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np


def find_shift(sig1, sig2):
    '''Shift shorter signal to be at same point'''
    l_s1 = sig1.shape[0]
    l_s2 = sig2.shape[0]
    L = np.max([l_s1, l_s2])

    sig1_s = np.zeros((L, 3))
    sig2_s = np.zeros((L, 3))

    sig1_s[0:l_s1] = sig1

    sig2_s[0:l_s2] = sig2

    n_s1 = np.mean(sig1_s, axis=1)
    n_s2 = np.mean(sig2_s, axis=1)

    conv = sig.correlate(n_s1, n_s2)
    m_ind = np.argmax(conv)
    delay = int(m_ind - np.round(len(conv)/2)+1)

    sig2_s = np.roll(sig2_s, delay, axis=0)

    return sig1_s, sig2_s


def evalauate_move(model_data, train_data, plot_data=False):
    '''

    Args:
        model_data(DataReader): Data to set model for the algorithm
        train_data(DataReader): Compare this data to the model

    Returns:
        Error for acceleration and rotation

    '''

    sig1, sig2 = find_shift(model_data.acceleration, train_data.acceleration)

    acc_error = np.power(np.linalg.norm(sig1-sig2), 2)
    sig3, sig4 = find_shift(model_data.ang_velocity, train_data.ang_velocity)

    rot_error = np.linalg.norm(sig3-sig4)

    if plot_data is True:
        fig, axes = plt.subplots(4, 1)
        axes[0].plot(sig1)
        axes[0].legend(['x', 'y', 'z'])
        axes[1].plot(sig2)
        axes[1].legend(['x', 'y', 'z'])
        axes[2].plot(sig3)
        axes[2].legend(['x', 'y', 'z'])
        axes[3].plot(sig4)
        axes[3].legend(['x', 'y', 'z'])
        plt.show()

    return acc_error, rot_error


if __name__ == '__main__':
    model_data = csv2data.DataReader('../testdata/mallisuoritus.csv')
    train_data = csv2data.DataReader('../testdata/Aivan_tautta_kuraa.csv')

    acc, rot = evalauate_move(model_data, train_data, plot_data=True)
    print('Acceleration error: {}'.format(acc))
    print('Rotation error: {}'.format(rot))
