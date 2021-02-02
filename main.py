import os, importlib, shutil
from pathlib import Path
import argparse
import json

def GHRateLimit():
    #gh = Github(credentials.github_token)
    #core_rate_limit = gh.get_rate_limit().core
    #print(core_rate_limit)
    pass

def clearFolders(folderlist):
    for folder in folderlist:
        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="TeamNeptune's DeepSea build script.")
    requiredNamed = parser.add_argument_group('Options required to build a release candidate')
    requiredNamed.add_argument('-v', '--version', help='DeepSea version tag', required=True)
    requiredNamed.add_argument('-p', '--package', help='json file that specifies the included modules', required=True)
    requiredNamed.add_argument('-gt', '--githubToken', help='Github Token', required=True)
    args = parser.parse_args()

    modules = []
    try:
        with open(Path.joinpath(Path.cwd(), "packages", args.package+".json")) as json_file:
            modules = json.load(json_file)
    except:
        print("Could not load Package.")
        exit()


    currpath = Path.cwd()
    modulepath = Path.joinpath(currpath, "modules")
    dirpath = Path.joinpath(currpath, "tmp")
    finalPath = Path.joinpath(currpath, "switch_out")

    clearFolders([dirpath, finalPath])
    os.mkdir(finalPath)

    for basename in modules:
        importlib.import_module("modules."+basename)

    filename = "deepsea-"+Path(args.package).stem+"_"+args.version
    shutil.make_archive(filename,'zip',finalPath)
    clearFolders([dirpath, finalPath])
