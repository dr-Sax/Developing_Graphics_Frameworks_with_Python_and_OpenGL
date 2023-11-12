from core.base import Base

# check input
class Test(Base):

    def initialize(self):
        print("initializing program...")
    
    def update(self):

        # debug printing
        if len(self.input.keyDownList) > 0:
            print('Keys down:', self.input.keyDownList)
        
        if len(self.input.keyPressedList) > 0:
            print('Keys pressed:', self.input.keyPressedList)
        
        if len(self.input.keyUpList) > 0:
            print('Keys up:', self.input.keyUpList)

# instantiate this class and run the program
Test().run()