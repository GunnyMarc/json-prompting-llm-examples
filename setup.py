"""Setup configuration for json-prompting-llm-examples package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="json-prompting-llm-examples",
    version="1.0.0",
    author="GunnyMarc",
    description="Comprehensive examples and research on JSON prompting techniques for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GunnyMarc/json-prompting-llm-examples",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="llm, json, prompting, openai, anthropic, gpt, claude, ai, machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/GunnyMarc/json-prompting-llm-examples/issues",
        "Source": "https://github.com/GunnyMarc/json-prompting-llm-examples",
    },
)
