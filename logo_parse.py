import requests
import os
import re
import argparse
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


primary_link = 'https://www.brandsoftheworld.com'
database_link = 'https://www.brandsoftheworld.com/logos/categories'

page_html = requests.get(database_link, timeout=30).text
page_source = BeautifulSoup(page_html, 'html.parser')
category_links = page_source.select('#primaryInner a')
category_links = list(map(lambda css: [css.text, primary_link + css.get('href')], category_links))
category_names = tuple(map(lambda s: s[0], category_links))

arg_parser = argparse.ArgumentParser(
    description='Download Logos from www.brandsoftheworld.com to local directory'
)

arg_parser.add_argument('Path',
                        metavar='path',
                        type=str,
                        help='Path to logos directory')
arg_parser.add_argument('--max_pages',
                        nargs='?',
                        const=1000,
                        type=int,
                        default=1000,
                        help=f'Select maximum amount of category pages to parse')
arg_parser.add_argument('--categories',
                        nargs='+',
                        type=str,
                        default=category_names,
                        help=f'Select from {category_names}')

args = arg_parser.parse_args()

logo_dir = args.Path
to_parse = args.categories
max_pages = args.max_pages

if not os.path.exists(logo_dir):
    os.mkdir(logo_dir)

for category_name, category_link in category_links:
    if category_name in to_parse:
        for i in range(max_pages):
            if i == 0:
                page_link = category_link
            else:
                page_link = f'{category_link}?page={i}'
            page_html = requests.get(page_link, timeout=50).text
            page_source = BeautifulSoup(page_html, 'html.parser')
            logo_names = page_source.select('.views-row .title')
            if len(logo_names) > 0:
                logo_names = list(map(lambda css: css.text, logo_names))
                logo_pics = page_source.select('.image')
                logo_pics = list(map(lambda css: css.get('src'), logo_pics))
                if len(logo_pics) == len(logo_names):
                    logo_imgs, logo_strs = [], []
                    for logo_src, logo_str in zip(logo_pics, logo_names):
                        try:
                            img_response = requests.get(logo_src, timeout=10)
                            img = Image.open(BytesIO(img_response.content))
                            logo_imgs.append(img.convert('RGB'))
                            logo_strs.append(logo_str)
                        except BaseException as e:
                            print('Some error has occured')
                            pass
                    assert len(logo_imgs) == len(logo_strs)
                    if category_name not in os.listdir(logo_dir):
                        os.mkdir(f'{logo_dir}/{category_name}')
                    for index, (logo_image, logo_name) in enumerate(zip(logo_imgs, logo_strs)):
                        logo_name_cor = re.sub(re.compile(r'\W'), ' ', logo_name)
                        logo_name_cor = re.sub(re.compile(r'\s{2,10}'), ' ', logo_name_cor)
                        image_name = f'{logo_name_cor}_{category_name}_{i+1}_{index+1}.jpg'
                        logo_image.save(f'{logo_dir}/{category_name}/{image_name}')
                    print(f'Loaded {len(logo_imgs)} logos at page {i + 1} for category: {category_name}')
                else:
                    print('Not equal lengths of images and quotes')
            else:
                print(f'No more logos on page {i+1}')
                break
