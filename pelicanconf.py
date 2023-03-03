import sys
import os

sys.path.append('.')
from console import *

import os
from pelican import signals


def get_subfolders(path, root):
    subfolders = {}
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if os.path.join(root, dir) != root:
                subfolder = os.path.relpath(os.path.join(root, dir), root)
                subfolders[subfolder] = os.listdir(
                    os.path.join(root, subfolder))
    return dict(sorted(subfolders.items()))


JINJA_GLOBALS = {}
JINJA_GLOBALS['subfolders'] = get_subfolders('content', '.')
print(JINJA_GLOBALS['subfolders'])

AUTHOR = 'Arunabh Sharma'
SITENAME = 'Advanced C++'
SITEURL = 'https://arunabhcode.github.io/advanced_cpp_by_example/'

PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = 'themes/Papyrus'
THEME_STATIC_PATHS = ['static']
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['readtime', 'search', 'neighbors', 'pelican-toc']

DISPLAY_PAGES_ON_MENU = True
ARTICLE_ORDER_BY = 'date'

# Site search plugin
SEARCH_MODE = "output"
SEARCH_HTML_SELECTOR = "main"
# Table of Content Plugin
TOC = {
    'TOC_HEADERS': '^h[1-3]',  # What headers should be included in
    # the generated toc
    # Expected format is a regular expression
    'TOC_RUN': 'true',  # Default value for toc generation,
    # if it does not evaluate
    # to 'true' no toc will be generated
    'TOC_INCLUDE_TITLE': 'false',  # If 'true' include title in toc
}

# Tell Pelican to use templates from the 'templates' folder before using the default theme templates
# THEME_TEMPLATES_OVERRIDES = ['templates']

DIRECT_TEMPLATES = ['index', 'search']

JINJA_FILTERS = {'console': console_filter}

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'use_pygments': True,
            'linenums': True,
        },
    },
    'output_format': 'html5'
}

# Blogroll
LINKS = (
    ('Pelican', 'https://getpelican.com/'),
    ('Python.org', 'https://www.python.org/'),
    ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
    ('You can modify those links in your config file', '#'),
)

# Social widget
SOCIAL = (
    ('You can add links in your config file', '#'),
    ('Another social link', '#'),
)

DEFAULT_PAGINATION = False
DISPLAY_PAGES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = True
USE_FOLDER_AS_CATEGORY = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True