from setuptools import setup, find_packages

setup(
    name='coin_infra',
    version='0.5',
    description='infrastration of coin project',
    author='Yi Te',
    author_email='coastq22889@icloud.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'websockets',
        'websocket-client'
    ],
)