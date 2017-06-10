# encoding=utf8
# author=spenly
# mail=i@spenly.com


from setuptools import setup

setup(
    name = "idocker",
    version = "0.1",
    packages = ["idocker"],
    scripts = ['bin/idocker'],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    setup_requires = [],
    install_requires = [],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
    },
    # metadata for upload to PyPI
    author = "spenly",
    author_email = "i@spenly.com",
    description = "docker helper, make docker more simple.",
    license = "PSF",
    keywords = "docker idocker",
    url = "https://github.com/spenly/idocker",
    # could also include long_description, download_url, classifiers, etc.
    entry_points={'console_scripts': [
        'idocker = idocker.idocker:main',
    ]},
)

