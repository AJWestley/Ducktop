from setuptools import setup, find_packages

setup(
    name="DuckTop",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow==9.2.0',
    ],
    package_data={
        "ducktop": ["assets/*.png"],
    },
    entry_points={
        "console_scripts": [
            "DuckTop = ducktop.app:main",
        ],
    },
)