
import csv

class DataReader:
    
    def __init__(self,csvfile):
        self.file = csvfile
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        self.length = None
    

    def compile_lists(self,row,lista,column):
        row = ''.join(row)
        tiedot = row.split(",")
        lista.append(tiedot[column])

    def read_file(self):
    
        timestampcolumn = 0
        xcolumn=1
        ycolumn=2
        zcolumn=3
        
        with open(self.file, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                DataReader.compile_lists(row,self.time,timestampcolumn)
                DataReader.compile_lists(row,self.x,xcolumn)
                DataReader.compile_lists(row,self.y,ycolumn)
                DataReader.compile_lists(row,self.z,zcolumn)
            self.length = len(self.time)
            
        
    
        
        
