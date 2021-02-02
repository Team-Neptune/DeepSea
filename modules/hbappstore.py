from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "fortheusers",
    "reponame": "hb-appstore",
    "assetRegex": ".*switch-extracttosd.*\\.zip"
}


class Hbappstore(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Hbappstore(config)