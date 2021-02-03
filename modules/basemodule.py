
from distutils.dir_util import copy_tree
from pathlib import Path
from github import Github
import urllib.request
import uuid, os, re
import zipfile
import shutil
import argparse
import glob

parser = argparse.ArgumentParser(description="TeamNeptune's DeepSea build script.")
requiredNamed = parser.add_argument_group('Options required to build a release candidate')
requiredNamed.add_argument('-v', '--version', help='DeepSea version tag', required=True)
requiredNamed.add_argument('-p', '--package', help='json file that specifies the included modules', required=True)
requiredNamed.add_argument('-gt', '--githubToken', help='Github Token', required=True)
args = parser.parse_args()

class Basemodule:
    def __init__(self, config):
        print("Init module: ", self.__module__)
        self.config = config
        self.uuid = ""
        self.workspaceFullPath = self.__createWorkspace()
        self.handleModule()

    def __createWorkspace(self):
        self.uuid = str(uuid.uuid4())
        workdir = Path.cwd().joinpath('tmp', self.uuid)
        os.makedirs(workdir)
        return workdir

    def getLatestRelease(self):
        # gh = Github(credentials.github_username, credentials.github_password)
        gh = Github(args.githubToken)
        if self.config["service"] == 1:
            try:
                repo = gh.get_repo(self.config["username"] + "/" + self.config["reponame"])
            except:
                print("Unable to get: ", self.config["username"], "/", self.config["reponame"])
                return None
            releases = repo.get_releases()
            if releases.totalCount == 0:
                print("No available releases for: ", self.config["username"], "/", self.config["reponame"])
                return None
            return releases[0]

    def downloadAsset(self, release):
        pattern = self.config["assetRegex"]
        if self.config["service"] == 1:
            if release is None:
                return None
            matched_asset = None
            for asset in release.get_assets():
                if re.search(pattern, asset.name):
                    matched_asset = asset
                    break
            if matched_asset is None:
                print("Did not find asset for pattern: ", pattern)
                return None
            download_path = Path.joinpath(self.workspaceFullPath, matched_asset.name)
            urllib.request.urlretrieve(matched_asset.browser_download_url, download_path)
            return matched_asset.name

    def downloadAssets(self, release):
        assetPaths = []
        for pattern in self.config["assetPatterns"]:
            self.config["assetRegex"] = pattern
            assetPaths.append(self.downloadAsset(release))
        return assetPaths

    def unpackAsset(self, assetName):
        if assetName is None:
            return None
        assetpath = Path.joinpath(self.workspaceFullPath, assetName)
        folder = Path.joinpath(self.workspaceFullPath, "extracted")
        os.mkdir(folder)
        with zipfile.ZipFile(assetpath, 'r') as zip_ref:
            zip_ref.extractall(folder)
        return folder

    def copyFileToPackage(self, source, target):
        pass

    def removeFile(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    def findAndRemove(self, filename):
        if self.__module__ == "modules.atmosphere":
            pass
        elif self.__module__ == "modules.ovlloader": 
            pass
        else:
            search = Path.joinpath(self.workspaceFullPath, "**", filename)
            fileList = glob.glob(str(search), recursive=True)
            for filePath in fileList:
                try:
                    os.remove(filePath)
                except:
                    pass


    def copyFolderContentToPackage(self, source_dir, target_dir=""):
        if source_dir is None:
            return None
        if target_dir == "":
            target_dir = Path.joinpath(Path.cwd(), "switch_out")
        copy_tree(str(source_dir), str(target_dir))

    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        self.findAndRemove("boot2.flag")
        self.copyFolderContentToPackage(extracted)