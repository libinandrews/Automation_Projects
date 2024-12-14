import os
import re
import pandas as pd
from pytube import Playlist, YouTube


markdown_file_path = input(r"Enter the Markdown File path to save the File : ")
playlist_url = input("Enter Playlist URL : ")
excel_bool = input("Dou you want Excel Output (y/n) : ")
playlist = Playlist(playlist_url)
out_dict = {}
FileName = str(playlist.title)
pattern = r"[^a-zA-Z0-9\s]"
FileName = re.sub(pattern, "", FileName)
FileName = FileName.replace(" ", "_") + ".md"
markdown_file_path = os.path.join(markdown_file_path, FileName)
for video in playlist.videos:
    # print(video.title)
    out_dict[video.title] = video.watch_url
Pandas_Data = dict()
if not excel_bool.lower() == "n":
    Pandas_Data["Video_Name"] = out_dict.keys()
    Pandas_Data["Video_Url"] = out_dict.values()
    df = pd.DataFrame(Pandas_Data)
    df.to_excel("output.xlsx", index=False)
with open(markdown_file_path, "wb") as md_file:
    md_file.write("# Play List\n\n".encode("utf-8"))
    for file_name, file_path in out_dict.items():
        md_file.write(f"- [ ] [{file_name}]({file_path})     \n".encode("utf-8"))
print(f"Script created successfully {markdown_file_path}")
