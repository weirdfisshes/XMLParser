import xml.etree.ElementTree
import tempfile
import functools

import models


class Parser():

    def get_item_from_node(self, node, item):
        try:
            return node.find(item).text
        except Exception:
            return

    def parse(self, file_path):
        try:
            tree = xml.etree.ElementTree.parse(file_path)
            root = tree.getroot()
            data = []
            for category in root.iter('category'):
                for item in category.iter('item'):
                    get_item = functools.partial(
                        self.get_item_from_node, item
                    )

                    name_total = [get_item('name'), get_item('sort')]

                    name = ' '.join(
                        filter(
                            None, name_total
                        )
                    )

                    data.append(
                        models.FlowerPriceItem(
                            code=get_item('code'),
                            name=name,
                            group=get_item('group'),
                            price=get_item('price')
                        )
                    )

            return data

        except Exception as e:
            print(e)
