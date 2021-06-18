from modules.basemodule import Basemodule
from pathlib import Path
import shutil

config = {
    "service": 1,
    "username": "Team-Neptune",
    "reponame": "CommonProblemResolver",
    "assetRegex": ".*\\.bin"
}

def modifyFiles(workpath, assetName):
    Path(Path.joinpath(workpath, "bootloader", "payloads")).mkdir(parents=True, exist_ok=True)
    shutil.move(Path.joinpath(workpath, assetName), Path.joinpath(workpath, "bootloader", "payloads", assetName))


class Commonproblemresolver(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        #extracted = self.unpackAsset(assetName)
        modifyFiles(self.workspaceFullPath, assetName)
        self.copyFolderContentToPackage(self.workspaceFullPath)

package = Commonproblemresolver(config)