# import os
# import random
# import shutil
# from pathlib import Path

# # Set seed for reproducibility
# random.seed(42)

# # Base paths
# base_path = Path("data/agri_data")  # replace this with your data path if you are not using this folder structure

# data_path = base_path / "data"
# output_path = base_path / "dataset"

# # Target structure
# image_train_path = output_path / "images/train"
# image_val_path = output_path / "images/val"
# image_test_path = output_path / "images/test"
# label_train_path = output_path / "labels/train"
# label_val_path = output_path / "labels/val"
# label_test_path = output_path / "labels/test"

# # Create directories if they don't exist
# for p in [image_train_path, image_val_path, image_test_path, label_train_path, label_val_path, label_test_path]:
#     p.mkdir(parents=True, exist_ok=True)

# # Get all JPEG image files
# images = list(data_path.glob("*.jpeg"))
# random.shuffle(images)

# # Split into 70% train, 20% val 10% test
# split_index_train = int(0.7 * len(images))

# train_images = images[:split_index_train]
# val_images = images[split_index_train:]
# split_index_test = int(0.5 * len(val_images))
# test_images = images[-split_index_test:]    

# # Helper function to copy image and its corresponding label
# def copy_pair(img_path, target_img_dir, target_lbl_dir):
#     # Copy image
#     shutil.copy(img_path, target_img_dir)
#     # Copy label
#     label_path = img_path.with_suffix(".txt")
#     if label_path.exists():
#         shutil.copy(label_path, target_lbl_dir)
#     else:
#         print(f"⚠️ Warning: Label not found for image {img_path.name}")

# # Copy training data
# for img_path in train_images:
#     copy_pair(img_path, image_train_path, label_train_path)

# # Copy validation data
# for img_path in val_images:
#     copy_pair(img_path, image_val_path, label_val_path)

# # Copy test data
# for img_path in test_images:
#     copy_pair(img_path, image_test_path, label_test_path)

# print("✅ Dataset reorganized successfully in YOLOv8 format.")


import random, shutil
from pathlib import Path

random.seed(42)

# Adjust this to your actual data location
base_path   = Path("data/agri_data")  
data_path   = base_path
output_path = base_path / "dataset"

print("▶️ data_path:", data_path)
print("▶️ Exists? ", data_path.exists())
print("▶️ Files in it:", list(data_path.iterdir())[:5])


# Create target dirs
for sub in ("train","val","test"):
    (output_path / f"images/{sub}").mkdir(parents=True, exist_ok=True)
    (output_path / f"labels/{sub}").mkdir(parents=True, exist_ok=True)

# Grab all image files (jpg/jpeg any case)
images = []
for ext in ("*.jpg","*.JPG","*.jpeg","*.JPEG"):
    images.extend(data_path.glob(ext))
random.shuffle(images)

n = len(images)
n_train = int(0.7 * n)
n_val   = int(0.2 * n)
n_test  = n - n_train - n_val

train_images = images[:n_train]
val_images   = images[n_train:n_train + n_val]
test_images  = images[n_train + n_val:]

def copy_pair(img_list, img_dir, lbl_dir):
    for img_path in img_list:
        shutil.copy(img_path, img_dir)
        lbl = img_path.with_suffix(".txt")
        if lbl.exists():
            shutil.copy(lbl, lbl_dir)
        else:
            print(f"⚠️ Warning: No label for {img_path.name}")

# Copy them
copy_pair(train_images, output_path/"images/train", output_path/"labels/train")
copy_pair(val_images,   output_path/"images/val",   output_path/"labels/val")
copy_pair(test_images,  output_path/"images/test",  output_path/"labels/test")

print("✅ Dataset reorganized successfully in YOLOv8 format.")
