import shutil, os, logging, re, zipfile, glob
from pathlib import Path

class FS():
    def __init__(self):
        shutil.rmtree("./base", ignore_errors=True)
        shutil.rmtree("./menv", ignore_errors=True)
        shutil.rmtree("./sd", ignore_errors=True)
        for elements in glob.glob(f"./*.zip"):
            os.remove(elements)

    def createSDEnv(self):
        shutil.rmtree("./sd", ignore_errors=True)
        Path("./sd").mkdir(parents=True, exist_ok=True)

    def createModuleEnv(self, module):
        shutil.rmtree("./menv", ignore_errors=True)
        Path("./menv").mkdir(parents=True, exist_ok=True)
        shutil.copytree(f"./base/{module['repo']}", f"./menv/", dirs_exist_ok=True)

    def finishModule(self):
        self.__copyToSD()
        shutil.rmtree("./menv", ignore_errors=True)

    def executeStep(self, module, step):
        if step["name"] == "extract":
            self.__extract(step["arguments"][0])
        
        if step["name"] == "create_dir":
            self.__createDir(step["arguments"][0])

        if step["name"] == "create_file":
            self.__createFile(step["arguments"][0], step["arguments"][1])

        if step["name"] == "replace_content":
            self.__replaceFileContent(step["arguments"][0], step["arguments"][1], step["arguments"][2])

        if step["name"] == "delete":
            self.__delete(step["arguments"][0])

        if step["name"] == "copy":
            self.__copy(step["arguments"][0], step["arguments"][1])

        if step["name"] == "move":
            self.__copy(step["arguments"][0], step["arguments"][1])
            self.__delete(step["arguments"][0])
        


    def __extract(self, source):
        path = f"./menv/"
        for filename in os.listdir(path):
            if re.search(source, filename):
                assetPath = f"./menv/{filename}"
                with zipfile.ZipFile(assetPath, 'r') as zip_ref:
                    zip_ref.extractall(path)
                self.__delete(filename)   

    def __delete(self, source):
        if not os.path.isdir(f"./menv/{source}"):
            if os.path.exists(f"./menv/{source}"):
                os.remove(f"./menv/{source}")
        else:
            shutil.rmtree(f"./menv/{source}", ignore_errors=True)
    
    def __copy(self, source, dest):
        for elements in glob.glob(f"./menv/{source}"):
            if not os.path.isdir(elements):
                if os.path.exists(elements):
                    shutil.copy(f"{elements}", f"./menv/{dest}")
                    break
            else:
                shutil.copytree(f"{elements}", f"./menv/{dest}", dirs_exist_ok=True)
                break
    
    def __createDir(self, source):
        Path(f"./menv/{source}").mkdir(parents=True, exist_ok=True)
    
    def __createFile(self, source, content):
        with open(f"./menv/{source}", "w") as f:
            f.write(content)
    
    def __replaceFileContent(self, source, search, replace):
        fin = open(f"./menv/{source}", "rt")
        data = fin.read()
        data = data.replace(search, replace)
        fin.close()
        fin = open(f"./menv/{source}", "wt")
        fin.write(data)
        fin.close()

    def __copyToSD(self):
        shutil.copytree("./menv", "./sd/", dirs_exist_ok=True)


