"""
Created on May 21, 2024
@author: andrewslibin@gmail.com
Update : May 21, 2024- Initial version
Updated by : andrewslibin@gmail.com
"""

import os
import re
from moviepy.editor import VideoFileClip


def find_mf4_files(folder):
    """
    Finds all .mp4 files in the given folder and its subfolders.

    Args:
        folder (str): The folder to search for .mp4 files.

    Returns:
        list: A list of paths to the found .mp4 files.
    """
    mf4_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp4"):
                mf4_files.append(os.path.join(root, file))
    return mf4_files


def get_video_length(mp4_file):
    """
    Returns the duration of a video file in seconds.

    Args:
        mp4_file (str): The path to the video file.

    Returns:
        float: The duration of the video in seconds.
    """
    clip = VideoFileClip(mp4_file)
    video_length = clip.duration
    return video_length


import re


def create_markdown_file(mf4_file_paths, out_dict, markdown_file_path):
    """
    Creates a markdown file with a list of MP4 files and their durations.

    Parameters:
        mf4_file_paths (list): List of file paths of MP4 files.
        out_dict (dict): Dictionary of file names and file paths.
        markdown_file_path (str): Path to the markdown file to be created.
    """

    with open(markdown_file_path, "wb") as md_file:
        md_file.write("# ALL_MP4_FILES \n\n".encode("utf-8"))
        total = len(mf4_file_paths)
        n = 0
        for file_name, file_path in out_dict.items():
            n += 1
            try:
                length = get_video_length(file_path)
                pattern = r"[^a-zA-Z0-9\s]"
                file_name = re.sub(pattern, "", file_name)
                md_file.write(
                    f"- [ ] {int(length/60)} Min_{file_name} \n ```{file_path}```     \n".encode(
                        "utf-8"
                    )
                )
                print(f"{n}/{total} completed file - {file_name}")
            except Exception as e:
                print(e)


# Example usage
folder_path = "C:\data_home"
markdown_file_path = os.path.join(folder_path, "ALL_MP4_FILES.md")
mf4_file_paths = find_mf4_files(folder_path)
out_dict = {}
for file in mf4_file_paths:
    out_dict[os.path.basename(file).replace(".mp4", "")] = file

with open(markdown_file_path, "wb") as md_file:
    md_file.write("# ALL_MP4_FILES \n\n".encode("utf-8"))
    total = len(mf4_file_paths)
    n = 0
    for file_name, file_path in out_dict.items():
        n += 1
        try:
            length = get_video_length(file_path)
            pattern = r"[^a-zA-Z0-9\s]"
            name = re.sub(pattern, "", file_name)
            md_file.write(
                f"- [ ] {int(length/60)} Min_{name} \n \n ```{file_path}```     \n".encode(
                    "utf-8"
                )
            )
            md_file.write(f"![[{file_name}.mp4]] \n \n *** \n \n ".encode("utf-8"))
            print(f"{n}/{total} completed file - {file_name}")
        except Exception as e:
            print(e)
print(markdown_file_path)
