import sys
sys.path.insert(0, './GUI/')
import wireframe
import skeleton

sys.path.insert(0, './src/')
import Kdata2spatial as k
import csv2data

import pygame
import numpy as np
import matrices as m
import pandas as pd

key_to_function = {
    pygame.K_LEFT:  (lambda x: x.translate(np.array([-10,0,0]))),
    pygame.K_RIGHT: (lambda x: x.translate(np.array([ 10,0,0]))),
    pygame.K_UP:    (lambda x: x.translate(np.array([0,-10,0]))),
    pygame.K_DOWN:  (lambda x: x.translate(np.array([0, 10,0]))),
    pygame.K_4:     (lambda x: x.rotateNode(1,'x')),
    pygame.K_1:     (lambda x: x.rotateNode(1,'x-')),
    pygame.K_5:     (lambda x: x.rotateNode(1,'y')),
    pygame.K_2:     (lambda x: x.rotateNode(1,'y-')),
    pygame.K_6:     (lambda x: x.rotateNode(1,'z')),
    pygame.K_3:     (lambda x: x.rotateNode(1,'z-'))
}

def getAnimation(df):
    """Helper function for loading the animation from dataframes"""
    out = []

    cols = list(df.columns)
    cols.pop(0)

    for index, row in df.iterrows():
        r = []
        for c in cols:
            vals = row[c][1:-1].split(",")
            vals = [int(x) for x in vals]
            r.append(vals)
        out.append(r)
    return out

class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    camera = m.affine(m.rotX(0), np.array([0,0,0]))
    cT = m.affine(m.rotX(0), np.array([500,500,0]))
    cR = m.affine(m.rotX(np.pi/6),np.array([0,0,0]))
    rotationToggle = False
    animToggle = False

    animation = []
    frame = 0


    def __init__(self, width, height, f1 = "./testdata/Mallisuoritus.csv", f2 = "./testdata/Nopea_oikein.csv"):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

        self.cT = m.affine(m.rotX(0), np.array([width/2, height/2, 0]))

        self.dataModel = csv2data.DataReader(f1)
        self.dataCmp = csv2data.DataReader(f2)

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                    elif event.key == pygame.K_q:
                        self.rotateCameraR()
                    elif event.key == pygame.K_e:
                        self.rotateCameraL()
                    elif event.key == pygame.K_r:
                        self.rotationToggle = not self.rotationToggle
                    elif event.key == pygame.K_a:
                        self.animToggle = not self.animToggle

            if self.rotationToggle:
                self.rotateCameraR(0.01)

            if self.animToggle:
                if len(self.animation) == 0:
                    self.loadAni()

                self.animate()
                self.frame += 1
                self.frame = self.frame%len(self.animation[0][0])

            self.display()
            pygame.display.flip()
            clock.tick(60)

    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)
        i = 0
        color = [(255,255,0),(200,200,200)]
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    c = color[i]
                    r1 = np.array([edge.start.x, edge.start.y,edge.start.z,1])
                    R1 = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(wireframe.ori.mat.dot(r1))))
                    r2 = np.array([edge.stop.x, edge.stop.y,edge.stop.z,1])
                    R2 = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(wireframe.ori.mat.dot(r2))))
                    pygame.draw.line(self.screen, c, (R1[0], R1[1]), (R2[0],R2[1]), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    rr = np.array([node.x, node.y, node.z, 1])
                    R = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(wireframe.ori.mat.dot(rr))))
                    pygame.draw.circle(self.screen, self.nodeColour, (int(R[0]), int(R[1])), self.nodeRadius, 0)
                    ori = np.asarray(node.ori.mat)
                    X = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(ori.dot(np.array([20,0,0, 0])))))
                    X += R
                    Y = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(ori.dot(np.array([0, -20,0, 0])))))
                    Y += R

                    Z = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(ori.dot(np.array([0,0,20, 0])))))
                    Z += R
                    pygame.draw.line(self.screen, (255,0,0),[R[0],R[1]], [X[0],X[1]], 1)
                    pygame.draw.line(self.screen, (0,255,0),[R[0],R[1]], [Y[0],Y[1]], 1)
                    pygame.draw.line(self.screen, (0,0,255),[R[0],R[1]], [Z[0],Z[1]], 1)

            i+=1

    def translate(self, d):
        """Translates the wireframe"""
        T = m.affine(m.rotX(0), d)
        for wireframe in self.wireframes.values():
            wireframe.ori.set(wireframe.ori*T)

    def rotateCameraR(self, a = 0.05):
        """Rotates the camera"""
        R = m.rotY(a*np.pi)
        aff_ = m.affine(R,np.array([0,0,0]))
        self.camera.set(aff_*self.camera)

    def rotateCameraL(self, a = 0.05):
        """Rotates the camera"""
        R = m.rotY(-a*np.pi)
        aff_ = m.affine(R,np.array([0,0,0]))
        self.camera.set(aff_*self.camera)

    def loadAni(self):
        """Loads animation csv:s from malli.csv and testi.csv"""
        #df = pd.read_csv("malli.csv")
        #df2 = pd.read_csv("testi.csv")


        data1 = k.getSpatial(self.dataModel)
        data2 = k.getSpatial(self.dataCmp)

        l1 = len(list(data1.values())[0])
        l2 = len(list(data2.values())[0])


        if(l1 < l2):
            for j in data1.values():
                v = np.asarray(j)
                for i in range(l1,l2):
                    v = np.append(j,np.array([0,0,0]))

        else:
            for j in data2.values():
                v = np.asarray(j)
                for i in range(l2,l1):
                    v = np.append(j,np.array([0,0,0]))


        self.animation.append(list(data1.values()))
        self.animation.append(list(data2.values()))

        #ani1 = getAnimation(df)
        #ani2 = getAnimation(df2)
        #self.animation.append(ani1)
        #self.animation.append(ani2)

    def animate(self):
        """Helper function that runs the animation"""
        if len(self.animation) == 0:
            return
        else:
        #    print(np.asarray(self.animation).shape)
            for i in range(len(self.wireframes)):
                wireframe = list(self.wireframes.values())[i]
                wireframe.setNodes(self.animation[i],self.frame)

    def rotateNode(self, node, axis):
        R = []
        if (axis == 'x'): R = m.affine(m.rotX(0.1*np.pi),np.array([0,0,0]))
        if (axis == 'y'): R = m.affine(m.rotY(0.05*np.pi),np.array([0,0,0]))
        if (axis == 'z'): R = m.affine(m.rotZ(0.05*np.pi),np.array([0,0,0]))
        if (axis == 'x-'): R = m.affine(m.rotX(-0.05*np.pi),np.array([0,0,0]))
        if (axis == 'y-'): R = m.affine(m.rotY(-0.05*np.pi),np.array([0,0,0]))
        if (axis == 'z-'): R = m.affine(m.rotZ(-0.05*np.pi),np.array([0,0,0]))


        for wireframe in self.wireframes.values():
            wireframe.nodes[node].rotate(R)

if __name__ == '__main__':
    pv = ProjectionViewer(1600, 1200)

    arm = wireframe.Wireframe()
    arm.addNodes([(0,0,0), (100,0,0)])
    arm.addEdges([(0,1)])

    arm2 = wireframe.Wireframe()
    arm2.addNodes([(0,0,0), (100,00,0)])
    arm2.addEdges([(0,1)])

    pv.addWireframe('model', arm2)
    pv.addWireframe('arm', arm)
    pv.run()
