import os
from gnutools.utils import name, parent

class CyMake:
    def __init__(self, root, setup, version="1.0a28"):
        self.root=root
        self.setup=setup
        self.lib_name = name(root)
        self.curdir = parent(os.path.realpath(__file__))
        self.version=version
        self.exe = os.path.sys.executable
        os.environ["VERSION"] = self.version
        self.clean()

    def clean(self):
        # Clean
        os.system("rm -r build")
        os.system("rm -r dist")
        os.system("rm -r {lib_name}*".format(lib_name=self.lib_name))


    def make(self, submodule="core"):
        self._compile(submodule)
        self._build_wheel()
        self._copy_init()
        self._clean_wheel()
        self.clean()


    def _compile(self, submodule):
        os.environ["PACKAGE"] = "{lib_name}_{submodule}".format(lib_name=self.lib_name, submodule=submodule)
        os.environ["PACKAGE_VERSION"] = os.environ["PACKAGE"] + "-" + os.environ["VERSION"]
        os.environ["WHL_NAME"] = os.environ["PACKAGE_VERSION"] + "-py3-none-any.whl"
        os.environ["WHL_NAME_NEW"] = os.environ["PACKAGE_VERSION"] + "-py36-none-any.whl"

        os.system("mkdir {PACKAGE}".format(PACKAGE= os.environ["PACKAGE"]))
        os.system("mkdir {PACKAGE}/iyo".format(PACKAGE= os.environ["PACKAGE"]))
        os.system("cp -r {root}/{PACKAGE_NAME} {PACKAGE}/iyo".format(root=self.root,
                                                                     PACKAGE_NAME=submodule,
                                                                     PACKAGE=os.environ["PACKAGE"]))


        compile ="{curdir}/compile.py".format(curdir=self.curdir)
        os.system("{exe} {compile} build_ext --build-lib {PACKAGE_VERSION}".format(exe=self.exe,
                                                                                   compile=compile,
                                                                                   PACKAGE_VERSION=os.environ["PACKAGE_VERSION"]))
        os.system("mv {PACKAGE_VERSION}/{PACKAGE}/iyo {PACKAGE_VERSION}".format(PACKAGE_VERSION=os.environ["PACKAGE_VERSION"],
                                                                                PACKAGE=os.environ["PACKAGE"]))
        os.system("rm -r {PACKAGE_VERSION}/{PACKAGE}".format(PACKAGE_VERSION=os.environ["PACKAGE_VERSION"],
                                                             PACKAGE=os.environ["PACKAGE"]))

    def _build_wheel(self):
        os.system("{exe} {setup} bdist_wheel --python-tag py35".format(exe=self.exe,
                                                                       setup=self.setup))
        os.system("mv dist/*.whl {WHL_NAME_NEW}".format(WHL_NAME_NEW=os.environ["WHL_NAME_NEW"]))
        os.system("rm -r dist")

    def _copy_init(self):
        copy_init ="{curdir}/copy_init.py".format(curdir=self.curdir)
        os.system("{exe} {copy_init} {PACKAGE} {PACKAGE_VERSION}".format(exe=self.exe,
                                                                         copy_init=copy_init,
                                                                         PACKAGE=os.environ["PACKAGE"],
                                                                         PACKAGE_VERSION=os.environ["PACKAGE_VERSION"]))
    def _clean_wheel(self):
        os.system("zip --delete {WHL_NAME_NEW} '{PACKAGE}/*'".format(PACKAGE=os.environ["PACKAGE"],
                                                                     WHL_NAME_NEW=os.environ["WHL_NAME_NEW"]))
        os.system("mv {PACKAGE_VERSION}/iyo ./".format(PACKAGE_VERSION=os.environ["PACKAGE_VERSION"]))
        os.system("rm -r {PACKAGE_VERSION}".format(PACKAGE_VERSION=os.environ["PACKAGE_VERSION"]))
        os.system("zip -ur {WHL_NAME_NEW} iyo".format(WHL_NAME_NEW=os.environ["WHL_NAME_NEW"]))
        os.system("mkdir wheels")
        os.system("mv {WHL_NAME_NEW} wheels".format(WHL_NAME_NEW=os.environ["WHL_NAME_NEW"]))