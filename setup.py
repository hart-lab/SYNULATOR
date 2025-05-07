from setuptools import setup, find_packages
 
from synulator.utils.version import __version__
 

setup(name='SYNULATOR', version=__version__,
      author='Juihsuan Chou, Traver Hart',
      author_email='',
      description='Synulator: simulation for synthetic lethality',
      license='MIT', packages=find_packages(),
      entry_points={'console_scripts': ['synulator = synulator.cli:__main__']},
      install_requires=['numpy==2.0.2', 'pandas==2.2.3', 'scipy==1.13.1'])
