from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics import Line, Rectangle, RoundedRectangle, Triangle, Ellipse
from kivy.config import Config
from kivy.graphics.context_instructions import Color
from kivy.animation import Animation

class BizingoPiece(Widget):
    def __init__(self, position, circle_radius, **kwargs):
        super(BizingoPiece, self).__init__(**kwargs)

        with self.canvas:
            Color(207/255,4/255,6/255)
            self.piece = Ellipse(pos=position, size=(circle_radius,circle_radius))
            self.bind(pos = self.updatePosition)

        self.pos = self.piece.pos

    def updatePosition(self, *args):
        self.piece.pos = self.pos

class BizingoBoard(Widget):
    piece = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BizingoBoard, self).__init__(**kwargs)
        with self.canvas:
            # default parameters
            self.triangle_size = 50
            self.circle_radius = 15
            # self.color_board = Color(203,236,215)
            # self.color_btype1 = Color(65,167,107)
            # self.color_btype2 = Color(255,253,254)
            # self.color_ptype1 = Color(207,4,6)
            # self.color_pctype1 = Color(248,236,18)
            # self.color_ptype1 = Color(6,2,6)
            # self.color_pctype1 = Color(108,0,213)

            # variables
            self.board_obj = [[],[]]
            self.board_pos = [[],[]]

            # board area
            Color(203/255,236/255,215/255)
            self.board_area = RoundedRectangle(pos=(60, 60), size=(600, 600), radius=[10])
            self.game_name_label = Label(text="B I Z I N G O", pos=(310,640), font_size=60, font_name='fonts/comicate.ttf') # fonts: comicate, grasping, outwrite, valuoldcaps

            # type 1 triangles
            Color(65/255,167/255,107/255)
            base_x = self.board_area.pos[0] + 50
            base_y = self.board_area.pos[1] + 80
            for element in self.generate_triangles_type_1(base_x,base_y,self.triangle_size):
                self.board_obj[0].append(Triangle(points=element))
                self.board_pos[0].append(element)

            # type 0 triangles
            Color(255/255, 253/255, 254/255)
            base_x = self.board_area.pos[0] + 50
            base_y = self.board_area.pos[1] + 80
            for element in self.generate_triangles_type_2(base_x,base_y,self.triangle_size):
                self.board_obj[1].append(Triangle(points=element))
                self.board_pos[1].append(element)

            # piece animation example
            self.bizingo_piece = BizingoPiece(self.cntr_t(self.board_pos[0][0]), self.circle_radius)
            self.add_widget(self.bizingo_piece)
            anim = Animation(pos=self.cntr_t(self.board_pos[0][1]), duration=1.) + Animation(pos=self.cntr_t(self.board_pos[0][0]), duration=1.)
            anim.start(self.bizingo_piece)

    def cntr_t(self, points):
        # return the center of triangle
        new_x = ( ((points[0]+points[2]+points[4])/3) - (self.circle_radius/2.0) )
        new_y = ( ((points[1]+points[3]+points[5])/3) - (self.circle_radius/2.0) )
        return (new_x, new_y) 

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

class BizingoChat(Widget):

    def __init__(self, **kwargs):
        super(BizingoChat, self).__init__(**kwargs)
        with self.canvas:
            Color(128/255,128/255,128/255)

class BizingoPanel(Widget):
    def __init__(self, **kwargs):
        super(BizingoPanel, self).__init__(**kwargs)
        with self.canvas:
            Color(100/255,100/255,100/255)
            self.panel = Rectangle(pos=(0, 0), size=(1280, 720))
            
class BizingoApp(App):
    def build(self):
        # Configs
        Config.set('graphics', 'resizable', '0')
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')

        # Parent widget
        parent = Widget()

        # widgets
        self.panel = BizingoPanel()
        self.board = BizingoBoard()
        self.chat = BizingoChat()

        # add widgets
        parent.add_widget(self.panel)
        parent.add_widget(self.board)
        parent.add_widget(self.chat)

        return parent

if __name__ == '__main__':
    BizingoApp().run()