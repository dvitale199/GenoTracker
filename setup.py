from setuptools import setup, find_packages

setup(
    name='GenoTracker',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "google-cloud-storage",
        "sqlalchemy",
        "urllib3",
        "pandas",
        "numpy",
        "streamlit",
        "google-api-core==2.19.1",
        "google-auth==2.30.0",
        "google-cloud-core==2.4.1",
        "google-cloud-storage==2.17.0",
        "requests"
    ],
)