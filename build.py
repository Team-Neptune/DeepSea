import src.scripts.gh as GH, src.scripts.fs as FS
import argparse, json, os, importlib, shutil
from pathlib import Path
from distutils.dir_util import copy_tree

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="TeamNeptune's DeepSea build script.")
    requiredNamed = parser.add_argument_group('Options required to build a release candidate')
    requiredNamed.add_argument('-v', '--version', help='DeepSea version tag', required=True)
    requiredNamed.add_argument('-gt', '--githubToken', help='Github Token', required=True)
    args = parser.parse_args()

    try:
        with open(Path.joinpath(Path.cwd(), "src", "settings.json")) as json_file:
            settings = json.load(json_file)
    except:
        print("Could not load Package.")
        exit()

    shutil.rmtree("tmp", ignore_errors=True)
    gh = GH.GH(args.githubToken)
    fs = FS.FS()


    for packageName in settings["packages"]:
        packageObj = settings["packages"][packageName]
        if packageObj["active"] == True:
            for moduleName in packageObj["modules"]:
                if fs.doesFilesExist(False, "src/modules/"+moduleName+".json"):
                    module = fs.getJson(False, "src/modules/"+moduleName+".json")
                    if not fs.doesFolderExist(True, moduleName):
                        print("Downloading: " + module["repo"])
                        dlPath = fs.createDirs(moduleName)
                        downloadedFiles = gh.downloadLatestRelease(module, dlPath)

                        for customStep in module["customSteps"]:

                            if customStep["action"] == "createDir":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.createDir(moduleName, customStep["source"])
                            
                            if customStep["action"] == "extract":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.extract(moduleName, customStep["source"])

                            if customStep["action"] == "delete":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.delete(moduleName, customStep["source"])

                            if customStep["action"] == "copy":
                                if "fileRegex" in customStep:
                                    print("- custom step: " + customStep["action"] + " -> " + customStep["fileRegex"])
                                    fs.copy(moduleName, customStep["source"], customStep["destination"], customStep["fileRegex"])
                                else:
                                    print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                    fs.copy(moduleName, customStep["source"], customStep["destination"])

                            if customStep["action"] == "move":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.move(moduleName, customStep["source"], customStep["destination"])

                            if customStep["action"] == "replaceText":
                                print("- custom step: " + customStep["action"] + " -> " + customStep["source"])
                                fs.replaceText(moduleName, customStep["source"], customStep["target"], customStep["replacement"])
                    else:
                        print("Already downloaded: " + module["repo"])

                    outPath = str(fs.createDirs("switch_out"))
                    shutil.copytree(str(Path(Path.joinpath(fs.workdir, moduleName))), str(Path(Path.joinpath(fs.workdir, "switch_out"))), dirs_exist_ok=True)
                    # fs.copy("", str(Path(Path.joinpath(fs.workdir, moduleName))), outPath)
                else:
                    print("module file does not exist")

            print("Zipping package: " + "deepsea-"+packageName+"_v"+settings["version"])
            shutil.make_archive("deepsea-"+packageName+"_v"+settings["version"],'zip',outPath)
            fs.delete("",outPath)

        else:
            print("package inactive")


