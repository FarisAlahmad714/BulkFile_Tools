from pydub import AudioSegment
import os

# Source and destination folder
source_folder = "MZ Drum Kit 2019"
output_folder = "MZ Drum Kit 2019 MP3"  # New folder to avoid overwriting originals

# Create output folder if it doesn’t exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Supported formats
input_formats = ('.wav', '.mp3')

# Walk through all subfolders and files
for root, dirs, files in os.walk(source_folder):
    # Replicate subfolder structure in output
    relative_path = os.path.relpath(root, source_folder)
    current_output_folder = os.path.join(output_folder, relative_path)
    if not os.path.exists(current_output_folder):
        os.makedirs(current_output_folder)

    for file in files:
        if file.lower().endswith(input_formats):
            input_path = os.path.join(root, file)
            # Output name: replace extension with .mp3
            output_name = os.path.splitext(file)[0] + '.mp3'
            output_path = os.path.join(current_output_folder, output_name)

            print(f"Converting: {input_path} -> {output_path}")
            try:
                # Load audio file
                audio = AudioSegment.from_file(input_path)
                # Export as MP3, 192kbps (good quality, small size)
                audio.export(output_path, format="mp3", bitrate="192k")
                print(f"Success: {output_path}")
            except Exception as e:
                print(f"Error converting {input_path}: {e}")

print("Conversion complete!")