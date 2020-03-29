# coding: utf-8
import os

from setuptools import find_packages, setup


# Include __about__.py.
__dir__ = os.path.dirname(__file__)
about = {}
with open(os.path.join(__dir__, 'baruda', '__about__.py')) as f:
    exec(f.read(), about)

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

# TODO: need a download url to go on pypi
# download_url='https://pypi.org/project/{baruda?}/'
setup(
    name='baruda',
    version=about['__version__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__maintainer_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    url='https://github.com/naubull2/baruda',
    download_url='https://pypi.org/project/baruda/',
    description='Fix and normalize Korean Jamo typos',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    platforms='any',
    packages=find_packages(),
    zip_safe=False,
    keywords=['Korean', 'Hangul', 'Jamo'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Korean',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'jamo>=0.4.1'
    ],
)
