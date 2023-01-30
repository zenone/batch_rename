# Batch MP3 Renamer 🎶
A Python script that uses EyeD3 to batch rename MP3 files based on the ID3 tags.

This script standardizes the filenames of MP3 files for DJing. My preferred filenaming system is "Artist - Title (Remix title).mp3", which eliminates extraneous information, such as track number which isn't useful for DJs. Sorting the directory listing alphabetically by artist results in a well-organized collection of songs.

## Features 🎉
- Recursively looks through subdirectories for MP3 files
- Renames files to "ARTIST - TITLE.mp3" format
- Handles missing ID3 tags and new file name conflicts
- Uses concurrent processing for faster processing
- Source directory can be given as a command line argument
- Logs errors in a separate file

## Usage 📖
```python batch_rename.py -d <source_directory> [-v <verbosity_level>]```


## Requirements 💻
- Python 3.x
- EyeD3 library

## Contributing 🤝
This project welcomes contributions and suggestions. Feel free to open an issue or create a pull request.

## License 🔓
This project is licensed under the MIT License.
