from setuptools import setup


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="vpype-scribbletrace",
    version="0.1.0",
    description="",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Mike and Jason",
    url="",
    license=license,
    packages=["vpype_scribbletrace"],
    install_requires=[
        'click',
        'vpype',
    ],
    entry_points='''
            [vpype.plugins]
            scribbletrace=vpype_scribbletrace.scribbletrace:scribbletrace
        ''',
)
