import os
import torch
from ultralytics import YOLO
from pathlib import Path

"""
Gabriel:
Hello! Welcome to my code contribution!

Updates:
-This uses the other dataset instead! Last dataset has a lot of error's soo I moved on to another one.
-The train code has been modified again quite a bit. Just some imporvements

That's all
-C.C
"""

def main():
    PROJECT_ROOT = Path(__file__).resolve().parent
    os.chdir(PROJECT_ROOT)
    print(f"Working directory changed to: {os.getcwd()}")

    DATA_YAML = PROJECT_ROOT / "dataset" / "data.yaml"
    SAVE_DIR = PROJECT_ROOT / "runs" / "detect"
    DATASET_ROOT = PROJECT_ROOT / "dataset"

    # Dataset splits and folders
    splits = ["train", "val", "test"]
    for split in splits:
        images_dir = DATASET_ROOT / split / "images"
        labels_dir = DATASET_ROOT / split / "labels"
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)
        print(f"Ensured {split} folders exist: {images_dir}, {labels_dir}")

    # Error checking
    if not DATA_YAML.exists():
        raise FileNotFoundError(f"Data YAML file not found: {DATA_YAML}")
    if not DATASET_ROOT.exists():
        raise FileNotFoundError(f"Dataset root directory not found: {DATASET_ROOT}")
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    # Model
    model = YOLO("yolo26s.pt")  # Will download automatically if missing

    # Training
    model.train(
        data=str(DATA_YAML),
        epochs=5,        # short test
        batch=8,         # small batch
        device="cuda" if torch.cuda.is_available() else "cpu",
        save_dir=str(SAVE_DIR),
        augment=True     # mild augment to help validation
    )
    print(f"Training complete. Weights and results saved to: {SAVE_DIR}")


if __name__ == "__main__":
    main()