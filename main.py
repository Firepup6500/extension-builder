from requests import get
import subprocess, os

oldVer = ""

try:
    from localVersionCache import oldVer  # pyright: ignore [reportMissingImports]
except:
    ...

current = get("https://api.github.com/repos/material-extensions/material-icons-browser-extension/releases/latest").json()

version = current["name"]

if version == oldVer:
    exit(0)

subprocess.run(['rm','-rf','github-material-icons-chrome-extensio*'])

# Below is modifed from https://stackoverflow.com/a/16696317

file = get(current["assets"][0]["browser_download_url"], stream=True)

with open("github-material-icons-chrome-extension.zip", "wb") as f:
    for chunk in file.iter_content(chunk_size=8192):
        f.write(chunk)

os.mkdir('github-material-icons-chrome-extension')

subprocess.run(['unzip','github-material-icons-chrome-extension.zip','-d','github-material-icons-chrome-extension'])