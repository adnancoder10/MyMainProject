from kivy.lang import Builder

def LoadAllKvFiles():

    Builder.load_file('./kivymd_files_folder/MainPageStyle.kv')
    Builder.load_file('./kivymd_files_folder/HomePageStyle.kv')
    Builder.load_file('./kivymd_files_folder/AccountPageStyle.kv')
    Builder.load_file('./kivymd_files_folder/BusinessesPage.kv')
    Builder.load_file('./kivymd_files_folder/ProductesPage.kv')
    Builder.load_file('./kivymd_files_folder/SignupAndLoginPageStyle.kv')
    Builder.load_file('./kivymd_files_folder/UserProfilePageStyle.kv')
    Builder.load_file('./kivymd_files_folder/SignupPagesStyle.kv')



