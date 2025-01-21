from requests import get
import subprocess as sub
from datetime import datetime as dt, timezone as tz

startTime = dt.now(tz.utc)
print(f"[INFO] Script started at {startTime.strftime('%Y-%m-%d %H:%M:%S.%f')}")

oldVer = ""

try:
    from localVersionCache import oldVer  # pyright: ignore [reportMissingImports]

    print(f"[INFO] Old version is {oldVer}")
except:
    print("[WARN] No old version found!")

current = get(
    "https://api.github.com/repos/material-extensions/material-icons-browser-extension/releases/latest"
).json()

version = current["name"].lstrip(
    "v"
)  # Not sure if chrome extension versions can have a v?

print(f"[INFO] Latest version is {version}")

if version == oldVer:
    endTime = dt.now(tz.utc)
    print(
        f"""[INFO] No updates available
[INFO] Script finished at {endTime.strftime('%Y-%m-%d %H:%M:%S.%f')}
[INFO] Execution time {endTime - startTime}"""
    )
    exit(0)

print(
    """[INFO] Updating...
[INFO] Removing old files..."""
)

sub.run(
    [
        "rm",
        "-rf",
        "github-material-icons-chrome-extension",
        "github-material-icons-chrome-extension.zip",
        "github-material-icons-chrome-extension.crx",
        "github-material-icons-chrome-extension.xml",
    ],
    stdout=sub.DEVNULL,
    stderr=sub.DEVNULL,
)

print("[INFO] Downloading new .zip file...")

# Below is modifed from https://stackoverflow.com/a/16696317

file = get(current["assets"][0]["browser_download_url"], stream=True)

with open("github-material-icons-chrome-extension.zip", "wb") as f:
    for chunk in file.iter_content(chunk_size=8192):
        f.write(chunk)

print("[INFO] Making directory to unzip to...")

sub.run(
    [
        "mkdir",
        "github-material-icons-chrome-extension",
    ],
    stdout=sub.DEVNULL,
    stderr=sub.DEVNULL,
)

print("[INFO] Unzipping...")

sub.run(
    [
        "unzip",
        "github-material-icons-chrome-extension.zip",
        "-d",
        "github-material-icons-chrome-extension",
    ],
    stdout=sub.DEVNULL,
    stderr=sub.DEVNULL,
)

print("[INFO] Packing extension...")

sub.run(
    [
        "chromium",
        "--pack-extension=github-material-icons-chrome-extension",
        "--pack-extension-key=github-material-icons-chrome-extension.pem",
    ],
    stdout=sub.DEVNULL,
    stderr=sub.DEVNULL,
)

print("[INFO] Writing new XML file...")

with open("github-material-icons-chrome-extension.xml", "w") as f:
    f.writelines(
        [
            '<gupdate xmlns="http://www.google.com/update2/response" protocol="2.0">\n',
            '<app appid="jgjnmncmeidgipocjmaikclfojdlcain">\n',
            f'<updatecheck codebase="https://cf.firepup650.com/raw/github-material-icons-chrome-extension.crx" version="{version}"/>\n',
            "</app>\n",
            "</gupdate>",
        ]
    )

endTime = dt.now(tz.utc)
print(
    f"""[INFO] Script finished at {endTime.strftime('%Y-%m-%d %H:%M:%S.%f')}
[INFO] Execution time {endTime - startTime}"""
)
