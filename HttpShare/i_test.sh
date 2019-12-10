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
    username="myuser"
    password="mypass"
}

act() {
    ./share.sh $temp_folder $port $username $password
    sleep 2s
}

assert() {
    result=$(curl --insecure --silent -u $username:$password "https://0.0.0.0:$port")
    if [[ $result == *"foo"* ]] && [[ $result == *"bar"* ]]; then
      echo "Everything OK."
    else
      echo "Could not share folder on specified port."
    fi
}

teardown() {
    docker ps | grep python_https_server | awk '{print $1}' | xargs docker kill > /dev/null
}

arrange
act
assert
teardown
