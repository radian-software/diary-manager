from setuptools import setup

# https://python-packaging.readthedocs.io/en/latest/minimal.html
setup(
    author="Radian LLC",
    author_email="contact+diary-manager@radian.codes",
    description="If you want your diary on the command line.",
    license="MIT",
    install_requires=["python-dateutil"],
    name="diary-manager",
    scripts=["diary"],
    url="https://github.com/radian-software/diary-manager",
    version="2.0.2",
    zip_safe=True,
)
