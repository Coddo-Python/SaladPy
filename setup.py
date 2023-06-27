from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='saladpy',
    author='Coddo-Python',
    url='https://github.com/Coddo-Python/SaladPy',
    project_urls={
        'Github': 'https://github.com/Coddo-Python/SaladPy',
        'Issue tracker': 'https://github.com/Coddo-Python/SaladPy/issues',
        'Docs': 'https://saladpy.gitbook.io/saladpy-docs/'
    },
    version="1.0.2-a.2",
    license='MIT',
    description='A Python wrapper for the Salad Web API',
    long_description=readme,
    packages=["saladpy", "saladpy.methods", "saladpy.methods.types"],
    install_requires=requirements,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)