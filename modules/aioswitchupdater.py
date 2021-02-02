from modules.basemodule import Basemodule
from pathlib import Path
import os

config = {
    "service": 1,
    "username": "HamletDuFromage",
    "reponame": "aio-switch-updater",
    "assetRegex": ".*aio-switch-updater.*\\.zip"
}


def deleteNotNeededNro(extracted):
    folder = Path.joinpath(extracted, "switch", "aio-switch-updater")
    entrys = os.listdir(folder)
    for i in entrys:
        if os.path.isfile(Path.joinpath(folder, i)):
            if i.startswith("aio-switch-updater-v"):
                os.remove(Path.joinpath(folder, i))
                return None

class Aioupdater(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        deleteNotNeededNro(extracted)
        self.copyFolderContentToPackage(extracted)


package = Aioupdater(config)