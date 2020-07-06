from setuptools import setup, find_packages

setup(
    name="photoworkshop_postprocess",
    author="Julien Esseiva",
    description="Find a filename in image files in the input directory.",
    version="0.1",
    packages=find_packages(),
    scripts=["bin/photoworkshop_postprocess"],
    install_requires=[
        "pytesseract>=0.3.4"
    ]
)
