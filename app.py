from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from python_files_folder import MainPage, HomePage, BusinessesPage,ProductesPage, AccountPage, UserProfilePage, SignupAndLoginPage, SignupPages
from kivy.core.window import Window
from kivymd_files_folder import loadKvFiles
from kivy import Config
from kivy.core.text import LabelBase

Window.size = (355, 670)


# Load kv style files here 
loadKvFiles.LoadAllKvFiles()

class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainPage.MainPage(name='mainPage'))
        self.sm.add_widget(SignupPages.SignupPageScreens(name='SignupPageScreens'))
        return self.sm


if __name__=="__main__":
    MainApp().run()