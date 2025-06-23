from setuptools import setup, find_packages

setup(
    name="lighting_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-adk>=0.5.0",
        "google-generativeai",
        "python-dotenv",
        "google-cloud-aiplatform",
        "requests",
        "pydantic",
    ],
    python_requires=">=3.8",
)