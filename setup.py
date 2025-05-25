from setuptools import setup, find_packages

setup(
    name="distill-cli",
    version="0.1.0",
    description="Compress CLI output for LLM consumption",
    author="Karan Singh",
    author_email="karansingh25822@gmail.com",
    py_modules=["cli"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "distill=cli:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)