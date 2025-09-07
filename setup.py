from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="soccerviz",
    version='..-snapshot',  # quote simple !!!
    packages=find_packages(),
    package_data={
        "soccerviz.sql": ["**/*.sql"],
    },
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "soccerviz = soccerviz.main:main",
        ],
    },
)
