from setuptools import setup

setup(
    name='supernova-keyring-helper',
    version='0.4',
    description=('Store all required information for a Rackspace '
                 'Cloud environment in supernova-keyring.'),
    author='Carl George',
    author_email='carl@carlgeorge.us',
    url='https://github.com/cgtx/supernova-keyring-helper',
    packages=['supernova_keyring_helper'],
    install_requires=['supernova', 'rackspace-novaclient'],
    entry_points={
        'console_scripts': [
            'supernova-keyring-helper = supernova_keyring_helper.shell:main'
        ]
    }
)

# vim: set syntax=python sw=4 ts=4 expandtab :
