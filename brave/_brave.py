import os
import json
import logging

logger = logging.getLogger(__name__)



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


    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.html)

    def to_jupyter(self,  width=800, height=600):

        from IPython.lib.display import IFrame
        self.save('temp_visual.html')
        return IFrame('temp_visual.html', width=width, height=height)
