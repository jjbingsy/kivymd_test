from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
#from kivymd.uix.recyclegridlayout import RecycleGridLayout

Builder.load_string('''
#:import MDRecycleGridLayout kivymd.uix.recyclegridlayout

<StatefulLabel>:
    active: stored_state.active
    orientation: 'horizontal'
    CheckBox:
        id: stored_state
        size_hint_x: None
        width: dp(50)
        active: root.active
        on_release: root.store_checkbox_state()
    Label:
        size_hint_x: None
        width: dp(60)
        text: f"{root.text} {root.generated_state_text}"

<RV>:
    viewclass: 'StatefulLabel'
    md_bg_color: app.theme_cls.primaryColor
    MDRecycleGridLayout:
        cols: 1
        #padding: dp(4)
        #spacing: dp(2)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
    # MDRecycleBoxLayout:
    #     size_hint_y: None
    #     height: self.minimum_height
    #     orientation: 'vertical'
''')

class StatefulLabel(RecycleDataViewBehavior, MDBoxLayout):
    text = StringProperty()
    generated_state_text = StringProperty()
    active = BooleanProperty()
    index = 0

    '''
    To change a viewclass' state as the data assigned to it changes,
    overload the refresh_view_attrs function (inherited from
    RecycleDataViewBehavior)
    '''
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        x = int(data['text'])
        if not x:
            self.generated_state_text = "is zero"
        elif x % 2 == 1:
            self.generated_state_text = "is odd"
        else:
            self.generated_state_text = "is even"

        super(StatefulLabel, self).refresh_view_attrs(rv, index, data)

    '''
    To keep state changes in the viewclass with associated data,
    they can be explicitly stored in the RecycleView's data object
    '''
    def store_checkbox_state(self):
        rv = MDApp.get_running_app().rv
        rv.data[self.index]['active'] = self.active


class RV(MDRecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x), 'active': False} for x in range(100)]
        MDApp.get_running_app().rv = self

class realApp(MDApp):

    def build(self):
        return RV() 





if __name__ == '__main__':
    realApp().run()