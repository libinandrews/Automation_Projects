# Automation_Projects
All tools developed by myself for personal purposes.

# Youtube Tools
- Convert YouTube playlist to Obsidian checklist (With Links) - 01_Youtube_Tools/youtube_playlist_to_md.py
    - Use case for this tool: You are studying a YouTube playlist in your free time, and you need to track the videos you've watched. You can use this tool
---
# Generate Requiements.txt

    ##**Overview: `generate_requirements.py`**

    This Python script generates a `requirements.txt` file by capturing the installed Python packages and their versions from a specified Python interpreter or virtual environment. It uses the `pip freeze` command to list the packages and saves the output to a text file, making it easy to replicate the environment.

    ### **Usage**
    - Provide the path to the Python interpreter (e.g., from a virtual environment) and specify where to save the `requirements.txt` file.
    - The script will generate a `requirements.txt` with all installed packages.

---
# Obsidian Tool
    ## Generate Mf4 to List

        ## **Overview**
        This script scans a folder (and its subfolders) for `.mp4` files, retrieves the duration of each video, and generates a markdown file listing the videos with their durations and file paths.

        ## **Key Functions**

        ### `find_mf4_files(folder)`
        - Searches for all `.mp4` files in the specified folder and subfolders.
        - **Returns**: List of file paths to `.mp4` files.

        ### `get_video_length(mp4_file)`
        - Retrieves the duration of a given `.mp4` file in seconds.
        - **Returns**: Duration in seconds.

        ### `create_markdown_file(mf4_file_paths, out_dict, markdown_file_path)`
        - Creates a markdown file listing video names, durations (in minutes), and file paths.
        - **Arguments**:
        - `mf4_file_paths`: List of `.mp4` file paths.
        - `out_dict`: Dictionary of file names and paths.
        - `markdown_file_path`: Path where the markdown file will be saved.

        ## **Usage**
        1. Provide the folder path to search for `.mp4` files.
        2. The script will generate a markdown file (`ALL_MP4_FILES.md`) listing all `.mp4` files with their durations and paths.

