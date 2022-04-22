import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="dollarify-FredPerr",
    version="0.0.1",
    author="Frederic Perron",
    author_email="frederic.perr@gmail.com",
    description="A Complete Finance Overview in a single app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/FredPerr/Dollarify/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: UNLICENSED",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['dollarify'],
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Click',
        'flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'psycopg2',
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'run=dollarify.scripts.run:cli',
            'manage=dollarify.scripts.manage:cli',
        ]
    }
)