from os import popen
from json import load,dumps

# popen(f"ping {domain_name}").read()
def main():

    package_json = ""
    with open("package.json") as pack:
        package_json = load(pack)

    github_username = str(input("Enter your Github username: "))
    app_name = str(input("Enter your app name: "))
    
    package_json["homepage"] = f"http://{github_username}.github.io/{app_name}"
    execute_popen("npm install gh-pages --save-dev")

    scripts = package_json["scripts"]
    scripts["predeploy"] = "npm run build"
    scripts["deploy"]= "gh-pages -d build"

    json_object = dumps(package_json,indent=4)
    with open("package.json", "w") as outfile:
        outfile.write(json_object)
        
    execute_popen("git init")
    execute_popen(str(f"git remote set-url  origin https://github.com/{github_username}/{app_name}.git"))
    execute_popen("npm run deploy")

    want_to_commit = str(input("Do u want to push code in github?(y/n)"))
    
    if want_to_commit == "y":
        execute_popen("git add .")
        comment = str(input("Enter commit comment: "))
        execute_popen(str(f"git commit -m {comment}"))
        execute_popen("git push origin master")


def execute_popen(command):
    try:
        result = popen(command).read()
    
    finally:
        print(result)


if __name__ == '__main__':
    main()
    
