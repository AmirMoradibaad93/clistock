from setuptools import setup

setup(
    name = 'clistock',
    version = '0.1.0',
    packages = ['clistock'],
    entry_points = {
        'console_scripts': [
            'clistock = clistock.__main__:main'
        ]
    })
