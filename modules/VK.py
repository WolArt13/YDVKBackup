import requests, sys
from urllib.parse import urlparse
from datetime import datetime

class VK:
    """Класс для работы с VK API"""
    def __init__(self, token, user_id, version='5.131') -> None:
        self.token = token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.main_url = 'https://api.vk.com/method/'
        self.count = 0
    
    def get_profile_photos(self, count = 5):
        """
        Возвращает лог и список имен и url фотографий профиля в самом высоком качестве. 
        Количество возвращаемых фото по умолчанию ограничено значением 5
        """
        if not isinstance(self.id, int):
            self.id = self.get_user_id()
            
        url = f'{self.main_url}photos.get'
        params = {'owner_id': {self.id}, 
                  'album_id': 'profile', 
                  'rev': 1, 
                  "extended": 1, 
                  'count': count}
        r = requests.get(url, params={**self.params, **params})
        if 'error' in r.json().keys():
            if r.json()['error']['error_code'] == 5:
                """Ошибка если токен не считывается"""
                print('Ошибка авторизации. Проверьте правильность введенного токена VK API.')
                sys.exit()
            else:
                print('Ошибка на стороне клиента. (VK API)')
                sys.exit()
        if r.status_code == 200:
            # Словарь с данными о фото в виде - имя_файла: url
            log = []
            url_list = {}

            for value in r.json()['response']['items']:
                key = value['likes']['count']
                # Если ключ с количеством лайков существует, то добавляем дату
                if key in url_list:
                    key = f'{value['likes']['count']}_{datetime.fromtimestamp(value['date']).strftime('%d_%m_%Y')}'
                    # Здесь я внес повторную проверку ключа, так как на этапе тестирования
                    # ключ в новом виде, также попадался в словаре
                    if key in url_list:
                        key = f'{value['likes']['count']}-{datetime.fromtimestamp(value['date']).strftime('%d_%m_%Y')}'
                        url_list[key] = value['sizes'][-1]['url']
                    else:
                        url_list[key] = value['sizes'][-1]['url']
                else:
                    url_list[key] = value['sizes'][-1]['url']
                log.append({'file_name': f'{key}.{urlparse(value['sizes'][-1]['url']).path.split('.')[-1]}',
                            'size': value['sizes'][-1]['type']})
                
            print('\nДанные о фото получены.')
            return(url_list, log)
        else:
            print('Ошибка запроса.')
        
    def get_user_id(self):

        url = f'{self.main_url}users.get'
        params = {'user_ids': self.id, "fields": "screen_name"}
        r = requests.get(url, params={**self.params, **params})
        if "error" in r.json().keys():
            if r.json()['error']['error_code'] == 1116:
                print('Ошибка. Не действительный токен VK API.')
                sys.exit()
            else:
                print('Ошибка на стороне клиента.(VK API)')
        elif not r.json()['response']:
            print('Введен некорректный идентификатор пользователя VK.')
            sys.exit()
        return r.json()['response'][0]['id']