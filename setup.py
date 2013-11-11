import setuptools

setuptools.setup(
    name='supernova-keyring-helper',
    version='0.4',
    description=('Store all required information for a Rackspace '
                 'Cloud environment in supernova-keyring.'),
    author='Carl George',
    author_email='carl@carlgeorge.us',
    url='https://github.com/cgtx/supernova-keyring-helper',
    license='Apache License, Version 2.0',
    py_modules=['supernova_keyring_helper'],
    install_requires=['supernova', 'rackspace-novaclient'],
    entry_points={
        'console_scripts': [
            'supernova-keyring-helper=supernova_keyring_helper:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux'
    ]
)

# vim: set syntax=python sw=4 ts=4 expandtab :
