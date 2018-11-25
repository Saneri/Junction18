import sys
import os
from csvFetcher import csvFetcher
from csv2data import DataReader
from data2correlations import evaluate_move
sys.path.insert(0, '../GUI/')
from display import ProjectionViewer
import wireframe



def set_paths():

    # sets variable paths if the user so wishes
    answer = input('\nWould you like to set the environment variable MOVESENSEPATH? (press enter to skip)\n')
    if len(answer) != 0:
        os.environ['MOVESENSEPATH'] = answer

    answer = input('Would you like to set the environment variable MOVESENSEPASTEPATH? (press enter to skip)\n')
    if len(answer) != 0:
        os.environ['MOVESENSEPASTEPATH'] = answer


def fetcher():

    # Creates an instance of csvFetcher to fetch latest csv-files
    fetcher = csvFetcher()
    answer = input('Do you want to create a new model? (y = yes, n=no)\n')
    if answer == 'yes' or answer == 'y':
        input('Please perform a model measurement with your sensor and then press any key to continue\n')
        modelpath = fetcher.fetch(True)
    else:
        modelpath = input('Please give the path for .csv model file\n')
    input('Please perform a test measurement with your sensor and then press any key to continue\n')
    testpath = fetcher.fetch(False)

    return modelpath,testpath

def view_projection(modelpath, testpath):

    pv = ProjectionViewer(1600, 1200,modelpath,modelpath)

    arm = wireframe.Wireframe()
    arm.addNodes([(0, 0, 0), (100, 0, 0)])
    arm.addEdges([(0, 1)])

    arm2 = wireframe.Wireframe()
    arm2.addNodes([(0,0,0), (100,00,0)])
    arm2.addEdges([(0,1)])

    pv.addWireframe('model', arm2)
    pv.addWireframe('arm', arm)
    pv.run()

def evaluate(modelpath, testpath):
    model_reader = DataReader(modelpath)
    test_reader = DataReader(testpath)
    acc_score, rotation_score = evaluate_move(model_reader, test_reader, True)

def main():

    #set_paths()
    modelpath, testpath = fetcher()
    evaluate(modelpath, testpath)
    # view_projection(modelpath, testpath)
    while True:
        answer = input('Want to retry? (y/yes = yes)\n')
        if answer == 'y' or answer == 'yes':
            input('Please perform a test measurement with your sensor and then press any key to continue\n')
            f = csvFetcher()
            testpath = f.fetch(False)
            evaluate(modelpath, testpath)
            # view_projection(modelpath, testpath)
        else:
            print('The program will now close.')
            break


main()
