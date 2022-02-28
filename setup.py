from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="my_package",
    version="0.0.1",
    author="Nikhil Saraswat",
    author_email="nikhilsaraswat@kgpian.iitkgp.ac.in",
    description="This package is for my assignment-3 (Python- Data Science) of Software Engineering",
    long_description=long_description,
    long_description_content_type="markdown",
    packages=['my_package', 'my_package.analysis',
              'my_package.data', 'my_package.data.transforms'],
    install_requires=['matplotlib', 'torch',
                      'numpy', 'torchvision', 'opencv-python', 'tk']
)
