from modules.basemodule import Basemodule
from pathlib import Path

config = {
    "service": 1,
    "username": "XorTroll",
    "reponame": "emuiibo",
    "assetRegex": ".*emuiibo.*\\.zip"
}


class Emuiibo(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
    
    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        extracted = Path.joinpath(extracted, "SdOut")
        self.findAndRemove("boot2.flag")
        self.copyFolderContentToPackage(extracted)

package = Emuiibo(config)