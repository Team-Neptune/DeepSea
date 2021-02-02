from modules.basemodule import Basemodule


config = {
    "service": 1,
    "username": "cathery",
    "reponame": "sys-ftpd-light",
    "assetRegex": ".*sys-ftpd-light.*\\.zip"
}


class Sysftplight(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)


package = Sysftplight(config)