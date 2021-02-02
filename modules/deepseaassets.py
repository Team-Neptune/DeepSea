from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "Team-Neptune",
    "reponame": "DeepSea-Assets",
    "assetRegex": ".*DeepSea-Assets.*\\.zip"
}


class DSAssets(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = DSAssets(config)