# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
Redpen validator for Sphinx
'''

requires = ['Sphinx>=1.0', 'setuptools']

setup(
    name='sphinxcontrib_redpen',
    version='0.0.1',
    url='http://github.com/shirou/sphinxcontrib-redpen',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-redpen',
    license='Apache',
    author='WAKAYAMA Shirou',
    author_email='shirou.faw@gmail.com',
    description='Redpen validator for Sphinx',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
