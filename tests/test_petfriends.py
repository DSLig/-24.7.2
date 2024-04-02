from app.api import PetFrends
from app.settings import valid_email, valid_password, incorrect_email, incorrect_password, name, animal_type, age, pet_photo, name_1, animal_type_1, age_1, pet_photo_1
import os

pf = PetFrends()
new_pet_id = ''

def test_settings(email = valid_email, password = valid_password):
    """Проверяем наилчие данных пользоватея для тестов"""
    assert len(email) != 0
    assert len(password) != 0


def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """"Проверяем возможность получить ключь для корректного пользователя"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter = ''):
    """"Проверяем возможность получить весь список питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pet_with_photo():
    """Проверяем возможность добавить нового питомца с фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert len(result['id']) > 0
    return new_pet_id == id

def test_delete_my_pet_valid_user():
    """Проверяем возможность удаление питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_my_pet_simple(auth_key, "cat", "cat", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_self_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_info_to_existing_pet(name = name_1, animal_type = animal_type_1, age = age_1):
    """Проверяем возможность обновления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    
    if len(my_pets['pets']) == 0:
        pf.create_my_pet_simple(auth_key, "cat", "cat", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    
    
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name

#Задание 24.7.2

def test_create_my_pet_simple():
    """"Проверяем возможность добавление питомца упрощенным способом"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
   
    status, result = pf.create_my_pet_simple(auth_key, name, animal_type, age,)
    assert status == 200
    assert len(result['id']) > 0

def test_get_my_pets_with_valid_key(filter = 'my_pets'):
    """"Проверяем возможность получить список питомцев валидного пользователя"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pf.create_my_pet_simple(auth_key, "cat", "cat", "1")
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_photo_to_existing_pet():
    """Проверяем возможность добавленрие фото к существующему питомцу"""
   
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    
    if len(my_pets['pets']) == 0:
        pf.create_my_pet_simple(auth_key, "cat", "cat", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        
    assert status == 200
    assert result['pet_photo'] is not None

def test_updating_a_photo_of_an_existing_pet():
    """Проверяем возможность обновления фото у существующего питомца"""
  
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_1)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    
    
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        
    assert status == 200
    assert result['pet_photo'] is not None

def test_api_key_with_incorrect_email(email=incorrect_email, password=valid_password):
    """Проверяем что запрос api ключа возвращает статус 403 и пустой ключ при введенном некоректном email"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    
def test_api_key_with_incorrect_password(email=valid_email, password=incorrect_password):
    """Проверяем что запрос api ключа возвращает статус 403 и пустой ключ при введенном некоректном пароле"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    
def test_api_key_for_non_existent_user(email=incorrect_email, password=incorrect_password):
    """Проверяем что запрос api ключа возвращает статус 403 и пустой ключ при введении данных для незарегистрированного пользователя"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    
def test_post_add_new_pet_with_not_number_data_age(age = 'fff'):
    """Проверяем что для данных питомца age возможны только числа, при введении некоректного значения сервер возвращает статус 400."""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    
    #BUG#BUG#BUG#BUG#BUG#BUG#BUG#BUG#BUG
    
    assert status == 400
    assert len(result['id']) == 0
    
def test_post_add_new_pet_with_negative_number_data_age(age = '-1'):
    """Проверяем что для данных питомца age возможны только положительние числа, при введении некоректного значения сервер возвращает статус 400."""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    
    #BUG#BUG#BUG#BUG#BUG#BUG#BUG#BUG#BUG
    
    assert status == 400
    assert len(result['id']) == 0
    
def test_create_my_pet_simple_with_empty_values(name = '', animal_type = '', age = ''):
    """"Проверяем что для данных не может буть пустых значений, при введение пустих значений при простом добавлении питомца сервер возвращает статус 400"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_my_pet_simple(auth_key, name, animal_type, age,)
    
    #BUG#BUG#BUG#BUG#BUG#BUG#BUG#BUG#BUG    
    
    assert status == 400
    assert len(result['id']) == 0
    
   

    
    
    


    





    
    

    
    

    
    
    
    
    
