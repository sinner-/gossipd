""" gossipd
"""

from setuptools import setup, find_packages

setup(
    name='gossipd',
    version='0.1',
    url='https://github.com/sinner-/gossipd',
    author='Sina Sadeghi',
    description='G',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gossipd = gossipd.cmd.cli:main',
        ]},
)
