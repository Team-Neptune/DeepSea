import subprocess
import json


def getModuleMarkdown(_mName, _mVersion):
    for module in modules:
        if module["name"] != _mName:
            continue
        url = ""
        if module["git"]["service"] == 0:
            url = "https://github.com/"
        else:
            url = "https://gitlab.com/"
        url = url + module["git"]["org_name"] + \
            "/" + module["git"]["repo_name"]
        md = "["+_mName+" - "+_mVersion+"]("+url+")"
        return md


with open('VERSION', 'r') as myfile:
    data = myfile.read()
obj = json.loads(data)
packages = obj['buildPackages']
version = obj['buildVersion']

with open('./builder/Modules/modules-definitions.json', 'r') as myfile:
    data = myfile.read()
modules = json.loads(data)

release = {}
release["bodyText"] = "Release " + version + "\n\n" + \
    "DeepSea v" + version + " built with:\n\n"

packageOutputs = ""

for package in packages:
    command = 'cd ./builder && python ./builder.py -v v' + \
        version+' '+package+'.json output="./' + package+'.zip"'
    process = subprocess.run(command, shell=True, check=True,
                             stdout=subprocess.PIPE, universal_newlines=True)
    print(process.stdout)
    packageOutputs = packageOutputs + "\n" + process.stdout

lines = sorted(list(set(packageOutputs.splitlines())))

for line in lines:
    if line.startswith('  '):

        mName = line.split(" - ")[0].strip()
        mVersion = line.split(" - ")[1].strip()
        release["bodyText"] = release["bodyText"] + "* " + \
            getModuleMarkdown(mName, mVersion) + "\n"

with open("release_body.txt", 'w') as filetowrite:
    filetowrite.write(release["bodyText"])
