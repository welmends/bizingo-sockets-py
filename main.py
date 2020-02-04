from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle, RoundedRectangle, Triangle
from kivy.config import Config
from kivy.graphics.context_instructions import Color

class BizingoBoardWidget(Widget):
    def __init__(self, **kwargs):
        super(BizingoBoardWidget, self).__init__(**kwargs)
        with self.canvas:
            triangle_size = 50
            # board area
            Color(.5, .5, .5)
            self.board_area = RoundedRectangle(pos=(60, 60), size=(600, 600), radius=[10])
            self.game_name_label = Label(text="B I Z I N G O", pos=(310,640), font_size=60, font_name='fonts/comicate.ttf') # fonts: comicate, grasping, outwrite, valuoldcaps

            #Type 1 triangles
            Color(0, 0, 0)
            self.board = set()
            base_x = self.board_area.pos[0] + 50
            base_y = self.board_area.pos[1] + 80
            for element in self.generate_triangles_type_1(base_x,base_y,triangle_size):
                self.board.add(Triangle(points=element))

            # Type 0 triangles
            Color(1, 1, 1)
            self.board = set()
            base_x = self.board_area.pos[0] + 50
            base_y = self.board_area.pos[1] + 80
            for element in self.generate_triangles_type_2(base_x,base_y,triangle_size):
                self.board.add(Triangle(points=element))
    
    def generate_triangles_type_1(self, base_x, base_y, size):
        triangles_type_1 = []
        amount = [9,10,11,10,9,8,7,6,5,4,3] # Fixed
        a = b = c = d = e = f = 0
        a = base_x - size
        b = base_y - (size-10)
        for triangles in amount:
            a = base_x - int(size/2)*(1+(triangles-amount[0]))
            b = b + (size-10)
            for triangle in range(triangles):
                a = a + size
                c = a + int(size/2)
                d = b + (size-10)
                e = a + size
                f = b

                triangles_type_1.append([a,b,c,d,e,f])
        return triangles_type_1

    def generate_triangles_type_2(self, base_x, base_y, size):
        triangles_type_2 = []
        amount = [10,11,10,9,8,7,6,5,4,3,2] # Fixed
        a = b = c = d = e = f = 0
        a = base_x
        b = base_y
        for triangles in amount:
            a = base_x + int(size/2) - int(size/2)*(1+(triangles-amount[0]))
            b = b + (size-10)
            for triangle in range(triangles):
                a = a + size
                c = a - int(size/2)
                d = b - (size-10)
                e = a - size
                f = b
                triangles_type_2.append([a,b,c,d,e,f])
        return triangles_type_2
                    
class BizingoApp(App):
    def build(self):
        # Configs
        Config.set('graphics', 'resizable', '0')
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')

        # Parent widget
        parent = Widget()

        # widgets
        self.board = BizingoBoardWidget()
        
        # add widgets
        parent.add_widget(self.board)

        return parent


if __name__ == '__main__':
    BizingoApp().run()