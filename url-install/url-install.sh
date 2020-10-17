#! /bin/bash

####################### Utils
set -xue

function err() {
    echo -e "\e[1;31m${@}\e[0m" >&2
    exit 1
}
export -f err

function extract_command() {
    FILE=$1
    if [ ${FILE: -7} == ".tar.gz" ]; then
        tar -xvf "$FILE" 
    elif [ ${FILE: -4} == ".zip" ]; then
        unzip "$FILE"
    else err Sorry, "$FILE" has unknown extension.
    fi
}

function determine_executable() {
    COMMAND=$1
    FILE_WITHOUT_EXTENSION=$2
    SOURCE=""
    if   [ -f "$COMMAND" ]; then
        SOURCE="$COMMAND"
    elif [ -d "$FILE_WITHOUT_EXTENSION" ]; then
        SOURCE="$FILE_WITHOUT_EXTENSION/$COMMAND"
    elif [ $(find . -executable -type f | wc -l) -eq 1 ]; then
        SOURCE=$(find . -executable -type f)
    else err Sorry, cannot determine executable.
    fi

    echo $SOURCE
}

###################### Logic

TARGET=$1
FILE="${TARGET##*/}"
FILE_WITHOUT_EXTENSION="${FILE%.*}"
COMMAND=$(echo $FILE | cut -d '-' -f1)

cd $(mktemp -d)
wget --quiet "${TARGET}"

extract_command "$FILE"

EXECUTABLE=$(determine_executable "$COMMAND" "$FILE_WITHOUT_EXTENSION")

echo mv "$EXECUTABLE" /usr/bin/"$COMMAND"
