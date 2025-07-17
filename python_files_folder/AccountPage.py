from kivy.uix.screenmanager import Screen, ScreenManager


class AccountPageScreenManager(ScreenManager):

    def on_kv_post(self, base_widget):
        self.isUserRegister()

    def isUserRegister(self):
        if (1==2):
            self.current = 'UserProfilePageScreen'
        else:
            self.current = 'SignupAndLoginPageScreen'


    