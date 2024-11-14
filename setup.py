from setuptools import setup, find_packages

with open("requirements.txt", encoding="UTF8") as f:
    requirements = f.read().splitlines()

setup(
    name="KDOne",
    version="1.0.0",
    author="Soul Lee",
    author_email="alus20x@gmail.com",
    description="KDOne Navien Home Network API Wrapper",
    long_description=open("README.md", encoding="UTF8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/soulee-dev/KDOne",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
