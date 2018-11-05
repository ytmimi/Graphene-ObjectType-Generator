import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="Graphene-ObjectType-Generator",
    version="0.0.1",
    author="Yacin Tmimi",
    author_email="yacintmimi@gmail.com",
    description="Quickly generate Graphene ObjectType definitions from dictionaries, lists, or JSON strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytmimi/Graphene-ObjectType-Generator",
    packages=setuptools.find_packages(exclude=['test']),
    install_requires=['jinja2>=2.10'],
    extras_require={
        'dev': ['coverage', 'pytest'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
