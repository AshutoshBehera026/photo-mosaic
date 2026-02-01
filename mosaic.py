import os
import glob
import argparse
import sys
import logging
import random
import numpy as np
from PIL import Image, ImageOps, ImageDraw

# ==========================================
# 1. LOGGING & USAGE SETUP
# ==========================================
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler("mosaic.log"), logging.StreamHandler(sys.stdout)]
    )

def print_usage_guide(error_msg=None):
    if error_msg:
        print(f"\n❌ ERROR: {error_msg}")
    
    guide = """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🚀 PHOTO MOSAIC PRO (CLI VERSION)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    REQUIRED:
    --target    : Path to the main large photo.
    --tiles     : Folder path containing your small photos.

    OPTIONAL:
    --output    : Destination path (default: output/result.jpg)
    --density   : Grid width in tiles (default: 100)
    --blend     : Original color overlay 0.0-1.0 (default: 0.15)
    --tile_size : Resolution of each tile in px (default: 50)
    --random    : Variety factor. Higher = more shuffle (default: 5)
    --msg       : Custom text at bottom-right (e.g., "Pune 2026")

    EXAMPLE:
    python mosaic.py --target main.jpg --tiles ./pics --density 120 --msg "HIN x BBSR" --output output/mosaic_result.jpg
    python mosaic.py --target "D:\Downloads\Gemini_Generated_Image_tn9bgvtn9bgvtn9b.png" --tiles D:\Pictures\Wallpapers --blend 0.5 --output output/mosaic_result.jpg
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(guide)

# ==========================================
# 2. IMAGE PROCESSING FUNCTIONS
# ==========================================
def process_single_tile(img_path, size):
    """Failsafe image loading and center-cropping."""
    try:
        valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
        if not img_path.lower().endswith(valid_exts):
            return None, None

        with Image.open(img_path) as img:
            img = img.convert('RGB')
            # Center-crop 1:1 ratio
            img = ImageOps.fit(img, (size, size), Image.Resampling.LANCZOS)
            avg_col = np.mean(np.array(img), axis=(0, 1))
            return img, avg_col
    except Exception:
        return None, None

def add_text_overlay(canvas, message):
    """Adds a subtle watermark to the bottom right."""
    try:
        draw = ImageDraw.Draw(canvas)
        width, height = canvas.size
        # Simple text placement
        draw.text((width - 150, height - 30), message, fill=(255, 255, 255))
        logging.info(f"Added message: {message}")
    except Exception as e:
        logging.warning(f"Could not add text: {e}")

# ==========================================
# 3. CORE LOGIC
# ==========================================
def create_mosaic():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--target")
    parser.add_argument("--tiles")
    parser.add_argument("--output", default="output/mosaic_result.jpg")
    parser.add_argument("--density", type=int, default=100)
    parser.add_argument("--blend", type=float, default=0.15)
    parser.add_argument("--tile_size", type=int, default=50)
    parser.add_argument("--random", type=int, default=5)
    parser.add_argument("--msg", type=str, default="")
    parser.add_argument('--help', action='store_true')

    args = parser.parse_args()

    # --- FAILSAFE ARGUMENT CHECK ---
    if args.help or not args.target or not args.tiles:
        print_usage_guide()
        sys.exit()
    if not os.path.exists(args.target) or not os.path.isdir(args.tiles):
        print_usage_guide("Path error: Ensure target file and tiles folder exist.")
        sys.exit()

    setup_logging()
    
    # 1. Load Tiles
    logging.info(f"Loading tiles from {args.tiles}...")
    all_files = glob.glob(os.path.join(args.tiles, "*"))
    processed_tiles = []
    
    for f in all_files:
        tile_img, avg_col = process_single_tile(f, args.tile_size)
        if tile_img:
            processed_tiles.append((tile_img, avg_col))
    
    if not processed_tiles:
        logging.error("No valid images found. Check folder.")
        return

    # 2. Setup Target Canvas
    try:
        with Image.open(args.target) as target:
            target = target.convert('RGB')
            ratio = target.size[1] / target.size[0]
            num_h = int(args.density * ratio)
            
            small_target = target.resize((args.density, num_h), Image.Resampling.LANCZOS)
            blend_overlay = target.resize((args.density * args.tile_size, num_h * args.tile_size), Image.Resampling.LANCZOS)
            mosaic_canvas = Image.new('RGB', (args.density * args.tile_size, num_h * args.tile_size))

        # 3. Stitching (With Shuffling & Randomness)
        logging.info(f"Building {args.density}x{num_h} grid...")
        for x in range(args.density):
            if x % (args.density // 10 + 1) == 0:
                logging.info(f"Progress: {int((x/args.density)*100)}%")
                
            for y in range(num_h):
                target_rgb = np.array(small_target.getpixel((x, y)))
                
                # Find best N matches and pick one randomly (Shuffle Logic)
                distances = [np.linalg.norm(t[1] - target_rgb) for t in processed_tiles]
                # Partitioning is faster than full sort O(n) vs O(n log n)
                top_indices = np.argpartition(distances, args.random)[:args.random]
                chosen_idx = random.choice(top_indices)
                
                mosaic_canvas.paste(processed_tiles[chosen_idx][0], (x * args.tile_size, y * args.tile_size))

        # 4. Final Polish
        if args.blend > 0:
            mosaic_canvas = Image.blend(mosaic_canvas, blend_overlay, alpha=args.blend)
        
        if args.msg:
            add_text_overlay(mosaic_canvas, args.msg)

        # Ensure output folder exists
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        mosaic_canvas.save(args.output, quality=95)
        logging.info(f"✅ DONE! Result: {args.output}")

    except Exception as e:
        logging.error(f"Critical error during build: {e}")

if __name__ == "__main__":
    create_mosaic()