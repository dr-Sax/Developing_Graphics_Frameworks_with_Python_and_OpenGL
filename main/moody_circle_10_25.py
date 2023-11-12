from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *
from core.shapes import circle

# animate triangle moving across screen
class Test(Base):

    def initialize(self):

        ### initialize program ###
        vsCode = '''
        in vec3 position;
        void main()
        {
            vec3 pos = position;
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        '''

        fsCode = '''
        uniform vec3 baseColor;
        uniform vec3 translation;
        out vec4 fragColor;
        void main()
        {
            vec3 bc = baseColor - translation;
            fragColor = vec4(bc.r, bc.g, bc.b, 1.0);
        }
        '''

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        # specify color used when clearing
        glClearColor(0.0, 0.0, 0.0, 1.0)

        ### set up vertex array object ###
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ### set up vertex attribute ###
        positionData = [
            [0.0, 0.2, 0.0], 
            [0.2, -0.2, 0.0], 
            [-0.2, -0.2, 0.0]
        ]

        self.vertexCount = len(positionData)
        positionAttribute = Attribute('vec3', positionData)
        positionAttribute.associateVariable(self.programRef, 'position')

        ### set up uniforms ###
        self.translation = Uniform('vec3', [-0.05, -0.05, -0.05])
        self.translation.locateVariable(self.programRef, 'translation')

        self.baseColor = Uniform('vec3', [1.0, 1.0, 1.0])
        self.baseColor.locateVariable(self.programRef, "baseColor")

        # triangle speed, units per second
        self.speed = 0.5
    
    def update(self):

        ### update data ###

        distance = self.speed * self.deltaTime  # elapsed time since previous render
        if self.input.isKeyPressed('left'):
            self.translation.data[0] -= distance
        if self.input.isKeyPressed('right'):
            self.translation.data[0] += distance
        if self.input.isKeyPressed('down'):
            self.translation.data[1] -= distance
        if self.input.isKeyPressed('up'):
            self.translation.data[1] += distance

        ### render scene ###
        
        # reset color buffer with specified color
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programRef)

        # draw the triangle
        self.translation.uploadData()
        self.baseColor.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

# instantiate this class and run the program
Test().run()


