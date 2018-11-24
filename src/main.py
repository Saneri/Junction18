import sys
import os
from csvFetcher import csvFetcher
from csv2data import DataReader
sys.path.insert(0, '../GUI/')
from display import ProjectionViewer


def set_paths():

    # sets variable paths if the user so wishes
    answer = input("Would you like to set the environment variable 'MOVESENSEPATH'? (press enter to skip)\n")
    if len(answer) != 0:
        os.environ["MOVESENSEPATH"] = answer

    answer = input("Would you like to set the environment variable 'MOVESENSEPASTEPATH'? (press enter to skip)\n")
    if len(answer) != 0:
        os.environ["MOVESENSEPASTEPATH"] = answer


def ask_data_type():

    # Asks the data type
    while True:
        answer = input("Is this a training move (type: 't') or a model move (type: 'm')?\n")
        if answer != "t" and answer != "m":
            print("Please type 't' for training move or 'm' for model move!")
        else:
            break
    return answer


def fetcher(answer):

    # Creates an instance of csvFetcher to fetch latest csv-files
    print("Test:" +str(answer))
    fetcher = csvFetcher()
    if answer == "t":
        is_model = False
    elif answer == "m":
        is_model = True
    else:
        raise Exception("ERROR")

    filepath = fetcher.fetch(is_model)
    reader = DataReader(filepath)
    reader.read_file()


def main():

    set_paths()
    answer = ask_data_type()
    fetcher(answer)


main()
