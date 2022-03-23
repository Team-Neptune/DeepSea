
import pathlib
from github import Github
import urllib.request
import re
import logging

class GH():
    def __init__(self, ghToken):
        self.token = ghToken
        self.github = Github(self.token)

    def downloadReleaseAssets(self, module):
        try:
            ghRepo = self.github.get_repo(module["repo"])
        except:
            logging.exception(f"Unable to get: {module['repo']}")
            return
        
        releases = ghRepo.get_releases()
        if releases.totalCount == 0:
            logging.warning(f"No available release for: {module['repo']}")
            return
        ghLatestRelease = releases[0]

        for pattern in module["regex"]:
            for asset in ghLatestRelease.get_assets():
                if re.search(pattern, asset.name):
                    logging.info(f"[{module['repo']}] Downloading: {asset.name}")
                    fpath = f"./base/{module['repo']}/"
                    pathlib.Path(fpath).mkdir(parents=True, exist_ok=True)
                    urllib.request.urlretrieve(asset.browser_download_url, f"{fpath}{asset.name}")
        return True