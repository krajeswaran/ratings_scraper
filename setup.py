from setuptools import find_packages
from setuptools import setup

author = maintainer = "Kumaresan Rajeswaran"
author_email = maintainer_email = "kumaresan.rajeswaran@gmail.com"
license = 'gplv3'

setup_args = {
    'name': 'scraper',
    'version': '0.0.1',
    'author': author,
    'author_email': author_email,
    'maintainer': maintainer,
    'maintainer_email': maintainer_email,
    'url': 'https://github.com/krajeswaran/ratings_scraper',
    'packages': find_packages(),
    'include_package_data': True,
    'license': license,
    'zip_safe': False,
    'package_data': {"": ['*.*']},
    'install_requires': [
        'certifi==2017.11.5',
        'chardet==3.0.4',
        'html5lib==0.999999999',
        'idna==2.6',
        'microdata==0.6.1',
        'requests>=2.20.0',
        'six==1.11.0',
        'urllib3>=1.23',
        'webencodings==0.5.1',
        ],
}

# setup
setup(**setup_args)
