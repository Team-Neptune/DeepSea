from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "WerWolv",
    "reponame": "Tesla-Menu",
    "assetRegex": ".*ovlmenu.*\\.zip"
}


class Teslamenu(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Teslamenu(config)