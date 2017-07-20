from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from importlib import import_module
from random import getrandbits


def try_import_ipython():
    try:
        return import_module('IPython')
    except ImportError:
        return None


def get_init_script():
    return """
    <script>
    if(!$('.brave_css').size()){
        var link = document.createElement("link");
        link.class = 'brave_css'
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = "https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/style-vis.css";
        document.getElementsByTagName("head")[0].appendChild(link);
    }
    requirejs.config(
        {

            'paths': {
                'jquery': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/lib/jquery.min',
                'svg': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/lib/jquery.svg.min',
                'svgdom': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/lib/jquery.svgdom.min',
                'brat_config': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/configuration',
                'brat_utils': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/util',
                'brat_annotation': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/annotation_log',
                'brat_webfont': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/lib/webfont',
                'brat_dispatcher': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/dispatcher',
                'brat_monitor': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/url_monitor',
                'brat_visualizer': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/visualizer'

            }})
    if(!window.Util){
        requirejs(['svg', 'svgdom', 'brat_config', 'brat_annotation', 'brat_webfont', 'brat_dispatcher', 'brat_monitor', 'brat_visualizer', 'brat_utils'])
    }        
    </script>
    """


def get_embedded_html(coll_data, doc_data):
    return """
    <div id="embed_area_{rand}"></div>
    <script type='text/javascript'>
    var bratLocation = 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog';
    var webFontURLs = [
            bratLocation + '/static/fonts/Astloch-Bold.ttf',
            bratLocation + '/static/fonts/PT_Sans-Caption-Web-Regular.ttf',
            bratLocation + '/static/fonts/Liberation_Sans-Regular.ttf'
        ];
    var collData = {collData};
    var docData = {docData};   
    Util.embed( 'embed_area_{rand}',collData, docData, webFontURLs);
    </script>
    """.format(collData=coll_data, docData=doc_data, rand=getrandbits(64))
