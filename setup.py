from setuptools import setup, find_packages

setup(
    name="jsonresume-to-rendercv",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jsonschema",
        "requests",
        "pyyaml"
    ],
    extras_require={
        "dev": [
            "pytest",
            "twine"
        ]
    },
    entry_points={
        "console_scripts": [
            "jsonresume_to_rendercv=jsonresume_to_rendercv.converter:main",
        ],
    },
    package_data={
        '': ['*.json', '*.yaml'],
    },
    include_package_data=True,
    author="Govind Singh",
    author_email="connect.govinds@gmail.com",
    description="A CLI tool to convert JSON Resume schema to RenderCV schema",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guruor/jsonresume-to-rendercv",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
