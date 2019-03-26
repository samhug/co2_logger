import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='co2_logger',
    version='0.1.0',
    author='Sam Hug',
    author_email='s@m-h.ug',
    description='CO2 Google Sheets logger',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'co2_logger = co2_logger.__main__:main',
        ],
    },
)
