import os
import json


def brave(collData, docData):
    current_file = os.path.dirname(__file__)
    parent = os.path.abspath(os.path.join(current_file, os.pardir))
    fn = os.path.join(parent, 'templates', 'embedded_brat__template.html')
    template = open(fn).read()

    template = template.replace("{0}", json.dumps(collData))
    template = template.replace("{1}", json.dumps(docData))
    return HtmlContainer(template)


class HtmlContainer(object):
    def __init__(self, html):
        self.html = html

    def _repr_html_(self):
        return self.html

    def save(self, path):
        pass
