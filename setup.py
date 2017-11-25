from setuptools import setup

# https://python-packaging.readthedocs.io/en/latest/minimal.html
setup(
    author="Radon Rosborough",
    author_email="radon.neon@gmail.com",
    description="If you want your diary on the command line.",
    license="MIT",
    install_requires=["dateutils"],
    name="diary_manager",
    scripts=["diary"],
    url="https://github.com/raxod502/diary-manager",
    version="1.0",
    zip_safe=True,
)
