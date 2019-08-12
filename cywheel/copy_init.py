from gnutools.utils import listfiles
import argparse
import os

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument('dir_src')
   parser.add_argument('dir_dst')
   args = parser.parse_args()
   for file in listfiles(root=args.dir_src, patterns=["__init__.py"]):
       command="cp {file_src} {file_dst}".format(file_src=file, file_dst=file.replace("/" + args.dir_src, "/" + args.dir_dst))
       os.system(command)
       print(command)
