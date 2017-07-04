from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import json
import logging

from brave.palettes import *

logger = logging.getLogger(__name__)

__mode = 'script'


def start_notebook_mode(in_iframe=True):
    global __mode
    if in_iframe:
        __mode = 'iframe'
    else:
        __mode = 'embedded'


def save(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def brave(collData, docData, save_to_path=None, width=800, height=600):
    parent = os.path.dirname(__file__)
    parent = os.path.dirname(parent)
    fn = os.path.join(parent, 'templates', 'embedded_brat__template.html')
    template = open(fn).read()

    template = template.replace("{0}", json.dumps(collData))
    html = template.replace("{1}", json.dumps(docData))

    if save_to_path:
        save(html, save_to_path)

    if __mode == 'iframe':
        if save_to_path:
            eff_path = save_to_path
        else:
            eff_path = 'temp_visual.html'
            save(html, eff_path)

        ret_val = HtmlContainer("""<iframe
                    width="{width}"
                    height="{height}"
                    src="{src}"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
                """.format(src=eff_path,
                           width=width,
                           height=height))
    elif __mode == 'embedded':
        raise NotImplementedError(
            'Pure `embedded` mode is not supported yet. If running in Jupyter, use `iframe` mode.')
    else:
        ret_val = html
    return ret_val


def brave_simple(doc_data):
    """
    This method currently supported only entities and relations!
    Args:
        doc_data:

    Returns:

    """
    brave_data = BraveData(doc_data)
    return brave(brave_data.coll_data, brave_data.doc_data)


class HtmlContainer(object):
    def __init__(self, html):
        self.html = html

    def _repr_html_(self):
        return self.html


class BraveData(object):
    def __init__(self, doc_data, coll_data=None):
        self.doc_data = doc_data
        if coll_data is not None:
            self.coll_data = coll_data
        else:
            self.coll_data = {}
            self.__parse_entities()
            self.__parse_relations()

    def __parse_entities(self):
        self.ent_dict = dict([(x[0], x[1]) for x in self.doc_data['entities']])
        ent_types = set(self.ent_dict.values())
        ent_colors = dict(zip(ent_types, entities_palettte[0:len(ent_types)]))
        entity_types = []
        for name in ent_types:
            t = {
                'bgColor': ent_colors[name],
                'borderColor': 'darken',
                'labels': [name, name[0:3]],
                'type': name
            }
            entity_types.append(t)
        self.coll_data['entity_types'] = entity_types

    def __parse_relations(self):
        relation_args = {}
        for rel in self.doc_data['relations']:
            key, name, role_ents = rel
            for role, ent_key in role_ents:
                curr_roles = relation_args.get(name, {})
                curr_types = curr_roles.get(role, set())
                curr_types.add(self.ent_dict[ent_key])
                curr_roles[role] = curr_types
                relation_args[name] = curr_roles
        rel_colors = dict(zip(relation_args.keys(), relations_palette[0:len(relation_args.keys())]))
        relation_types = []
        for name, args in relation_args.iteritems():
            rel_dict = {
                'args': [{'role': role, 'targets': list(targets)} for role, targets in args.iteritems()],
                'color': rel_colors[name],
                'dashArray': '3,3',
                'labels': [name, name[0:3]],
                'type': name

            }
            relation_types.append(rel_dict)
        self.coll_data['relation_types'] = relation_types
