from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from geometry.sphereGeometry import SphereGeometry
from geometry.cylinderGeometry import CylinderGeometry
from geometry.pyramidGeometry import PyramidGeometry
from material.surfaceMaterial import SurfaceMaterial
from geometry.coneGeometry import ConeGeometry
from geometry.halfSphereGeometry import HalfSphereGeometry
from material.textureMaterial import TextureMaterial
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
import cv2
from math import sin, cos, pi, sqrt
from OpenGL.GL import *
from material.material import Material
import pygame

Z = 20
PTS = 360
# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 1)
        self.camera.setPosition([0, 0, Z])

        self.geometry = SphereGeometry(radius = 0.1, heightSegments = 20)
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

        fsCode1 = '''
            in vec3 position;
            out vec4 fragColor;
            void main()
            {
                vec3 color = mod(vec3(0.0, 0.0, 0.0), 1.0);
                fragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
        '''

        fsCode2 = '''
            in vec3 position;
            out vec4 fragColor;
            void main()
            {
                vec3 color = mod(vec3(0.0, 0.0, 0.0), 1.0);
                fragColor = vec4(0.0, 1.0, 0.0, 1.0);
            }
        '''

        self.material1 = Material(vsCode, fsCode1)
        material2 = Material(vsCode, fsCode2)
        self.material1.locateUniforms()
        material2.locateUniforms()


        self.mesh_list = []
        for i in range(0, PTS):
            theta = i / PTS * 2 * pi
            self.n = 1
            R = 8 * sin(self.n * theta) 
            self.temp_mesh = Mesh(self.geometry, self.material1)
            self.temp_mesh.translate(x = R * cos(theta), y = R * sin(theta), z = 0)
            self.mesh_list.append(self.temp_mesh)
            self.scene.add(self.temp_mesh)

        self.renderer.render(self.scene, self.camera)
        self.counter = 0
        self.renderer.render(self.scene, self.camera)
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, "../polar_shapes/1.png")


    def update(self):
        self.counter += 1

        if self.counter % 10 == 0:
            if self.n == 1000:
                self.n = 1
            else:
                self.n += 1
            
            for i in range(0, PTS - 1):
                theta = i / PTS * 2 * pi
                x_pos_i = self.mesh_list[i].getPosition()[0]
                y_pos_i = self.mesh_list[i].getPosition()[1]
                R = 8 * sin(self.n * theta) 
                temp_mesh = Mesh(self.geometry, self.material1)
                temp_mesh.translate(x = R * cos(theta), y = R * sin(theta), z = 0)

                self.mesh_list[i].translate(x = temp_mesh.getPosition()[0] - x_pos_i, y = temp_mesh.getPosition()[1] - y_pos_i, z = 0)
            

            
            self.renderer.render(self.scene, self.camera)
            screen = pygame.display.get_surface()
            size = screen.get_size()
            buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
            screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
            pygame.image.save(screen_surf, f"../polar_shapes/{self.n}.png")
            


# instantiate this class and run the program
Test(screenSize = [900, 900]).run()
