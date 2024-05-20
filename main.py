import requests
from datetime import datetime
import sys
from progress.bar import IncrementalBar
import json
import os
from urllib.parse import urlparse

class YandexDisk:
    """Класс для работы с REST API Яндекс Диска"""
    def __init__(self, token) -> None:
        self._main_url = 'https://cloud-api.yandex.net/v1/disk'
        self._headers = {'Authorization': f'OAuth {token}'}

    def make_folder(self, folder_name):
        """Создание папки."""
        params = {'path': {folder_name}}
        r = requests.put(f"{self._main_url}/resources", params=params, headers=self._headers)

        # Проверка статуса ответа PUT запроса.
        if r.status_code == 201:
            print(f'Папка с именем "{folder_name}" успешно создана.')

        # Условие если папка с таким именем уже существует.
        elif r.status_code == 409:
            ans = input(f'Папка с именем "{folder_name}" уже существует.\nЗагрузить фото в нее? ("y" - yes/"n" - no)\n')
            if ans == 'y':
                return
            elif ans == 'n':
                sys.exit()
            else: 
                print('Ответ в неверном формате, попробуйте еще раз.\n')
                self.make_folder(folder_name)
        else:
            print('Ошибка создания папки.')
            sys.exit()

    def upload_file(self, file, path):
        """
        Загрузить файл на диск.
        В path нужно указать либо имя файла(для загрузки в корневой каталог), либо путь и имя файла(через "/")
        """
        params = {'path': {path}}
        # Запрос на получение ссылки для загрузки файла по указанному пути.
        resp = requests.get(f"{self._main_url}/resources/upload", params=params, headers=self._headers)

        if resp.status_code == 409:
            if resp.json()['error'] == 'DiskResourceAlreadyExistsError':
                print(f'\nФайл на диске с именем {path.split('/')[-1]} уже существует.')
                return

        # Полученная ссылка из ответа.
        upload_url = resp.json()['href']
        r = requests.put(upload_url,
                    files={'file': file})
        
class VK:
    """Класс для работы с VK API"""
    def __init__(self, token, user_id, version='5.131') -> None:
        self.token = token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.main_url = 'https://api.vk.com/method/'
    
    def get_profile_photos(self, count = 5):
        """
        Возвращает лог и список имен и url фотографий профиля в самом высоком качестве. 
        Количество возвращаемых фото по умолчанию ограничено значением 5
        """
        url = f'{self.main_url}photos.get'
        params = {'owner_id': {self.id}, 
                  'album_id': 'profile', 
                  'rev': 1, 
                  "extended": 1, 
                  'count': count}
        r = requests.get(url, params={**self.params, **params})
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



if __name__ == '__main__':
    # Токен REST API YandexDisk без OAuth
    token_yd = 'your_token'
    # Токен VK API
    token_vk = 'your_token'
    # Ваш VK user_id
    user_id = 'your_ID'

    disk = YandexDisk(token_yd)
    vk = VK(token_vk, user_id)

    # Получаем данные о фотографиях профиля
    photos_data, log = vk.get_profile_photos(count=5)

    # Название папки куда сохранить фото
    folder_name = "VK Profile Photos Backup"
    disk.make_folder(folder_name)

    # Загружаем полученые фотографии на диск
    bar = IncrementalBar('Загрузка фото', max = len(photos_data))
    for name, url in photos_data.items():
        content = requests.get(url).content
        disk.upload_file(content, f'{folder_name}/{name}')
        bar.next()
    bar.finish()
    print('Фото успешно загружены на YandexDisk')
    
    # Сохраняем лог с данными о загруженных фото в .json файл
    with open(f'{os.getcwd()}/upload_log.json', 'w') as f:
        json.dump(obj=log, fp=f, indent=4)
