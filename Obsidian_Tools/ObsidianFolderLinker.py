'''
Created on July 05, 2024
@author: andrewslibin@gmail.com
Update : Jul 05, 2024- Initial version
Updated by : andrewslibin@gmail.com
'''
import os
import re
import os
import re

class ObsidianFolderLinker:
    def __init__(self, file_path, directory):
        self.file_path = file_path
        self.directory = directory
        self.excluded_folders = [""]

    def read_markdown_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def read_all_folders(self, root, file_path):
        content = self.read_markdown_file(file_path) if os.path.exists(file_path) else ""
        content = content.strip()
        read_data = content

        for dir_name in os.listdir(root):
            path = os.path.join(root, dir_name)
            if dir_name.startswith('.') or os.path.isfile(path) or f'[[{dir_name}]]' in content:
                continue

            print(f"Root: {dir_name}")
            if not re.search("## Archive", content):
                content += '  \n## Archive'
            content += f'  \n[[{dir_name}]]'

        if content != read_data or len(content) == 0:
            with open(file_path, 'w') as file:
                file.write(content)

        for dir_name in os.listdir(root):
            path = os.path.join(root, dir_name)
            if dir_name.startswith('.') or os.path.isfile(path) or dir_name in self.excluded_folders:
                continue
            sub_file_name = os.path.join(path, f'{dir_name}.md')
            self.read_all_folders(path, sub_file_name)


if __name__ == "__main__":
    # Specify the directory and file path
    file = "Home_Page.md"
    root = r"C:\Obsidian_Data"
    file_path = os.path.join(root,file)

    # Instantiate the class and call the method
    processor = ObsidianFolderLinker(file_path, root)
    processor.read_all_folders(root, file_path)
