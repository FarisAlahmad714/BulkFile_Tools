import cv2
import numpy as np
import os

def process_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                # Read image with original quality
                img = cv2.imread(input_path)
                height, width = img.shape[:2]
                
                # Create copy for safe manipulation
                working_copy = img.copy()
                
                # Define protected areas
                text_area_height = int(height * 0.1)      # Bottom 10% for text
                time_scale_height = int(height * 0.05)    # Additional 5% for datetime scale
                legend_width = int(width * 0.15)          # Left 15% for colored indicators
                
                # Split image into regions
                main_area = working_copy[:-text_area_height-time_scale_height, legend_width:]
                legend_area = working_copy[:-text_area_height-time_scale_height, :legend_width]
                time_scale_area = working_copy[-text_area_height-time_scale_height:-text_area_height, :]
                bottom_area = working_copy[-text_area_height:, :]
                
                # Process only the main chart area
                lower_white = np.array([245, 245, 245], dtype=np.uint8)
                upper_white = np.array([255, 255, 255], dtype=np.uint8)
                
                # Create precise mask for main area
                mask = cv2.inRange(main_area, lower_white, upper_white)
                inverse_mask = cv2.bitwise_not(mask)
                
                # Create black background for main area
                black_bg = np.zeros_like(main_area)
                
                # Combine foreground and background for main area
                foreground = cv2.bitwise_and(main_area, main_area, mask=inverse_mask)
                background = cv2.bitwise_and(black_bg, black_bg, mask=mask)
                processed_main_area = cv2.add(foreground, background)
                
                # Process legend area (preserve colors, only convert pure white)
                legend_mask = cv2.inRange(legend_area, lower_white, upper_white)
                legend_inverse_mask = cv2.bitwise_not(legend_mask)
                legend_black_bg = np.zeros_like(legend_area)
                
                legend_foreground = cv2.bitwise_and(legend_area, legend_area, mask=legend_inverse_mask)
                legend_background = cv2.bitwise_and(legend_black_bg, legend_black_bg, mask=legend_mask)
                processed_legend_area = cv2.add(legend_foreground, legend_background)
                
                # Combine all regions back together
                top_half = np.hstack((processed_legend_area, processed_main_area))
                # Stack the regions vertically: main chart area, time scale, and bottom text
                result = np.vstack((top_half, time_scale_area, bottom_area))
                
                # Preserve quality settings
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    cv2.imwrite(output_path, result, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                elif filename.lower().endswith('.png'):
                    cv2.imwrite(output_path, result, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                else:
                    cv2.imwrite(output_path, result)
                    
                print(f"Processed: {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    process_images("input_images", "output_images")