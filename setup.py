
from setuptools import setup

setup(
    name='django-classy-settings',
    version='2.0.1',
    description='Simple class-based settings for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    packages=[
        'cbs',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'Django',
    ],
    test_suite='tests',
)
