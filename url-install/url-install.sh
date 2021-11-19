#!/bin/bash
set -x 
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

function main() {
    COMPUTE_CHECKSUMS_ONLY=False
    DRY_RUN=False
    EXTRACT=True
    INSTALL_ALL=False

    until test "$1" = ""
    do
        [ $1 = "--compute_checksums_only" ] && COMPUTE_CHECKSUMS_ONLY=True && shift
        [ $1 = "--dry_run" ] && DRY_RUN=True && shift
        [ $1 = "--no_extract" ] && EXTRACT=False && shift
        [ $1 = "--install_all" ] && INSTALL_ALL=True && shift

        TARGET=$1; 
        [ $COMPUTE_CHECKSUMS_ONLY = False ] && printf %"100"s | tr " " "-" && echo && shift && CHECKSUM=$1
        shift

        FILE="${TARGET##*/}"
        FILE_WITHOUT_EXTENSION="${FILE%.*}"
        COMMAND=$(echo $FILE | cut -d '-' -f1)

        cd $(mktemp -d)
        wget --quiet "${TARGET}"
        [ $COMPUTE_CHECKSUMS_ONLY = True ] && echo -n "$TARGET "&& sha256sum $FILE | cut -d ' ' -f1 | tr '\n' ' ' && echo " \\" && continue
        echo "$CHECKSUM $FILE" | sha256sum -c || err "Checksum mismatch: $CHECKSUM incorrect."
        [ $EXTRACT = True ] && extract_command "$FILE" && rm "$FILE"
        [ $INSTALL_ALL = True ] && chmod +x *
       

        [ $INSTALL_ALL = False ] && EXECUTABLE=$(determine_executable "$COMMAND" "$FILE_WITHOUT_EXTENSION") || EXECUTABLE="*"
        [ $DRY_RUN = False  ] && mv "$EXECUTABLE" ~/.local/bin/"$COMMAND"
    done
    echo
    echo "Done."
}

main $@
