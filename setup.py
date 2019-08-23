import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stuboto",
    version="0.3",
    author="Jordan Sanders",
    author_email="jordan@jordansanders.com",
    description="Stub boto3 clients to avoid hitting real AWS endpoints in tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmsanders/stuboto",
    py_modules = ["stuboto"],
    install_requires=["boto3>=1.9.213"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
