import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="healthpy",
    version=open("healthpy/version.py").readlines()[-1].split()[-1].strip("\"'"),
    description="API Health Checks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["test"]),
    install_requires=[
        # Used to ensure Black code style is checked on pre-commit
        "pre-commit==1.17.0"
    ],
    extras_require={
        "testing": [
            # Used to mock HTTP responses
            "responses==0.10.6",
            # Used to check redis health
            "redis==3.2.1",
        ]
    },
    python_requires=">=3.6",
    project_urls={
        "Changelog": "https://github.tools.digital.engie.com/GEM-Py/healthpy/blob/master/CHANGELOG.md",
        "Issues": "https://github.tools.digital.engie.com/GEM-Py/healthpy/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords=["health", "api"],
    platforms=["Windows", "Linux"],
)
