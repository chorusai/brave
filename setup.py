import os

from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='brave',

    version='0.1.0',

    description='Brave: Brat rapid annotation visualization enabler',
    long_description=long_description,

    url='https://github.com/chorusai/brave',

    author='chorus research',

    license='Apache Software License',

    classifiers=[

        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='visualization tool for NLP tasks',
    packages=find_packages(exclude=[]),
    install_requires=['future'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    data_files=
    [
        ('templates', [os.path.join('templates', fn) for fn in os.listdir(os.path.join(here, 'templates'))]),
    ]
    ,

    entry_points={
        'console_scripts': [
        ],
    },
)
