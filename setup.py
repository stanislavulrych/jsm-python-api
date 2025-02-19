import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsm-python-api",
    version="0.1",
    author="Stanislav Ulrych",
    author_email="stanislav.ulrych@gmail.com",
    description="Python bindings for Jira Service Management API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stanislavulrych/jsm-python-api",
    packages=setuptools.find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/stanislavulrych/jsm-python-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.11',
)
