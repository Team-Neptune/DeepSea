from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "WerWolv",
    "reponame": "nx-ovlloader",
    "assetRegex": ".*nx-ovlloader.*\\.zip"
}


class Ovlloader(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Ovlloader(config)