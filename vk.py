import requests
import json
import os


class Vk:
    url = 'https://api.vk.com/method/'
    vk_id = input('Введите id: ')

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, count=5):
        """Получаем json-файл с информацией по файлу и записываем фотографии в папку"""
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': self.vk_id,
            'album_id': 'profile',
            'extended': '1',
            'count': count
        }
        photos_all_info = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        photos_all_info = photos_all_info['response']['items']

        photos_info = []
        likes = set()
        urls = []

        for element in photos_all_info:
            url = element['sizes'][-1].get('url')
            size = element['sizes'][-1].get('type')
            date = element['date']
            like = element['likes']['count']
            file_name = f'{like}.jpg'

            if like in likes:
                file_name = f'{like}_{date}.jpg'

            photos_info.append({
                'file_name': file_name,
                'size': size
            })

            likes.add(like)
            urls.append(url)

            current = os.getcwd()
            folder = 'images'
            full_path = os.path.join(current, folder, file_name)

            if not os.path.exists(os.path.join(current, folder)):
                os.mkdir(os.path.join(current, folder))

            with open(full_path, 'wb') as f:
                response = requests.get(url)
                f.write(response.content)

        with open('photos_info.json', 'w') as file:
            json.dump(photos_info, file, indent=2)

        return photos_info
