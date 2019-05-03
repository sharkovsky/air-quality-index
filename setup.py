# Always prefer setuptools over distutils
from setuptools import setup, find_packages

VERSION = '1.0.0'

pkg_meta = dict(
    name='airqualityindex',
    version=VERSION,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.4, <4',
    install_requires=['requests'],
    tests_require=['pytest', 'pytest-mock', 'requests-mock']
)

if __name__ == '__main__':
    setup(**pkg_meta)
