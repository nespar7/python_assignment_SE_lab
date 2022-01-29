from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name = 'package',
    version= '1.0.0',
    author= 'N Surya Prakash Reddy',
    author_email= 'nsuryaprakashreddy1234@gmail.com',
    description='package for image segmentation assignment',
    packages=['my_package', 'my_package.data', 'my_package.data.transforms', 'my_package.analysis']    
)
