import requests
import json

class PetFrends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        
    def get_api_key(self, email:str, password:str) -> json:
        """"Метод делает запрос к API сервера и возвращает статус и результат в формате JSON с уникальным ключем пользователя, найденного по указанному email и паролем"""
        
        headers = {'email': email,'password': password}
        
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        
        result = ""
        
        try:
            result = res.json()
        except:
            result = res.text
            
        return status, result
    
    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и резултат в формате JSON со списком найденых питомцев, 
        совпадающих с фильтром. На данный момент фильтр может иметь любое пустое значение - получить список всех питомцев, 
        либо 'my_pets' - получить список пользователя"""
        
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
   
    def add_new_pet_with_photo(self, auth_key: json, name:str, animal_type:str, age:str, pet_photo) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
                запроса  и результат в формате JSON с данными добавленного питомца"""
        
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        
        res = requests.post(self.base_url+'api/pets',headers=headers,data=data,files=file)
        status = res.status_code
        result = ""
        
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    
    def delete_self_pet(self, auth_key:json, pet_id:str ) -> json:
        
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json: 
        """Метод отправляет на сервер данные для изменение иформации о питомце, и возращает статус запроса 
                и результат в формате json с данными питомца."""
        
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        
        return status, result

    def create_my_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
                запроса  и результат в формате JSON с данными добавленного питомца"""
        
        headers = {'auth_key': auth_key['key']}
        data={
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные для изменение фото, и возращает статус запроса 
                и результат в формате json с данными питомца."""

        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=file)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        
        return status, result

        