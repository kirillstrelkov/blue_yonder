import argparse
import codecs
import os
import shutil
import requests


def __download_file(url, output):
    print('Downloading {} to {}'.format(url, output))
    with codecs.open(output, 'wb') as f:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def download_images(input_file, output_folder):
    with open(input_file) as f:
        for url in f.readlines():
            url = url.strip()
            if url:
                output_path = os.path.join(output_folder, url.split('/')[-1])
                __download_file(url, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download images from file.')
    parser.add_argument('input_file', help='Input file which contains urls')
    parser.add_argument('output_folder', help='Output folder where to save all images')

    args = parser.parse_args()
    download_images(args.input_file, args.output_folder)
