
from pathlib import Path
from github import Github
import urllib.request
import re

class GH():
    def __init__(self, ghToken):
        self.token = ghToken
        self.github = Github(self.token)

    def downloadLatestRelease(self, moduleJson, downloadPath):
        try:
            ghRepo = self.github.get_repo(moduleJson["repo"])
        except:
            print("Unable to get: ", moduleJson["repo"])
            return
        
        releases = ghRepo.get_releases()
        if releases.totalCount == 0:
            print("No available releases for: ", moduleJson["repo"])
            return
        ghLatestRelease = releases[0]

        downloadedFiles = []

        for pattern in moduleJson["assetRegex"]:
            matched_asset = None
            for asset in ghLatestRelease.get_assets():
                if re.search(pattern, asset.name):
                    matched_asset = asset
                    break
            if matched_asset is None:
                print("Did not find asset for pattern: ", pattern)
                return

            downloadFilePath = Path.joinpath(downloadPath, matched_asset.name)
            urllib.request.urlretrieve(matched_asset.browser_download_url, downloadFilePath)
            downloadedFiles.append(downloadFilePath)
        
        return downloadedFiles