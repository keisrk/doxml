from setuptools import setup
import doxml

setup(name='doxml',
      version=doxml.__version__,
      install_requires=[
          'docutils>=0.11',
          'sphinx>=1.4.0'
      ],
      packages=['doxml']
     )
