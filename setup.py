from setuptools import find_packages
from setuptools import setup

author = maintainer = "Kumaresan Rajeswaran"
author_email = maintainer_email = "kumaresan.rajeswaran@gmail.com"
license = 'gplv3'

setup_args = {
    'name': 'mkvcage',
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
        'scrapy==1.5.0',
        ],
}

# setup
setup(**setup_args)
