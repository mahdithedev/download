import argparse
import os
import re
import subprocess
import sys

def download_and_move_files(uri, file_extension, start, end , storage):
    # download the webpage i use curl beacuse i just want to stick to the stdlib of python
    webpage = subprocess.check_output(["curl" , uri]).decode("utf-8")
    # extract all URLs that end with the specified file extension
    pattern = f"(https?:\/\/[^\s]+){file_extension}"

    urls = [url + file_extension for url in re.findall(pattern, webpage)]

    if len(urls) == 0:
        pattern = f"href=[^\s]+{file_extension}"
        urls = [uri + url[6:] for url in re.findall(pattern , webpage)]

    print(f"\033[92m{len(urls)} URLs extracted.\033[00m")

    # set end to len(urls) if end value is -1
    if end == -1:
        end = len(urls)

    # check if start and end are valid
    if start < 0 or end > len(urls) or start >= end:
        print("Invalid values for start and end.")
        sys.exit()

    # download and move files
    for i, file_url in enumerate(urls):
        if i < start or i >= end:
            continue
        filename = os.path.basename(file_url)
        try:
            subprocess.run(["curl", "-o", filename, file_url], check=True , )
            if storage:
                subprocess.run(["mv", filename, storage], check=True)
            print(f"\033[92mDownloaded {filename} successfully.\033[00m ")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mFailed to download {filename}. Error: {e}\033[00m")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="URL of the webpage to download")
    parser.add_argument("-f", "--file_extension", type=str, default=".mkv", help="File extension to extract (default: .mkv)")
    parser.add_argument("-s", "--start", type=int, default=0, help="The starting url to download (default: 0)")
    parser.add_argument("-e", "--end", type=int, default=-1, help="The last url to download (default: -1)")
    parser.add_argument("-env", "--envorinment", type=str, default="Termux", help="The envorinment that this script is running on Termux or other")

    args = parser.parse_args()

    if args.envorinment == "Termux":
        storage = "/sdcard/DCIM"
    else:
        storage = None

    download_and_move_files(args.url, args.file_extension, args.start, args.end , storage)