import json, os, argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group()
    requiredNamed.add_argument('-gt')
    args = parser.parse_args()

json = json.loads(open("./VERSION").read())

for p in json["buildPackages"]:
    os.system("python3 ./main.py -p='"+p+"' -v='v"+json["buildVersion"]+"' -gt='"+args.gt+"'")