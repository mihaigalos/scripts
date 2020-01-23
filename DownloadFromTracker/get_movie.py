#! /usr/bin/python3

from dialog import Dialog
import json
import requests
import sys
import subprocess
import os

destination = "/mnt/Vera_SeagateC/incomplete"
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


def prefilter(raw_data):
    result = {}
    i = 0
    for element in raw_data:
        result[str(element["id"])] = {
            "name": element["name"],
            "link": element["download_link"],
            "seeders": str(element["seeders"])}

        if i == 10:
            break
        i += 1
    return result


def download(url, output_file):
    print("Downloading: ", url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()


def make_dialog(input):
    def to_list_of_tuples(input):
        result = []

        for k, v in input.items():
            result.append((k, v["seeders"]+" "+v["name"]))
        return result
    d = Dialog(dialog="dialog")
    d.set_background_title("Dialog")

    choices = to_list_of_tuples(input)

    code, tag = d.menu("OK, then you have two options:",
                       choices=choices)
    if code == d.OK:
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
    torrent_url = make_dialog(filtered)

    if torrent_url:
        download(torrent_url, destination+"/"+torrent)
        delegate_to_transmission()


if __name__ == "__main__":
    main(sys.argv[1:])
