import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="healthpy",
    version=open("healthpy/version.py").readlines()[-1].split()[-1].strip("\"'"),
    author="Colin Bounouar",
    author_email="colin.bounouar.dev@gmail.com",
    maintainer="Colin Bounouar",
    maintainer_email="colin.bounouar.dev@gmail.com",
    url="https://colin-b.github.io/healthpy/",
    description="Health Check for HTTP APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://pypi.org/project/healthpy/",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords=["health", "api", "http", "redis"],
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    extras_require={
        "testing": [
            # Used to mock requests HTTP responses
            "pytest-responses==0.4.*",
            # Used to mock httpx HTTP responses
            "pytest-httpx==0.8.*",
            # Used to check redis health
            "redis==3.*",
            # Used to check starlette endpoint
            "starlette==0.13.*",
            # Used to check flask-restx endpoint
            "flask-restx==0.2.*",
            # Used to check coverage
            "pytest-cov==2.*",
        ]
    },
    python_requires=">=3.7",
    project_urls={
        "GitHub": "https://github.com/Colin-b/healthpy",
        "Changelog": "https://github.com/Colin-b/healthpy/blob/master/CHANGELOG.md",
        "Issues": "https://github.com/Colin-b/healthpy/issues",
    },
    platforms=["Windows", "Linux"],
)
