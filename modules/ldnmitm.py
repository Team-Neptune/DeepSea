from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "spacemeowx2",
    "reponame": "ldn_mitm",
    "assetRegex": ".*ldn_mitm.*\\.zip"
}


class Ldnmitm(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Ldnmitm(config)