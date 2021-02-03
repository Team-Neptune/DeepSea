from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "Team-Neptune",
    "reponame": "DeepSea-Cleaner",
    "assetRegex": ".*DeepSea-Cleaner.*\\.zip"
}


class Deepseacleaner(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
    
    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        self.copyFolderContentToPackage(extracted)


package = Deepseacleaner(config)