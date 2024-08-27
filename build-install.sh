#!/bin/bash

pyinstaller_out=$(pyinstaller --onefile idle-cli.py 2>&1)
pyinstaller_ec=$?

if [ $pyinstaller_ec -ne 0 ]; then
    echo "$pyinstaller_out"
    exit 1
fi

bin_dirs=("$HOME/bin" "$HOME/.local/bin")

executable="dist/idle-cli"

for bin_dir in "${bin_dirs[@]}"; do
    if [ -d "$bin_dir" ]; then
        if echo "$PATH" | grep -q "$bin_dir"; then
            chmod +x $executable
	    cp "$executable" "$bin_dir"
            echo "Installed $executable in $bin_dir"
            exit 0
        fi
    fi
done

echo "No suitable bin directory found in PATH"
exit 1
