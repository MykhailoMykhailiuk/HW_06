from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.0.1',
    description='This package will sort the files of a given folder by extension',
    url='',
    author='Mykhailo Mykhailiuk',
    entry_points={
        'console_scripts':['clean-folder=clean_folder.clean:main']
                  },
    packages=find_packages()


)