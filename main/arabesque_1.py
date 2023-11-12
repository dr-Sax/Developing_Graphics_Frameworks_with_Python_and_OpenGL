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
from math import sin, cos, pi
from OpenGL.GL import *

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

        geometry = SphereGeometry(radius = 0.1, heightSegments = 20)
        grid = Texture('images/rain.png')
        material = TextureMaterial(grid)

        self.mesh_list = []
        for i in range(0, 10*PTS):

            temp_mesh = Mesh(geometry, material)
            #temp_mesh.translate(x = Z / 3 * cos(-2 * pi * i / PTS - pi / 2), y = Z / 3 * sin(-2 * pi * i / PTS - pi / 2), z = 0)
            #temp_mesh.translate(x = Z / 3 * cos(-2 * pi * i / PTS - pi / 2)*(1 - cos(-2 * pi * i / PTS - pi / 2)), y = Z / 3 * sin(-2 * pi * i / PTS - pi / 2)*(1 - cos(-2 * pi * i / PTS - pi / 2)), z = 0)
            #temp_mesh.translate(x = Z / 3 * sin(5 / 4 * (i)) * (cos(5 / 4 * (i))), y = Z / 3 * sin(5 / 4 * (i)) * (sin(5 / 4 * (i))), z = 0)
            temp_mesh.translate(x = Z / 3 * sin(5/4 * (-2 * pi * i / PTS - pi / 2)) * cos(-2 * pi * i / PTS - pi / 2), y = Z / 3 * sin(5/4 * (-2 * pi * i / PTS - pi / 2)) *sin(-2 * pi * i / PTS - pi / 2), z = 0)
            self.mesh_list.append(temp_mesh)
            self.scene.add(temp_mesh)

        self.mesh_list = self.mesh_list[::-1]


    def update(self):

        for i in range(0, PTS):
            x_pos = self.mesh_list[i].getPosition()[0]
            if x_pos > Z / 2:
                self.mesh_list[i].translate(x = -x_pos - Z/2, y = 0, z = 0)
            else:
                self.mesh_list[i].translate(x = i/1000, y = 0, z = 0)

        self.renderer.render(self.scene, self.camera)

# instantiate this class and run the program
Test(screenSize = [900, 900]).run()
