from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "ndeadly",
    "reponame": "MissionControl",
    "assetRegex": ".*MissionControl.*\\.zip"
}


class Missioncontrol(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Missioncontrol(config)