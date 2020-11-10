#! /usr/bin/python3

from dialog import Dialog
import json
import math
import os
import requests
import subprocess
import sys

destination = "/mnt/VeraA/incomplete"
torrent = "new_torrent.torrent"


def setup():
    try:
        os.remove(destination+"/"+torrent)
    except OSError:
        pass


def construct_url(argv):
    tracker = argv[2]
    username = argv[0]
    token = argv[1]
    query = "%20".join(argv[3:])
    url = tracker+'/api.php?username='+username+'&passkey=' + \
        token+'&action=search-torrents&type=name&query='+query
    return url


def get_results(url):
    results = requests.get(url).text
    return results


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s%s" % (s, size_name[i])


def prefilter(raw_data):
    result = {}
    for element in raw_data:
        result[str(element["id"])] = {
            "name": element["name"],
            "link": element["download_link"],
            "size": convert_size(int(element["size"])),
            "seeders": str(element["seeders"])}

    return result

def download(url, file_name):
    print("Downloading: ", url)
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

def make_dialog(input):
    def format(key, value):
        rest_of_line = str(value[0]).ljust(
            3)+" "+str(value[1]).ljust(6)+" "+str(value[2])
        line = (key, rest_of_line)
        return line

    def sort_list_of_tuples(input, column):
        return sorted(input, key=lambda x: x[column], reverse=True)

    def to_list_of_tuples(input):
        output = []

        for key, value in input.items():
            output.append(
                (key, int(value["seeders"]), value["size"], value["name"]))
        return output

    def squash_to_kv_pair(items):
        output = []
        for item in items:
            output.append(format(item[0], item[1:]))
        print(output)
        return output

    def create_choices(input):
        list_of_tuples = to_list_of_tuples(input)
        list_of_tuples = sort_list_of_tuples(list_of_tuples, column=1)
        return squash_to_kv_pair(list_of_tuples)

    d = Dialog(dialog="dialog")
    d.set_background_title("Download")

    choices = create_choices(input)

    code, tag = d.menu("Results:",
                       choices=choices)
    if code == d.OK:
        print(tag)
        return input[tag]["link"]

    return None


def delegate_to_transmission():
    process = subprocess.Popen(["transmission-remote", "localhost:9091", "-a", destination+"/"+torrent],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)


def main(argv):
    setup()
    url = construct_url(argv)
    results = get_results(url)
    filtered = prefilter(json.loads(results))
    if filtered:
        torrent_url = make_dialog(filtered)
        if torrent_url:
            download(torrent_url, destination+"/"+torrent)
            delegate_to_transmission()
    else:
        print("No results.")


if __name__ == "__main__":
    main(sys.argv[1:])
