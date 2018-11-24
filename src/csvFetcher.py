import os
import glob
import pandas
import shutil

# This is the path on Santeri's Ubuntu 18 with samsung A3 phone
DEFAULT_MOVESENSEPATH = "/run/user/1000/gvfs/mtp:host=%5Busb%3A001%2C011%5D/Phone/Movesense/"
DEFAULT_PASTEPATH = "/home/santeri/Programming/Junction18/testdata/"
MODEL_FILE_NAME = "modelRun.csv"
TEST_FILE_NAME = "testRun.csv"

# Fetch csv files from a connected phone
class csvFetcher(object):

    # Read movesense folder path from env variable
    def __init__(self):
        # Define
        path = os.getenv("MOVESENSEPATH")
        if path is None:
            print("Using default path "\
                + str(DEFAULT_MOVESENSEDIR))
            self.fetch_path = DEFAULT_MOVESENSEDIR
        else:
            self.fetch_path = path

        path = os.getenv("MOVESENSEPASTEPATH")
        if path is None:
            print("Using default path "\
                + str(DEFAULT_PASTEPATH))
            self.paste_path = DEFAULT_PASTEPATH
        else:
            self.paste_path = path

    def fetch(self, is_model):

        list_of_files = glob.glob(str(self.fetch_path)+'/*.csv')

        # Check if self_path contains any .cs files
        if not list_of_files:
            print("No .csv found from "+ self.fetch_path)
            return
        latest_file = max(list_of_files, key=os.path.getctime)

        # Model run and test run csv files are named differently
        if is_model:
            csv_name = MODEL_FILE_NAME
        else:
            csv_name = TEST_FILE_NAME

        full_path = self.paste_path + csv_name
        shutil.move(latest_file, os.path.abspath(full_path))
        return(full_path)
