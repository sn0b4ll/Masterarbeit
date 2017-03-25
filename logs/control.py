import io
import os
import shutil
import signal
import subprocess
import xml.etree.ElementTree as ET


from time import sleep

def read_bin_xml(FILE):
    """Convert plist binary to readable xml"""
    try:
        args = ['plutil', '-convert', 'xml1', FILE]
        dat = subprocess.check_output(args)
        with io.open(FILE, mode='r', encoding="utf8", errors="ignore") as f:
            dat = f.read()
        return dat
    except:
        print("[ERROR] Converting Binary XML to Readable XML")

ipa_path = "/Users/dominik/Masterarbeit/MobSF/Testfiles/Test2_sim.ipa"

# Chain together path
working_path = os.path.join(os.getcwd(), "tmp")

# Creat if not existing
if not os.path.exists(working_path):
    os.makedirs(working_path)

# Extract to path
subprocess.call(
    [
        "unzip", ipa_path,
        "-d", working_path
    ]
)

# Look for file
import fnmatch
import plistlib

plist_matches = []
app = ""
for root, dirnames, filenames in os.walk(working_path):
    for filename in fnmatch.filter(filenames, 'Info.plist'):
        plist_matches.append(os.path.join(root, filename))
    for dirname in dirnames:
        if dirname.endswith(".app"):
            app = os.path.join(root, dirname)

# Read XML
bundle_identifier = ""
for elem in plist_matches:
    xml = plistlib.readPlistFromString(read_bin_xml(elem))
    if 'CFBundleIdentifier' in xml:
        bundle_identifier = xml['CFBundleIdentifier']
        break

subprocess.call(["open", "/Applications/Xcode.app/Contents/Developer/Applications/Simulator.app"])

raw_input("Press Enter when simulator is started...")

subprocess.call(["xcrun", "simctl", "install", "booted", app])
subprocess.call(["xcrun", "simctl", "launch", "booted", bundle_identifier])

sleep(5)

raw_input("Press Enter to start testing...")

# Start mitmproxy
mitm = subprocess.Popen(["python", "mitm_test.py", "--file", "test"], preexec_fn=os.setsid)

raw_input("Press Enter when done testing...")

# Stop mitmproxy
os.killpg(os.getpgid(mitm.pid), signal.SIGTERM)

subprocess.call(["xcrun", "simctl", "terminate", "booted", bundle_identifier])
sleep(2)
subprocess.call(["xcrun", "simctl", "uninstall", "booted", bundle_identifier])



## Cleanup
# Remove after everything is done
shutil.rmtree(working_path)
