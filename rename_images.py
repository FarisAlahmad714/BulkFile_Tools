import os
import uuid
import argparse
from os.path import join, splitext, getmtime, getctime, isfile

def main():
    parser = argparse.ArgumentParser(description='Rename images chronologically.')
    parser.add_argument('--directory', default='.', help='Target directory (default: current)')
    parser.add_argument('--sort-by', choices=['mtime', 'ctime'], default='mtime',
                       help='Sort by modification (mtime) or creation time (ctime)')
    args = parser.parse_args()

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    files = [f for f in os.listdir(args.directory) 
             if isfile(join(args.directory, f)) and 
             splitext(f)[1].lower() in image_extensions]

    if not files:
        print("No image files found.")
        return

    # Sort files by specified time attribute
    sort_func = getmtime if args.sort_by == 'mtime' else getctime
    files.sort(key=lambda x: sort_func(join(args.directory, x)))

    # Generate unique temporary prefix
    temp_prefix = f"temp_{uuid.uuid4().hex}_"
    temp_files = []

    try:
        # First pass: rename to temporary names
        for idx, filename in enumerate(files, 1):
            src = join(args.directory, filename)
            ext = splitext(filename)[1]
            temp_name = f"{temp_prefix}{idx}{ext}"
            dst = join(args.directory, temp_name)
            os.rename(src, dst)
            temp_files.append((dst, ext))
            print(f"Temporary: {filename} -> {temp_name}")

        # Second pass: rename to final numbered names
        for idx, (temp_path, ext) in enumerate(temp_files, 1):
            new_name = f"{idx}{ext}"
            new_path = join(args.directory, new_name)
            os.rename(temp_path, new_path)
            print(f"Renamed: {os.path.basename(temp_path)} -> {new_name}")

        print(f"\nSuccessfully renamed {len(files)} files.")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("Attempting to roll back changes...")
        # Rollback temporary renames
        for temp_path, _ in temp_files:
            if isfile(temp_path):
                os.rename(temp_path, join(args.directory, files[len(temp_files)-1]))
        print("Rollback completed. No changes were made.")

if __name__ == "__main__":
    main()