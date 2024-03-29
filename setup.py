import setuptools
import os
from gnutools.utils import parent, listfiles
import numpy as np
import pathlib


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

def get_requirements(txt_file):
    """
    Get the list of requirements for setup_requires in setup.py

    :param txt_file:
    :return list:
    """
    def is_req(req):
        return (not (req[0]=="#")) if len(req)>0 else False
    lines = [line.split("\n")[0] for line in open(txt_file,"r").readlines()]
    return [line for line in lines if is_req(line)]

def get_packages(root):
    """
    Get the list of packages availables in a root

    :param root: package root
    :return list:
    """
    root = os.path.realpath(root)
    proot = parent(root) + "/"
    py_files = [file.rsplit(proot)[1] for file in listfiles(root, patterns=[".py"]) if ((os.stat(file).st_size > 0) &
                                                                                        (not file.__contains__(
                                                                                            ".pyc")))]
    packages = list(np.unique([parent(file).replace("/", ".") for file in py_files]))
    # return list(np.unique([parent(file).replace("/", ".").split(".{name_root}.".format(name_root=name(root)))[1]
    #                        for file in py_files]))
    return packages


setuptools.setup(
    name="cywheel",
    version="1.0a5",
    author="Jean Maximilien Cadic",
    author_email="j.cadic@9dw-lab.com",
    description="Easy packaging for cython wheels.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JeanMaximilienCadic/cywheel-python",
    python_requires='>=3.5',
    install_requires=get_requirements("requirements.txt"),
    packages=["cywheel"],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
