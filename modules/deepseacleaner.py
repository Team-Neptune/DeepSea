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


package = Deepseacleaner(config)