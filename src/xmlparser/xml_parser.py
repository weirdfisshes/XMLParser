import xml.etree.ElementTree
import tempfile
import functools
import requests
import zipfile
import io
import os

from . import logs
from . import models


class Parser():

    def __init__(self, url):
        self.url = url

    def find_xml(self, path):
        for _, _, files in os.walk(path):
            for name in files:
                if str(name).lower().endswith('.xml'):
                    logs.logger.debug('Find XML file')
                    return str(path + '/' + name)

                logs.logger.error('XML file not found')

    def get_file(self, url, directory):
        response = requests.get(url, verify=False)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file.extractall(directory)
        logs.logger.debug('File extracted')
        file_path = self.find_xml(directory)

        return file_path

    def get_item_from_node(self, node, item):
        try:
            return node.find(item).text

        except Exception:
            return

    def parse(self):
        with tempfile.TemporaryDirectory() as directory:
            try:
                file_path = self.get_file(self.url, directory)

            except Exception:
                file_path = None
                logs.logger.exception('Failed to get file')

                return

            tree = xml.etree.ElementTree.parse(file_path)
            root = tree.getroot()
            data = []
            errors = 0
            length = 0
            for category in root.iter('category'):
                length += len(category)
                for item in category.iter('item'):
                    get_item = functools.partial(
                        self.get_item_from_node, item
                    )

                    name_total = list(map(get_item, ['name', 'sort']))

                    name = ' '.join(
                        filter(
                            None, name_total
                        )
                    )
                    price = get_item('price')
                    if price is None:
                        logs.logger.error('Invalid item')
                        errors += 1
                        continue

                    data.append(
                        models.FlowerPriceItem(
                            code=get_item('code'),
                            name=name,
                            group=get_item('group'),
                            price=price
                        )
                    )

            return data, length, errors
