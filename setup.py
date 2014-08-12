
from distutils.core import setup

setup(
    name='django-classy-settings',
    version='1.0.0',
    description='Simple class-based settings for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    packages=['cbs',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
    ],
    requires=[
        'Django (>=1.6)',
        'six (>=1.7.3)',
    ],
)
