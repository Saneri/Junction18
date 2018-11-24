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
    answer = input("Do you want to create a new model? (y = yes, n=no)\n")
    if answer == "yes" or answer == "y":
        input("Please perform a model measurement with your sensor and then press any key to continue\n")
        modelpath = fetcher.fetch(True)
    input("Please perform a test measurement with your sensor and then press any key to continue\n")
    testpath = fetcher.fetch(False)
    reader = DataReader(testpath)
    reader.read_file()
    return modelpath,testpath


def view_projection(modelpath, testpath):

    pv = ProjectionViewer(1600, 1200,modelpath,testpath)

    arm = wireframe.Wireframe()
    arm.addNodes([(0, 0, 0), (100, 0, 0)])
    arm.addEdges([(0, 1)])

    arm2 = wireframe.Wireframe()
    arm2.addNodes([(0,0,0), (100,00,0)])
    arm2.addEdges([(0,1)])

    pv.addWireframe('model', arm2)
    pv.addWireframe('arm', arm)
    pv.run()


def main():

    set_paths()
    answer = ask_data_type()
    modelpath, testpath = fetcher(answer)
    view_projection(modelpath, testpath)


main()
