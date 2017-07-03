from brave import brave

import os

coll_data = {
    "entity_types": [
        {
            "type": "Person",
            "labels": [ "Person", "Per" ],
            "bgColor": "#7fa2ff",
            "borderColor": "darken"
        }
    ],
    "entity_attribute_types": [
        {
            "type": "Notorious",
            "values": {
                "Notorious": { "glyph": "*" }
            },
            "bool": "Notorious"
        }
    ],
    "relation_types": [
        {
            "type": "Anaphora",
            "labels": [ "Anaphora", "Ana" ],
            "dashArray": "3,3",
            "color": "purple",
            "args": [
                {
                    "role": "Anaphor",
                    "targets": [ "Person" ]
                },
                {
                    "role": "Entity",
                    "targets": [ "Person" ]
                }
            ]
        }
    ],
    "event_types": [
        {
            "type": "Assassination",
            "labels": [ "Assassination", "Assas" ],
            "bgColor": "lightgreen",
            "borderColor": "darken",
            "arcs": [
                {
                    "type": "Victim",
                    "labels": [ "Victim", "Vict" ]
                },
                {
                    "type": "Perpetrator",
                    "labels": [ "Perpetrator", "Perp" ],
                    "color": "green"
                }
            ]
        }
    ]
}

doc_data = {
    "text": "Ed O'Kelley was the man who shot the man who shot Jesse James.",
    "entities": [
        [
            "T1",
            "Person",
            [ [ 0, 11 ] ]
        ],
        [
            "T2",
            "Person",
            [ [ 20, 23 ] ]
        ],
        [
            "T3",
            "Person",
            [ [ 37, 40 ] ]
        ],
        [
            "T4",
            "Person",
            [ [ 50, 61 ] ]
        ]
    ],
    "attributes": [ [ "A1", "Notorious", "T4" ] ],
    "relations": [
        [
            "R1",
            "Anaphora",
            [ [ "Anaphor", "T2" ], [ "Entity", "T1" ] ]
        ]
    ],
    "triggers": [
        [
            "T5",
            "Assassination",
            [ [ 45, 49 ] ]
        ],
        [
            "T6",
            "Assassination",
            [ [ 28, 32 ] ]
        ]
    ],
    "events": [
        [
            "E1",
            "T5",
            [ [ "Perpetrator", "T3" ], [ "Victim", "T4" ] ]
        ],
        [
            "E2",
            "T6",
            [ [ "Perpetrator", "T2" ], [ "Victim", "T3" ] ]
        ]
    ]
}

container = brave(coll_data, doc_data)
current_file = os.path.dirname(__file__)
output_path = current_file[:current_file.rfind("/")] + "/example_1.html"
with open(output_path, 'wb') as f:
    f.write(container.html)

