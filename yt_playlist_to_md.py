'''
YouTube Playlist Exporter

This script allows users to fetch videos from a YouTube playlist and export them 
to a Markdown file and optionally an Excel file. The generated Markdown file 
provides a checklist format with video links, making it useful for tracking 
progress when watching a playlist.

Features:
- Fetches video titles and URLs from a given YouTube playlist.
- Saves the playlist as a Markdown file (`.md`) with a checkbox list.
- Optionally exports the playlist to an Excel file (`.xlsx`).
- Supports configurable output directories for better reusability.
- Ensures filenames are sanitized for cross-platform compatibility.
- Structured using the SOLID principles for maintainability and extensibility.

Usage:
1. Run the script, provide a YouTube playlist URL, and choose whether to export Excel.
2. The Markdown and Excel files will be saved inside the `output/youtube_playlist_to_md/` folder by default.
3. The script can also be imported as a module in other Python tools for further automation.

'''

import os
import re , time
import pandas as pd
from pytube import Playlist
from pytube.exceptions import PytubeError
from tqdm import tqdm

class YouTubePlaylistExporter:
    """Exports YouTube playlists to Markdown and optionally Excel."""

    def __init__(self, playlist_url: str, output_dir: str = "output/youtube_playlist_to_md", export_excel: bool = False):
        """
        Initializes the exporter.

        :param playlist_url: The URL of the YouTube playlist.
        :param output_dir: The directory where output files will be saved.
        :param export_excel: Boolean flag to indicate if Excel output is needed.
        """
        self.playlist_url = playlist_url
        self.output_dir = output_dir
        self.export_excel = export_excel
        self.video_data = {}

        try:
            self.playlist = Playlist(self.playlist_url)
        except PytubeError as e:
            print(f"Error loading playlist: {e}")
            self.playlist = None

        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def sanitize_filename(title: str) -> str:
        """Sanitizes a title for safe file naming."""
        try:
            pattern = r"[^a-zA-Z0-9\s]"
            sanitized_title = re.sub(pattern, "", title).strip().replace(" ", "_")
            return f"{sanitized_title}.md"
        except Exception as e:
            print(f"Error sanitizing filename: {e}")
            return "playlist.md"



    def fetch_videos(self) -> None:
        """Fetches video titles and URLs with a compact progress bar and dynamic comments."""
        if not self.playlist:
            print("No valid playlist found.")
            return

        with tqdm(
        total=len(self.playlist.videos),
        desc="Fetching Videos",
        bar_format="{l_bar}{bar:20} {n_fmt}/{total_fmt} [elapsed: {elapsed} | remaining: {remaining} | avg: {rate_fmt}] {postfix}",
        dynamic_ncols=True
        ) as pbar:
            for video in self.playlist.videos:
                try:
                    try :
                        title = video.title
                    except Exception as e:
                        title = video.watch_url

                    if not video.watch_url:
                        pbar.set_postfix_str(f"❌ Skipping: {title}")
                        pbar.update(1)
                        continue

                    self.video_data[title] = video.watch_url
                    pbar.set_postfix_str(f"✅ Fetched: {title}")
                except KeyError as e:
                    pbar.set_postfix_str(f"⚠️ Missing data: {e}")

                except PytubeError as e:
                    pbar.set_postfix_str(f"❗ Pytube error: {e}")

                except Exception as e:
                    pbar.set_postfix_str(f"❌ Error: {e}")
                finally :
                    pbar.update(1)




    def export_to_markdown(self) -> str:
        """Exports video details to a Markdown file."""
        try:
            markdown_file = os.path.join(self.output_dir, self.sanitize_filename(self.playlist.title))
            with open(markdown_file, "w", encoding="utf-8") as md_file:
                md_file.write("# Playlist\n\n")
                for title, url in self.video_data.items():
                    md_file.write(f"- [ ] [{title}]({url})\n")
            print(f"Markdown file created: {markdown_file}")
            return markdown_file
        except Exception as e:
            print(f"Error writing Markdown file: {e}")
            return ""

    def export_to_excel(self) -> str:
        """Exports video details to an Excel file."""
        try:
            excel_file = os.path.join(self.output_dir, "playlist_output.xlsx")
            df = pd.DataFrame({"Video Name": self.video_data.keys(), "Video URL": self.video_data.values()})
            df.to_excel(excel_file, index=False)
            print(f"Excel file created: {excel_file}")
            return excel_file
        except Exception as e:
            print(f"Error writing Excel file: {e}")
            return ""

    def run(self) -> None:
        """Executes the full process of fetching and exporting the playlist data."""
        self.fetch_videos()

        if self.video_data:
            self.export_to_markdown()
            if self.export_excel:
                self.export_to_excel()
        else:
            print("No videos were fetched. Exiting.")


def main():
    """Main function to execute the script."""
    playlist_url = input("Enter Playlist URL: ").strip()
    export_excel = input("Do you want Excel Output (y/n): ").strip().lower() == "y"

    exporter = YouTubePlaylistExporter(playlist_url, export_excel=export_excel)
    exporter.run()


if __name__ == "__main__":
    main()
