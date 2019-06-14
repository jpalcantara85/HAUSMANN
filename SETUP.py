from setuptools import setup

setup(
    name = 'HAUSMANN',
    
    url = 'https://github.com/jpalcantara85',
    
    author = 'João Alcántara',
    
    author_email = 'joao_alcantara@student.hks.harvard.edu',
    
    packages = ['HAUSMANN'],

    install_requires = ['numpy'],
   
    version = '1.0',
    
    license = 'MIT',
    
    description='An example of a python package from pre-existing code',
  
    long_description = open('README.txt').read(),
)