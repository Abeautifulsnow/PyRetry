import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyretry",
    version="0.0.1",
    author="runstone",
    author_email="lnrunstone.0727@gmail.com",
    description="A nice decorator tool for retrying tasks when they failed.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abeautifulsnow/PyRetry",
    project_urls={
        "Bug Tracker": "https://github.com/Abeautifulsnow/PyRetry/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
