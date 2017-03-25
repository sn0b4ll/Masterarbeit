def tools_binscope():
    """Download and install Binscope for MobSF"""

    mobsf_subdir_tools = CONFIG['MobSF']['tools']
    binscope_path = mobsf_subdir_tools + 'BinScope'

    # Download the right version for os
    if platform.machine().endswith('64'):
        binscope_url = CONFIG['binscope']['url_x64']
        binscope_installer_path = binscope_path + "\\BinScope_x64.msi"
    else:
        binscope_url = CONFIG['binscope']['url_x86']
        binscope_installer_path = binscope_path + "\\BinScope_x86.msi"

    if not os.path.exists(binscope_path):
        os.makedirs(binscope_path)

    binscope_installer_file = open(binscope_installer_path, "wb")

    # Downloading File
    print("[*] Downloading BinScope..")
    binscope_installer = urlrequest.urlopen(binscope_url)

    # Save content
    print("[*] Saving to File {}".format(binscope_installer_path))

    # Write content to file
    binscope_installer_file.write(bytes(binscope_installer.read()))

    # Aaaand close
    binscope_installer_file.close()

    # Execute the installer
    print("[*] Installing BinScope to {}".format(binscope_path))
    os.system(
        'msiexec' + ' '
        'INSTALLLOCATION="' + binscope_path + '" ' +
        '/i "' + binscope_installer_path + '" ' +
        '/passive'
    )

    CONFIG['binscope']['file'] = binscope_path + "\\Binscope.exe"

    # Write to config
    with open(os.path.join(CONFIG_PATH, CONFIG_FILE), 'w') as configfile:
        CONFIG.write(configfile)  # pylint: disable-msg=E1101
