"""
manage-thorium.py
Copyright (C) 2023 by Kai Froeb
This script is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Description:
    This script automates the installation, update, or removal of the Thorium browser 
    on Debian-based Linux distributions. It checks for the latest version of Thorium 
    from its GitHub releases, downloads the .deb package, and manages the installation 
    or update using 'nala', a front-end for 'apt'. The script can also remove an 
    existing installation of Thorium.

Usage:
    To install Thorium: python manage-thorium.py install
    To update Thorium: python manage-thorium.py update
    To remove Thorium: python manage-thorium.py remove

Dependencies:
    This script uses 'nala' for package management, which is a front-end for 'apt'.
    Ensure 'nala' is installed on your system. To install 'nala', use:
    sudo apt install nala
"""

import requests
import os
import subprocess
import argparse
import tempfile

def get_installed_version():
    """
    Retrieves the installed version of Thorium browser.
    Returns:
        str: Installed version number, or None if not installed.
    """
    try:
        result = subprocess.run(["thorium-browser", "--version"], capture_output=True, text=True, check=True)
        version_line = result.stdout.strip()
        if version_line.startswith("Thorium"):
            return version_line.split()[1]
    except subprocess.CalledProcessError:
        print("Thorium browser is not installed or unable to get version.")
    except FileNotFoundError:
        print("Thorium browser is not installed.")
    return None

def install_deb(file_path):
    """
    Installs a .deb file using Nala, with a fallback to dpkg.
    Args:
        file_path (str): Path to the .deb file.
    """
    try:
        subprocess.run(["sudo", "nala", "install", file_path], check=True)
    except subprocess.CalledProcessError:
        print("Nala failed to install the package. Attempting with dpkg...")
        subprocess.run(["sudo", "dpkg", "-i", file_path], check=True)
        subprocess.run(["sudo", "nala", "install", "-f"], check=True)
        
def remove_package(package_name):
    """
    Removes a package using Nala, with a fallback to dpkg.
    Args:
        package_name (str): Name of the package to remove.
    """
    try:
        subprocess.run(["sudo", "nala", "remove", package_name], check=True)
    except subprocess.CalledProcessError:
        print("Nala failed to remove the package. Attempting with dpkg...")
        subprocess.run(["sudo", "dpkg", "-r", package_name], check=True)

def download_file(url, destination_folder):
    """
    Downloads a file from a given URL to a specified destination.
    Args:
        url (str): URL of the file to download.
        destination_folder (str): Folder where the file will be saved.
    Returns:
        str: Path to the downloaded file.
    """
    local_filename = url.split('/')[-1]
    path = os.path.join(destination_folder, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return path

def get_latest_deb_release(owner, repo):
    """
    Fetches the latest .deb release from a GitHub repository.
    Args:
        owner (str): GitHub username or organization name.
        repo (str): GitHub repository name.
    Returns:
        str: URL of the latest .deb release, or None if not found.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch release data from GitHub API")
        return None
    release_data = response.json()
    for asset in release_data.get('assets', []):
        if asset['name'].endswith('.deb'):
            return asset['browser_download_url']
    return None

def main():
    """
    Manages the installation, removal, and updating of Thorium browser.
    Supported commands: install, remove, update.
    """
    parser = argparse.ArgumentParser(description='Manage Thorium Browser installation.')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Add parsers for 'install', 'remove', and 'update' commands
    install_parser = subparsers.add_parser('install')
    remove_parser = subparsers.add_parser('remove')
    update_parser = subparsers.add_parser('update')

    args = parser.parse_args()

    # Define a general temporary directory for downloads
    temp_dir = tempfile.gettempdir()

    if args.command in ['install', 'update']:
        installed_version = get_installed_version()

        if args.command == 'update' and installed_version is None:
            print("Thorium is not installed. Use 'install' command to install it.")
            return
            
        latest_deb_url = get_latest_deb_release("Alex313031", "Thorium")
        if not latest_deb_url:
            print("No .deb release found")
            return

        latest_version = latest_deb_url.split('/')[-1].split('_')[1]
        if installed_version == latest_version:
            print(f"Latest version {latest_version} is already installed.")
            return

        if args.command == 'update':
            print(f"Updating Thorium from version {installed_version} to {latest_version}...")

        print("Latest .deb release URL:", latest_deb_url)
        destination_folder = "/home/kai/projects/renew-thorium"  # Update this path
        downloaded_file = download_file(latest_deb_url, destination_folder)
        install_deb(downloaded_file)
        print(f"Installed {downloaded_file}")

    elif args.command == 'remove':
        remove_package("thorium-browser")  # Replace with the actual package name if different

if __name__ == "__main__":
    main()

