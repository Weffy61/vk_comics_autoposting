import requests
from pathlib import Path
from os.path import splitext
from urllib.parse import unquote, urlsplit
from environs import Env


def get_file_extension(url):
    last_part_of_link = unquote(urlsplit(url).path)
    _, extension = splitext(last_part_of_link)
    return extension


def save_image(link, image_name):
    image_extension = get_file_extension(link)
    path = f'images/{image_name}{image_extension}'
    image_path = Path(path).parent
    image_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(link)
    response.raise_for_status()
    with open(f'{path}', 'wb') as image:
        image.write(response.content)


def get_comics(link):
    response = requests.get(link)
    response.raise_for_status()
    response_content = response.json()
    image_name = response_content['title']
    image_link = response_content['img']
    save_image(image_link, image_name)
    image_comment = response_content['alt']
    print(image_comment)


def get_vk_groups(access_token):
    full_group_info = 1
    api_version = 5.154
    payload = {
        'access_token': access_token,
        'extended': full_group_info,
        'v': api_version
    }
    url = 'https://api.vk.com/method/groups.get'
    response = requests.get(url, params=payload)
    print(response.json())


def get_vk_url_to_upload_img(access_token, group_id):
    api_version = 5.154
    payload = {
        'access_token': access_token,
        'group_id': group_id,
        'v': api_version
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def send_image_to_vk_wall(img_path, ulr_address):
    with open(img_path, 'rb') as file:
        url = ulr_address
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        print(response.json())


def main():
    env = Env()
    env.read_env()
    vk_client_id = env.int('VK_CLIENT_ID')
    vk_access_token = env.str('VK_ACCESS_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')
    # get_comics('https://xkcd.com/353/info.0.json')
    # get_vk_groups(vk_access_token)
    # get_vk_url_to_upload_img(vk_access_token, vk_group_id)
    url_address = get_vk_url_to_upload_img(vk_access_token, vk_group_id)
    send_image_to_vk_wall('images/Python.png', url_address)


if __name__ == '__main__':
    main()
