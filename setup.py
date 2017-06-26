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
    install_requires=[
        'PyTomCrypt>=0.10.1'
    ],
    entry_points={
        'console_scripts': [
            'gossipd = gossipd.cmd.gossipd:main',
            'gossipc = gossipd.cmd.gossipc:main',
        ]
    }
)
