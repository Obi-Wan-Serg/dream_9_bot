from importlib.metadata import entry_points
from setuptools import setup, find_namespace_packages

setup(name='dream_9_bot',
      version='1.0.0',
      description='Personal Address book - dream_9_bot',
      url='https://github.com/Obi-Wan-Serg/dream_9_bot',
      author='dream_9_bot team',
      packages=find_namespace_packages(),
      install_requires=[
          'rich>=13.7.0',
          'setuptools>=69.0.2',
          'requests>=2.31.0'],
      entry_points={'console_scripts': [
          'dream_9_bot = dream_9_bot.__main__:main']}
      )
