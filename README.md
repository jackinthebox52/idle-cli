## About

This is a simple 'clone' of the IDLE Python interpreter GUI as a terminal application for Linux, specifially the code execution, visualization, and automatic saving of the session to a file.
Great for use in homework assignments.

## Installation
Install Python 3 (Version must support pyinstaller to use install script)
`pip install -r requirements.txt`

Set execution flag on installer script
`chmod +x build-install.sh`

... And execute it
`.build-install.sh`

## Usage
Simply execute the script by invoking the `idle-cli` binary in your terminal, followed by the output path you'd like to write to.

Example: `idle-cli ~/Documents/assignment1.txt`

