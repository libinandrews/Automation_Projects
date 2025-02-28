# -*- coding: utf-8 -*-
"""
Author: Libin Andrews

Purpose:
This script is designed to search for and delete all .AAE files within a specified directory and its subdirectories.
The .AAE files are typically associated with Apple's photo editing metadata, which may not be needed when transferring images.

Encryption:
No encryption is used in this script as it is intended for file deletion only.

Usage:
- Run the script and provide the target directory.
- The script will recursively find and remove all .AAE files.

"""
import os
from typing import List
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

def find_aae_files(directory: str) -> List[str]:
    """Recursively finds all .AAE files in the given directory."""
    aae_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".aae"):
                aae_files.append(os.path.join(root, file))
    return aae_files

def delete_files(files: List[str]):
    """Deletes the given list of files with a progress bar."""
    with Progress(
        TextColumn("[cyan]Deleting .AAE files:[/]"),
        BarColumn(),
        TextColumn("[bold blue]{task.percentage:>3.0f}%[/bold blue]"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("", total=len(files))
        
        for file_path in files:
            try:
                os.remove(file_path)
            except Exception as e:
                console.log(f"[red]Error deleting {file_path}:[/red] {e}")
            finally:
                progress.update(task, advance=1)

def main():
    """Main function to execute the file cleanup process."""
    target_directory = input("Enter the directory to clean up: ")
    if not os.path.isdir(target_directory):
        console.print("[bold red]Invalid directory path.[/bold red]")
        return
    
    console.print(f"[bold cyan]Scanning {target_directory} for .AAE files...[/bold cyan]")
    aae_files = find_aae_files(target_directory)
    
    if not aae_files:
        console.print("[bold yellow]No .AAE files found.[/bold yellow]")
        return
    
    delete_files(aae_files)
    console.print("[bold green]Cleanup complete![/bold green]")

if __name__ == "__main__":
    main()
