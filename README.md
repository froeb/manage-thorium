# manage-thorium
This script automates the installation, update, or removal of the Thorium browser on Debian-based Linux distributions.

## Description:
    This script automates the installation, update, or removal of the Thorium browser 
    on Debian-based Linux distributions. It checks for the latest version of Thorium 
    from its GitHub releases, downloads the .deb package, and manages the installation 
    or update using 'nala', a front-end for 'apt'. The script can also remove an 
    existing installation of Thorium.

## Usage:
    To install Thorium: python manage-thorium.py install
    To update Thorium: python manage-thorium.py update
    To remove Thorium: python manage-thorium.py remove

## Dependencies:
    This script uses 'nala' for package management, which is a front-end for 'apt'.
    Ensure 'nala' is installed on your system. To install 'nala', use:
    sudo apt install nala

## Automatic Daily Updates

To ensure you always have the latest version of the Thorium browser, you can set up a daily job on your Linux system using `cron`.

1. Open your crontab file by running `crontab -e` in the terminal.

2. Add the following line to schedule the script to run daily (example time is 2 AM):

    ```
    0 2 * * * /usr/bin/python3 /path/to/manage-thorium.py update
    ```

    Make sure to replace `/path/to/manage-thorium.py` with the actual path to the script on your system.

3. Save the file and exit the editor. Your system will now automatically check for and install updates to the Thorium browser each day at the specified time.
