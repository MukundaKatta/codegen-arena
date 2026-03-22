from setuptools import setup, find_packages

setup(
    name="codegen-arena",
    version="0.1.0",
    description="Benchmark and compare AI code generation tools side by side",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mukunda Katta",
    author_email="mukunda.vjcs6@gmail.com",
    url="https://github.com/MukundaKatta/codegen-arena",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
    ],
)
