import os
from PIL import Image
import argparse

def crop_16_9_to_ultrawide(image_path, output_path):
    """Crops 3840x2160 images to 3840x1664 with center alignment"""
    with Image.open(image_path) as img:
        if img.size != (3840, 2160):
            raise ValueError(f"Invalid image size {img.size} - expected 3840x2160")
        
        # Calculate crop coordinates (left, upper, right, lower)
        crop_box = (0, 248, 3840, 2160 - 248)
        cropped = img.crop(crop_box)
        cropped.save(output_path)
        return True

def main():
    parser = argparse.ArgumentParser(description='Crop 3840x2160 images to 3840x1664')
    parser.add_argument('--input', default='imgs', 
                      help='Input directory (default: "imgs")')
    parser.add_argument('--output', default='cropped',
                      help='Output directory (default: "cropped")')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    processed = 0
    skipped = []
    
    for filename in os.listdir(args.input):
        input_path = os.path.join(args.input, filename)
        output_path = os.path.join(args.output, filename)
        
        try:
            if crop_16_9_to_ultrawide(input_path, output_path):
                print(f"✓ Cropped {filename}")
                processed += 1
        except Exception as e:
            print(f"✗ Skipping {filename}: {str(e)}")
            skipped.append(filename)
    
    print(f"\nFinished processing: {processed} images cropped")
    if skipped:
        print(f"Skipped {len(skipped)} files:")
        for name in skipped:
            print(f"  - {name}")

if __name__ == "__main__":
    main()