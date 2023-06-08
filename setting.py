from setuptools import setup, find_packages
from package import Package

from setuptools import setup, find_packages
from package import Package


setup(
    name="moov-web",
    author="codeandscale.com",
    author_email="hi@codeandscale.com",
    version="1.0",
    packages=find_packages(),
    description="moov web",
    install_requires=[
        "black ==22.1.0",
        "beautifulsoup4 ==4.10.0",
        "build ==0.7.0",
        "click ==8.0.4",
        "ipython ==7.8.0",
        "markdown2 ==2.4.2",
        "flask ==2.0.2",
        "Flask-WTF ==1.0.0",
        "gunicorn ==20.1.0",
        "requests ==2.26.0",
        "WTForms ==2.3.1",
        "openpyxl ==3.0.9",
        "pandas ==1.4.1",
        "PyMySQL >=1.0.2",
        "rich >=10.14.0",
        "cryptography >=36.0.0",
        "tqdm >=4.62.3",
        "pydantic >=1.8.2",
        "peewee >=3.14.8",
        "requests",
        "requests-html",
        "captcha==0.4",
        "APScheduler==3.9.1"
    ],
    entry_points={
        "console_scripts": ["moov = moov.api.cli:cmd"],
    },
    include_package_data=True,
    cmdclass={"package": Package},
)
