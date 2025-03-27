from setuptools import setup, find_packages

setup(
    name="Meine",  # Change to your package name
    version="0.1.0",
    packages=find_packages(),  # Automatically finds "Meine" and subpackages
    include_package_data=True,
    package_data={"Meine": ["*.json", "resources/*.json", "tcss/*.css"]},  # Include extra files
    install_requires=[],  # Add dependencies if needed (e.g., ['click', 'rich'])
    entry_points={
        "console_scripts": [
            "meine-cli=Meine.app:run",  # Creates `meine-cli` command
        ],
    },
    author="Balaji",
    author_email="j.balaji2468@gmail.com",
    description="Meine is a file management and system utilities tool for terminal",
    url="https://github.com/Balaji01-4D/MeineRE",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
