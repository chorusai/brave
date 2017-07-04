from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from ast import literal_eval

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


def brave_compare(true_doc_data, pred_doc_data, true_suffix='*', pred_suffix=''):
    if true_doc_data['text'] != pred_doc_data['text']:
        raise ValueError('The text should be equal in both true_doc_data and pred_doc_data')
    if true_suffix == pred_suffix:
        raise ValueError('true_suffix should be different than pred_suffix')

    ret_val = {}
    ret_val['text'] = true_doc_data['text']

    add_suffix(ret_val, true_doc_data, suffix=true_suffix)
    add_suffix(ret_val, pred_doc_data, suffix=pred_suffix)

    return brave_simple(ret_val)


def add_suffix(ret_val, doc_data, suffix='*'):

    ret_val['entities'] = ret_val.get('entities', [])
    for key, type_, span in doc_data['entities']:
        ret_val['entities'].append((key + suffix, type_ + suffix, span))

    ret_val['triggers'] = ret_val.get('triggers', [])
    for key, type_, span in doc_data['triggers']:
        ret_val['triggers'].append((key + suffix, type_ + suffix, span))

    ret_val['attributes'] = ret_val.get('attributes', [])
    for key, type_, ent_key in doc_data['attributes']:
        ret_val['attributes'].append((key + suffix, type_ + suffix, ent_key + suffix))

    ret_val['relations'] = ret_val.get('relations', [])
    for key, type_, lst in doc_data['relations']:
        new_lst = []
        for role, ent_key in lst:
            new_lst.append((role, ent_key + suffix))
    ret_val['relations'].append((key + suffix, type_ + suffix, new_lst))

    ret_val['events'] = ret_val.get('events', [])
    for key, trigger_key, lst in doc_data['events']:
        new_lst = []
        for role, ent_key in lst:
            new_lst.append((role, ent_key + suffix))
    ret_val['events'].append((key + suffix, trigger_key + suffix, new_lst))


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
        range_ = range(0, len(entities_palettte), (len(entities_palettte) // len(ent_types)))
        colors = [entities_palettte[i] for i in range_]
        ent_colors = dict(zip(ent_types, colors))
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
        range_ = range(0, len(relations_palette), (len(relations_palette) // len(relation_args.keys())))
        colors = [relations_palette[i] for i in range_]
        rel_colors = dict(zip(relation_args.keys(), colors))
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


def merge_doc_datas(*docs):
    """
    Merges several docDatas into one, updating values and indexes as necessary.
    ***Currently supports only Entities and Relations***

    Args:
        *docs:

    Returns: docData

    """
    res = {"text": "", "entities": [], "relations": []}
    offsets = [0]
    t_index = 0
    r_index = 0
    for i, doc in enumerate(docs):
        # Offset initializaion
        offset = offsets[i]
        # Update doc
        doc["entities"] = update_doc_data_entities(doc["entities"], offset, t_index)
        doc["relations"] = update_doc_data_relations(doc["relations"], r_index, t_index)
        # Update indexes
        t_index = int(doc["entities"][-1][0][1:])
        r_index = int(doc["relations"][-1][0][1:])
        # Extend res
        res["text"] += (doc["text"] + "\n")
        res["entities"].extend(doc["entities"])
        res["relations"].extend(doc["relations"])
        # Update offsets
        offsets.append(len(res["text"]))
    return res


def update_doc_data_entities(entity, offset, t_index):
    indexes, types, spans = zip(*entity)

    indexes = ["T" + str(int(ind[1:]) + t_index) for ind in indexes]

    new_spans = []
    for span in spans:
        new_span = increase_spans(span, offset)
        new_spans.append(new_span)

    res = zip(indexes, types, new_spans)
    res = [list(ent) for ent in res]
    return res


def update_doc_data_relations(relation, r_index, t_index):
    indexes, types, entities = zip(*relation)

    indexes = ["R" + str(int(ind[1:]) + r_index) for ind in indexes]

    entities = [[[t1[0], "T" + str(int(t1[1][1:]) + t_index)], [t2[0], "T" + str(int(t2[1][1:]) + t_index)]] for t1, t2
                in entities]

    res = zip(indexes, types, entities)
    res = [list(ent) for ent in res]
    return res


def increase_spans(spans_input, x):
    if type(spans_input) == str: spans_input = literal_eval(spans_input)
    groups = []
    for span in spans_input:
        span[0] += x
        span[1] += x
        groups.append(span)
    return groups