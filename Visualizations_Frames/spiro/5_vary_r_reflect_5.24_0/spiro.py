# Internal Packages
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from material.surfaceMaterial import SurfaceMaterial
from geometry.polygonGeometry import PolygonGeometry

from operator import add, sub
from math import sin, cos, tan, cosh, exp, pi
from OpenGL.GL import *
import numpy as np
import pygame
from time import sleep
import cv2
import os
import shutil

# Constants:
WIDTH = 1080
HEIGHT = 1080
Z = 10  # Sets camera distance away from xy plane
SIZE = Z / 3

BASE_PATH = 'C:/Users/nicor/.vscode/Developing_Graphics_Frameworks_with_Python_and_OpenGL/Visualizations_Frames/spiro/'

# Define the Materiality of each circle on the screen
vsCode = '''
            in vec3 vertexPosition;
            out vec3 position;
            uniform mat4 modelMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 projectionMatrix;
            void main()
            {
                vec4 pos = vec4(vertexPosition, 1.0);
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
                position = vertexPosition;
            }
        ''' 

# render a basic scene
class Test(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])
        self.renderer.render(self.scene, self.camera)
        
        # iterative variables
        self.iter0 = 0
        self.iter = self.iter0
        self.angle = self.iter0 * pi / 1000
        self.wr = 0
        self.wR = 0
        self.capture_iter = 0

        # Spirograph params
        self.x_offset = 5*pi/3
        self.y_offset = 0
        self.R = 5
        self.r = 3
        

        self.line_container = []
        self.point_container = []
        self.spiro_container = []
        self.x_list = []
        self.y_list = []
        self.draw_dots = True


    def remove_spiro(self):
        for i in range(0, len(self.spiro_container)):
            self.scene.remove(self.spiro_container[i])
        self.spiro_container = []

    def material_gen(self, r, g, b, draw_style = GL_LINE_STRIP, wireframe = True):
        material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': wireframe,
                'lineWidth': 3,
                'drawStyle': draw_style
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [r, g, b]
        )
        return material
    
    def screen_recorder(self, file_name):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        screen_surf = pygame.transform.flip(screen_surf, True, True)
        pygame.image.save(screen_surf, BASE_PATH + f'{self.config}/frames/{file_name}.jpg')

    def build_movie(self):
        img_array = []
        file_array = []
        dir_path = BASE_PATH + self.config + '/frames/'
        frame_cnt = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
        print(frame_cnt)
        for i in range(0, frame_cnt):
            f = dir_path + str(i) + '.jpg'
            file_array.append(f)


        for filename in file_array:
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)

        out = cv2.VideoWriter(f'../Visualizations_Frames/spiro/{self.config}/vout.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 10, size)
        
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()

        shutil.copyfile('spiro.py', f'../Visualizations_Frames/spiro/{self.config}/spiro.py')


    def ring_pts(self, xc, yc, r0, phi, color, a, n, t, poly_radius):
        n_dots = int(np.pi * r0 / poly_radius)
        namp = n
        for theta in np.linspace(phi, 2 * np.pi + phi, n_dots, endpoint=False):
            n = namp
            x0 = xc + (r0 + a * np.sin(n * (theta + t))) * np.cos(theta)
            y0 = yc +(r0 + a * np.sin(n * (theta + t)))* np.sin(theta)
            p1 = PolygonGeometry(
                sides = 20,
                radius = poly_radius,
                x = x0,
                y = y0,
                theta1 = 0,
                theta2 = 2 * np.pi
            )

            material = self.material_gen(r = color[0], g = color[1], b = color[2])
            self.point_container.append(Mesh(p1, material))
            self.scene.add(self.point_container[-1])

    def spiro(self, x, y, color, poly_radius):
    
        p1 = PolygonGeometry(
            sides = 20,
            radius = poly_radius,
            x = x,
            y = y,
            theta1 = 0,
            theta2 = 2 * np.pi
        )

        if len(self.x_list) >= 1:
            x_near = abs(x - self.x_list[0]) < 0.05
            y_near = abs(y - self.y_list[0]) < 0.05

            if x_near and y_near:
                self.draw_dots = False
            
        self.x_list.append(x)
        self.y_list.append(y)


        material = self.material_gen(r = color[0], g = color[1], b = color[2])
        self.spiro_container.append(Mesh(p1, material))
        self.scene.add(self.spiro_container[-1])

        
        

    ## main loop ##  (At 60 fps, this runs once every 0.017 secs.)

    def update(self):
        d = self.R - self.r
        Rate = 0.015
        xc = d * np.cos(self.wR)
        yc = d * np.sin(self.wR) 
        xs = xc + (self.r/5)* (np.cos(self.wr + self.x_offset))
        ys = yc + self.r/2 * np.sin(self.wr + self.y_offset)

        
        if self.iter == 0 and self.capture_iter == 0:
            self.config = f'{self.R}_vary_r_reflect_{round(self.x_offset, 2)}_{round(self.y_offset, 2)}'
            os.mkdir(BASE_PATH + self.config)
            os.mkdir(BASE_PATH + self.config + '/frames')
        if self.iter == 0:
            # self.ring_pts(r0 = R, phi = 0, color = [0.0, 1.0, 1.0], poly_radius= 0.05, a = 0, n = 1, t = 0, xc = 0, yc = 0)
            # self.ring_pts(r0 = r, phi = 0, color = [0.0, 1.0, 1.0], poly_radius = 0.05, a = 0, n = 1, t = 0, xc = d * np.cos(self.wR), yc = d * np.sin(self.wR))
            self.spiro(xs, ys, color = [1.0, 1.0, 0.0], poly_radius=0.001)
        else:
            # self.remove_hex1()
            # self.ring_pts(r0 = R, phi = 0, color = [0.0, 1.0, 1.0], poly_radius= 0.05, a = 0, n = 1, t = 0, xc = 0, yc = 0)
            # self.ring_pts(r0 = r, phi = -self.wr, color = [0.0, 1.0, 1.0], poly_radius = 0.05, a = 0, n = 1, t = 0, xc = d * np.cos(self.wR), yc = d * np.sin(self.wR))
            self.spiro(xs, ys, color = [0.0, 1.0, 0.0], poly_radius=0.001)
            self.spiro(-xs, -ys, color = [0.0, 0.0, 1.0], poly_radius=0.001)
        self.renderer.render(self.scene, self.camera)
        

        if not self.draw_dots:
            
            self.screen_recorder(self.capture_iter)
            self.remove_spiro()
            self.x_list = []
            self.y_list = []
            self.iter = self.iter0
            self.wr = 0
            self.wR = 0
            self.x_offset += 0.1
            self.capture_iter += 1
            self.r = 3 + 3*sin(self.x_offset/2)
            self.draw_dots = True

        if self.capture_iter == 200: #63
            self.build_movie()
            self.capture_iter = 0
            pygame.quit()
            


        self.wR += Rate
        self.wr += Rate * self.R / self.r
        self.iter += 1
        

t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


