import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='BlackBlock',
    version='1.0.4',
    author='BlackHole-Consulting',
    author_email='',
    description='BLACKBLOCK IOT BLOCK, allow to manage BLACKBLOCK IOT devices with blockchain communications using the blockchain transactions as a communication mechanism to interactive and aployment devices and monitorize the events in the network, encrypted with ECC keys .',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    #packages=find_packages(exclude=['tests']),
    packages=['BlackBlock','BlackBlock/modules','BlackBlock/lib','BlackBlock/lib/contracts'],
    # trying to add files...
    include_package_data = True,
    package_data = {
        'BlackBlock': ['*']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='BlackBlock',
    python_requires='>=3.6.0',
    install_requires=[
        'configparser',
        'lxml',
        'elasticsearch==7.0',
        'pytz',
        'colorama',
        'requests',
        'libeospy',
        'prettytable',
        'eciespy',
        'rich',
        'flask',
        'flasgger'
    ],
    entry_points={
        'console_scripts': [
            'BlackBlock=BlackBlock.cli:cli'
        ],
    },
    project_urls={
        'Source': 'https://github.com/BlackHole-Consulting/BlackBlock',
    },
)
