# setup.py
from setuptools import setup
setup(
    name="momnetit",
    version="1.0.0",
    py_modules=["momnetit"],
    entry_points={"console_scripts": ["momnetit=momnetit:main"]},
    author="WinterGate Intelligence Collective",
    description="THE MOMNE TIT - Connection Killer. One look is all you get.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WinterGate-IC/MomneTit",
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License"],
    python_requires=">=3.8",
)
