# Batch MP3 Renamer 🎶
A Python script that uses EyeD3 to batch rename MP3 files based on the ID3 tags.

This script standardizes the filenames of MP3 files for DJing. My preferred filenaming system is "Artist - Title (Remix title).mp3", which eliminates extraneous information, such as track number which isn't useful for DJs. Sorting the directory listing alphabetically by artist results in a well-organized collection of songs.

## Features 🎉
- Recursively looks through subdirectories for MP3 files
- Renames files to "ARTIST - TITLE.mp3" format
- Handles missing ID3 tags and new file name conflicts
- Uses concurrent processing for faster processing
- Source directory can be given as a command line argument
- Displays the progress of the renaming process
- Logs errors in a separate file

## Usage 📖
```python batch_rename.py [-h] [-l LOG_FILE] [-v {0,1,2}] root_dir```

### Basic Usage
```python batch_rename.py /path/to/mp3/folder```

### Usage With Log File
```python batch_rename.py /path/to/mp3/folder -l /path/to/logfile.txt```

### Usage With Verbosity
```python batch_rename.py /path/to/mp3/folder -v 2```

### Usage With Both Log File and Verbosity
```python batch_rename.py /path/to/mp3/folder -l /path/to/logfile.txt -v 1```

## Requirements 💻
- Python 3.x
- EyeD3 library: EyeD3 is a Python library used for reading and manipulating ID3 tags of MP3 files. It is used in this project to extract artist and title information from the ID3 tags to rename the MP3 files.
- TQDM library: TQDM is a Python library used for displaying progress bars. It is used in this project to show the progress of the renaming process.

## Contributing 🤝
This project welcomes contributions and suggestions. Feel free to open an issue or create a pull request.

## License 🔓
This project is licensed under the [MIT License](https://mit-license.org/).
