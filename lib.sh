#!/bin/bash
LibName="python_system_wide"
ExecutablesDir="$HOME/bin/python"
LibLink="$ExecutablesDir/$LibName"

LibFolder=""
LibFullPath=""


# Getting Original Library's Directory
[[ ! -d "$ExecutablesDir" ]] && mkdir -p -m 777 "$ExecutablesDir"

if [[ -f "$LibLink" ]]; then LibFullPath="$(readlink -f "$LibLink")"
elif [[ "$BASH_SOURCE" != "" ]]; then LibFullPath="$BASH_SOURCE"
else LibFullPath="$0"
fi
[[ "${LibFullPath: 0:1}" == "." ]] && LibFullPath="$PWD${LibFullPath: 1}"


LibFolder="$(dirname "$LibFullPath")"


# ------------------------
convert-to-cli py "$LibFolder" "$LibFolder/__cli__"
sleep 3
CreateFolderLink "$LibFolder/__cli__" "$LibLink"
