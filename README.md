# 📸 Pro Photo Mosaic Creator

A robust Python tool that transforms a single "Big Picture" into a high-resolution mosaic composed of hundreds of tiny "Tile" photos. Perfect for anniversary gifts, posters, or digital art.

## ✨ Key Features

-   **Smart Center-Crop:** Automatically squares your tile photos (1:1) to prevent squashing.
-   **Top-K Randomness:** Uses Euclidean distance to find color matches but shuffles between the top candidates to avoid repetitive patterns.
-   **Color Blending:** Subtly overlays the original image's colors for professional-grade clarity.
-   **Robust Logging:** Tracks progress and catches non-image files automatically without crashing.

## 🛠️ Installation

1. Clone the repository:

    ```bash
    git clone [https://github.com/yourusername/photo-mosaic-pro.git](https://github.com/yourusername/photo-mosaic-pro.git)
    ```

2. Navigate to the folder:

```bash
cd photo-mosaic-pro

```

3. Install dependencies:

```bash
pip install -r requirements.txt

```

## 🚀 Usage

Trigger the script via terminal with your custom images:

```bash
python mosaic.py --target "main.jpg" --tiles "./my_folder" --density 120 --msg "HIN x BBSR"

```

### Arguments:

| Argument    | Description                               | Default           |
| ----------- | ----------------------------------------- | ----------------- |
| `--target`  | Path to the main base image (Required)    | -                 |
| `--tiles`   | Folder containing small photos (Required) | -                 |
| `--output`  | Destination path for the result           | output/result.jpg |
| `--density` | Number of tiles across the width          | 100               |
| `--blend`   | Original color overlay (0.0 to 1.0)       | 0.15              |
| `--msg`     | Optional text overlay at bottom right     | ""                |

## 🖨️ Physical Print & Resolution Guide

When moving from a digital script to a physical poster, the relationship between **Density**, **Tile Resolution**, and **DPI (Dots Per Inch)** is critical. A professional print requires 300 DPI for "retina-level" clarity.

### 1. The Core Variables

-   **Density (`--density`):** Controls the "Big Picture" clarity. Higher density makes the main subject sharper but makes individual tiles smaller.
-   **Tile Size (`--tile_size`):** Controls the "Small Picture" clarity. This is the internal pixel resolution of each memory.
-   **DPI:** The printer's hardware limit. (Standard: 300 for high quality, 150 for budget/large scale).

### 2. Recommended Configuration Matrix

Use the following settings to match standard Indian frame sizes:

| Poster Size (Inches) | Target Frame  | Density   | Tile Size | Final Resolution | Recommended View Distance |
| :------------------- | :------------ | :-------- | :-------- | :--------------- | :------------------------ |
| **12" x 18"**        | A3+           | 80 - 100  | 60 px     | 6000 x 9000 px   | 1-2 Feet                  |
| **18" x 24"**        | Medium Wall   | 120 - 150 | 50 px     | 7500 x 11250 px  | 3-5 Feet                  |
| **24" x 36"**        | Large Gallery | 180 - 220 | 40 px     | 8800 x 13200 px  | 6+ Feet                   |

### 3. The Math (For the Curious)

To calculate the physical size of an individual photo tile:
$$\text{Physical Tile Size (Inches)} = \frac{\text{Poster Width (Inches)}}{\text{Density}}$$

_Example:_ On an 18-inch wide poster with a density of 120, each photo of your memories will be **0.15 inches** (~3.8mm) wide. This is the ideal size for a "hidden detail" effect.

### 4. Printing Best Practices

-   **Format:** Export as `.jpg` with `quality=95` or `.tiff` to avoid compression artifacts.
-   **Color Profile:** The script uses RGB. Ensure your print shop (e.g., Printo or local Pune labs) converts to CMYK correctly or supports high-gamut RGB printing.
-   **Finish:** Use **Matte or Satin paper**. High-gloss finishes create glare that makes it difficult to see the tiny tile details.

## 📊 Technical Concept

This project utilizes **Vector Space Search** to achieve its results.

-   **Data Transformation:** Each tile image is downsampled and converted into an RGB mean vector.
-   **Distance Calculation:** The script performs a **Nearest Neighbor Search** using the **L2 Norm (Euclidean Distance)** to match the target pixel's color to the most suitable tile in the library.
-   **Optimization:** Uses `numpy` partitioning for selection of the top matches, ensuring performance even with large tile libraries.
