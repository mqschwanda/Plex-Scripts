#!/bin/bash
# Usage: ./CompressFile.sh <input file>

NOW=$(date +"%m%d%Y")
HAND_BRAKE=/usr/local/Cellar/handbrake/1.0.7/bin/HandBrakeCLI
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

echo "Starting HandBrake $NOW"
$HAND_BRAKE --input "$1" --output "$BASE_PATH/$FILE_NAME.mp4" --encoder x264 --quality 22.0 -ab 192 --maxWidth 1080 –preset="Normal" --optimize
CHECK_ERROR $? "Failed to convert file $1"

# echo "Removing original file."
# rm -f "$1"
# CHECK_ERROR $? "Failed to remove original file $1"

echo "Renaming new video to old name"
mv "$BASE_PATH/$FILE_NAME.mp4" "$1"
CHECK_ERROR $? "Failed to rename new file to original file name $1"
