from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import os
from unittest import TestCase


from brave import brave
from examples.brave_example import coll_data, doc_data


class BasicTest(TestCase):
    def test_basic(self):

        html = brave(doc_data, coll_data, save_to_path='temp_visual.html').strip()

        baseline = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples', 'output_example.html')

        self.assertEqual(html, open(baseline).read().strip())
        self.assertEqual(html, open('temp_visual.html').read().strip())
