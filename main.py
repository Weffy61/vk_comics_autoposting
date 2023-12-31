import requests
from os.path import splitext
from urllib.parse import unquote, urlsplit
from environs import Env
import random
import os


def get_file_extension(url):
    last_part_of_link = unquote(urlsplit(url).path)
    _, extension = splitext(last_part_of_link)
    return extension


def download_image(link, image_name):
    image_extension = get_file_extension(link)
    path = os.path.join('images', f'{image_name}{image_extension}')
    response = requests.get(link)
    response.raise_for_status()
    with open(f'{path}', 'wb') as image:
        image.write(response.content)
    return image_extension


def get_comic(link):
    response = requests.get(link)
    response.raise_for_status()
    response_content = response.json()
    image_name = response_content['title']
    image_link = response_content['img']
    image_extension = download_image(image_link, image_name)
    image_comment = response_content['alt']
    return image_name, image_extension, image_comment


def get_upload_url(access_token, group_id):
    api_version = 5.154
    payload = {
        'access_token': access_token,
        'group_id': group_id,
        'v': api_version
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    upload_url = response.json()
    raise_for_vk_status(upload_url)
    return upload_url['response']['upload_url']


def upload_image(img_path, url_address):
    with open(img_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url_address, files=files)
    response.raise_for_status()
    uploaded_image = response.json()
    raise_for_vk_status(uploaded_image)
    return uploaded_image['photo'], uploaded_image['server'], uploaded_image['hash']


def save_wall_image(access_token, group_id, photo, server, photo_hash):
    api_version = 5.154
    payload = {
        'access_token': access_token,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'v': api_version
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    wall_image = response.json()
    raise_for_vk_status(wall_image)
    attachments = wall_image['response'][0]
    owner_id = attachments['owner_id']
    save_id = attachments['id']
    return owner_id, save_id


def create_wall_post(access_token, group_id, owner_id, save_id, comment):
    api_version = 5.154
    payload = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': comment,
        'attachments': f'photo{owner_id}_{save_id}',
        'v': api_version
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    raise_for_vk_status(response.json())


def get_random_comics_url():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    max_comics_number = response.json()['num']
    random_comics_number = random.randrange(1, max_comics_number + 1)
    return f'https://xkcd.com/{random_comics_number}/info.0.json'


def raise_for_vk_status(request):
    if request.get("error"):
        status_code = request['error']['error_code']
        reason = request['error']['error_msg']
        http_error_msg = (
            f"{status_code} VK API Error: {reason}"
        )
        raise requests.HTTPError(http_error_msg)


def main():
    env = Env()
    env.read_env()
    vk_access_token = env.str('VK_ACCESS_TOKEN')
    vk_group_id = env.int('VK_GROUP_ID')
    os.makedirs('images', exist_ok=True)
    comics_img_name, comics_image_ext, comics_img_comment = get_comic(get_random_comics_url())
    get_upload_url(vk_access_token, vk_group_id)
    url_address = get_upload_url(vk_access_token, vk_group_id)
    img_path = os.path.join('images', f'{comics_img_name}{comics_image_ext}')
    try:
        photo, server, photo_hash = upload_image(img_path, url_address)
    finally:
        os.remove(img_path)
    owner_id, save_id = save_wall_image(vk_access_token, vk_group_id, photo, server, photo_hash)
    create_wall_post(vk_access_token, vk_group_id, owner_id, save_id, comics_img_comment)


if __name__ == '__main__':
    main()
