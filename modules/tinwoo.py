from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "mrdude2478",
    "reponame": "TinWoo",
    "assetRegex": ".*TinWoo-Installer.*\\.zip"
}


class Tinwoo(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Tinwoo(config)