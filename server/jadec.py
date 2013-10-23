from os import listdir
from os.path import isfile, join
from pyjade.ext.django import Compiler
from pyjade.utils import process

def init(path):
    files = [ f for f in listdir(path) ]
    for f in files:
        if isfile(join(path,f)):
            if f.endswith(".jade"): compile(join(path, f))
            
        else:
            init(join(path,f))
    return True

def compile(path):
    template = open(path, 'r').read()
    output = process(template, compiler=Compiler)
    newpath = path.replace("jade", "html")
    f = open(newpath, "w")
    f.write(output)
    f.close()
    print "%s -> %s" % (path, newpath)


if "__main__"==__name__:
    jades = init("./")
