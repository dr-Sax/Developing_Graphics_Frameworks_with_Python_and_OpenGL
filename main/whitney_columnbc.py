# https://github.com/jbum/Whitney-Music-Box-Examples/blob/master/processing/digital_harmony_examples/whitney_columnbc/whitney_columnbc.pde

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.sphereGeometry import SphereGeometry
from math import sin, cos, pi
from OpenGL.GL import *
from material.material import Material
import pygame

Z = 1000  # Sets camera distance away from xy plane
PTS = 360
STEPSTART = 0
STEPEND = 1/60
RADIUS = 900 * 0.9 / 2
XCENTER = 0
YCENTER = 0

# render a basic scene
class Test(Base):

    def initialize(self):

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 1)
        self.camera.setPosition([0, 0, Z])
        self.geometry = SphereGeometry(radius = 1, heightSegments = 20)

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

        fsCode = '''
            in vec3 position;
            out vec4 fragColor;
            void main()
            {
                vec3 color = mod(vec3(0.0, 0.0, 0.0), 1.0);
                fragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
        '''

        self.material = Material(vsCode, fsCode)
        self.material.locateUniforms()
        self.mesh_list = []
        self.timer = 0


    def update(self):     

        ftime = self.timer * 0.01
        step = STEPSTART + (ftime * (STEPEND - STEPSTART))

        for i in range(0, PTS):

            A = 2 * pi * step * i
            R_t = RADIUS * sin(A * ftime)
            x = XCENTER + cos(A) * (i / PTS) * R_t
            y = YCENTER + sin(A) * (i / PTS) * R_t
            

            self.temp_mesh = Mesh(self.geometry, self.material)

            if self.timer == 0:
                self.temp_mesh.translate(x = x, y = y, z = 0)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

            else:
                self.temp_mesh.translate(x = x, y = y, z = 0)
                x_pos_i = self.mesh_list[i].getPosition()[0]
                y_pos_i = self.mesh_list[i].getPosition()[1]
                self.mesh_list[i].translate(
                    x = self.temp_mesh.getPosition()[0] - x_pos_i, 
                    y = self.temp_mesh.getPosition()[1] - y_pos_i, 
                    z = 0
                    )

        self.renderer.render(self.scene, self.camera) 
        # screen = pygame.display.get_surface()
        # size = screen.get_size()
        # buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        # screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        # pygame.image.save(screen_surf, f"../spiral/{ftime}.jpg")

        self.timer = self.timer + 0.017  # number of secs that pass after each update
        


# instantiate this class and run the program
Test(screenSize = [900, 900]).run()
