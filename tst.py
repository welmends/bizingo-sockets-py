from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.scroll_type = ['bars']

class ScrollApp(App):
    def build(self):
        long_text = 'hey ' * 2000
        return ScrollableLabel(text=long_text)

if __name__ == "__main__":
    ScrollApp().run()