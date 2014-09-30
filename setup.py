from setuptools import setup, find_packages
import os

name = 'seantis.placemap'

description = (
    "Shows placemarks from multiple maps in one map, "
    "by combining kml-documents from other different urls."
)

version = '0.1'

tests_require = [
    'plone.app.testing',
    'collective.betterbrowser[pyquery]',
    'seantis.plonetools[tests]',
    'mock'
]


def get_long_description():
    readme = open('README.rst').read()
    history = open(os.path.join('docs', 'HISTORY.rst')).read()
    contributors = open(os.path.join('docs', 'CONTRIBUTORS.rst')).read()

    # cut the part before the description to avoid repetition on pypi
    readme = readme[readme.index(description) + len(description):]

    return '\n'.join((readme, contributors, history))


setup(
    name=name, version=version, description=description,
    long_description=get_long_description(),
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='plone seantis map government municipality kml',
    author='Seantis GmbH',
    author_email='info@seantis.ch',
    url='https://github.com/seantis/seantis.placemap',
    license='GPL v2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['seantis'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone>=4.3',
        'plone.api',
        'five.grok',
        'plone.app.dexterity [grok]',
        'collective.geo.openlayers',
        'fastmkl',
        'seantis.plonetools'
    ],
    extras_require=dict(
        tests=tests_require
    ),
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """
)
