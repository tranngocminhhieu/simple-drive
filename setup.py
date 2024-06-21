from pathlib import Path
from setuptools import setup

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name='simple-drive',
    version='2.0.0',
    description='Use Google Drive API in the simplest way',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/tranngocminhhieu/simple-drive',
    author='Tran Ngoc Minh Hieu',
    author_email='tnmhieu@gmail.com',
    packages=['simple_drive'],
    install_requires=[
        'colorama',
        'pydrive2',
        'google-api-python-client',
        'oauth2client',
    ]
)