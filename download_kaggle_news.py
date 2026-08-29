import kagglehub
import shutil
import os

import config

# Download latest version
path = kagglehub.dataset_download("rmisra/news-category-dataset")

print("Path to dataset files:", path)
# Define the destination folder
destination_folder = str(config.NEWS_DIR)

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Move the downloaded files to the destination folder
for file_name in os.listdir(path):
    full_file_name = os.path.join(path, file_name)
    if os.path.isfile(full_file_name):
        shutil.move(full_file_name, destination_folder)

print("Files moved to:", destination_folder)