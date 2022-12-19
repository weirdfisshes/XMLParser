import xml.etree.ElementTree
import tempfile
import functools
import requests
import zipfile
import io
import os
import logs

import models


class Parser():

    def __init__(self):
        self.url = 'https://downloader.disk.yandex.ru/disk/bc3361b678dc9bdc0efda0634f7b20a84ddc57f7fb94f2506c53461a61c66c93/63a053ac/kRr_ciSTbdzj2h0OYshapMa-lSygEYeEUb62dBxoKUCDc22G8XFVJRYRAelxR3lf3J7dzHPVq-9MV6e3GMjhNA%3D%3D?uid=0&filename=test_file.zip&disposition=attachment&hash=R7J1Yeo9wu4N92WnPu5gRWd10VpaEb1ktP/Wt/8awW8AALWtZJCywNM56qKINiTYq/J6bpmRyOJonT3VoXnDag%3D%3D%3A&limit=0&content_type=application%2Fzip&owner_uid=53816453&fsize=479&hid=66581fe7c661556f3e753c64cba304c0&media_type=compressed&tknv=v2'

    def find_xml(self, path):
        for _, _, files in os.walk(path):
            for name in files:
                if str(name).lower().endswith('.xml'):
                    logs.logger.info('Find XML file')

                    return str(path + '/' + name)

    def get_file(self, url, directory):
        response = requests.get(url, verify=False)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file.extractall(directory)
        logs.logger.info('File extracted')
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

            except Exception as error:
                logs.logger.error(f'Failed to get file: {error}')

            try:
                tree = xml.etree.ElementTree.parse(file_path)
                root = tree.getroot()
                data = []
                for category in root.iter('category'):
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
                            logs.logger.error(f'Invalid item')
                            continue

                        data.append(
                            models.FlowerPriceItem(
                                code=get_item('code'),
                                name=name,
                                group=get_item('group'),
                                price=price
                            )
                        )

                return data

            except Exception as e:
                print(e)
