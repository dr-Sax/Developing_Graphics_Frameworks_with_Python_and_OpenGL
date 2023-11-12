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
from OpenGL.GL import *
from geometry.geometry import Geometry
from math import sin
from numpy import arange
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial
from material.material import Material
from extras.axisHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from math import pi

# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 800 / 600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0.5, 1, 5])
        self.scene.add(self.rig)

        axes = AxesHelper(axisLength = 2)
        self.scene.add(axes)

        grid = GridHelper(size = 20, gridColor = [1, 1, 1], centerColor = [1, 1, 1])
        grid.rotateX(-pi / 2)
        self.scene.add(grid)
        self.renderer.render(self.scene, self.camera)

        

    def update(self):
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)

# instantiate this class and run the program
Test(screenSize = [800, 600]).run()

