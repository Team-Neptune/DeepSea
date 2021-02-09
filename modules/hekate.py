from modules.basemodule import Basemodule
from pathlib import Path
import configparser
import os, shutil

config = {
    "service": 1,
    "username": "CTCaer",
    "reponame": "hekate",
    "assetRegex": ".*hekate.*\\.zip"
}

def overridePayload(extracted):
    folder = extracted
    entrys = os.listdir(folder)
    for i in entrys:
        if os.path.isfile(Path.joinpath(folder, i)):
            if i.endswith(".bin"):
                os.mkdir(Path.joinpath(folder, "atmosphere"))
                #os.rename(Path.joinpath(folder, i), Path.joinpath(folder, "atmosphere", "reboot_payload.bin"))
                shutil.copy2(Path.joinpath(folder, i), Path.joinpath(folder, "atmosphere", "reboot_payload.bin"))
                shutil.copy2(Path.joinpath(folder, i), Path.joinpath(folder, "bootloader", "update.bin"))
                return None

class Hekate(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
                    
    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        overridePayload(extracted)
        self.copyFolderContentToPackage(extracted)


package = Hekate(config)