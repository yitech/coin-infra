from setuptools import setup, find_packages

setup(
    name='coin_infra',
    version='0.1',
    description='infrastration of coin project',
    author='Yi Te',
    author_email='coastq22889@icloud.com',
    packages=find_packages(),
    install_requires=[
        # list packages your project relies on
        'numpy',
        'pandas',
        # etc.
    ],
)