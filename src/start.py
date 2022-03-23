import logging, json, argparse, shutil
from gh import GH
from fs import FS
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    
  parser = argparse.ArgumentParser(description="TeamNeptune's DeepSea build script.")
  requiredNamed = parser.add_argument_group('Options required to build a release candidate')
  requiredNamed.add_argument('-v', '--version', help='DeepSea version tag', required=True)
  requiredNamed.add_argument('-gt', '--githubToken', help='Github Token', required=True)
  args = parser.parse_args()

  sdcard = FS()
  github = GH(args.githubToken)

  with open('./settings.json', 'r') as f:
    settings = json.load(f)

  neededModules = []
  for package in settings["packages"]:
    if package["active"]:
      for module in package["modules"]:
        if module not in neededModules:
          neededModules.append(module)


  for i in neededModules:
    module = settings["moduleList"][i]
    github.downloadReleaseAssets(module)


  for package in settings["packages"]:
    if package["active"]:
      logging.info(f"[{package['name']}] Creating package")
      sdcard.createSDEnv()

      for i in package["modules"]:
        module = settings["moduleList"][i]
        logging.info(f"[{package['name']}][{module['repo']}] Creating module env")
        sdcard.createModuleEnv(module)
        for step in module["steps"]:
          logging.info(f"[{package['name']}][{module['repo']}] Executing step: {step['name']}")
          sdcard.executeStep(module, step)
        
        logging.info(f"[{package['name']}][{module['repo']}] Moving MENV to SD")
        sdcard.finishModule()
      
      logging.info(f"[{package['name']}] All modules processed.")
      logging.info(f"[{package['name']}] Creating ZIP")
      shutil.make_archive(f"deepsea-{package['name']}_v{settings['releaseVersion']}", 'zip', "./sd")


