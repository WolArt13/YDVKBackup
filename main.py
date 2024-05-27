import requests, json, os, configparser
from progress.bar import IncrementalBar
from modules.VK import VK
from modules.YandexDisk import YandexDisk

def get_VK_token():
    """Получение токена VK API из файла settings.ini"""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config['VK API']['token']

def get_YD_token():
    """Получение токена YandexDisk REST API из файла settings.ini"""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config['YandexDisk REST API']['token']

def upload_photo(folder_name):
    """Функция для загрузки фото из профиля ВК на Яндекс Диск"""
    # Получаем данные о фотографиях профиля
    photos_data, log = vk.get_profile_photos(count=int(input('Введите количество загружаемых фото: ')))

    # Название папки куда сохранить фото
    folder_name = folder_name
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
    print('Создан лог загрузки.')

if __name__ == '__main__':
    # Токен REST API YandexDisk без OAuth
    token_yd = get_YD_token()
    # Токен VK API
    token_vk = get_VK_token()
    # VK user_id или screen_name
    user_id = input('Введите id пользователя: ')

    disk = YandexDisk(token_yd)
    vk = VK(token_vk, user_id)

    folder_name = "VK Profile Photos Backup"

    upload_photo(folder_name)
