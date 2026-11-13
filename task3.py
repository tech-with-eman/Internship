import os
import shutil
from pathlib import Path

# Extension mapping dictionary
EXTENSION_MAP = {
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.doc': 'Documents',
    '.txt': 'Documents',
    '.xlsx': 'Documents',
    '.csv': 'Documents',
    '.pptx': 'Documents',
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.svg': 'Images',
    '.webp': 'Images',
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.avi': 'Videos',
    '.mov': 'Videos',
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.7z': 'Archives',
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',
    '.css': 'Code',
    '.cpp': 'Code',
    '.java': 'Code',
    '.sql': 'Code',
    '.json': 'Code'
}

def organize_directory(target_dir):
    path = Path(target_dir).resolve()
    if not path.exists():
        print(f"❌ Error: The directory '{target_dir}' does not exist.")
        return

    print("========================================")
    print("  AUTOMATED FILE ORGANIZER & CLEANUP   ")
    print("========================================")
    print(f"Target Directory: {path}\n")

    relocated_count = 0
    error_count = 0

    # Scan directory using os.scandir
    with os.scandir(path) as entries:
        for entry in entries:
            # Skip directories and hidden files/folders
            if entry.is_file() and not entry.name.startswith('.'):
                file_path = Path(entry.path)
                ext = file_path.suffix.lower()

                # Determine category folder (defaults to 'Others')
                category = EXTENSION_MAP.get(ext, 'Others')
                destination_folder = path / category

                try:
                    # Create category subfolder if it doesn't exist
                    destination_folder.mkdir(exist_ok=True)
                    
                    destination_path = destination_folder / file_path.name

                    # Safely handle naming collisions (FileExistsError prevention)
                    if destination_path.exists():
                        base_name = file_path.stem
                        counter = 1
                        while destination_path.exists():
                            new_filename = f"{base_name}_{counter}{ext}"
                            destination_path = destination_folder / new_filename
                            counter += 1

                    # Move file securely
                    shutil.move(str(file_path), str(destination_path))
                    print(f"✅ Moved: {file_path.name} -> /{category}/")
                    relocated_count += 1

                except PermissionError:
                    print(f"⚠️ Permission Denied: Cannot access or move '{file_path.name}'.")
                    error_count += 1
                except Exception as e:
                    print(f"❌ Error moving '{file_path.name}': {e}")
                    error_count += 1

    print("\n" + "="*42)
    print("          EXECUTION SUMMARY             ")
    print("="*42)
    print(f"Total files successfully relocated: {relocated_count}")
    print(f"Encountered errors / skipped:      {error_count}")
    print("="*42)

if __name__ == "__main__":
    target = input("Enter path of the directory to organize (press Enter for current directory): ").strip()
    if not target:
        target = "."
    organize_directory(target)