from kivy.core.text import LabelBase
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivy.metrics import dp
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox
import regex as re
import os 
from kivy.storage.jsonstore import JsonStore
import requests
import mimetypes
import json


signupDateAndErrors = JsonStore('/home/adnan-khan/Desktop/MyMainProject/JsonStore_files_folder/signupDateAndError.json')

class SignupPageScreens(Screen):pass
class SignupPageScreenManager(ScreenManager):pass

class HoverButton(Button, HoverBehavior):
    def on_enter(self):
        self.background_color = (0.6, 0.6, 0.6, 0.6)

    def on_leave(self):
        self.background_color = (0.9, 0.9, 0.9, 1)

# Showing dropdown menu start here
def DropDownMenu(textfield, focus, options):
    dropdown = DropDown()
    textfield.bind(text=lambda instance, value: dismiss_on_typing(dropdown, value))
    if focus:
        for option in options:
            btn = HoverButton(text=option, 
                size_hint_y=None, 
                height=30,
                background_normal='',  # Remove default button background
                background_color=(0.9, 0.9, 0.9, 1),  # Pure white buttons
                color=(0, 0, 0, 1),  # Black text color
                border = (1, 1, 0, 0))
            btn.bind(on_release=lambda btn: select_option(textfield, dropdown, btn.text))
            dropdown.add_widget(btn)

        dropdown.open(textfield)

def dismiss_on_typing(dropdown, value):
    dropdown.dismiss()

def select_option(textfield, dropdown, text):
    textfield.text = text  # Set the selected text
    dropdown.dismiss()  # Close dropdown
# Showing dropdown menu end here


class BusinesNameAndCagegoryScreen(Screen):
    IsClickedOnNext = False
    SignupBusinessNameInputError = False
    SignupBusinessCategoryInputError = False
        
    def GoingToBusinesseIndustryAndDescriptionScreen(self, boxlayoutOfBNC):
        global signupDateAndErrors
        self.IsInputValid = True
        self.IsClickedOnNext = True
        SignupBusinessNameInput = self.ids.SignupBusinessNameInput.text.strip()
        SignupBusinessCategoryInput = self.ids.SignupBusinessCategoryInput.text.strip()

        def CheckBNFormOldServerErrors(NameInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessNameError' in oldServerError:
                    for erros in oldServerError['BusinessNameError']:
                        if erros['value'] == NameInputValue:
                            self.ShowSignupBusinessNameInputError(boxlayoutOfBNC, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBCFormOldServerErrors(CategoryInput):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessCategoryError' in oldServerError:
                    for erros in oldServerError['BusinessCategoryError']:
                        if erros['value'] == CategoryInput:
                            self.ShowSignupBusinessCategoryInputError(boxlayoutOfBNC, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False            

        # Singup business name error start here
        # Create the error label only once
        if (self.SignupBusinessNameInputError == False):
            self.SignupBusinessNameInputError = MDLabel( size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        if (self.SignupBusinessCategoryInputError == False):
            self.SignupBusinessCategoryInputError = MDLabel( size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        # Determine error message based on input
        if len(SignupBusinessNameInput) == 0:
            self.ShowSignupBusinessNameInputError(boxlayoutOfBNC, "Business name is required")
            self.IsInputValid = False

        elif len(SignupBusinessNameInput) == 1:
            self.ShowSignupBusinessNameInputError(boxlayoutOfBNC, "Business name must be more than 1 letter")
            self.IsInputValid = False

        elif not re.match(r"^[\p{L}0-9\s&'.\-–—,:/()`’‘“”]+$", SignupBusinessNameInput):
            self.ShowSignupBusinessNameInputError(boxlayoutOfBNC, "Business name contains invalid characters")
            self.IsInputValid = False
            
        elif re.match(r"^[\d\s]+$", SignupBusinessNameInput):
            self.ShowSignupBusinessNameInputError(boxlayoutOfBNC, "Business name cannot be just numbers")
            self.IsInputValid = False

        elif(CheckBNFormOldServerErrors(SignupBusinessNameInput)):
            self.IsInputValid = False

        else:
            self.RemoveSignupBusinessNameInputError(boxlayoutOfBNC)

        if (len(SignupBusinessCategoryInput) == 0):
            self.ShowSignupBusinessCategoryInputError(boxlayoutOfBNC, 'Business category is required')
            self.IsInputValid = False

        elif len(SignupBusinessCategoryInput) == 1:
            self.ShowSignupBusinessCategoryInputError(boxlayoutOfBNC, 'Business category must be more then 1 letter')
            self.IsInputValid = False
        
        elif not re.match(r"^[\p{L}0-9\s&'.\-–—,:/()`’‘“”]+$", SignupBusinessCategoryInput):
            self.ShowSignupBusinessCategoryInputError(boxlayoutOfBNC, "Business category contains invalid characters")
            self.IsInputValid = False
            
        elif re.match(r"^[\d\s]+$", SignupBusinessCategoryInput):
            self.ShowSignupBusinessCategoryInputError(boxlayoutOfBNC, "Business category cannot be just numbers")
            self.IsInputValid = False


        elif (CheckBCFormOldServerErrors(SignupBusinessCategoryInput)):
            self.IsInputValid = False
            
        else:
            self.RemoveSignupBusinessCategoryInputError(boxlayoutOfBNC)
            
        # if len(SignupBusinessNameInput.text.strip()) >= 2 and len(SignupBusinessCategoryInput.text.strip()) >= 2:
        if (self.IsInputValid):

            signupDateAndErrors.put('SignupUserBusinessForm', name=SignupBusinessNameInput, Category=SignupBusinessCategoryInput)
            self.parent.transition.direction = 'left'
            self.parent.current = 'BusinesseIndustryAndDescriptionScreen'
            print('Name of business: ',SignupBusinessNameInput)
            print('Category of business: ',SignupBusinessCategoryInput.strip())


    def ShowSignupBusinessNameInputError(self, boxlayout, ErrorText):
        self.SignupBusinessNameInputError.text = ErrorText  # Always update the text
        indexOf = boxlayout.children.index(self.ids.SignupBusinessNameInput)
        # Add the label only if it's not already in the layout
        if self.SignupBusinessNameInputError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessNameInputError, index=indexOf)

    def ShowSignupBusinessCategoryInputError(self, boxlayout, ErrorText):
        self.SignupBusinessCategoryInputError.text = ErrorText
        indexOf = boxlayout.children.index(self.ids.SignupBusinessCategoryInput)
        if self.SignupBusinessCategoryInputError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessCategoryInputError, index= indexOf)

        if self.SignupBusinessCategoryInputError.text == 'Business category must be more then 1 letter' or self.SignupBusinessCategoryInputError.text == "Business category contains invalid characters":
            self.SignupBusinessCategoryInputError.size_hint_y = dp(1)
        elif self.SignupBusinessCategoryInputError.text == 'Business category is required':
            self.SignupBusinessCategoryInputError.size_hint_y = dp(0.1)


    def RemoveSignupBusinessNameInputError(self, boxlayout):
        if self.SignupBusinessNameInputError in boxlayout.children:
            boxlayout.remove_widget(self.SignupBusinessNameInputError)
    
    def RemoveSignupBusinessCategoryInputError(self, boxlayout):
        if self.SignupBusinessCategoryInputError in boxlayout.children:
            boxlayout.remove_widget(self.SignupBusinessCategoryInputError)
        
    def TextingToSignupBusinessNameInput(self, text, boxlayout):
        if self.IsClickedOnNext:
            if len(text.strip()) >= 2:
                self.RemoveSignupBusinessNameInputError(boxlayout)
    def TextingToSignupBusinessCategoryInput(self, text, boxlayout):
        if self.IsClickedOnNext:
            if len(text.strip()) >= 2:
                self.RemoveSignupBusinessCategoryInputError(boxlayout)

    def show_dropdown(self, textfield, focus):
        DropDownMenu(textfield, focus, ["Shop","Hospital and Healthcare","Company","Educational Institution","Restaurant and Food Service","Hotels and Accommodation","Transportation","Entertainment","Non-Profit Organization"])
    
    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        boxlayout = self.ids.signupBNACbox

        if inputName == 'name':
            self.ShowSignupBusinessNameInputError(boxlayout, inputError[0])
            
        elif inputName == 'Category':
            self.ShowSignupBusinessCategoryInputError(boxlayout, inputError[0])

        
        print('Hey this server error method in BusinesNameAndCagegoryScreen')
        print(f'The server say there is an error "{inputName}" and the error is "{inputError}"')

class BusinesseIndustryAndDescriptionScreen(Screen):
    SignupBusinessIndustryInputError = False
    SignupBusinessDescriptionInputError = False
    IsClickedOnNext = False

    def show_dropdown(self, textfield, focus):
        global SignupUserForm
        global signupDateAndErrors
        getCategoryForOption = signupDateAndErrors.get('SignupUserBusinessForm')['Category']
        if (getCategoryForOption == "Shop"):
            ShopsIndustriesList = ["Apparel store","Bakery","Bank","Barber shop","Beauty salon","Bookstore","Cafe","Car wash","Coffee shop","Convenience store","Department store","Electronics store","Florist","Furniture store","Gas station","Gift shop","Grocery store","Gym","Hair salon","Hardware store","Hotel","Ice cream parlor","Insurance agency","Jewelry store","Juice bar","Kitchenware store","Laundry service","Lingerie store","Mattress store","Medical clinic","Men's clothing store","Mobile phone store","Movie theater","Nail salon","Office supply store","Optical store","Outlet store","Paint store","Pet store","Pharmacy","Photo studio","Restaurant","Rug store","Shoe store","Sporting goods store","Supermarket","Tanning salon","Tea house","Travel agency","Women's clothing store"]
            DropDownMenu(textfield, focus, ShopsIndustriesList)

        elif (getCategoryForOption == "Hospital and Healthcare"):
            Hospital_and_HealthcareIndustriesList = ['General Hospital (Public and Private)', 'Specialty Hospital', 'Teaching and Research Hospital','Children’s Hospital', 'Psychiatric Hospital', 'Military Hospital', 'Government Hospital', 'General Practice Clinics','Specialty Clinics ', 'Urgent Care Centers', 'Dental Clinics', 'Outpatient Surgery Centers', 'Diagnostic and Imaging Centers','NurSign Homes', 'Assisted Living Facilities', 'Rehabilitation Centers', 'Palliative Care and Hospice Centers','Surgical Instruments Manufacturers', 'Diagnostic Equipment Companies ', 'Prosthetics and Orthotics Providers','Mobility Devices ', 'Pharmaceutical Companies', 'Biotechnology Firms ', 'Drug Distribution Companies','Private Insurance Companies', 'Public Health Insurance Programs', 'Telemedicine Platforms', 'Health Data Analytics Companies','Remote Monitoring Systems', 'Government Health Agencies', 'Physical Therapy and Occupational Therapy Clinics','Nutrition and Dietetics Services', 'Speech and Language Therapy', 'Diagnostic Laboratories', 'Clinical Research Organizations','Academic Research Institutions', 'Home NurSign Services', 'Elderly Care Services', 'Home-Based Therapy Services','Chiropractic Clinics', 'Acupuncture and Traditional Medicine Centers', 'Wellness and Spa Services']
            DropDownMenu(textfield, focus, Hospital_and_HealthcareIndustriesList)

        elif (getCategoryForOption == "Company"):
            CompanyIndustriesList = ['Banking', 'Investment Management', 'Insurance', 'FinTech', 'Accounting Services', 'Pharmaceuticals','Biotechnology', 'Medical Devices', 'Health Insurance', 'Hospitals & Clinics', 'Telemedicine','Automotive', 'Aerospace', 'Electronics', 'Chemicals', 'Heavy Machinery', 'Oil & Gas', 'Renewable Energy','Utilities', 'Nuclear Energy', 'Film & Television Production', 'Music Industry', 'Gaming', 'Publishing','AdvertiSign & Marketing', 'Airlines', 'Railways', 'Shipping & Maritime', 'Logistics & Supply Chain', 'Software Development','Hardware Manufacturing', 'Information Technology Services', 'Cybersecurity', 'Artificial Intelligence', 'Cloud Computing','E-learning', 'Educational Technology', 'K-12 Education Services', 'Higher Education Institutions','Residential Real Estate', 'Commercial Real Estate', 'Property Management', 'Real Estate Investment Trusts', 'Farming', 'Agritech','Livestock', 'Fisheries', 'E-commerce', 'Apparel & Accessories', 'Food & Beverage', 'Home Goods', 'Beauty & Cosmetics','Hotels & Resorts', 'Travel Agencies', 'Event Management',]
            DropDownMenu(textfield, focus, CompanyIndustriesList)

        elif (getCategoryForOption == "Educational Institution"):
            EducationalInstitutionIndustriesList = ["Public Schools", "Private Schools", "Charter Schools", "Colleges", "Universities", "Community Colleges","Technical Institutes", "MOOCs (Massive Open Online Courses)", "Virtual Classrooms", "Language Learning Platforms","Learning Management Systems (LMS)", "Educational Software Development", "AI-driven Learning Tools", "Plumbing, Electrical, Carpentry","Corporate Training Programs", "Certification Courses", "Culinary Schools", "Fashion Design Schools", "Test Prep Centers","Subject-Specific Tutoring", "STEM Education Centers", "Arts & Music Programs", "Sports Coaching", "Scientific Research Facilities","Policy Think Tanks", "Educational Research Organizations", "Schools for the Visually Impaired","Hearing Impaired", "Autism and ADHD-focused Institutions", "Curriculum Development Firms","College Admission Consulting", "Academic Book Publishers", "Educational Content Creation","Standardized Testing Organizations", "Psychometric Testing Providers", "Public and Private Libraries","Adult Literacy Programs", "Skill-building Workshops"]        
            DropDownMenu(textfield, focus, EducationalInstitutionIndustriesList)

        elif (getCategoryForOption == "Restaurant and Food Service"):
            Restaurant_and_Food_ServiceIndustriesList = ["Fine Dining Restaurants","Casual Dining Restaurants","Quick Service Restaurants (QSR)","Fast Casual Restaurants","Family Style Restaurants","Buffets","Food Trucks","Ethnic","International Restaurants","Pop-Up Restaurants","Rooftop Restaurants","Drive-In Restaurants","Dine-In Theaters","Farm-to-Table Restaurants","Beachfront Restaurants","Vegan","Vegetarian Restaurants","Seafood Restaurants","Steakhouse Restaurants","Pizzerias","BBQ Joints","Dessert-Only Restaurants","Catering Services","Institutional Food Service","Vending Services","Corporate Cafeterias","Meal Delivery Services","Coffee Shops","Bars and Pubs","Specialty Food Providers","Airline Catering Services","Cruise Ship Food Services","Stadium","Arena Food Services","Hotel Restaurants and Room Service","Street Food Vendors","Concession Stands","Food Halls","Commissary Kitchens","Grocery Store Deli and Prepared Foods","Private Chefs and Personal Catering","School Cafeterias","Senior Living Facility Food Services",]
            DropDownMenu(textfield, focus, Restaurant_and_Food_ServiceIndustriesList)

        elif (getCategoryForOption == "Hotels and Accommodation"):
            Hotels_and_AccommodationIndustriesList = ["Luxury Hotels","Budget Hotels","Boutique Hotels","Resorts","Hostels","Motels","Bed & Breakfasts (B&B)","Vacation Rentals ","Serviced Apartments","Guesthouses","Business Hotels","Spa & Wellness Hotels","Eco-Friendly Hotels","All-Inclusive Resorts","Conference Hotels","Airport Hotels","Timeshare Resorts","Holiday Parks & Campgrounds","Farm Stays","Cabins & Cottages","Cruise Ships & Floating Hotels","Extended Stay Hotels","Cultural/Heritage Hotels","Mountain & Ski Resorts","Beach Resorts"]
            DropDownMenu(textfield, focus, Hotels_and_AccommodationIndustriesList)

        elif (getCategoryForOption == "Transportation"):
            TransportationIndustriesList = ["Trucking and Freight Hauling","Taxi and Ride-Hailing Services","Bus Services ","Courier and Delivery Services","Moving and Relocation Services","Freight Rail Services","Passenger Rail Services","High-Speed Rail Systems","Commercial Airlines","Cargo and Logistics Airlines","Charter Flights and Private Jets","Aviation Maintenance and Repair","Shipping and Freight Lines","Ferry Services","Cruise Line Services","Port and Harbor Operations","Metro/Subway Systems","Streetcars and Trams","Commuter Bus Services","Intercity Bus and Coach Services","Freight Forwarding","WarehouSign and Distribution","Last-Mile Delivery","Supply Chain Consulting","Medical Transport","Vehicle Transport Services","Hazardous Material Transportation","Oversized and Heavy Equipment Transport","Electric Vehicle (EV) Charging and Rentals","Autonomous Vehicle Development and Services","Drone Delivery Services","Hyperloop Development","Highway Construction and Maintenance","Airport Management","Rail Infrastructure Maintenance","Maritime Infrastructure Development"]
            DropDownMenu(textfield, focus, TransportationIndustriesList)
    
        elif (getCategoryForOption == "Entertainment"):
            EntertainmentIndustrisList = ["Motion picture production and distribution","TV broadcasting","Animation and visual effects","Film and TV streaming services","Music production and distribution","Concerts and live performances","Music streaming platforms","Record labels and artists' management","Game development and publishing","Game streaming and esports","Mobile gaming","Virtual reality (VR) and augmented reality (AR) gaming","Broadway and regional theater productions","Ballet and dance performances","Opera","Stand-up comedy","Book publishing","Magazines and newspapers","Digital content platforms","Comics and graphic novels","Professional sports leagues and teams","Sports broadcasting","Sports tourism and events management","Amateur and recreational sports","Fashion design and retail","Celebrity endorsements and modeling","Fashion events","Lifestyle media","Museums and galleries","Art auctions and exhibitions","Cultural heritage sites and tourism","Music festivals and art fairs","Content creators","Influencers and brand partnerships","Online video platforms and live streaming","Podcasts","Theme park design and operations","Amusement parks and water parks","Attractions, rides, and themed events","Interactive experiences"]
            DropDownMenu(textfield, focus, EntertainmentIndustrisList)

        elif (getCategoryForOption == "Non-Profit Organization"):
            NonProfit_OrganizationIndustriesList = ["Schools and Universities","Scholarships and Grants","Educational Resources and Support","Hospitals and Clinics","Disease Prevention and Awareness","Mental Health Services","Research and Medical Innovations","Homelessness and HouSign Assistance","Foster Care and Adoption","Child and Family Welfare","Youth Services","Disability Services","Wildlife Protection","Environmental Advocacy","Climate Change Action","Conservation Programs","Civil Rights Organizations","Refugee and Immigrant Support","Museums and Galleries","Performing Arts Groups","Cultural Preservation","Community Art Programs","Emergency Response","Humanitarian Aid and Development","Poverty Alleviation","Refugee Assistance","Religious Charities and Missions","Faith-Based Community Outreach","Interfaith Dialogue and Cooperation","Animal Shelters and Rescue Groups","Wildlife Protection","Veterinary Care and Animal Rights Advocacy","Economic Empowerment","Job Training and Placement","Affordable HouSign Projects","Volunteer and Community Engagement Programs","Think Tanks and Research Organizations","Government Transparency and Accountability","Legal Aid and Advocacy","Foundations that provide funding for other NPOs","Charity FundraiSign","Youth Sports Programs","Recreational Services","Community Health and Fitness Initiatives", "Veteran Services and Advocacy","Support for Military Families","Emergency Relief Organizations","Crisis Management and Recovery Services"];
            DropDownMenu(textfield, focus, NonProfit_OrganizationIndustriesList)
    def GoingToBusinesseAddressAndImageScreen(self, boxlayoutOfBID):
        SignupBusinessIndustryInput = self.ids.SignupBusinessIndustryInput.text.strip()
        SignupBusinessDescriptionInput = self.ids.SignupBusinessDescriptionInput.text.strip()
        self.isInputValid = True

        if self.SignupBusinessIndustryInputError == False:
            self.SignupBusinessIndustryInputError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        if (self.SignupBusinessDescriptionInputError == False):
            self.SignupBusinessDescriptionInputError = MDLabel(theme_text_color="Custom", text_color=(1, 0, 0, 1))

        def CheckBIFormOldServerErrors(IndustryInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessIndustryError' in oldServerError:
                    for erros in oldServerError['BusinessIndustryError']:
                        if erros['value'] == IndustryInputValue:
                            self.ShowSignupIndustryInputInputError(boxlayoutOfBID, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBDFormOldServerErrors(DescriptionInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessDescriptionError' in oldServerError:
                    for erros in oldServerError['BusinessDescriptionError']:
                        if erros['value'] == DescriptionInputValue:
                            self.ShowSignupDescriptionInputError(boxlayoutOfBID, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        if (len(SignupBusinessIndustryInput) == 0):
            self.ShowSignupIndustryInputInputError(boxlayoutOfBID, 'Business industry is required')
            self.isInputValid = False

        elif (len(SignupBusinessIndustryInput) == 1):
            self.ShowSignupIndustryInputInputError(boxlayoutOfBID, 'Business industry must be more the 1 letter')
            self.isInputValid = False

        elif not re.match(r"^[\p{L}0-9\s&'.\-–—,:/()`’‘“”]+$", SignupBusinessIndustryInput):
            self.ShowSignupIndustryInputInputError(boxlayoutOfBID, "Business industry contains invalid characters")
            self.isInputValid = False

        elif re.match(r"^[\d\s]+$", SignupBusinessIndustryInput):
            self.ShowSignupIndustryInputInputError(boxlayoutOfBID, "Business industry cannot be just numbers")
            self.isInputValid = False

        elif(CheckBIFormOldServerErrors(SignupBusinessIndustryInput)):
            self.isInputValid = False

        else:
            self.RemoveSignupIndustryInputError(boxlayoutOfBID)

        if (len(SignupBusinessDescriptionInput) == 0):
            self.ShowSignupDescriptionInputError(boxlayoutOfBID, 'Business description is required')
            self.isInputValid = False

        elif (len(SignupBusinessDescriptionInput.split(' ')) < 10):
            self.ShowSignupDescriptionInputError(boxlayoutOfBID, 'Business description must be more then 10 words')
            self.isInputValid = False
        
        elif not re.match(r"^[\p{L}0-9\s.,'\"’‘“”!?()&\-–—:;%$@/\\\[\]{}+=*#°…|`~^<>]*$", SignupBusinessDescriptionInput):
            self.ShowSignupDescriptionInputError(boxlayoutOfBID, "Description contains invalid characters")
            self.isInputValid = False

        elif re.match(r"^[\d\s]+$", SignupBusinessDescriptionInput):
            self.ShowSignupDescriptionInputError(boxlayoutOfBID, "Description cannot be just numbers")
            self.isInputValid = False


        elif(CheckBDFormOldServerErrors(SignupBusinessDescriptionInput)):
            self.isInputValid = False

        else:
            self.RemoveSignupDescriptionInputError(boxlayoutOfBID)

        if (self.isInputValid):
            self.parent.transition.direction = 'left'
            self.parent.current = 'BusinesseAddressAndImageScreen'
            global signupDateAndErrors

            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "Industry":SignupBusinessIndustryInput,
                "Description": SignupBusinessDescriptionInput
            })
            
            signupDateAndErrors.put('SignupUserBusinessForm',**oldSignupUserBusinessForm)

            print('Industry of business: ', SignupBusinessIndustryInput)
            print('Descrition of business: ', SignupBusinessDescriptionInput)


    def ShowSignupIndustryInputInputError(self, boxlayout, TextError):
        self.SignupBusinessIndustryInputError.text = TextError
        indexOfSBII = boxlayout.children.index(self.ids.SignupBusinessIndustryInput)
        if self.SignupBusinessIndustryInputError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessIndustryInputError, index= indexOfSBII)
    
    def ShowSignupDescriptionInputError(self, boxlayout, TextError):
        indexOfSBDI = boxlayout.children.index(self.ids.SignupBusinessDescriptionInput)
        self.SignupBusinessDescriptionInputError.text = TextError
        if self.SignupBusinessDescriptionInputError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessDescriptionInputError, index= indexOfSBDI)

        if TextError == 'Business description is required':
            self.SignupBusinessDescriptionInputError.size_hint_y = dp(0.1)
        else:
            print('change the height')
            self.SignupBusinessDescriptionInputError.size_hint_y = dp(1)
    
    def RemoveSignupIndustryInputError(self, boxlayout):
        if self.SignupBusinessIndustryInputError in boxlayout.children:
            boxlayout.remove_widget(self.SignupBusinessIndustryInputError)

    def RemoveSignupDescriptionInputError(self, boxlayout):
        if self.SignupBusinessDescriptionInputError in boxlayout.children:
            boxlayout.remove_widget(self.SignupBusinessDescriptionInputError)

    def TextingToSignupBusinessIndustryInput(self, text, boxlayout):
        if len(text.strip()) >= 2:
            self.RemoveSignupIndustryInputError(boxlayout)
    
    def TextingToSignupBusinessDescriptionInput(self, text, boxlayout):
        if len(text.strip().split(' ')) > 10:
            self.RemoveSignupDescriptionInputError(boxlayout)
    
        
    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        boxlayout = self.ids.signupBIDbox

        if inputName == 'Industry':
            self.ShowSignupIndustryInputInputError(boxlayout, inputError[0])
            
        elif inputName == 'Description':
            self.ShowSignupDescriptionInputError(boxlayout, inputError[0])

full_path_of_business_profile = None

class BusinesseAddressAndImage(Screen):
    SignupBusinessAddressInputError = False
    SignupBusinessProfilesError = False

    def ShowBottomSheet(self, text):
        box = self.ids.boxOfBottomSheet
        
        # Clear the existing widgets before adding new ones
        box.clear_widgets()

        search_path = '/home/adnan-khan/Pictures' # Consider making this path dynamic later
        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")

        for root, dirs, files in os.walk(search_path, topdown=True):
            for file in files:
                full_path = os.path.join(root, file)
                
                # Check if the file has a valid image extension (case-insensitive)
                if full_path.lower().endswith(image_extensions):
                    # --- START OF THE FIX ---
                    # This try-except block now correctly validates the image
                    try:
                        # 1. Attempt to pre-load the image data.
                        # If this fails, it will raise an exception, and we'll skip the file.
                        _ = CoreImage(full_path)

                        # 2. If the image is valid, create and add the button.
                        ImagesAsButton = Button(
                            background_normal=full_path,
                            background_down='',
                            size_hint_y=None,
                            height=dp(100) # Give buttons a consistent height
                        )
                        ImagesAsButton.bind(on_release=lambda btn, path=full_path: self.on_image_click(path, 'Yes'))
                        self.AddImagesAsButton(ImagesAsButton)

                    except Exception as e:
                        # 3. If the image is invalid/corrupt, catch the error.
                        # This prevents the app from crashing.
                        print(f"Skipping invalid image file: {full_path}. Reason: {e}")
                    # --- END OF THE FIX ---
                        # Create button
                        ImagesAsButton = Button(
                            background_normal='/home/adnan-khan/Desktop/MyMainProject/icon_folder/placeholder.png',
                            background_down='',
                            size_hint_y=None,
                            height=dp(100)
                        )

                        # Store real image path (even if invalid)
                        ImagesAsButton.file_path = full_path

                        # Bind using stored file_path, not button source
                        ImagesAsButton.bind(on_release=lambda btn: self.on_image_click(btn.file_path, 'No'))
                        self.AddImagesAsButton(ImagesAsButton)



    def AddImagesAsButton(self, buttons):
        box = self.ids.boxOfBottomSheet
        box.add_widget(buttons)  # Add the button to the layout
    # Event function for button click
    def on_image_click(self, image_path, isImageValid):
        if isImageValid == 'Yes':
            self.parent.transition.direction = 'left'
            self.parent.current = 'ShowFullImageForSingupBusinessProfilesScreen'
            x = self.manager.get_screen("ShowFullImageForSingupBusinessProfilesScreen")
            ImageOfSingupBusinessProfiles = x.ids.ImageOfSingupBusinessProfiles
            ImageOfSingupBusinessProfiles.source = image_path
        else:
            # def redirect_to_error_input(*args):
            #     self.SignupErrorDialog.dismiss()
            #     print("Navigate back to form or highlight first error field")
            #     self.parent.current = ISNkvFile
            #     self.parent.transition.direction = 'right'

            self.SignupErrorDialog = MDDialog(
                text="This image is invalid or corrupted. Please select another.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.SignupErrorDialog.dismiss()  # ← use the inner function
                    ),
                ],
            )
            self.SignupErrorDialog.open()
    
    def TextingToSignupBusinessAddressInput(self, text, boxlayout):
        if len(text.strip()) >= 2:
            self.RemovingErrorForSignupBusinessAddressInput(boxlayout)
    
    
    def GoingToBusinesseOpenTimeAndCloseTimeAndHolidayScreen(self, APboxlayout):
        SignupBusinessAddressInput = self.ids.SignupBusinessAddressInput.text.strip()
        singupBusinessProfileBotton = self.ids.singupBusinessProfileBotton
        self.IsInputValid = True

        if self.SignupBusinessAddressInputError == False:
            self.SignupBusinessAddressInputError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))
        if self.SignupBusinessProfilesError == False:
            self.SignupBusinessProfilesError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        def CheckBAFormOldServerErrors(AddressInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessAddressError' in oldServerError:
                    for erros in oldServerError['BusinessAddressError']:
                        if erros['value'] == AddressInputValue:
                            self.ShowingErrorForSignupBusinessAddressInput(APboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBPPFormOldServerErrors(PathOfBusinessProfiles):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessProfileError' in oldServerError:
                    for erros in oldServerError['BusinessProfileError']:
                        if erros['value'] == PathOfBusinessProfiles:
                            self.ShowingErrorForBusinessProfileInput(APboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False


        if len(SignupBusinessAddressInput) == 0:
            self.ShowingErrorForSignupBusinessAddressInput(APboxlayout, 'Business address is required')
            self.IsInputValid = False

        elif len(SignupBusinessAddressInput) == 1:
            self.ShowingErrorForSignupBusinessAddressInput(APboxlayout, 'Business address must be more than 1 letter')
            self.IsInputValid = False
    
        elif re.match(r"^[\d\s]+$", SignupBusinessAddressInput):
            self.ShowingErrorForSignupBusinessAddressInput(APboxlayout, 'Business address cannot be just numbers')
            self.IsInputValid = False


        elif not re.match(r"^[\p{L}0-9\s,.\-/#&():'\"’‘“”]+$", SignupBusinessAddressInput):
            self.ShowingErrorForSignupBusinessAddressInput(APboxlayout, "Business address contains invalid characters")
            self.IsInputValid = False

        
        elif(CheckBAFormOldServerErrors(SignupBusinessAddressInput)):
            self.IsInputValid = False
            
        else:
            self.RemovingErrorForSignupBusinessAddressInput(APboxlayout)

        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
        if not singupBusinessProfileBotton.text.endswith(image_extensions):
            self.IsInputValid = False
            self.ShowingErrorForBusinessProfileInput(APboxlayout, 'Please select business profiles')

        elif(CheckBPPFormOldServerErrors(singupBusinessProfileBotton.text)):
            self.IsInputValid = False
            
        else:
            self.RemovingErrorForSignupBusinessProfileInput(APboxlayout)

        if (self.IsInputValid):
            self.parent.transition.direction = 'left'
            self.parent.current = 'BusinesseOpenTimeAndCloseTimeAndHolidayScreen'
            ShowFullImageForSingupBusinessProfiles = self.manager.get_screen('ShowFullImageForSingupBusinessProfilesScreen')
            FullPathOfBusinessProfiles = ShowFullImageForSingupBusinessProfiles.ids.ImageOfSingupBusinessProfiles.source

            global signupDateAndErrors
            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "Address": SignupBusinessAddressInput, 
                "PathOfBusinessProfiles": FullPathOfBusinessProfiles})
            signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)
            print('Address of business: ', SignupBusinessAddressInput)
            print('profiles path of business: ', FullPathOfBusinessProfiles)

    def ShowingErrorForSignupBusinessAddressInput(self, boxlayout, ErrorText):
        indexOfBAI = boxlayout.children.index(self.ids.SignupBusinessAddressInput)
        self.SignupBusinessAddressInputError.text = ErrorText
        if self.SignupBusinessAddressInputError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessAddressInputError, index= indexOfBAI)

        if ErrorText == 'Business address is required':
            self.SignupBusinessAddressInputError.size_hint_y = dp(0.1)
        else:
            self.SignupBusinessAddressInputError.size_hint_y = dp(1)
        
    def ShowingErrorForBusinessProfileInput(self, boxlayout, ErrorText):
        if self.SignupBusinessProfilesError not in boxlayout.children:
            indexOfSBPI = boxlayout.children.index(self.ids.singupBusinessProfileBotton)
            self.SignupBusinessProfilesError.text = ErrorText
            boxlayout.add_widget(self.SignupBusinessProfilesError, index= indexOfSBPI)
        

    def RemovingErrorForSignupBusinessAddressInput(self, boxlayout):
        if self.SignupBusinessAddressInputError in boxlayout.children:
            boxlayout.remove_widget(self.SignupBusinessAddressInputError)
        
    def RemovingErrorForSignupBusinessProfileInput(self, boxlayout):
        if self.SignupBusinessProfilesError in boxlayout.children:
            boxlayout.remove_widget(self.SignupBusinessProfilesError)

    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        boxlayout = self.ids.boxOFBusinessAddressAndImage

        if inputName == 'Address':
            self.ShowingErrorForSignupBusinessAddressInput(boxlayout, inputError[0])
            
        elif inputName == 'PathOfBusinessProfiles':
            self.ShowingErrorForBusinessProfileInput(boxlayout, inputError[0])

class ShowFullImageForSingupBusinessProfiles(Screen):
    
    def imageIsNotGoodForBuinessProfiles(self,l):
        self.parent.transition.direction = 'right'
        self.parent.current = 'BusinesseAddressAndImageScreen'
        print("Not ")

    def imageIsGoodForBuinessProfiles(self, l):
        self.parent.transition.direction = 'right'
        self.parent.current = 'BusinesseAddressAndImageScreen'

        BusinesseAddressAndImage = self.manager.get_screen("BusinesseAddressAndImageScreen")
        bottm_sheet = BusinesseAddressAndImage.ids.bottom_sheet
        bottm_sheet.dismiss()

        nameOFBusinessProfile = self.ids.ImageOfSingupBusinessProfiles.source.split('/')
        BusinesseAddressAndImage.ids.singupBusinessProfileBotton.text = nameOFBusinessProfile[-1]

        # Now remove the error
        boxOFBusinessAddressAndImage = BusinesseAddressAndImage.ids.boxOFBusinessAddressAndImage
        for widget in boxOFBusinessAddressAndImage.children:
            if isinstance(widget, MDLabel):
                if widget.text == 'Please select business profiles':
                    boxOFBusinessAddressAndImage.remove_widget(widget)
                
class BusinesseOpenTimeAndCloseTimeAndHoliday(Screen):
    SingupBusinessOpenTimeError = False
    SingupBusinessCloseTimeError = False
    SingupBusinessHolidaysError = False

    SingupBusinessOpenTime = ''
    SingupBusinessCloseTime = ''
    SaveHolidays = []

    def PressingOnOpenTimeButton(self):
        SignupOpenTime = MDTimePicker(
            title='Select the time when you open your business')
        SignupOpenTime.bind(on_save=self.SignupOpenTimeSelected)
        SignupOpenTime.open()

    def SignupOpenTimeSelected(self, instance, time):
        print(
            f'You selected open time {instance.hour}:{instance.minute}: {instance.am_pm} of your business')
        self.ids.signupOpenTimeButton.icon = 'check'
        self.SingupBusinessOpenTime = f'{instance.hour}:{instance.minute}: {instance.am_pm}'
        message = f'You open your business at {instance.hour}:{instance.minute}: {instance.am_pm}'
        MDSnackbar(MDLabel(text=message,),).open()
        if self.ids.signupOpenTimeButton.icon == 'check':
            if self.SingupBusinessOpenTimeError in self.ids.boxOfBusinessOpenTimeCloseTimeAndHolidays.children[-1].children:
                self.ids.boxOfBusinessOpenTimeCloseTimeAndHolidays.children[-1].remove_widget(self.SingupBusinessOpenTimeError)

    def PressingOnCloseTimeButton(self):
        SignupCloseTime = MDTimePicker(
            title='Select the time when you close your business')
        SignupCloseTime.bind(on_save=self.SignupCloseTimeSelected)
        SignupCloseTime.open()

    def SignupCloseTimeSelected(self, instance, time):
        print(f'You selected close time {instance.hour}:{instance.minute}: {instance.am_pm} of your business')
        self.ids.signupCloseTimeButton.icon = 'check'
        message = f'You open your business at {instance.hour}:{instance.minute}: {instance.am_pm}'
        self.SingupBusinessCloseTime = f'{instance.hour}:{instance.minute}: {instance.am_pm}'
        MDSnackbar(MDLabel(text=message,),).open()

        if self.ids.signupCloseTimeButton.icon == 'check':
            if self.SingupBusinessCloseTimeError in self.ids.boxOfBusinessOpenTimeCloseTimeAndHolidays.children[0].children:
                self.ids.boxOfBusinessOpenTimeCloseTimeAndHolidays.children[0].remove_widget(self.SingupBusinessCloseTimeError)

    def PressingOnHolidayButton(self):
        SignupHolidayOptions = ["None", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.checkboxes = {}  # Store checkboxes for easy access

        self.box = MDGridLayout(cols=2, spacing="12dp", size_hint_y=None, height="180dp")

        for option in SignupHolidayOptions:
            checkbox = MDCheckbox()
            checkbox.active = option in self.SaveHolidays  # Restore saved selections
            checkbox.bind(active=lambda instance, value, opt=option: self.on_checkbox_active(instance, value, opt))   

            self.box.add_widget(MDLabel(text=option))
            self.box.add_widget(checkbox)
            self.checkboxes[option] = checkbox  # Store checkbox reference

        self.SignupHolidayDialog = MDDialog(
            title="Select Options:",
            type="custom",
            content_cls=self.box,
            buttons=[
                # MDFlatButton(text="CANCEL", on_release=lambda x: self.SignupHolidayDialog.dismiss()),
                MDFlatButton(text="OK", on_release=lambda x: self.SignupHolidayDialog.dismiss()),
            ],
        )
        self.SignupHolidayDialog.open()

    def on_checkbox_active(self, checkbox, value, option_name):
        if value:
            if option_name == "None":
                # If "None" is selected, unselect all others
                self.SaveHolidays = ["None"]
                for opt, cb in self.checkboxes.items():
                    if opt != "None":
                        cb.active = False  # Uncheck other checkboxes
            else:
                # If any other is selected, unselect "None"
                if "None" in self.SaveHolidays:
                    self.SaveHolidays.remove("None")
                    self.checkboxes["None"].active = False

                if option_name not in self.SaveHolidays:
                    self.SaveHolidays.append(option_name)
        else:
            # Remove unchecked option
            if option_name in self.SaveHolidays:
                self.SaveHolidays.remove(option_name)

        print("Selected Holidays:", self.SaveHolidays)

        if self.SaveHolidays:
            self.ids.SingupHolidayButton.icon = 'check'
            if self.SingupBusinessHolidaysError in self.ids.box.children:
                self.ids.box.remove_widget(self.SingupBusinessHolidaysError)
        else:
            self.ids.SingupHolidayButton.icon = 'chevron-down'
    
    def GoingToBusinesseOwnerFirstNameAndLastNameScreen(self):
        signupOpenTimeButton = self.ids.signupOpenTimeButton
        signupCloseTimeButton = self.ids.signupCloseTimeButton
        self.SingupHolidayButton = self.ids.SingupHolidayButton
        boxOfBusinessOpenTimeCloseTimeAndHolidays = self.ids.boxOfBusinessOpenTimeCloseTimeAndHolidays
        self.isInputValid = True

        if self.SingupBusinessOpenTimeError == False and self.SingupBusinessCloseTimeError == False and self.SingupBusinessHolidaysError == False:
            self.SingupBusinessOpenTimeError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1), padding=[0,10,0,0])
            self.SingupBusinessCloseTimeError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1), padding=[0,10,0,0])
            self.SingupBusinessHolidaysError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1), padding=[0,10,0,0])
        
        # boxOfBusinessOpenTimeCloseTimeAndHolidays.children[1].add_widget(MDLabel(text='Hello wrold',size_hint_y= 0.1))

        if signupOpenTimeButton.icon == 'clock':
            self.isInputValid = False
            self.ShowErrorForSignupOpenTime(boxOfBusinessOpenTimeCloseTimeAndHolidays, 'Open time is required')

        else:
            if self.SingupBusinessOpenTimeError in boxOfBusinessOpenTimeCloseTimeAndHolidays.children[-1].children:
                boxOfBusinessOpenTimeCloseTimeAndHolidays.children[-1].remove_widget(self.SingupBusinessOpenTimeError)

        if signupCloseTimeButton.icon == 'clock':
            self.isInputValid = False
            self.ShowErrorForSignupCloseTime(boxOfBusinessOpenTimeCloseTimeAndHolidays ,'Close time is required')

        else:
            if self.SingupBusinessCloseTimeError in boxOfBusinessOpenTimeCloseTimeAndHolidays.children[0].children:
                boxOfBusinessOpenTimeCloseTimeAndHolidays.children[0].remove_widget(self.SingupBusinessCloseTimeError)

        if self.SingupHolidayButton.icon == 'chevron-down':
            self.isInputValid = False
            self.ShowErrorForSignupHolidays(boxOfBusinessOpenTimeCloseTimeAndHolidays ,'Please select the holiday or none')

        else:
            if self.SingupBusinessHolidaysError in self.ids.box.children:
                self.ids.box.remove_widget(self.SingupBusinessHolidaysError)
                

        if (self.isInputValid):
            self.parent.current = 'BusinesseOwnerFirstNameAndLastNameScreen'
            self.parent.transition.direction = 'left'
            global signupDateAndErrors
            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "OpenTime":self.SingupBusinessCloseTime, 
                "CloseTime":self.SingupBusinessOpenTime, 
                "Holidays":self.SaveHolidays
            })
            signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)

            print('Open time of business', self.SingupBusinessOpenTime)
            print('Close time of business', self.SingupBusinessCloseTime)
            print('Hoildays of business', self.SaveHolidays)
    def ShowErrorForSignupOpenTime(self, boxOfBusinessOpenTimeCloseTimeAndHolidays, TextError):
        if self.SingupBusinessOpenTimeError not in boxOfBusinessOpenTimeCloseTimeAndHolidays.children[-1].children:
            self.SingupBusinessOpenTimeError.text = TextError
            boxOfBusinessOpenTimeCloseTimeAndHolidays.children[-1].add_widget(self.SingupBusinessOpenTimeError)
 
    def ShowErrorForSignupCloseTime(self, boxOfBusinessOpenTimeCloseTimeAndHolidays, TextError):
        if self.SingupBusinessCloseTimeError not in boxOfBusinessOpenTimeCloseTimeAndHolidays.children[0].children:
            self.SingupBusinessCloseTimeError.text = TextError
            boxOfBusinessOpenTimeCloseTimeAndHolidays.children[0].add_widget(self.SingupBusinessCloseTimeError)

    def ShowErrorForSignupHolidays(self, boxOfBusinessOpenTimeCloseTimeAndHolidays, TextError):
        self.SingupBusinessHolidaysError.text = TextError
        self.SingupBusinessHolidaysError.padding = [10, 0, 0, 0]
        if self.SingupBusinessHolidaysError not in self.ids.box.children:
            self.ids.box.add_widget(self.SingupBusinessHolidaysError, index=self.ids.box.children.index(self.SingupHolidayButton))


    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        boxOfBusinessOpenTimeCloseTimeAndHolidays = self.ids.boxOfBusinessOpenTimeCloseTimeAndHolidays

        if inputName == 'OpenTime':
            self.ShowErrorForSignupOpenTime(boxOfBusinessOpenTimeCloseTimeAndHolidays, inputError[0])
            
        elif inputName == 'CloseTime':
            self.ShowErrorForSignupCloseTime(boxOfBusinessOpenTimeCloseTimeAndHolidays, inputError[0])

        elif inputName == 'Holidays':
            self.ShowErrorForSignupHolidays(boxOfBusinessOpenTimeCloseTimeAndHolidays, inputError[0])

class BusinesseOwnerFirstNameAndLastName(Screen):
    SignupBusinessOwnerFirstNameError = False
    SignupBusinessOwnerLastNameError = False
    def GoingToBusinessePhoneNumberAndEmailAddressScreen(self, BOFLboxlayout):
        self.isInputValid = True
        self.SignupBusinessOwnerFirstName = self.ids.SignupBusinessOwnerFirstName
        self.SignupBusinessOwnerLastName = self.ids.SignupBusinessOwnerLastName

        if self.SignupBusinessOwnerFirstNameError == False:
            self.SignupBusinessOwnerFirstNameError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        if self.SignupBusinessOwnerLastNameError == False:
            self.SignupBusinessOwnerLastNameError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))
        
        def CheckBOFFormOldServerErrors(FirstNameInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessOwnerFirstNameError' in oldServerError:
                    for erros in oldServerError['BusinessOwnerFirstNameError']:
                        if erros['value'] == FirstNameInputValue:
                            self.ShowingErrorForSignupBusinessOwnerFirstNameInput(BOFLboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBOLFormOldServerErrors(LastNameInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessOwnerLastNameError' in oldServerError:
                    for erros in oldServerError['BusinessOwnerLastNameError']:
                        if erros['value'] == LastNameInputValue:
                            self.ShowingErrorForSignupBusinessOwnerLastNameInput(BOFLboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False


        if len(self.SignupBusinessOwnerFirstName.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessOwnerFirstNameInput(BOFLboxlayout, 'First is required')

        elif len(self.SignupBusinessOwnerFirstName.text.strip()) == 1:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessOwnerFirstNameInput(BOFLboxlayout, 'First is must be more then 1 letter')

        elif re.match(r"^\d+$", self.SignupBusinessOwnerFirstName.text.strip()):
            self.ShowingErrorForSignupBusinessOwnerFirstNameInput(BOFLboxlayout, "First name cannot be just numbers")
            self.isInputValid = False

        elif not re.match(r"^[\p{L}\s'.\-\"’‘“”]+$", self.SignupBusinessOwnerFirstName.text.strip()):
            self.ShowingErrorForSignupBusinessOwnerFirstNameInput(BOFLboxlayout, "First name contains invalid characters")
            self.isInputValid = False

        elif(CheckBOFFormOldServerErrors(self.SignupBusinessOwnerFirstName.text)):
            self.isInputValid = False

        else:
            if self.SignupBusinessOwnerFirstNameError in BOFLboxlayout.children:
                BOFLboxlayout.remove_widget(self.SignupBusinessOwnerFirstNameError)

        if len(self.SignupBusinessOwnerLastName.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessOwnerLastNameInput(BOFLboxlayout, 'Last is required')

        elif len(self.SignupBusinessOwnerLastName.text.strip()) == 1:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessOwnerLastNameInput(BOFLboxlayout, 'Last is must be more then 1 letter')

        elif re.match(r"^\d+$", self.SignupBusinessOwnerLastName.text.strip()):
            self.ShowingErrorForSignupBusinessOwnerLastNameInput(BOFLboxlayout, "Last name cannot be just numbers")
            self.isInputValid = False

        elif not re.match(r"^[\p{L}\s'.\-\"’‘“”]+$", self.SignupBusinessOwnerLastName.text.strip()):
            self.ShowingErrorForSignupBusinessOwnerLastNameInput(BOFLboxlayout, "Last name contains invalid characters")
            self.isInputValid = False

        elif(CheckBOLFormOldServerErrors(self.SignupBusinessOwnerLastName.text)):
            self.isInputValid = False
            
        else:
            if self.SignupBusinessOwnerLastNameError in BOFLboxlayout.children:
                BOFLboxlayout.remove_widget(self.SignupBusinessOwnerLastNameError)

        if (self.isInputValid):
            self.parent.current = 'BusinessPhoneNumberAndEmailAddressScreen'
            self.parent.transition.direction = 'left'
            global signupDateAndErrors
            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "ownerFirstName": self.SignupBusinessOwnerFirstName.text,
                "ownerLastName": self.SignupBusinessOwnerLastName.text
            })
            signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)
        
            print('First name of business owner: ', self.SignupBusinessOwnerFirstName.text)
            print('Last name of business owner: ', self.SignupBusinessOwnerLastName.text)


    def TextingToSignupBusinessOwnerFirstNameInput(self, text, boxlayout):
        if len(text.strip()) >= 2 :
           if self.SignupBusinessOwnerFirstNameError in boxlayout.children:
                boxlayout.remove_widget(self.SignupBusinessOwnerFirstNameError)

    def TextingToSignupBusinessOwnerLastNameInput(self, text, boxlayout):
        if len(text.strip()) >= 2 :
            if self.SignupBusinessOwnerLastNameError in boxlayout.children:
                boxlayout.remove_widget(self.SignupBusinessOwnerLastNameError)

    def ShowingErrorForSignupBusinessOwnerFirstNameInput(self, boxlayout, ErrorText):
        self.SignupBusinessOwnerFirstNameError.text = ErrorText
        if self.SignupBusinessOwnerFirstNameError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessOwnerFirstNameError, index=boxlayout.children.index(self.SignupBusinessOwnerFirstName))

    def ShowingErrorForSignupBusinessOwnerLastNameInput(self, boxlayout, ErrorText):
        self.SignupBusinessOwnerLastNameError.text = ErrorText
        if self.SignupBusinessOwnerLastNameError not in boxlayout.children:
            boxlayout.add_widget(self.SignupBusinessOwnerLastNameError, index=boxlayout.children.index(self.SignupBusinessOwnerLastName))

    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        box = self.ids.boxSignupBusinessOwnerName

        if inputName == 'ownerFirstName':
            self.ShowingErrorForSignupBusinessOwnerFirstNameInput(box, inputError[0])
            
        elif inputName == 'ownerLastName':
            self.ShowingErrorForSignupBusinessOwnerLastNameInput(box, inputError[0])

class BusinessPhoneNumberAndEmailAddress(Screen):
    # Enter a valid email address
    SignupBusinessOwnerPhoneNumberPattern = r'^[0-9]{10,15}$'
    SignupBusinessOwnerEmailPattern = r"^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"

    SingupPhoneNumberError = False
    SingupEmailAddressError = False

    def GoingToBusinessSignupOTPVerificationScreen(self, BPHEMBoxlayout):
        self.SignupBusinessPhoneNumber = self.ids.SignupBusinessPhoneNumber
        self.SignupBusinessEmailAddress = self.ids.SignupBusinessEmailAddress
        self.isInputValid = True

        if self.SingupPhoneNumberError == False:
            self.SingupPhoneNumberError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        if self.SingupEmailAddressError == False:
            self.isInputValid = False
            self.SingupEmailAddressError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        def CheckBOPHFormOldServerErrors(PhoneNumberInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessPhoneNumberError' in oldServerError:
                    for erros in oldServerError['BusinessPhoneNumberError']:
                        if erros['value'] == PhoneNumberInputValue:
                            self.ShowingErrorForSignupBusinessPhoneNumberInput(BPHEMBoxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBOEAFormOldServerErrors(EmailAddressInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessEmailAddressError' in oldServerError:
                    for erros in oldServerError['BusinessEmailAddressError']:
                        if erros['value'] == EmailAddressInputValue:
                            self.ShowingErrorForSignupBusinessEmailAddressInput(BPHEMBoxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False


        if len(self.SignupBusinessPhoneNumber.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessPhoneNumberInput(BPHEMBoxlayout, 'Phone number is required')

        elif not re.match(self.SignupBusinessOwnerPhoneNumberPattern, self.SignupBusinessPhoneNumber.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessPhoneNumberInput(BPHEMBoxlayout, 'Enter a valid phone number (10-15 digits)')
        
        elif(CheckBOPHFormOldServerErrors(self.SignupBusinessPhoneNumber.text.strip())):
            self.isInputValid = False

        else:
            if self.SingupPhoneNumberError in BPHEMBoxlayout.children:
                BPHEMBoxlayout.remove_widget(self.SingupPhoneNumberError)

        if len(self.SignupBusinessEmailAddress.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessEmailAddressInput(BPHEMBoxlayout, 'Email Address is required')

        elif not re.match(self.SignupBusinessOwnerEmailPattern, self.SignupBusinessEmailAddress.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessEmailAddressInput(BPHEMBoxlayout, 'Enter a valid Email address')

        elif (CheckBOEAFormOldServerErrors(self.SignupBusinessEmailAddress.text.strip())):
            self.isInputValid = False

        else:
            if self.SingupEmailAddressError in BPHEMBoxlayout.children:
                BPHEMBoxlayout.remove_widget(self.SingupEmailAddressError)

        if (self.isInputValid):
            self.parent.current = 'BusinessSignupOTPVerificationScreen'
            self.parent.transition.direction = 'left'
            global signupDateAndErrors
            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "PhoneNumber": self.SignupBusinessPhoneNumber.text.strip(),
                "EmailAddress": self.SignupBusinessEmailAddress.text.strip()
            })
            signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)

            print('phone number of business: ', self.SignupBusinessPhoneNumber.text.strip())
            print('email address of business: ', self.SignupBusinessEmailAddress.text.strip())

    def ShowingErrorForSignupBusinessPhoneNumberInput(self, boxlayout, TextError):
        self.SingupPhoneNumberError.text = TextError
        if self.SingupPhoneNumberError not in boxlayout.children:
            boxlayout.add_widget(self.SingupPhoneNumberError, index=boxlayout.children.index(self.ids.SignupBusinessPhoneNumber))

    def ShowingErrorForSignupBusinessEmailAddressInput(self, boxlayout, TextError):
        self.SingupEmailAddressError.text = TextError
        if self.SingupEmailAddressError not in boxlayout.children:
            boxlayout.add_widget(self.SingupEmailAddressError, index=boxlayout.children.index(self.ids.SignupBusinessEmailAddress))

        print(self.SignupBusinessEmailAddress.text)

    def TextingToSignupBusinessPhoneNumberInput(self, text, boxlayout):
        if re.match(self.SignupBusinessOwnerPhoneNumberPattern, text.strip()):
            if self.SingupPhoneNumberError in boxlayout.children:
                boxlayout.remove_widget(self.SingupPhoneNumberError)


    def TextingToSignupBusinessEmailAddressInput(self, text, boxlayout):
        if re.match(self.SignupBusinessOwnerEmailPattern, text.strip()):
            if self.SingupEmailAddressError in boxlayout.children:
                boxlayout.remove_widget(self.SingupEmailAddressError)
            
    
    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        box = self.ids.boxSignupBusinessPAandEA

        if inputName == 'PhoneNumber':
            self.ShowingErrorForSignupBusinessPhoneNumberInput(box, inputError[0])
            
        elif inputName == 'EmailAddress':
            self.ShowingErrorForSignupBusinessEmailAddressInput(box, inputError[0])

class BusinessSignupOTPVerification(Screen):
    SignupEmailVerificationCodeError = False
    SignupPhoneNumberVerificationCodeError = False

    Signup_verification_codePattern = r"^\d{6}$"

    def GoingToSingupBusinesseUserPasswordScreen(self, Oboxlayout):
        self.SignupBusinessEmailVerificationCode = self.ids.SignupBusinessEmailVerificationCode
        self.SignupBusinessPhoneNumberVerificationCode = self.ids.SignupBusinessPhoneNumberVerificationCode
        self.isInputValid = True

        if self.SignupEmailVerificationCodeError == False:
            self.SignupEmailVerificationCodeError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        if self.SignupPhoneNumberVerificationCodeError == False:
            self.SignupPhoneNumberVerificationCodeError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))
        
        def CheckBPNOTPFormOldServerErrors(PhoneNumberOTPInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessPhoneNumberOTPError' in oldServerError:
                    for erros in oldServerError['BusinessPhoneNumberOTPError']:
                        if erros['value'] == PhoneNumberOTPInputValue:
                            self.ShowingErrorForSignupBusinessPhoneNumberVerificationCode(Oboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBEAOTPFormOldServerErrors(EmailAddressOTPInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessEmailAddressOTPError' in oldServerError:
                    for erros in oldServerError['BusinessEmailAddressOTPError']:
                        if erros['value'] == EmailAddressOTPInputValue:
                            self.ShowingErrorForSignupBusinessEmailVerificationCode(Oboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False


        if len(self.SignupBusinessEmailVerificationCode.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessEmailVerificationCode(Oboxlayout, 'Email address OTP is required')

        elif not re.match(self.Signup_verification_codePattern, self.SignupBusinessEmailVerificationCode.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessEmailVerificationCode(Oboxlayout, 'Enter valid OTP (6 digits)')
        
        elif(CheckBEAOTPFormOldServerErrors(self.SignupBusinessEmailVerificationCode.text)):
            self.isInputValid = False

        else:
            if self.SignupEmailVerificationCodeError in Oboxlayout.children:
                Oboxlayout.remove_widget(self.SignupEmailVerificationCodeError)

        if len(self.SignupBusinessPhoneNumberVerificationCode.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessPhoneNumberVerificationCode(Oboxlayout, 'Phone number OTP is required')

        elif not re.match(self.Signup_verification_codePattern, self.SignupBusinessPhoneNumberVerificationCode.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForSignupBusinessPhoneNumberVerificationCode(Oboxlayout, 'Enter valid OTP (6 digits)')
            
        elif (CheckBPNOTPFormOldServerErrors(self.SignupBusinessPhoneNumberVerificationCode.text)):
            self.isInputValid = False

        else:
            if self.SignupPhoneNumberVerificationCodeError in Oboxlayout.children:
                Oboxlayout.remove_widget(self.SignupPhoneNumberVerificationCodeError)
        
        if (self.isInputValid):
            self.parent.current = 'BusinesseUserPasswordScreen'
            self.parent.transition.direction = 'left'
            
            global signupDateAndErrors
            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "EmailAddressOTP": self.SignupBusinessEmailVerificationCode.text,
                "PhoneNumberOTP": self.SignupBusinessPhoneNumberVerificationCode.text
            })
            signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)
         

            print('OTP of business email: ', self.SignupBusinessEmailVerificationCode.text)
            print('OTP of business phone number: ', self.SignupBusinessPhoneNumberVerificationCode.text)
            

    def ShowingErrorForSignupBusinessEmailVerificationCode(self, boxlayout, ErrorText):
        self.SignupEmailVerificationCodeError.text = ErrorText
        if self.SignupEmailVerificationCodeError not in boxlayout.children:
            boxlayout.add_widget(self.SignupEmailVerificationCodeError, index=boxlayout.children.index(self.SignupBusinessEmailVerificationCode))
    
    def ShowingErrorForSignupBusinessPhoneNumberVerificationCode(self, boxlayout, ErrorText):
        self.SignupPhoneNumberVerificationCodeError.text = ErrorText
        if self.SignupPhoneNumberVerificationCodeError not in boxlayout.children:
            boxlayout.add_widget(self.SignupPhoneNumberVerificationCodeError, index=boxlayout.children.index(self.SignupBusinessPhoneNumberVerificationCode))

    def TextingToSignupBusinessEmailVerificationCodeInput(self, text, boxlayout):
        if re.match(self.Signup_verification_codePattern, text.strip()):
            if self.SignupEmailVerificationCodeError in boxlayout.children:
                boxlayout.remove_widget(self.SignupEmailVerificationCodeError)

    def TextingToSignupBusinessPhoneNumberVerificationCodeInput(self, text, boxlayout):
        if re.match(self.Signup_verification_codePattern, text.strip()):
            if self.SignupPhoneNumberVerificationCodeError in boxlayout.children:
                boxlayout.remove_widget(self.SignupPhoneNumberVerificationCodeError)
            
    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        box = self.ids.boxPHAndEAOTP

        if inputName == 'PhoneNumberOTP':
            self.ShowingErrorForSignupBusinessPhoneNumberVerificationCode(box, inputError[0])
            
        elif inputName == 'EmailAddressOTP':
            self.ShowingErrorForSignupBusinessEmailVerificationCode(box, inputError[0])

class BusinesseUserPasswordScreen(Screen):
    SignupUserPasswordError = False
    SignupUserConfirmPasswordError = False
    IsNextBottonClicked = False
    def GoingToSingupBusinesseUsernameScreen(self, Pboxlayout):
        self.IsNextBottonClicked = True
        self.SignupBusinessUserPassword = self.ids.SignupBusinessUserPassword
        self.SignupBusinessUserConfirmPassword = self.ids.SignupBusinessUserConfirmPassword
        self.isInputValid = True

        if self.SignupUserPasswordError == False:
            self.SignupUserPasswordError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        if self.SignupUserConfirmPasswordError == False:
            self.SignupUserConfirmPasswordError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        def CheckBPFormOldServerErrors(PasswordInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessPassWordError' in oldServerError:
                    for erros in oldServerError['BusinessPassWordError']:
                        if erros['value'] == PasswordInputValue:
                            self.ShowingErrorForUserPasswordInput(Pboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False

        def CheckBCPFormOldServerErrors(CPasswordInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessConfirmPasswordError' in oldServerError:
                    for erros in oldServerError['BusinessConfirmPasswordError']:
                        if erros['value'] == CPasswordInputValue:
                            self.ShowingErrorForUserConfirmPasswordInput(Pboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False


        if len(self.SignupBusinessUserPassword.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForUserPasswordInput(Pboxlayout, "Password is required.")

        elif len(self.SignupBusinessUserPassword.text.strip()) < 6:
            self.isInputValid = False

            self.ShowingErrorForUserPasswordInput(Pboxlayout, "Password must be at least 6 characters long.")

        elif not re.search(r"[A-Z]", self.SignupBusinessUserPassword.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForUserPasswordInput(Pboxlayout, "Password must contain at least one uppercase letter.")

        elif not re.search(r"[a-z]", self.SignupBusinessUserPassword.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForUserPasswordInput(Pboxlayout, "Password must contain at least one lowercase letter.")

        elif not re.search(r"\d", self.SignupBusinessUserPassword.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForUserPasswordInput(Pboxlayout, "Password must contain at least one digit.")

        elif not re.search(r"[!@#$%^&*()_+\-=]", self.SignupBusinessUserPassword.text.strip()):
            self.isInputValid = False
            self.ShowingErrorForUserPasswordInput(Pboxlayout, "Password must contain at least one special character. (!@#$%^&*()_+-=).")
        elif (CheckBPFormOldServerErrors(self.SignupBusinessUserPassword.text.strip())):
            self.isInputValid = False

        else:
            if self.SignupUserPasswordError in Pboxlayout.children:
                Pboxlayout.remove_widget(self.SignupUserPasswordError)
        
        if len(self.SignupBusinessUserConfirmPassword.text.strip()) == 0:
            self.isInputValid = False
            self.ShowingErrorForUserConfirmPasswordInput(Pboxlayout, 'Confirm password is required')

        elif len(self.SignupBusinessUserConfirmPassword.text.strip()) < 6:
            self.isInputValid = False
            self.ShowingErrorForUserConfirmPasswordInput(Pboxlayout, "Confirm password must be at least 6 characters long.")

        elif self.SignupBusinessUserConfirmPassword.text.strip() != self.SignupBusinessUserPassword.text.strip():
            self.isInputValid = False
            self.ShowingErrorForUserConfirmPasswordInput(Pboxlayout, "Password does not match.")
        elif (CheckBCPFormOldServerErrors(self.SignupBusinessUserConfirmPassword.text.strip())):
            self.isInputValid = False
        
        else:
            if self.SignupUserConfirmPasswordError in Pboxlayout.children:
                Pboxlayout.remove_widget(self.SignupUserConfirmPasswordError)
        
        # Now go
        if (self.isInputValid):
            self.parent.current = 'BusinesUsernameScreen'
            self.parent.transition.direction = 'left'
                        
            global signupDateAndErrors
            oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
            oldSignupUserBusinessForm.update({
                "Password": self.SignupBusinessUserPassword.text.strip() ,
                "ConfirmPassword": self.SignupBusinessUserConfirmPassword.text.strip()
            })
            signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)
         
            print('Password of user: ', self.SignupBusinessUserPassword.text.strip())
            print('Confirm password of user: ', self.SignupBusinessUserConfirmPassword.text.strip())

    def ShowingErrorForUserPasswordInput(self, boxlayout, ErrorText):
        self.SignupUserPasswordError.text = ErrorText
        if ErrorText == "Password must contain at least one digit." or ErrorText == "Password is required.":
            self.SignupUserPasswordError.size_hint_y = 0.1
        else:
            self.SignupUserPasswordError.size_hint_y = 1
        if self.SignupUserPasswordError not in boxlayout.children:
            boxlayout.add_widget(self.SignupUserPasswordError, index=boxlayout.children.index(self.SignupBusinessUserPassword))

    def ShowingErrorForUserConfirmPasswordInput(self, boxlayout, ErrorText):
        self.SignupUserConfirmPasswordError.text = ErrorText
        if ErrorText == "Confirm password must be at least 6 characters long.":
            self.SignupUserConfirmPasswordError.size_hint_y = 1
        else:
            self.SignupUserConfirmPasswordError.size_hint_y = 0.1

    
        if self.SignupUserConfirmPasswordError not in boxlayout.children:
            boxlayout.add_widget(self.SignupUserConfirmPasswordError, index=boxlayout.children.index(self.SignupBusinessUserConfirmPassword))
    
    def TextingToSignupSignupBusinessUserPasswordInput(self, password, boxlayout):
        if self.IsNextBottonClicked:
            if len(password.strip()) == 0:
                self.ShowingErrorForUserPasswordInput(boxlayout, "Password is required.")

            elif len(password.strip()) < 6:
                self.ShowingErrorForUserPasswordInput(boxlayout, "Password must be at least 6 characters long.")

            elif not re.search(r"[A-Z]", password.strip()):
                self.ShowingErrorForUserPasswordInput(boxlayout, "Password must contain at least one uppercase letter.")

            elif not re.search(r"[a-z]", password.strip()):
                self.ShowingErrorForUserPasswordInput(boxlayout, "Password must contain at least one lowercase letter.")

            elif not re.search(r"\d", password.strip()):
                self.ShowingErrorForUserPasswordInput(boxlayout, "Password must contain at least one digit.")

            elif not re.search(r"[!@#$%^&*()_+\-=]", password.strip()):
                self.ShowingErrorForUserPasswordInput(boxlayout, "Password must contain at least one special character. (!@#$%^&*()_+-=).")

            else:
                if self.SignupUserPasswordError in boxlayout.children:
                    boxlayout.remove_widget(self.SignupUserPasswordError)
        
    def TextingToSignupSignupBusinessUserConfirmPasswordInput(self, ConfirmPassword, boxlayout):
        if self.IsNextBottonClicked:
            if len(self.SignupBusinessUserConfirmPassword.text.strip()) == 0:
                self.ShowingErrorForUserConfirmPasswordInput(boxlayout, 'Confirm password is required')

            elif len(self.SignupBusinessUserConfirmPassword.text.strip()) < 6:
                self.ShowingErrorForUserConfirmPasswordInput(boxlayout, "Confirm password must be at least 6 characters long.")

            elif self.SignupBusinessUserConfirmPassword.text.strip() != self.SignupBusinessUserPassword.text.strip():
                self.ShowingErrorForUserConfirmPasswordInput(boxlayout, "Password does not match.")
            
            else:
                if self.SignupUserConfirmPasswordError in boxlayout.children:
                    boxlayout.remove_widget(self.SignupUserConfirmPasswordError)

    def showErrorHereIfTheErrorComeingForServer(self, inputName, inputError):
        box = self.ids.boxSignupPassword
        print(inputName)
        if inputName == 'Password':
            self.ShowingErrorForUserPasswordInput(box, inputError[0])
            print(inputError[0])

        elif inputName == 'ConfirmPassword':
            self.ShowingErrorForUserConfirmPasswordInput(box, inputError[0])
            print(inputError[0])


class BusinesUsernameScreen(Screen):
    SignupBusinessUserUsernameError = False
    def UserPressOnSigupCreateAccount(self, UNboxlayout):
        self.SignupBusinessUserUsername = self.ids.SignupBusinessUserUsername
        if self.SignupBusinessUserUsernameError == False:
            self.SignupBusinessUserUsernameError = MDLabel(size_hint_y=0.1, theme_text_color="Custom", text_color=(1, 0, 0, 1))

        def CheckBUFormOldServerErrors(UsernameInputValue):
            if (signupDateAndErrors.exists("TheErrorsOfServerForSignup")):
                oldServerError = signupDateAndErrors.get('TheErrorsOfServerForSignup')
                if 'BusinessUsernameError' in oldServerError:
                    for erros in oldServerError['BusinessUsernameError']:
                        if erros['value'] == UsernameInputValue:
                            self.ShowErrorForSigupBusinessUsernameInput(UNboxlayout, erros['Error'][0])
                            return True
                    else: False    
                else: return False
            else: return False


        if not self.SignupBusinessUserUsername.text.strip():
            self.ShowErrorForSigupBusinessUsernameInput(UNboxlayout, "Username is required.")

        elif len(self.SignupBusinessUserUsername.text.strip()) < 3 or len(self.SignupBusinessUserUsername.text.strip()) > 15:
            self.ShowErrorForSigupBusinessUsernameInput(UNboxlayout, "Username must be 3-15 characters long.")

        elif " " in self.SignupBusinessUserUsername.text.strip():  # Prevents spaces inside the username
            self.ShowErrorForSigupBusinessUsernameInput(UNboxlayout,"Username cannot contain spaces. Use underscores instead.")

        elif not re.match(r"^[a-zA-Z0-9_]+$", self.SignupBusinessUserUsername.text.strip()):
            self.ShowErrorForSigupBusinessUsernameInput(UNboxlayout, "Only letters, numbers, and underscores are allowed.")

        elif (CheckBUFormOldServerErrors(self.SignupBusinessUserUsername.text)):
            pass

        else:
            print('Good')
            global signupDateAndErrors
            self.NowSendFullFormToServer(UNboxlayout)

    def ShowErrorForSigupBusinessUsernameInput(self, boxLayout, ErrorText):
        self.SignupBusinessUserUsernameError.text = ErrorText

        if ErrorText == "Username cannot contain spaces. Use underscores instead." or ErrorText == "Only letters, numbers, and underscores are allowed.":
            self.SignupBusinessUserUsernameError.size_hint_y = 0.4
        else:
            self.SignupBusinessUserUsernameError.size_hint_y = 0.1

        if self.SignupBusinessUserUsernameError not in boxLayout.children:
            boxLayout.add_widget(self.SignupBusinessUserUsernameError, index= boxLayout.children.index(self.SignupBusinessUserUsername))

    def NowSendFullFormToServer(self, boxLayout):
        if self.SignupBusinessUserUsernameError in boxLayout.children:
            boxLayout.remove_widget(self.SignupBusinessUserUsernameError)

        global signupDateAndErrors
        oldSignupUserBusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')
        oldSignupUserBusinessForm.update({
            "Username": self.SignupBusinessUserUsername.text
        })
        signupDateAndErrors.put('SignupUserBusinessForm', **oldSignupUserBusinessForm)
                 
        
        file_path = signupDateAndErrors.get('SignupUserBusinessForm')['PathOfBusinessProfiles']
        # file_path = '/home/adnan-khan/Desktop/MyMainProject/p.png'
        allowed_mimes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg',]

        try:
            mime_type, _ = mimetypes.guess_type(file_path)

            if not mime_type or mime_type not in allowed_mimes:
                raise Exception("Only JPEG, PNG, JPG, or WEBP images are allowed")

            with open(file_path, 'rb') as Profile:
                print(Profile)
                BusinessForm = signupDateAndErrors.get('SignupUserBusinessForm')

                data =  {
                    'SignupBusinessNameInput': BusinessForm['name'],
                    'SignupBusinessCategoryInput': BusinessForm['Category'],
                    'SignupBusinessIndustryInput':BusinessForm['Industry'],
                    'SignupBusinessDescriptionInput': BusinessForm['Description'],
                    'SignupBusinessAddressInput': BusinessForm['Address'],
                    'SignupBusinessOpenTimeInput': BusinessForm['OpenTime'],
                    'SignupBusinessCloseTimeInput': BusinessForm['CloseTime'],
                    'SignupBusinessHolidaysInput': BusinessForm['Holidays'],
                    'SignupBusinessOwnerFirstNameInput': BusinessForm['ownerFirstName'],
                    'SignupBusinessOwnerLastNameInput': BusinessForm['ownerLastName'],
                    'SignupBusinessPhoneNumberInput': BusinessForm['PhoneNumber'],
                    'SignupBusinessEmailAddressInput': BusinessForm['EmailAddress'],
                    'SignupBusinessPhoneNumberOTPInput': BusinessForm['PhoneNumberOTP'],
                    'SignupBusinessEmailAddressOTPInput': BusinessForm['EmailAddressOTP'],
                    'SignupBusinessPassWordInput': BusinessForm['Password'],
                    'SignupBusinessConfirmPasswordInput': BusinessForm['ConfirmPassword'],
                    'SignupBusinessUsernameInput': BusinessForm['Username']
                }
                files = {
                    "Signupbusiness_profile": (file_path, Profile, mime_type)
                    }
                res = requests.post('http://localhost:8000/api', data=data, files=files)
                print("Status:", res.status_code)
                # print("Response:", res.text)
                if 'TheErrorsOfServerForSignup' in json.loads(res.text):
                    self.howAllErrorThatComeFromServer(json.loads(res.text))

                elif 'message' in json.loads(res.text):
                    self.finallyCreateAccountAndMoveOn(json.loads(res.text))
                else:
                    self.SignupErrorDialog = MDDialog(
                        text="Somethink went wrong",
                        buttons=[
                            MDFlatButton(
                                text="OK",
                                on_release=lambda x: self.SignupErrorDialog.dismiss()  # ← use the inner function
                            ),
                        ],
                    )
                    self.SignupErrorDialog.open()
    
        except FileNotFoundError:
            # print("File not found")
            self.SignupErrorDialog = MDDialog(
                text="Your business profile file not found",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.SignupErrorDialog.dismiss()  # ← use the inner function
                        ),
                    ],
                )
            self.SignupErrorDialog.open()
    

        except Exception as e:
            # print("Error:", (e))
            self.SignupErrorDialog = MDDialog(
                text="Somethink went wrong",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.SignupErrorDialog.dismiss()  # ← use the inner function
                    ),
                ],
            )
            self.SignupErrorDialog.open()
    

    def howAllErrorThatComeFromServer(self, ServerError):
        print('Now you have to fix your error')
        theErrors = ServerError['TheErrorsOfServerForSignup']
        
        if not signupDateAndErrors.exists('TheErrorsOfServerForSignup'):
            signupDateAndErrors.put('TheErrorsOfServerForSignup')

        theStoredErrors = signupDateAndErrors.get('TheErrorsOfServerForSignup')
        theBusinessInfo = signupDateAndErrors.get('SignupUserBusinessForm')

        def save_error_in_json_file(field_error_key, input_field_name, screen_name):
            if field_error_key in theErrors:
                if field_error_key == 'BusinessUsernameError':
                    self.ShowErrorForSigupBusinessUsernameInput(self.ids.boxSignupBusinessUsername, theErrors[field_error_key][0])
                else:
                    self.manager.get_screen(screen_name).showErrorHereIfTheErrorComeingForServer(input_field_name ,theErrors[field_error_key])

                if field_error_key not in theStoredErrors:
                    theStoredErrors[field_error_key] = []
                if not any(e['value'] == theBusinessInfo[input_field_name] for e in theStoredErrors[field_error_key]):
                    theStoredErrors[field_error_key].append({
                        'Error': theErrors[field_error_key],
                        'value': theBusinessInfo[input_field_name],
                        'ScreenName': screen_name
                    })

        error_mapping = [
            ("BusinessNameError", "name", "BusinesNameAndCagegoryScreen"),
            ("BusinessCategoryError", "Category", "BusinesNameAndCagegoryScreen"),
            ("BusinessIndustryError", "Industry", "BusinesseIndustryAndDescriptionScreen"),
            ("BusinessDescriptionError", "Description", "BusinesseIndustryAndDescriptionScreen"),
            ("BusinessAddressError", "Address", "BusinesseAddressAndImageScreen"),
            ("BusinessProfileError", "PathOfBusinessProfiles", "BusinesseAddressAndImageScreen"),
            ("BusinessOpenTimeError", "OpenTime", "BusinesseOpenTimeAndCloseTimeAndHolidayScreen"),
            ("BusinessCloseTimeError", "CloseTime", "BusinesseOpenTimeAndCloseTimeAndHolidayScreen"),
            ("BusinessHolidaysError", "Holidays", "BusinesseOpenTimeAndCloseTimeAndHolidayScreen"),
            ("BusinessOwnerFirstNameError", "ownerFirstName", "BusinesseOwnerFirstNameAndLastNameScreen"),
            ("BusinessOwnerLastNameError", "ownerLastName", "BusinesseOwnerFirstNameAndLastNameScreen"),
            ("BusinessPhoneNumberError", "PhoneNumber", "BusinessPhoneNumberAndEmailAddressScreen"),
            ("BusinessEmailAddressError", "EmailAddress", "BusinessPhoneNumberAndEmailAddressScreen"),
            ("BusinessPhoneNumberOTPError", "PhoneNumberOTP", "BusinessSignupOTPVerificationScreen"),
            ("BusinessEmailAddressOTPError", "EmailAddressOTP", "BusinessSignupOTPVerificationScreen"),
            ("BusinessPassWordError", "Password", "BusinesseUserPasswordScreen"),
            ("BusinessConfirmPasswordError", "ConfirmPassword", "BusinesseUserPasswordScreen"),
            ("BusinessUsernameError", "Username", "BusinesUsernameScreen"),
        ]
        for field_error_key, input_field_name, screen_name in error_mapping:
            save_error_in_json_file(field_error_key, input_field_name, screen_name)

        signupDateAndErrors.put('TheErrorsOfServerForSignup', **theStoredErrors)
        # let go to fix the error
        for field_error_key, input_field_name, screen_name in error_mapping:
            if field_error_key in theErrors:
                if field_error_key != 'BusinessUsernameError':
                    self.showSignupSubmitionErrorDialog(screen_name)
                    break

    def showSignupSubmitionErrorDialog(self,ISNkvFile):
        def redirect_to_error_input(*args):
            self.SignupErrorDialog.dismiss()
            print("Navigate back to form or highlight first error field")
            self.parent.current = ISNkvFile
            self.parent.transition.direction = 'right'

        self.SignupErrorDialog = MDDialog(
            title="⚠️ Input Error",
            text="There’s an error in your input. Please check the form.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=redirect_to_error_input  # ← use the inner function
                ),
            ],
        )
        self.SignupErrorDialog.open()

            
    def finallyCreateAccountAndMoveOn(self, ServerError):
        print('Now I should create your account')
        print("ServerError: ", ServerError)
