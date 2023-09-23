from setuptools import setup, find_packages

setup(
    name='general',
    version='2.2',
    description='infra of coin projects',
    author='Yi Te',
    author_email='coastq22889@icloud.com',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'redis',
        'requests',
        'websockets',
        'binance-futures-connector',
        'ccxt'
    ],
)