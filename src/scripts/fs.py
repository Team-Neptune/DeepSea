from distutils.dir_util import copy_tree
from pathlib import Path
import shutil
import uuid
import json
import os
import re
import zipfile
from os.path import normpath, basename

class FS():
    def __init__(self):
        self.workdir = Path.cwd().joinpath('tmp', str(uuid.uuid4()))
        Path(Path.joinpath(self.workdir)).mkdir(parents=True, exist_ok=True)

    def createDirs(self, path, override=True):
        newdir = Path(Path.joinpath(self.workdir, path))
        if override:
            newdir.mkdir(parents=True, exist_ok=True)
        return newdir

    def doesFolderExist(self, workspace, path):
        if not workspace: workspace = Path.cwd()
        else: workspace = self.workdir
        return Path(Path.joinpath(workspace, path)).is_dir()
    
    def doesFilesExist(self, workspace, path):
        if not workspace: workspace = Path.cwd()
        else: workspace = self.workdir
        return Path(Path.joinpath(workspace, path)).exists()
    
    def getJson(self, workspace, path):
        if not workspace: workspace = Path.cwd()
        else: workspace = self.workdir
        return json.loads(open(Path.joinpath(workspace,path)).read())

    ################### THIS IS WHAT SHOULD BE USED FOR MODULES ###################

    def delete(self, modulename, source):
        path = Path(Path.joinpath(self.workdir, modulename, source))
        if not path.is_dir():
            if os.path.exists(path):
                os.remove(path)
        else:
            shutil.rmtree(path, ignore_errors=True)
    
    def copy(self, modulename, source, dest, regex=False):

        if regex == False:
            spath = Path(Path.joinpath(self.workdir, modulename, source))
            dpath = Path(Path.joinpath(self.workdir, modulename, dest))
            if spath.is_dir():
                print(dpath.is_dir())
                copy_tree(str(spath), str(dpath))
            else:
                shutil.copyfile(str(spath), str(dpath))
        else:
            path = Path(Path.joinpath(self.workdir, modulename))
            for filename in os.listdir(path):
                if re.search(regex, filename):
                    assetPath = Path(Path.joinpath(path, filename))
                    dpath = Path(Path.joinpath(self.workdir, modulename, dest))
                    shutil.copyfile(str(assetPath), str(dpath))

    def move(self, modulename, source, dest):
        self.copy(modulename, source, dest)
        self.delete(modulename, source)

    def createDir(self, modulename, source):
        Path(Path.joinpath(self.workdir, modulename, source)).mkdir(parents=True, exist_ok=True)

    def extract(self, modulename, source):
        path = Path(Path.joinpath(self.workdir, modulename))
        for filename in os.listdir(path):
            if re.search(source, filename):
                assetPath = Path(Path.joinpath(path, filename))

                with zipfile.ZipFile(assetPath, 'r') as zip_ref:
                    zip_ref.extractall(path)

                self.delete(modulename, assetPath)
                break
    
    def replaceText(self, modulename, source, target, replacement):
        path = Path(Path.joinpath(self.workdir, modulename, source))
        fin = open(path, "rt")
        data = fin.read()
        data = data.replace(target, replacement)
        fin.close()
        fin = open(path, "wt")
        fin.write(data)
        fin.close()

    def createToolboxJson(self, modulename, source, requires_reboot):
        path = Path(Path.joinpath(self.workdir, modulename, source, "toolbox.json"))
        tid = basename(normpath(source))
        data = {
            "name"  : modulename,
            "tid"   : tid,
            "requires_reboot": requires_reboot
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)