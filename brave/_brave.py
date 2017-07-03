from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import json
import logging
from brave.palettes import *

logger = logging.getLogger(__name__)



def brave(collData, docData):
    current_file = os.path.dirname(__file__)
    parent = os.path.abspath(os.path.join(current_file, os.pardir))
    fn = os.path.join(parent, 'templates', 'embedded_brat__template.html')
    template = open(fn).read()

    template = template.replace("{0}", json.dumps(collData))
    template = template.replace("{1}", json.dumps(docData))
    return HtmlContainer(template)


def brave_entity_relations(doc_data, coll_data={}):
    brave_data = BraveData(doc_data, coll_data)
    return brave(brave_data.doc_data, brave_data.coll_data)


class HtmlContainer(object):
    def __init__(self, html):
        self.html = html

    def _repr_html_(self):
        return self.html


class BraveData(object):
    def __init__(self, doc_data, coll_data={}):
        self.doc_data = doc_data
        if len(coll_data) > 0:
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
