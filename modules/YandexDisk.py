import requests, sys

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