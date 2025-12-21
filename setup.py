from setuptools import setup, find_packages

setup(
    name="pywidgets",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    author="PizzaPost",
    description="Create GUIs for pygame.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://dein-repository.com",
)