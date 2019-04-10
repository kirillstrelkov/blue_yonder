import codecs
import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from nose.tools import assert_set_equal, raises

from download_images import download_images


class DownloadImagesTest(TestCase):
    TEST_DATA_FILE = 'data.txt'

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.input_file = os.path.join(self.temp_dir.name, self.TEST_DATA_FILE)

    def tearDown(self):
        self.temp_dir.cleanup()

    def __download_and_assert_images(self, file_content):
        with codecs.open(self.input_file, 'w') as f:
            f.write(file_content)

        download_images(self.input_file, self.temp_dir.name)
        assert_set_equal(
            {line.strip().split('/')[-1]
             for line in file_content.splitlines()
             if len(line.strip()) > 0},
            {filename for filename in os.listdir(self.temp_dir.name)
             if filename != self.TEST_DATA_FILE}
        )

    def test_simple_file(self):
        file_content = '''
        https://www.python.org/static/img/python-logo@2x.png
        https://www.raspberrypi.org/documentation/usage/python/images/python-logo.png
        https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/2000px-Python.svg.png
        https://manufacturingstories.com/wp-content/uploads/2018/01/01-rise-of-python-v02-1.png 
        '''
        self.__download_and_assert_images(file_content)

    def test_with_duplicates(self):
        file_content = '''
        https://www.raspberrypi.org/documentation/usage/python/images/python-logo.png
        https://www.raspberrypi.org/documentation/usage/python/images/python-logo.png
        https://www.raspberrypi.org/documentation/usage/python/images/python-logo.png
        '''
        self.__download_and_assert_images(file_content)

    @raises(FileNotFoundError)
    def test_non_existing_input_file(self):
        download_images('non_existing_file', self.temp_dir.name)

    @raises(FileNotFoundError)
    def test_non_existing_output_folder(self):
        download_images(self.input_file, 'non_existing_folder')
