import requests
import os
from tqdm import tqdm


class YandexDisk:
    token = input('Введите токен для YandexDisk: ')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        return href

    def _create_folder(self, folder_name):
        """Метод для создания папки на Яндекс диске"""
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=headers, params=params).status_code != 200:
            requests.put(url, headers=headers, params=params)
            print(f'\nПапка {folder_name} успешно создана.\n')
        else:
            print(f'\nПапка {folder_name} уже существует.\n')
        return folder_name

    def upload(self, ya_disk_file_path: str, target_dir_name):
        """Метод загружает файлы на Яндекс диск"""
        self._create_folder(ya_disk_file_path)

        file_list = os.listdir(path=target_dir_name)

        for file in tqdm(file_list):
            ya_disk_path = f'{ya_disk_file_path}/{file}'
            href = self._get_upload_link(disk_file_path=ya_disk_path)

            local_file_path = os.path.join(os.getcwd(), target_dir_name, file)
            requests.put(href, data=open(local_file_path, 'rb'))
