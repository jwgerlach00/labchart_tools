
from setuptools import setup, find_packages


setup(
    name='labchart_tools',
    version='0.0.3',
    license='MIT',
    author='Jacob Gerlach',
    author_email='jwgerlach00@gmail.com',
    url='https://github.com/jwgerlach00/labchart_tools',
    description='Package for processing data exported as txt files from ADInstruments LabChart',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=[
        'plotly',
    ],
)