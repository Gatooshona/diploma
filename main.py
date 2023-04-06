from vk import Vk
from ya import YandexDisk


with open('token_vk.txt', 'r') as file_vk:
    token_vk = file_vk.read().strip()

vk_client = Vk(token_vk, '5.131')
vk_client.get_photos()

ya_client = YandexDisk()
ya_client.upload('netology_diploma', 'images')
