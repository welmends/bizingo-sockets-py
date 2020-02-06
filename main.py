import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Line, Rectangle, RoundedRectangle, Triangle, Ellipse
from kivy.graphics.context_instructions import Color
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.animation import Animation
from kivy.lang import Builder
import math

# Utils

Builder.load_string('''
#:import C kivy.utils.get_color_from_hex

<RoundedTextInput@TextInput>:
    font_size: '14dp'
    background_color: 0,0,0,0
    cursor_color: C('#ffffff')
    canvas.before:
        Color:
            rgba: C('#ffffff')
    canvas.after:
        Color:
            rgb: C('#0f192e')
        Ellipse:
            angle_start:180
            angle_end:360
            pos:(self.pos[0] - self.size[1]/2.0, self.pos[1])
            size: (self.size[1], self.size[1])
        Ellipse:
            angle_start:360
            angle_end:540
            pos: (self.size[0] + self.pos[0] - self.size[1]/2.0, self.pos[1])
            size: (self.size[1], self.size[1])
        Color:
            rgba: C('#3f92db')
        Line:
            points: self.pos[0] , self.pos[1], self.pos[0] + self.size[0], self.pos[1]
        Line:
            points: self.pos[0], self.pos[1] + self.size[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]
        Line:
            ellipse: self.pos[0] - self.size[1]/2.0, self.pos[1], self.size[1], self.size[1], 180, 360
        Line:
            ellipse: self.size[0] + self.pos[0] - self.size[1]/2.0, self.pos[1], self.size[1], self.size[1], 360, 540
''')

class RoundedTextInput(TextInput):
    def build(self):
        return self
    
class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll_type = ['bars']

        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True)
        self.layout.add_widget(self.chat_history)

        self.scroll_to_point = Label()
        self.layout.add_widget(self.scroll_to_point)

    def on_size(self, *args):
        #self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=self.pos, size=self.size)

    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message

        # update
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        # scroll
        self.scroll_to(self.scroll_to_point)


# Bizingo

class BizingoPiece(Widget):
    def __init__(self, position, circle_radius, type, **kwargs):
        super(BizingoPiece, self).__init__(**kwargs)
        self.type = type

        with self.canvas:
            if self.type==1:# player 1
                Color(207/255,4/255,6/255)
            elif self.type==2: # player 1 (cap)
                Color(248/255,236/255,18/255)
            elif self.type==3: # player 2 
                Color(6/255,2/255,6/255)
            elif self.type==4: # player 2 (cap)
                Color(108/255,0/255,213/255)

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
            self.mouse_pos     = (0,0)

            # variables
            self.board_obj = [[],[]]
            self.board_pos = [[],[]]
            self.board_cnt = [[],[]]
            self.pieces    = [[],[]]

            # board button
            self.board_bt   = Button(pos=(65, 65), size=(590, 590))
            self.board_bt.bind(on_release=self.handle)
            self.add_widget(self.board_bt)

            # board area
            Color(203/255,236/255,215/255)
            self.board_area = RoundedRectangle(pos=(60, 60), size=(600, 600), radius=[10])
            self.game_name_label = Label(text="B I Z I N G O", pos=(310,640), font_size=60, font_name='fonts/comicate.ttf') # fonts: comicate, grasping, outwrite, valuoldcaps
            base_x = self.board_area.pos[0] + 50
            base_y = self.board_area.pos[1] + 80

            # type 1 triangles
            Color(255/255,253/255,254/255)
            for element in self.generate_triangles_type_1(base_x,base_y,self.triangle_size):
                self.board_obj[0].append(Triangle(points=element))
                self.board_pos[0].append(element)
                self.board_cnt[0].append(self.cntr_t(element))

            # type 2 triangles
            Color(65/255 ,167/255,107/255)
            for element in self.generate_triangles_type_2(base_x,base_y,self.triangle_size):
                self.board_obj[1].append(Triangle(points=element))
                self.board_pos[1].append(element)
                self.board_cnt[1].append(self.cntr_t(element))

            # player 1 pieces
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][13], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][14], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][15], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][16], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][17], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][23], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][24], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][25], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][26], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][27], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][28], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][32], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][34], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][35], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][36], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][38], self.circle_radius, 1))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][33], self.circle_radius, 2))
            self.pieces[0].append(BizingoPiece(self.board_cnt[0][37], self.circle_radius, 2))

            # player 2 pieces
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][50], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][52], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][53], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][55], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][58], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][59], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][60], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][61], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][62], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][65], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][66], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][67], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][68], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][71], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][72], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][73], self.circle_radius, 3))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][51], self.circle_radius, 4))
            self.pieces[1].append(BizingoPiece(self.board_cnt[1][54], self.circle_radius, 4))

            # bind
            #self.bind(on_release=self.release)

            # # piece animation example
            # anim = Animation(pos=self.cntr_t(self.board_pos[0][1]), duration=1.) + Animation(pos=self.cntr_t(self.board_pos[0][0]), duration=1.)
            # anim.start(self.pieces[0][0])

    def handle(self, instance):
        print(self.mouse_pos)

        x = self.mouse_pos[0]
        y = self.mouse_pos[1]
        close_type = 0
        close_piece = 0
        close_dist = math.sqrt( (x-self.board_cnt[0][0][0])**2 + (y-self.board_cnt[0][0][1])**2 )
        for i in range(len(self.board_cnt)):
            for j in range(len(self.board_cnt[i])):
                dist = math.sqrt( (x-self.board_cnt[i][j][0])**2 + (y-self.board_cnt[i][j][1])**2 )
                if dist < close_dist:
                    close_dist = dist
                    close_type = i
                    close_piece = j

        print(close_type,close_piece)


    def on_touch_move(self,touch):
        self.mouse_pos = (touch.x,touch.y)

    def cntr_t(self, points):
        # return the center of triangle
        new_x = ( ((points[0]+points[2]+points[4])/3) - (self.circle_radius/2.0) )
        new_y = ( ((points[1]+points[3]+points[5])/3) - (self.circle_radius/2.0) )
        return (new_x, new_y) 

    def generate_triangles_type_1(self, base_x, base_y, size):
        triangles_type_1 = []
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
                triangles_type_1.append([a,b,c,d,e,f])
        return triangles_type_1

    def generate_triangles_type_2(self, base_x, base_y, size):
        triangles_type_2 = []
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

                triangles_type_2.append([a,b,c,d,e,f])
        return triangles_type_2

class BizingoChat(GridLayout):
    def __init__(self, **kwargs):
        super(BizingoChat, self).__init__(**kwargs)

        # GridLayout flags
        self.cols = 1
        self.rows = 2
        self.padding = ([0, 20, 60, 20])

        # chat_scrllabel
        self.chat_scrllabel = ScrollableLabel()
        self.add_widget(self.chat_scrllabel)

        # text_input
        self.text_input = RoundedTextInput(text='', size_hint_y=None, height=35, multiline=False)
        self.text_input.focus = True
        self.text_input.bind(on_text_validate=self.on_enter)
        self.add_widget(self.text_input)

    def on_enter(self, instance):
        self.chat_scrllabel.update_chat_history(self.text_input.text)
        instance.text=''

class BizingoGamePage(GridLayout):
    def __init__(self, **kwargs):
        super(BizingoGamePage, self).__init__(**kwargs)

        # GridLayout flags
        self.cols = 2
        self.rows = 1
        self.spacing = ([150,0])

        # Backgorund
        with self.canvas:
            Color(100/255,100/255,100/255)
            self.panel = Rectangle(pos=(0, 0), size=(1280, 720))

        # Board
        self.board = BizingoBoard()
        self.add_widget(self.board)

        # Chat
        self.chat = BizingoChat()
        self.add_widget(self.chat)

class BizingoLoginPage(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas:

            Color(100/255,100/255,100/255)
            self.panel = Rectangle(pos=(0, 0), size=(1280, 720))

            # fonts: comicate, grasping, outwrite, valuoldcaps
            self.game_name_label = Label(text="B I Z I N G O  G A M E", pos=(600,500), font_size=100, font_name='fonts/grasping.ttf')
            

            self.ip_text_label = Label(text="IP", pos=(600,310), font_size=40)

            self.ip_text_input = TextInput(text='', pos=(550,300), size=(200,30), multiline=False, font_name='fonts/comicate.ttf')
            self.ip_text_input.focus = True
            self.ip_text_input.halign = 'center'
            self.ip_text_input.valign = 'middle'
            self.ip_text_input.bind(on_text_validate=self.on_enter)
            

            self.port_text_label = Label(text="Porta", pos=(600,210), font_size=40)

            self.port_text_input = TextInput(text='', pos=(550,200), size=(200,30), multiline=False, font_name='fonts/comicate.ttf')
            self.port_text_input.focus = True
            self.port_text_input.halign = 'center'
            self.port_text_input.valign = 'middle'
            self.port_text_input.bind(on_text_validate=self.on_enter)

            self.add_widget(self.ip_text_label)
            self.add_widget(self.ip_text_input)
            self.add_widget(self.port_text_label)
            self.add_widget(self.port_text_input)

            self.ip_button = Button(text="Connect", pos=(600,100), size=(100,50))
            self.ip_button.bind(on_release=self.connect)
            self.add_widget(self.ip_button)  

    def on_enter(self, instance):
        print(instance.text)
        instance.text=''

    def connect(self, _):
        print('connecting..')
        bizingo.screen_manager.current = 'game'

class BizingoApp(App):
    def build(self):
        # Configs
        Config.set('graphics', 'resizable', '0')
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')

        # Screen Manager
        self.screen_manager = ScreenManager()
        
        # Login Page
        self.login_page = BizingoLoginPage()
        screen = Screen(name='login')
        screen.add_widget(self.login_page)
        self.screen_manager.add_widget(screen)

        # Game Page
        self.game_page = BizingoGamePage()
        screen = Screen(name='game')
        screen.add_widget(self.game_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == '__main__':
    bizingo = BizingoApp()
    bizingo.run()