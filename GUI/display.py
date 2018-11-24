import wireframe
import skeleton
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
"""
    pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
    pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
    pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
    pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
    pygame.K_PLUS:   (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8))}
"""
"""
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1))
"""


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    camera = m.affine(m.rotX(0), np.array([0,0,0]))
    cT = m.affine(m.rotX(0), np.array([500,500,0]))
    cR = m.affine(m.rotX(np.pi/6),np.array([0,0,0]))
    rotationToggle = False
    animToggle = False

    animation = []
    frame = 0
    

    def __init__(self, width, height):
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
                self.frame = self.frame%len(self.animation)

            self.display()  
            pygame.display.flip()
            clock.tick(60)
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    r1 = np.array([edge.start.x, edge.start.y,edge.start.z,1])
                    #R1 = (self.cT.mat*(self.camera*wireframe.ori)).dot(r1)
                    R1 = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(wireframe.ori.mat.dot(r1))))
                    r2 = np.array([edge.stop.x, edge.stop.y,edge.stop.z,1])
                    R2 = self.cT.mat.dot(self.cR.mat.dot(self.camera.mat.dot(wireframe.ori.mat.dot(r2))))
                    pygame.draw.aaline(self.screen, self.edgeColour, (R1[0], R1[1]), (R2[0],R2[1]), 1)

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


    def translate(self, d):
        T = m.affine(m.rotX(0), d)
        for wireframe in self.wireframes.values():
            wireframe.ori.set(wireframe.ori*T)

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.values():
            wireframe.translate(axis,d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.values():
            wireframe.scale(centre_x, centre_y, scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.values():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)

    def rotateCameraR(self, a = 0.05):
        R = m.rotY(a*np.pi)
        aff_ = m.affine(R,np.array([0,0,0]))
        self.camera.set(aff_*self.camera)

    def rotateCameraL(self, a = 0.05):
        R = m.rotY(-a*np.pi)
        aff_ = m.affine(R,np.array([0,0,0]))
        self.camera.set(aff_*self.camera)

    def loadAni(self):
        df = pd.read_csv("testi.csv") 
        anim = []
        cols = list(df.columns)
        cols.pop(0)

        for index, row in df.iterrows():
            r = []
            for c in cols:
                vals = row[c][1:-1].split(",")
                vals = [int(x) for x in vals]
                r.append(vals)
            anim.append(r)

        self.animation = anim

    def animate(self):
        if len(self.animation) == 0:
            return
        else:
            for wireframe in self.wireframes.values():
                wireframe.setNodes(self.animation[self.frame]) 

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

    #cube = wireframe.Wireframe()
    #cube.addNodes([(x,y,z) for x in (-250,250) for y in (-250,250) for z in (-250,250)])
    #cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    
   # axes = wireframe.Wireframe()
   # axes.addNodes([(0,0,0),(50,0,0),(0,-50,0),(0,0,50)])
   # axes.addEdges([(0,1),(0,2),(0,3)])
    
    arm = wireframe.Wireframe()
    arm.addNodes([(0,0,0), (100,0,0), (200,0,0)])
    arm.addEdges([(0,1),(1,2)])

    #pv.addWireframe('axes', axes)
    pv.addWireframe('arm', arm)
    pv.run()
