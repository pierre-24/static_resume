# adapted over https://github.com/pypa/sampleproject/blob/master/setup.py

from setuptools import setup, find_packages
from os import path

import static_resume

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(path.join(here, 'requirements.in')) as f:
    requirements = f.readlines()

setup(
    name='static_resume',
    version=static_resume.__version__,

    # Description
    description=static_resume.__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',

    project_urls={
        'Bug Reports': 'https://github.com/pierre-24/static_resume/issues',
        'Source': 'https://github.com/pierre-24/static_resume',
    },

    url='https://github.com/pierre-24/static_resume',
    author=static_resume.__author__,

    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Specify the Python versions:
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=('*tests',)),
    python_requires='>=3.5',

    # requirements
    install_requires=requirements,
)
