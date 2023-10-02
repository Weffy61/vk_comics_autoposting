import requests
from pathlib import Path
from os.path import splitext
from urllib.parse import unquote, urlsplit


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


def main():
    response = requests.get('https://xkcd.com/353/info.0.json')
    response.raise_for_status()
    response_content = response.json()
    image_name = response_content['title']
    image_link = response_content['img']
    save_image(image_link, image_name)
    image_comment = response_content['alt']
    print(image_comment)


if __name__ == '__main__':
    main()