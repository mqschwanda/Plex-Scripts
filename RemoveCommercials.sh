#!/bin/bash
# Usage: ./RemoveCommercials.sh <input file>

NOW=$(date +"%m%d%Y")
SCRIPT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P) # get the base path relative to this file
CHECK_ERROR() { # Parameter 1 is the return code... Para. 2 is text to display on failure.
  if ["${1}" -ne "0"]; then
    echo "ERROR # ${1} : ${2}"
    exit ${1} # exit script with error code.
  fi
}

FILE_PATH=${1}
BASE_PATH=$(dirname "$FILE_PATH")
BASE_FILE=$(basename "$FILE_PATH")
FILE_NAME="${BASE_FILE%%.*}"

echo "Starting Comskip $NOW"
python "$SCRIPT_PATH/PlexComskip/Script.py" "$BASE_PATH/$FILE_NAME.ts"
CHECK_ERROR $? "Failed to remove commercials from file $1"
