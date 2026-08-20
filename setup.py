from setuptools import setup,find_packages
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path,'r') as file:
        lines = file.readlines()
        requirements=[line.replace('\n','')for line in lines]

    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

    

setup(
    name='mlproject',
    version='0.0.1',
    author='sahil',
    author_email='sahiljagtap9666@gmail.com',
    pacakages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)