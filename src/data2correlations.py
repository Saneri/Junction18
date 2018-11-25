import csv2data
import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np


def find_shift(sig1, sig2):
    '''Shift shorter signal to be at same point'''

    sig1[:, 2] = sig1[:, 2]
    sig2[:, 2] = sig2[:, 2]
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


def evaluate_move(model_data, train_data, plot_data=False):
    '''

    Args:
        model_data(DataReader): Data to set model for the algorithm
        train_data(DataReader): Compare this data to the model

    Returns:
        Error for acceleration and rotation

    '''

    sig1, sig2 = find_shift(model_data.acceleration, train_data.acceleration)

    max_acc_error = np.max([np.linalg.norm(sig1), np.linalg.norm(sig2)])
    acc_error = np.linalg.norm(sig1-sig2)/max_acc_error

    sig3, sig4 = find_shift(model_data.ang_velocity, train_data.ang_velocity)

    max_rot_error = np.max([np.linalg.norm(sig3), np.linalg.norm(sig4)])
    rot_error = np.linalg.norm(sig3-sig4)/max_rot_error

    print('Acceleration score: ' + str(acc_error))
    print('Rotation score: ' + str(rot_error))
    avg = (rot_error + acc_error)/2
    if avg <= 0.5:
        print('Grade: A - Perfect!')
    elif 0.5 < avg <= 0.7:
        print('Grade: B - Very good!')
    elif 0.7 < avg <= 1.0:
        print('Grade: C - Okay!')
    else:
        print('Grade: F - You need more practice!')

    if plot_data is True:
        fig, axes = plt.subplots(2, 2)
        axes[0, 0].plot(sig1)
        axes[0, 0].legend(['x', 'y', 'z'])
        axes[0, 0].set_title('Model acceleration')
        axes[1, 0].plot(sig2)
        axes[1, 0].legend(['x', 'y', 'z'])
        axes[1, 0].set_title('Training acceleration')
        axes[0, 1].plot(sig3)
        axes[0, 1].legend(['x', 'y', 'z'])
        axes[0, 1].set_title('Model rotation')
        axes[1, 1].plot(sig4)
        axes[1, 1].legend(['x', 'y', 'z'])
        axes[1, 1].set_title('Training rotation')
        plt.show()

    return acc_error, rot_error


if __name__ == '__main__':
    model_data = csv2data.DataReader('../testdata/mallisuoritus.csv')
    train_data = csv2data.DataReader('../testdata/Nopea_oikein.csv')

    acc, rot = evaluate_move(model_data, train_data, plot_data=True)
    print('Acceleration error: {}'.format(acc))
    print('Rotation error: {}'.format(rot))
