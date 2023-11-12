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

from OpenGL.GL import *

Z = 20
# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 540 / 960)
        self.camera.setPosition([0, 0, Z])

        geometry = ConeGeometry(radius = 1/2, heightSegments = 100)
        geometry2 = HalfSphereGeometry(heightSegments=100, radiusSegments=100)
        self.geometry3 = RectangleGeometry()

        geometry4 = RectangleGeometry(height = 25, width = 1)
        pane_grid = Texture('images/colorful.png')
        pane_material = TextureMaterial(pane_grid)
        self.mesh4 = Mesh(geometry4, pane_material)
        self.mesh4.translate(x = -6, y = 0, z = 0)
        self.scene.add(self.mesh4)

        geometry5 = RectangleGeometry(height = 25, width = 1)
        pane_grid = Texture('images/colorful.png')
        pane_material = TextureMaterial(pane_grid)
        self.mesh5 = Mesh(geometry5, pane_material)
        self.mesh5.translate(x = 6, y = 0, z = 0)
        self.scene.add(self.mesh5)

        geometry6 = RectangleGeometry(height = 1, width = 16)
        pane_grid = Texture('images/colorful.png')
        pane_material = TextureMaterial(pane_grid)
        self.mesh6 = Mesh(geometry6, pane_material)
        self.mesh6.translate(x = 0, y = -11, z = 0)
        self.scene.add(self.mesh6)

        geometry7 = RectangleGeometry(height = 1, width = 16)
        pane_grid = Texture('images/colorful.png')
        pane_material = TextureMaterial(pane_grid)
        self.mesh7 = Mesh(geometry7, pane_material)
        self.mesh7.translate(x = 0, y = 11, z = 0)
        self.scene.add(self.mesh7)

        geometry8 = RectangleGeometry(height = 23, width = 0.25)
        pane_grid = Texture('images/colorful.png')
        pane_material = TextureMaterial(pane_grid)
        self.mesh8 = Mesh(geometry8, pane_material)
        self.scene.add(self.mesh8)

        geometry9 = RectangleGeometry(height = 0.25, width = 13)
        pane_grid = Texture('images/colorful.png')
        pane_material = TextureMaterial(pane_grid)
        self.mesh9 = Mesh(geometry9, pane_material)
        self.scene.add(self.mesh9)

        grid = Texture('images/rain.png')
        material = TextureMaterial(grid)

        self.cap = cv2.VideoCapture('images/world.mp4')
        success, img = self.cap.read()
        grid3 = Texture(img)
        material3 = TextureMaterial(grid3)
    

        self.mesh = Mesh(geometry, material)
        self.mesh2 = Mesh(geometry2, material)
        self.mesh3 = Mesh(self.geometry3, material3)

        self.mesh2.translate(x = 0, y = -1/2, z = 0)
        self.mesh3.translate(x = 3, y = 0, z = 0)

        self.scene.add(self.mesh)
        self.scene.add(self.mesh2)
        self.scene.add(self.mesh3)

    def update(self):
        if self.mesh.getPosition()[1] >= - Z / 2 + 0.5:
            self.mesh.translate(x = 0, y = -0.3, z = 0)
            self.mesh2.translate(x = 0, y = -0.3, z = 0)
        else:
            self.mesh.translate(x = 0, y = Z + 0.3, z = 0)
            self.mesh2.translate(x = 0, y = Z + 0.3, z = 0)
        
        if self.mesh8.getPosition()[1] >= - Z / 2 + 0.5:
            self.mesh8.translate(x = 0, y = -0.3, z = 0)
            self.mesh8.translate(x = 0, y = -0.3, z = 0)
        else:
            self.mesh8.translate(x = 0, y = Z + 0.3, z = 0)
            self.mesh8.translate(x = 0, y = Z + 0.3, z = 0)
        
        success, img = self.cap.read()
        grid3 = Texture(img)
        material3 = TextureMaterial(grid3)
        self.scene.remove(self.mesh3)
        self.mesh3 = Mesh(self.geometry3, material3)
        self.scene.add(self.mesh3)
        
        self.renderer.render(self.scene, self.camera)

# instantiate this class and run the program
Test(screenSize = [540, 960]).run()
