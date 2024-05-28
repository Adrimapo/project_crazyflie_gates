#!/bin/bash

# Folders
frontal_images_dir="outDir/frontal_images"
labels_dir="outDir/labels"

# Function to check and delete label files without their corresponding images
check_and_delete_labels() {
    for label_file in "$labels_dir"/*.txt; do
        filename=$(basename -- "$label_file" .txt)
        if [ ! -e "$frontal_images_dir/$filename.jpg" ]; then
            echo "Deleting $label_file"
            rm "$label_file"
        fi
    done
}

# Function to check and delete images without their corresponding label files
check_and_delete_images() {
    for image_file in "$frontal_images_dir"/*.jpg; do
        filename=$(basename -- "$image_file" .jpg)
        if [ ! -e "$labels_dir/$filename.txt" ]; then
            echo "Deleting $image_file"
            rm "$image_file"
        fi
    done
}

# Execute both functions
check_and_delete_labels
check_and_delete_images