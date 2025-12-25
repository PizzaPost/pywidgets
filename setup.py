from setuptools import setup, find_packages

setup(
    name="easypygamewidgets",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "requests"
    ],
    author="PizzaPost",
    description="Create GUIs for pygame.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PizzaPost/pywidgets ",
)