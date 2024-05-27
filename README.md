# Резервное копирование
Резервное копирование фотографий профиля VK на YandexDisk в отдельную папку

<img src="backup.jpg" alt="Backup_image" width="600"/>

## Инструкция

1. Для начала необходимо получить токен YandexDisk REST API и VK API:
* [Инструкция по получению токена YandexDisk REST API](https://yandex.ru/dev/disk-api/doc/ru/concepts/quickstart#quickstart__oauth)
* [Инструкция по получению токена VK API](https://dev.vk.com/ru/api/access-token/getting-started)

2. Установите все необходимые библиотеки: ```pip install -r requirements.txt```
3. Вставьте токены в поля ```token``` в файле конфигурации ```settings.ini```
4. Скопируйте ID своего профиля в ВК
5. Запустите файл ```main.py``` и следуйте инструкции.

## Доп. информация

В поле ```folder_name``` можно изменить название создаваемой папки.

## Поддержка

Если у вас возникли сложности или вопросы по использованию программы, создайте [обсуждение](https://github.com/WolArt13/YDVKbackup/issues/new) в данном репозитории или напишите на электронную почту mdp3101@mail.ru.

## Зависимости
Эта программа зависит от интепретатора Python версии 3.12.2 или выше, PIP 24.0 или выше.