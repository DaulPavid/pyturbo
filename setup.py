#
# Python package script
#

from setuptools import setup


install_requires = []
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()


setup(
    name="pyturbo",
    version="0.10",
    author="daulpavid",
    url="https://github.com/daulpavid/pyturbo",
    license="MIT",
    description="A simple implementation of a turbo encoder and decoder",
    packages=["turbo"],
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'
    ]
)