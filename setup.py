import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    
    name = 'HAUSMANN',
    
    version = '1.0',
    
    author = 'João Alcántara',
    
    author_email = 'joao_alcantara@student.hks.harvard.edu',
    
    description = "GLQuery's public version",
    
    long_description = long_description,
    
    long_description_content_type = 'text/markdown',
    
    url = 'https://github.com/jpalcantara85/HAUSMANN',
    
    packages = setuptools.find_packages(),
   
    license = 'MIT',
  
)
