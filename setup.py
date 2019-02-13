import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gym_maze",
    version="0.0.1",
    author="Jonáš Kulhánek",
    author_email="jonas.kulhanek@live.com",
    description="Simple gym maze environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jkulhanek/gym-maze-env",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)