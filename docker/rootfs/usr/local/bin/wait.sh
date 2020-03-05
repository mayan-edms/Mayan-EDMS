#!/bin/bash

check_port() {
  !</dev/tcp/${ENTRY[0]}/${ENTRY[1]}
}

# Get the HOST:PORT pair from the argument list and turn into an array
IFS=' ' read -ra ENTRIES <<< "${@:1}"

for i in "${ENTRIES[@]}"
do
    # Further split each HOST:PORT entry into a two element array
    IFS=':' read -ra ENTRY <<< "${i}"
    echo "Waiting for ${i}"
    while check_port &>/dev/null
    do
        sleep 1
        echo "Waiting for ${i}"
    done
done
