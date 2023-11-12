from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *
from core.shapes import circle, triangle, pentagon
from math import pi, sqrt

# render 2 shapes
class Test(Base):

    def initialize(self):
        print('Initializing program...')
        ### initialize program ###

        # vertex shader code 
        vsCode = """
        in vec3 position;
        in vec3 vertexColor;
        out vec3 color;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
            color = vertexColor;
        }
        """

        # fragment shader code
        fsCode = '''
        in vec3 color;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(color.r, color.g, color.b, 1.0);
        }
        '''

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        glLineWidth(10)

        ### setup vertex array object - circle ###
        self.vao_c1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c1)
        c1 = circle.Circle(-pi / 2, 3 *pi/2, 1, 50000, 0, 0)
        positionData_c1 = c1.circle_array()
        self.vertexCount_c1 = len(positionData_c1)
        positionAttribute_c1 = Attribute("vec3", positionData_c1)
        positionAttribute_c1.associateVariable(self.programRef, "position")

        # circle color array
        circle_color_array = []
        for i in range(0, int(self.vertexCount_c1 / 5)):
            circle_color_array.append([1.,0.039,0.329])
            circle_color_array.append([1.,0.278,0.494])
            circle_color_array.append([1.,0.361,0.541])
            circle_color_array.append([1.,0.439,0.588])
            circle_color_array.append([1.,0.522,0.631])
            circle_color_array.append([1.,0.6,0.675])
            circle_color_array.append([0.984,0.694,0.741])
            circle_color_array.append([0.976,0.745,0.78])
            circle_color_array.append([0.969,0.792,0.816])
            circle_color_array.append([0.969,0.792,0.816])
            circle_color_array.append([0.98,0.878,0.894])
    

        colorAttribute_c1 = Attribute('vec3', circle_color_array)
        colorAttribute_c1.associateVariable(self.programRef, 'vertexColor')
        

        ### setup vertex array object - pentagon ###
        # self.vao_p1 = glGenVertexArrays(1)
        # glBindVertexArray(self.vao_p1)
        p1 = pentagon.Pentagon()
        positionData_p1 = p1.inverted_pentagon_coords()
        # self.vertexCount_p1 = len(positionData_p1)
        # positionAttribute_p1 = Attribute("vec3", positionData_p1)
        # positionAttribute_p1.associateVariable(self.programRef, "position")
        # colorAttribute_p1 = Attribute('vec3', [])
        # colorAttribute_p1.associateVariable(self.vao_p1, 'vertexColor')

        ### setup vertex array object - pentagon ###
        self.vao_t1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t1)
        positionData_t1 = [positionData_p1[1], positionData_p1[4], positionData_p1[3]]
        self.vertexCount_t1 = len(positionData_t1)
        positionAttribute_t1 = Attribute("vec3", positionData_t1)
        positionAttribute_t1.associateVariable(self.programRef, "position")
        t1_color_array = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]
        colorAttribute_t1 = Attribute('vec3', t1_color_array)
        colorAttribute_t1.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - pentagon ###
        self.vao_t2 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t2)
        positionData_t2 = [positionData_p1[2], positionData_p1[1], positionData_p1[4]]
        self.vertexCount_t2 = len(positionData_t2)
        positionAttribute_t2 = Attribute("vec3", positionData_t2)
        positionAttribute_t2.associateVariable(self.programRef, "position")
        t2_color_array = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]
        colorAttribute_t2 = Attribute('vec3', t2_color_array)
        colorAttribute_t2.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - pentagon ###
        self.vao_t3 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t3)
        positionData_t3 = [positionData_p1[3], positionData_p1[0], positionData_p1[2]]
        self.vertexCount_t3 = len(positionData_t3)
        positionAttribute_t3 = Attribute("vec3", positionData_t3)
        positionAttribute_t3.associateVariable(self.programRef, "position")
        t3_color_array = [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0]
        ]
        colorAttribute_t3 = Attribute('vec3', t3_color_array)
        colorAttribute_t3.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - circle ###
        self.vao_c2 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c2)
        c2 = circle.Circle(0, 2 * pi, 0.27, 550, 0.427, -0.585)
        positionData_c2 = c2.circle_array()
        self.vertexCount_c2 = len(positionData_c2)
        positionAttribute_c2 = Attribute("vec3", positionData_c2)
        positionAttribute_c2.associateVariable(self.programRef, "position")
        circle_color_array = []
        for i in range(0, int(self.vertexCount_c2 / 100)):
            circle_color_array.append([1.0, 1.0, 1.0])
            circle_color_array.append([0.0, 0.0, 0.0])


        colorAttribute_c2 = Attribute('vec3', circle_color_array)
        colorAttribute_c2.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - circle ###
        self.vao_c3 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c3)
        c3 = circle.Circle(0, 2 * pi, 0.27, 550, 0.688, 0.222)
        positionData_c3 = c3.circle_array()
        self.vertexCount_c3 = len(positionData_c3)
        positionAttribute_c3 = Attribute("vec3", positionData_c3)
        positionAttribute_c3.associateVariable(self.programRef, "position")
        circle_color_array = []
        for i in range(0, int(self.vertexCount_c3 / 100)):
            circle_color_array.append([1.0, 1.0, 1.0])
            circle_color_array.append([0.0, 0.0, 0.0])

        colorAttribute_c3 = Attribute('vec3', circle_color_array)
        colorAttribute_c3.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - circle ###
        self.vao_c4 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c4)
        c4 = circle.Circle(0, 2 * pi, 0.27, 550, -0.427, -0.585)
        positionData_c4 = c4.circle_array()
        self.vertexCount_c4 = len(positionData_c4)
        positionAttribute_c4 = Attribute("vec3", positionData_c4)
        positionAttribute_c4.associateVariable(self.programRef, "position")
        circle_color_array = []
        for i in range(0, int(self.vertexCount_c4 / 100)):
            circle_color_array.append([1.0, 1.0, 1.0])
            circle_color_array.append([0.0, 0.0, 0.0])

        colorAttribute_c4 = Attribute('vec3', circle_color_array)
        colorAttribute_c4.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - circle ###
        self.vao_c5 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c5)
        c5 = circle.Circle(0, 2 * pi, 0.27, 550, -0.688, 0.222)
        positionData_c5 = c5.circle_array()
        self.vertexCount_c5 = len(positionData_c5)
        positionAttribute_c5 = Attribute("vec3", positionData_c5)
        positionAttribute_c5.associateVariable(self.programRef, "position")
        circle_color_array = []
        for i in range(0, int(self.vertexCount_c5 / 100)):
            circle_color_array.append([1.0, 1.0, 1.0])
            circle_color_array.append([0.0, 0.0, 0.0])

        colorAttribute_c5 = Attribute('vec3', circle_color_array)
        colorAttribute_c5.associateVariable(self.programRef, 'vertexColor')

        ### setup vertex array object - circle ###
        self.vao_c6 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c6)
        c6 = circle.Circle(0, 2*pi, 0.27, 550, 0, 0.722)
        positionData_c6 = c6.circle_array()
        self.vertexCount_c6 = len(positionData_c6)
        positionAttribute_c6 = Attribute("vec3", positionData_c6)
        positionAttribute_c6.associateVariable(self.programRef, "position")
        circle_color_array = []
        for i in range(0, int(self.vertexCount_c6 / 100)):
            circle_color_array.append([1.0, 1.0, 1.0])
            circle_color_array.append([0.0, 0.0, 0.0])

        colorAttribute_c6 = Attribute('vec3', circle_color_array)
        colorAttribute_c6.associateVariable(self.programRef, 'vertexColor')

    
    def update(self):

        # select program to use when rendering
        glUseProgram(self.programRef)

        # draw the circle
        glBindVertexArray(self.vao_c1)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount_c1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw the pentagon
        #glBindVertexArray(self.vao_p1)
        #glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_p1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw triangle 1
        glBindVertexArray(self.vao_t1)
        glDrawArrays(GL_LINE_STRIP, 0, self.vertexCount_t1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw triangle 2
        glBindVertexArray(self.vao_t2)
        glDrawArrays(GL_LINE_STRIP, 0, self.vertexCount_t2)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw triangle 3
        glBindVertexArray(self.vao_t3)
        glDrawArrays(GL_LINE_STRIP, 0, self.vertexCount_t3)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES
        
        glBindVertexArray(self.vao_c2)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount_c2) 

        glBindVertexArray(self.vao_c3)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount_c3) 

        glBindVertexArray(self.vao_c4)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount_c4) 

        glBindVertexArray(self.vao_c5)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount_c5) 

        glBindVertexArray(self.vao_c6)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount_c6)

# instantiate this class and run the program
Test(screenSize=[1000, 1000]).run()
