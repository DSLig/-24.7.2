import os
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

incorrect_email = 'Basssster@gmail.com'
incorrect_password = 'passwordInc'

name = 'Tim'
animal_type = 'Cat'
age = '1'
pet_photo = 'tests\images\cat1.jpg'

name_1 = 'Sim'
animal_type_1 = 'Cat'
age_1 = '2'
pet_photo_1 = 'tests\images\cat2.jpg'