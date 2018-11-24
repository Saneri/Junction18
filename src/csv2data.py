import csv
import numpy as np
import sys


class DataReader:

    def __init__(self, filename):
        self.file = filename
        self.acceleration = np.empty(shape=[0, 3])
        self.ang_velocity = np.empty(shape=[0, 3])
        self.read_file()
        self.acceleration = self.acceleration.astype(np.float)
        self.ang_velocity = self.ang_velocity.astype(np.float)

    # Only logs data if both LinearAcc and AngularVelocity services are recording
    def read_file(self):

        try:
            with open(self.file, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                last_service_value = None
                for row in reader:
                    row = ''.join(row)
                    row = row.split(",")
                    if (row[0] == "LinearAcc") and (last_service_value == "AngularVelocity"):
                        self.column_to_array(row)
                    elif (row[0] == "AngularVelocity") and (last_service_value == "LinearAcc"):
                        self.column_to_array(row)
                    last_service_value = row[0]
        except OSError:
            print("Sry no tengo el file")
            sys.exit()

    def column_to_array(self, row):
        if row[0] == "LinearAcc":
            self.acceleration = np.append(self.acceleration, [[row[1], row[2], row[3]]], axis=0)
        else:
            self.ang_velocity = np.append(self.ang_velocity, [[row[1], row[2], row[3]]], axis=0)
