from kivy.uix.screenmanager import Screen

class MainPage(Screen):

    def on_pre_enter(self, *args):
        print(self.ids.AccountPage.name)
        print(self.ids.AccountPage.text)
    

