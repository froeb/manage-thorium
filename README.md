# manage-thorium
This script automates the installation, update, or removal of the Thorium browser on Debian-based Linux distributions.

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
