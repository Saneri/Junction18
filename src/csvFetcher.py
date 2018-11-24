import os
import glob
import pandas
import shutil

# This is the path on Santeri's Ubuntu 18 with samsung A3 phone
DEFAULT_MOVESENSEDIR = "/run/user/1000/gvfs/mtp:host=%5Busb%3A001%2C011%5D/Phone/Movesense"
DEFAULT_PASTEPATH = "/home/santeri/Programming/Junction18/testdata/"
PASTED_CSV_FILE_NAME = "latestRun.csv"

# Fetch csv files from a connected phone
class csvFetcher(object):

    # Read movesense folder path from env variable
    def __init__(self):
        # Define
        path = os.getenv("MOVESENSEPATH")
        if path is None:
            print("Couldn't find MOVESENEPATH env variable: using default path "\
                + str(DEFAULT_MOVESENSEDIR))
            self.fetch_path = DEFAULT_MOVESENSEDIR
        else:
            self.fetch_path = path

        path = os.getenv("MOVESENSEPASTEPATH")
        if path is None:
            print("Couldn't find MOVESENSEPASTEPATH env variable: using default path "\
                + str(DEFAULT_PASTEPATH))
            self.paste_path = DEFAULT_PASTEPATH
        else:
            self.paster_path = path

    def fetch(self):
        list_of_files = glob.glob(str(self.fetch_path)+'/*.csv')
        # Check if self_path contains any .cs files
        if list_of_files is None:
            print("No .csv found from "+ self.fetch_path)
            return
        latest_file = max(list_of_files, key=os.path.getctime)
        print os.path.abspath(self.paste_path + PASTED_CSV_FILE_NAME)
        shutil.move(latest_file, os.path.abspath(self.paste_path + PASTED_CSV_FILE_NAME))