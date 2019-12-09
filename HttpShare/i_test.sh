#! /bin/bash

arrange() {
    temp_folder=$(mktemp -d)
    touch "$temp_folder"/foo
    touch "$temp_folder"/bar
}

act() {
    ./share.sh $temp_folder 7001
    sleep 2s
    result=$(curl --silent http://0.0.0.0:7001)
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
