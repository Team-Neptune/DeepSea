from modules.basemodule import Basemodule
from pathlib import Path

config = {
    "service": 1,
    "username": "retronx-team",
    "reponame": "sys-clk",
    "assetRegex": ".*sys-clk.*\\.zip"
}



class Sysclk(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        self.removeFile(Path.joinpath(extracted, "README.md"))
        self.copyFolderContentToPackage(extracted)


package = Sysclk(config)