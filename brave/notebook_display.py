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
    {loadStyles}
    if(!window.Util){{
        {requireJsConfig}
        requirejs(['svg', 'brat_config', 'brat_annotation', 'brat_webfont', 'brat_dispatcher', 'brat_monitor', 'brat_visualizer', 'brat_utils']);
    }}        
    """.format(loadStyles=_get_load_styles_js(), requireJsConfig=_get_require_js_config())


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
    {loadStyles}
    if(!window.Util){{ 
        {requireJsConfig}
        requirejs(['svg', 'brat_config', 'brat_annotation', 'brat_webfont', 'brat_dispatcher', 'brat_monitor', 'brat_visualizer', 'brat_utils'], 
            function(){{
             window.Util.embed( 'embed_area_{rand}',{collData}, {docData}, webFontURLs);
        }});
     }}
    else {{ window.Util.embed( 'embed_area_{rand}',{collData}, {docData}, webFontURLs); }}
    </script>
    """.format(collData=coll_data, docData=doc_data, rand=getrandbits(64), loadStyles=_get_load_styles_js(),
               requireJsConfig=_get_require_js_config())


def _get_load_styles_js():
    return """
    if(!$('.brave_css').size()){
        var link = document.createElement("link");
        link.class = 'brave_css';
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = "https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/style-vis.css";
        document.getElementsByTagName("head")[0].appendChild(link);
    }
    """


def _get_require_js_config():
    return """
        requirejs.config(
            {

                'paths': {
                    'svg': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/lib/jquery.svg.min',
                    'brat_config': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/configuration',
                    'brat_utils': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/util',
                    'brat_annotation': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/annotation_log',
                    'brat_webfont': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/lib/webfont',
                    'brat_dispatcher': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/dispatcher',
                    'brat_monitor': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/url_monitor',
                    'brat_visualizer': 'https://cdn.jsdelivr.net/gh/nlplab/brat@v1.3_Crunchy_Frog/client/src/visualizer'

                }});
    """
