import os
import sys
import argparse
import concurrent.futures
import pathlib
import eyed3
from tqdm import tqdm

def rename_file(file_path, log_file):
    try:
        audiofile = eyed3.load(file_path)
        artist = audiofile.tag.artist
        title = audiofile.tag.title
        new_file_name = "{} - {}.mp3".format(artist, title)
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        if os.path.exists(new_file_path):
            new_file_name = "{} - {}_{}.mp3".format(artist, title, os.path.splitext(file_path)[0][-3:])
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        if new_file_path == file_path:
            log_file.write(f"Skipping file: {file_path} - already renamed\n")
            return
        os.rename(file_path, new_file_path)
    except Exception as e:
        log_file.write(f"Error processing file: {file_path} - {e}\n")

def rename_files(root_dir, log_file, verbosity):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        root_dir = pathlib.Path(root_dir)
        mp3_files = [entry.as_posix() for entry in root_dir.rglob("*.mp3")]
        if verbosity > 0:
            print(f"Renaming {len(mp3_files)} MP3 files in {root_dir} and its subdirectories")
        with tqdm(total=len(mp3_files)) as pbar:
            for future in concurrent.futures.as_completed(executor.submit(rename_file, file, log_file) for file in mp3_files):
                pbar.update(1)
                if verbosity > 1:
                    result = future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename MP3 files using ID3 tags")
    parser.add_argument("root_dir", help="Root directory containing MP3 files to rename")
    parser.add_argument("-l", "--log-file", help="File to store the log of the renaming process")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=0, help="Control the amount of output displayed. 0: only errors; 1: progress bar; 2: progress bar and verbose output")
    args = parser.parse_args()

    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print(f"Error: Invalid directory path: {root_dir}")
        sys.exit(1)

    log_file = None
    if args.log_file:
        log_file = open(args.log_file, "w")

    rename_files(root_dir, log_file, args.verbosity)

    if log_file:
        log_file.close()
