import csv
import numpy as np


class DataReader:

    def __init__(self,csvfile):
        self.file = csvfile
        #self.acceleration =  np.zeros(0, 3)
        #self.velocity = np.zeros(0, 3)

#        self.time = []
#        self.x = []
#        self.y = []
#        self.z = []
#        self.length = None

#    def compile_lists(self,row,lista,column):
#        row = ''.join(row)
#        tiedot = row.split(",")
#        lista.append(tiedot[column])

    def read_file(self):

        servicecolumn = 0
        xcolumn=1
        ycolumn=2
        zcolumn=3

        with open(self.file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            lastServiceValue = None
            for row in reader:
                row = ''.join(row)
                row = row.split(",")
                print(str(row[0]) + "  :  " + str(lastServiceValue))
                if (row[0] == "LinearAcc") and  (lastServiceValue == "AngularVelocity"):
                    columnToArray(row, row[0])
                elif (row[0] == "AngularVelocity") and (lastServiceValue == "LinearAcc"):
                    columnToArray(row, row[0])
                lastServiceValue = row[0]

    def columnToArray(self, row, type):
        pass
        # Ville hoitaa
