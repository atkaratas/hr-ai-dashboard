import os
from PIL import Image

def process_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            # Siyah-beyaz yap
            img = img.convert('L')
            # Boyutu küçült (maksimum genişlik 1000px, oran korunarak)
            max_width = 1000
            if img.width > max_width:
                w_percent = (max_width / float(img.width))
                h_size = int((float(img.height) * float(w_percent)))
                img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
            # Düşük kalite ile kaydet (optimize)
            img.save(output_path, "JPEG", quality=40, optimize=True)
            print(f"Image processed: {output_path} ({os.path.getsize(output_path) // 1024} KB)")
            return True
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

if __name__ == "__main__":
    # Test için mevcut fişi küçültelim
    process_image("projects/hr_ai_system/media/M-009.jpg", "projects/hr_ai_system/media/M-009.jpg")
