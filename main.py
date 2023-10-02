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


def work_with_vk_api(access_token):
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


def main():
    env = Env()
    env.read_env()
    vk_client_id = env.int('VK_CLIENT_ID')
    vk_access_token = env.str('VK_ACCESS_TOKEN')
    # get_comics('https://xkcd.com/353/info.0.json')
    work_with_vk_api(vk_access_token)


if __name__ == '__main__':
    main()
