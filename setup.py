
from distutils.core import setup

setup(
    name='django-classy-settings',
    version='1.0.3',
    description='Simple class-based settings for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    packages=['cbs',],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'Django>=1.6',
    ],
)
