from distutils.core import setup
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from gnutools.utils import listfiles, parent
import argparse
import os

from gnutools.utils import listfiles, parent, name, ext
import numpy as np
import os

def ext_modules(root, remove_c=True, filter_key=""):
    """
    Clean up the modules by removing undesired extensions default is ["c", "o", "pyc", "pyx"]
    Return a list if extension to use in setup.py

    :param root:
    :param remove_c: default True
    :return list:
    """
    from distutils.extension import Extension


    py_files = listfiles(root, patterns=[".py"], excludes=["/__init__.py", ".pyc"])
    modules_dict = {}
    proot = parent(root)
    for file in py_files:
        file = file.replace(proot, "")[1:]
        parent_modules = ".".join(parent(file).replace("/", ".").split(".")).replace("-", "_")
        key = "{parent_modules}.{leaf_module}".format(parent_modules=parent_modules,
                                                      leaf_module=name(file))
        if key.__contains__(filter_key):
            try:
                modules_dict[key].append(file)
            except:
                modules_dict[key] = [file]

    print(modules_dict)
    return [Extension(key, value) for key, value in list(modules_dict.items())]


def rename_prefixe_lib(root):
    """
    Rename automatically the generated .so files to be consistent.

    :param root:
    :return:
    """
    files = listfiles(root, patterns=[".so"])
    files = [(file, "{}/{}.so".format(parent(file), name(name(file)))) for file in files]
    for (file_before, file_after) in files:
        command = "mv {} {}".format(file_before, file_after)
        print(command)
        os.system(command)





def generate_rst(root, package):
    """
    Scan a package and generate automatically a rst string to save as a rst file for documentation.

    :param root: package root
    :param package: package or module to generate the rst file
    :return string:
    """
    root = os.path.realpath(root)
    package = os.path.realpath(package)
    proot = parent(root) + "/"

    modules = np.unique([file.replace(proot, "").replace("/", ".").replace("py", "")[:-1] for file in
                         listfiles(package, level=1, patterns=[".py"])])
    module_name = package.replace(proot, "").replace("/", ".").replace(".py", "")
    output = "{}\n==============================================================\n\n".format(module_name)
    for module in modules:
        splits = module.split("__init__")
        if len(splits)==2:
            path = "{}{}__init__.py".format(proot, splits[0].replace(".", "/"))
        else:
            path = "{}{}.py".format(proot, module.replace(".", "/"))
        with open(path, "r") as f:
            modules_dict = {}
            modules_dict[name(path)] = []
            members_class = {}
            functions = []
            lines = f.readlines()
            last = ""
            for line in lines:
                if ((line[:8] == "    def ") | (line[:6] == "class ")):
                    if line.__contains__("class "):
                        name_class = line.split("class ")[1].replace(":\n", "").split("(")[0].split("\n")[0]
                        modules_dict[name_class] = module
                        members_class[name_class] = []
                        last = "class"
                    else:
                        name_member_class = line.split("    def ")[1].split("(")[0]
                        if not name_member_class.__contains__("__"):
                            if last == "class":
                                members_class[name_class].append(name_member_class)
                                last = "class"
                elif line[:4] == "def ":
                    name_function = line.split("def ")[1].split("(")[0]
                    modules_dict[name_function] = module
                    functions.append(name_function)
                    last = "function"

            for name_class, class_value in members_class.items():
                output += ".. currentmodule:: {}\n\n".format(module_name)
                output += \
                    "{}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n" \
                    ".. autoclass:: {}\n" \
                    "    :members: {}\n" \
                    "    :special-members:\n\n".format(name_class, name_class, ", ".join(class_value))

            if len(functions) > 0:
                if not ext(module)=="__init__":
                    output += ".. currentmodule:: {}\n\n".format(module_name)
                    output += "{}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n".format(
                        ext(module))
                else:
                    output += ".. currentmodule:: {}\n\n".format(module_name)
                for function in functions:
                    output += \
                        ".. autofunction:: {}\n".format(function)
            output += "\n"
    print("{}\n============================================================================\n".format(output))
    return output




def append_file(filename, string):
    def __append(filename, string):
        open(filename, "a").write("{}\n".format(string))

    """

    :param filename:
    :param string:
    :return:
    """
    try:
        lines = open(filename, "r").read().split("\n")
        for line in lines:
            if line.__contains__(string):
                return
        __append(filename, string)
    except FileNotFoundError:
        __append(filename, string)

def copy_inits(py_package, in_pattern, out_pattern):
    """

    :param py_package:
    :param so_package:
    :return:
    """
    [os.remove(_f) for _f in listfiles(os.path.realpath(py_package), patterns=[".pyc"])]
    init_files_src = listfiles(py_package, patterns=["__init__.py"])
    init_files_dst = [parent(file)
                             .replace(in_pattern, out_pattern)
                             .replace("/{PACKAGE}/".format(PACKAGE=os.environ["PACKAGE"]),
                                      "/{PACKAGE}/".format(PACKAGE=os.environ["PACKAGE"].replace("-", "_")))
                      for file in init_files_src]
    commands = ["cp {} {}".format(src, dst) for src, dst in zip(init_files_src, init_files_dst)]
    [print(command) for command in commands]
    [os.system(command) for command in commands]


def copy_data(py_package, in_pattern, out_pattern):
    """

    :param py_package:
    :param so_package:
    :return:
    """
    data_files = listfiles(os.path.realpath(py_package), patterns=["__data__"])
    output_dirs = [parent(_f.replace(in_pattern, out_pattern)) for _f in data_files]
    [os.makedirs(_output_dir, exist_ok=True) for _output_dir in output_dirs]
    commands = ["cp {} {}".format(_f, _output_dir) for _f, _output_dir in zip(data_files, output_dirs)]
    [print(command) for command in commands]
    [os.system(command) for command in commands]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("build_ext", type=str, help="Build util")
    parser.add_argument("--build-lib", type=str, help="Build Directory")
    args = parser.parse_args()

    #Setup
    setup(
        name=os.environ["PACKAGE"],
        cmdclass = {'build_ext': build_ext},
        ext_modules=cythonize(module_list=ext_modules(os.path.realpath(os.environ["PACKAGE"]), filter_key=""),
                              nthreads=32)
    )

    rename_prefixe_lib(args.build_lib)
