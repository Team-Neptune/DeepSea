from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "cathery",
    "reponame": "sys-con",
    "assetRegex": ".*sys-con.*\\.zip"
}


class Syscon(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Syscon(config)