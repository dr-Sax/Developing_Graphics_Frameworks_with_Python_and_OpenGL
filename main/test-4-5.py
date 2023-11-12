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

# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 800 / 600)
        self.camera.setPosition([0, 0, 7])

        #geometry = SphereGeometry(radius = 3, radiusSegments = 128, heightSegments = 64)  # main geometry is a sphere
        geometry = PyramidGeometry(radius = 3, height = 3, heightSegments = 64)

        vsCode = '''
        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform float time;
        void main()
        {
            float offset = 0.5 * cos(32.0 * vertexPosition.x + time) * cos(32.0 * vertexPosition.x + time);  
            vec3 pos = vertexPosition + vec3(0.0, offset, 0.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1);
            color = vertexColor;
        }
        '''

        fsCode = '''
        in vec3 color;
        uniform float time;
        out vec4 fragColor;
        void main()
        {
            float r = abs(sin(time));
            vec4 c = vec4(r, -0.1 * r, 0.7 * r, 0.0);
            fragColor = vec4(color, 1.0) + c;
        }
        '''

        material = Material(vsCode, fsCode)
        material.addUniform('float', 'time', 0)
        material.locateUniforms()

        self.time = 0;
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)
        self.renderer.render(self.scene, self.camera)

    def update(self):
        self.time += 10/60
        self.mesh.material.uniforms['time'].data = self.time
        self.mesh.rotateY(.01)
        self.mesh.rotateX(.01)
        self.renderer.render(self.scene, self.camera)

# instantiate this class and run the program
Test(screenSize = [800, 600]).run()

