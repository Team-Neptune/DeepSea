from modules.basemodule import Basemodule
from pathlib import Path
import os
import shutil


config = {
    "service": 1,
    "username": "WerWolv",
    "reponame": "EdiZon",
    "assetRegex": ".*EdiZon.*\\.nro",
    "assetPatterns": [".*EdiZon.*\\.nro", ".*ovlEdiZon.*\\.ovl"]
}

def createEdizonStructure(workpath, assetNames):
    Path(Path.joinpath(workpath, "switch", ".overlays")).mkdir(parents=True, exist_ok=True)
    Path(Path.joinpath(workpath, "switch", "edizon")).mkdir(parents=True, exist_ok=True)
    for i in assetNames:
        if i.endswith(".nro"):
            shutil.move(Path.joinpath(workpath, i), Path.joinpath(workpath, "switch", "edizon", i))
        if i.endswith(".ovl"):
            shutil.move(Path.joinpath(workpath, i), Path.joinpath(workpath, "switch", ".overlays", i))

class Edizon(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
    
    def handleModule(self):
        release = self.getLatestRelease()
        assetNames = self.downloadAssets(release)
        createEdizonStructure(self.workspaceFullPath, assetNames)
        self.copyFolderContentToPackage(self.workspaceFullPath)

package = Edizon(config)