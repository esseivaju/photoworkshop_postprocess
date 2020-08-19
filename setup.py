from setuptools import setup, find_packages

setup(
    name="photoworkshop_postprocess",
    author="Julien Esseiva",
    description="Find a filename in image files in the input directory and rename each image file with the filename found",
    version="0.1.1",
    packages=find_packages(),
    scripts=["bin/photoworkshop_postprocess"],
    install_requires=[
        "pytesseract>=0.3.4",
        "pyzbar>=0.1.8",
        "Pillow>=7.2.0"
    ]
)
