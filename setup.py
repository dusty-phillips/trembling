from setuptools import setup, find_packages

setup(name='trembling',
    version='0.1.0',
    author="Dusty Phillips",
    author_email="dusty@buchuki.com",
    packages=find_packages('.'),
    long_description=open("README.md").read(),
    package_dir={'trembling': 'trembling'},
)

