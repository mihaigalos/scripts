#! /bin/bash

use_unused_port() {
    port=0
    while
      port=$(shuf -n 1 -i 49152-65535)
      netstat -atun | grep -q "$port"
    do
      continue
    done
}

arrange() {
    temp_folder=$(mktemp -d)

    touch "$temp_folder"/foo
    touch "$temp_folder"/bar
    use_unused_port
}

act() {
    ./share.sh $temp_folder $port
    sleep 2s
    result=$(curl --silent "http://0.0.0.0:$port")
}

assert() {
    if [[ $result == *"foo"* ]] && [[ $result == *"bar"* ]]; then
      echo "Everything OK."
    else
      echo "Could not share folder on specified port."
    fi
}

teardown() {
    docker ps | grep python_http_server | awk '{print $1}' | xargs docker kill > /dev/null
}

arrange
act
assert
teardown
