import os
import sys
import argparse
import concurrent.futures
import pathlib
import eyed3
from tqdm import tqdm


def rename_file(file_path, log_file):
    """Rename a single MP3 file using its ID3 tag information.

    :param file_path: The path of the MP3 file to rename.
    :param log_file: The log file to write any error messages to.
    """
    try:
        # Load the MP3 file using the eyeD3 library.
        audiofile = eyed3.load(file_path)

        # Get the artist and title information from the MP3 file's ID3 tag.
        artist = audiofile.tag.artist
        title = audiofile.tag.title

        # Generate the new file name based on the artist and title information.
        new_file_name = "{} - {}.mp3".format(artist, title)

        # Generate the new file path based on the new file name and the original file's directory.
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # If a file already exists with the new file name, add a suffix to the new file name to ensure uniqueness.
        if os.path.exists(new_file_path):
            new_file_name = "{} - {}_{}.mp3".format(artist, title, os.path.splitext(file_path)[0][-3:])
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        # If the new file path is the same as the original file path, skip renaming the file.
        if new_file_path == file_path:
            log_file.write(f"Skipping file: {file_path} - already renamed\n")
            return

        # Rename the MP3 file.
        os.rename(file_path, new_file_path)
    except Exception as e:
        # Write any errors to the log file.
        log_file.write(f"Error processing file: {file_path} - {e}\n")


def rename_files(root_dir, log_file, verbosity):
    """
    Batch rename MP3 files using ID3 tags

    :param root_dir: Root directory containing MP3 files to rename
    :param log_file: File to store the log of the renaming process
    :param verbosity: Control the amount of output displayed. 0: only errors; 1: progress bar; 2: progress bar and verbose output
    """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Convert root_dir to a Path object
        root_dir = pathlib.Path(root_dir)

        # Get a list of all MP3 files in the root_dir and its subdirectories
        mp3_files = [entry.as_posix() for entry in root_dir.rglob("*.mp3")]

        if verbosity > 0:
            print(f"Renaming {len(mp3_files)} MP3 files in {root_dir} and its subdirectories")

        # Use tqdm to show a progress bar
        with tqdm(total=len(mp3_files)) as pbar:
            # Use concurrent.futures to run the rename_file function in parallel
            for future in concurrent.futures.as_completed(executor.submit(rename_file, file, log_file) for file in mp3_files):
                # Increment the progress bar
                pbar.update(1)

                if verbosity > 1:
                    # Get the result of the rename_file function
                    result = future.result()


if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Batch rename MP3 files using ID3 tags")
    parser.add_argument("root_dir", help="Root directory containing MP3 files to rename")
    parser.add_argument("-l", "--log-file", help="File to store the log of the renaming process")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=0, help="Control the amount of output displayed. 0: only errors; 1: progress bar; 2: progress bar and verbose output")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the root directory is a valid directory
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print(f"Error: Invalid directory path: {root_dir}")
        sys.exit(1)

    # Open the log file if specified
    log_file = None
    if args.log_file:
        log_file = open(args.log_file, "w")

    # Call the rename_files function with the root directory, log file, and verbosity level
    rename_files(root_dir, log_file, args.verbosity)

    # Close the log file if it was opened
    if log_file:
        log_file.close()
