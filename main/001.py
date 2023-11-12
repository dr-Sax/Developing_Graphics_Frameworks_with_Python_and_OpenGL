from operator import add, sub
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from math import sin, cos, tan, cosh, exp, pi
from OpenGL.GL import *
from material.surfaceMaterial import SurfaceMaterial
from geometry.lineGeometry import LineGeometry
from geometry.rectangleGeometry import RectangleGeometry

import pygame

WIDTH = 1080 * 2
HEIGHT = 1350
Z = 10  # Sets camera distance away from xy plane
NUM_LINES = 50


# render a basic scene
class Test(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])
        self.line_container = []


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


        self.line_container = []
        self.line_container2 = []
        self.line_container3 = []
        self.pace = 0
        self.angle = 0

        # for i in range(0, NUM_LINES):
        #     x1 = -Z / 2 + i / NUM_LINES * Z
        #     x2 = -Z / 2 + i / NUM_LINES * Z
        #     y1 = - Z / 2
        #     y2 = Z / 2
        #     self.geometry = LineGeometry(
        #         x1 = x1,
        #         x2 = x2,
        #         y1 = y1,
        #         y2 = y2
        #     )
            
        
        #     material = self.material_gen(r = 0.0, g = 0.0, b = 0.0)
        #     m = Mesh(self.geometry, material).rotateX(pi / 2)
        #     print(m)
        #     self.line_container.append(m)
        #     self.scene.add(self.line_container[i])

        self.angled_grating(20, self.line_container)    
        #self.angled_grating(240, self.line_container2)
        #self.angled_grating(0, self.line_container3)

        
        r = RectangleGeometry(12, 12)
        material = self.material_gen(r = 1.0, g = 1.0, b = 1.0, draw_style = GL_TRIANGLE_FAN, wireframe = False)
        r_mesh = Mesh(r, material)
        self.scene.add(r_mesh)

        self.renderer.render(self.scene, self.camera) 


    def angled_grating(self, angle, line_list):
            for i in range(0, NUM_LINES):
                x1 = -Z / 2 + i / NUM_LINES * Z + Z / 2 * sin(angle)
                x2 = -Z / 2 + i / NUM_LINES * Z - Z / 2 * sin(angle)
                y1 = - Z / 2
                y2 = Z / 2

                self.geometry = LineGeometry(
                    x1 = x1,
                    x2 = x2,
                    y1 = y1,
                    y2 = y2
                )
            
                material = self.material_gen(r = 0.0, g = 0.0, b = 0.0)
                line_list.append(Mesh(self.geometry, material))
                self.scene.add(line_list[i])

    def remove_grating(self, line_list):
        for i in range(0, NUM_LINES):
            self.scene.remove(line_list[i])

        line_list = []


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
    
    def screen_recorder(self):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../hilbert_color/{self.order}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        pass 
        # if self.pace % 20 == 0:
        #     for i in range(0, NUM_LINES):
        #         self.scene.remove(self.line_container2[i])
        #     self.line_container2 = []
        #     self.angled_grating(self.angle, self.line_container2)
        #     self.angle += 1
        #     self.pace = 1
        # self.pace += 1

        pass

t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


