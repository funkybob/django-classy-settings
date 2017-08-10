
from setuptools import setup

setup(
    name='django-classy-settings',
    version='2.1.0',
    description='Simple class-based settings for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    packages=[
        'cbs',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'Django',
    ],
    test_suite='tests',
)
