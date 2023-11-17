import sys

import scan_folder
import move_files
import remove_empty_folders
import organize_files

def main():
    folder_path = sys.argv[1]
    destination_path = folder_path
    files, unknown_extensions = scan_folder(folder_path)

    move_files(folder_path, destination_path)
    remove_empty_folders(folder_path)
    organize_files(files, destination_path)

    print("List of files by type:")
    for category, file_list in files.items():
        print(f"{category}: {', '.join(file_list)}")

    print("Unknown extensions:")
    print(', '.join(unknown_extensions))


if __name__ == "__main__":
    main()