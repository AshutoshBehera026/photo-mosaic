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

## 📊 Technical Concept

This project utilizes **Vector Space Search** to achieve its results.

-   **Data Transformation:** Each tile image is downsampled and converted into an RGB mean vector.
-   **Distance Calculation:** The script performs a **Nearest Neighbor Search** using the **L2 Norm (Euclidean Distance)** to match the target pixel's color to the most suitable tile in the library.
-   **Optimization:** Uses `numpy` partitioning for selection of the top matches, ensuring performance even with large tile libraries.
