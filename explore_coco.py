
# 1. Find the project directory
from pathlib import Path
import json
from collections import defaultdict, Counter
from PIL import Image, ImageDraw

project_dir = Path(__file__).resolve().parent

# 2. Locate the annotation file
json_path = project_dir / "data" / "idd" / "annotations" / "instances.json"

print("Project directory:", project_dir)
print("JSON path:", json_path)
print("File exists:", json_path.exists())

# 3. Load the JSON file
with open(json_path, "r", encoding="utf-8") as file:
    coco = json.load(file)

print("COCO JSON loaded successfully!")

# 4. Read the three main sections
images = coco["images"]
categories = coco["categories"]
annotations = coco["annotations"]

# 5. Print dataset summary
print("\nDATASET SUMMARY")
print("Images:", len(images))
print("Categories:", len(categories))
print("Annotations:", len(annotations))

# 6. Print category information
print("\nAVAILABLE CATEGORIES")
for category in categories:
    print(category["id"], ":", category["name"])

# 7. Print image information
print("\nIMAGE INFORMATION")
for image in images:
    print(
        "Image ID:", image["id"],
        "| File:", image["file_name"],
        "| Width:", image["width"],
        "| Height:", image["height"]
    )

# 8. Print object annotations
print("\nOBJECT ANNOTATIONS")
for annotation in annotations:
    print(
        "Image ID:", annotation["image_id"],
        "| Category ID:", annotation["category_id"],
        "| Bounding Box:", annotation["bbox"]
    )

# 9. Define image and output directories
image_dir = project_dir / "data" / "idd" / "images"
output_dir = project_dir / "docs"
output_dir.mkdir(parents=True, exist_ok=True)

# 10. Convert category IDs into category names
category_names = {
    category["id"]: category["name"]
    for category in categories
}

# 11. Group annotations by image ID
annotations_by_image = defaultdict(list)

for annotation in annotations:
    annotations_by_image[annotation["image_id"]].append(annotation)

# 12. Generate previews for the first 3 valid annotated images
print("\nDRAWING FIRST 3 IMAGES")

generated_count = 0

for image_info in images:

    # Stop after generating 3 images
    if generated_count == 3:
        break

    image_id = image_info["id"]

    # Skip images without annotations
    if not annotations_by_image[image_id]:
        continue

    image_path = image_dir / image_info["file_name"]

    # Skip if image file does not exist
    if not image_path.exists():
        print("Image not found:", image_path)
        continue

    # Open image
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Draw bounding boxes and labels
    for annotation in annotations_by_image[image_id]:

        x, y, width, height = annotation["bbox"]

        x1, y1 = x, y
        x2, y2 = x + width, y + height

        label = category_names.get(
            annotation["category_id"], "Unknown"
        )

        draw.rectangle(
            [x1, y1, x2, y2],
            outline="red",
            width=3
        )

        label_position = (x1, max(0, y1 - 15))

        draw.rectangle(
            draw.textbbox(label_position, label),
            fill="red"
        )

        draw.text(label_position, label, fill="white")

    # Save preview
    output_path = output_dir / f"coco_preview_{image_id}.jpg"

    image.save(output_path)

    generated_count += 1

    print("Preview saved:", output_path)

print("\nTOTAL PREVIEWS GENERATED:", generated_count)

# 13. Objects per category
print("\nOBJECTS PER CATEGORY")

category_counts = Counter(a["category_id"] for a in annotations)

for category_id, name in category_names.items():
    print(
        f"{category_id:>3} : {name:<12} "
        f"{category_counts.get(category_id, 0)}"
    )

# 14. Images with and without annotations
print("\nImages with annotations:",
      sum(1 for im in images if annotations_by_image.get(im["id"])))

print("Images without annotations:",
      sum(1 for im in images if not annotations_by_image.get(im["id"])))

# 15. Verification checks
image_by_id = {image["id"]: image for image in images}

bad_image = [
    a["id"] for a in annotations
    if a["image_id"] not in image_by_id
]

bad_category = [
    a["id"] for a in annotations
    if a["category_id"] not in category_names
]

bad_size = [
    a["id"] for a in annotations
    if a["bbox"][2] <= 0 or a["bbox"][3] <= 0
]

outside = [
    a["id"] for a in annotations
    if a["image_id"] in image_by_id and (
        a["bbox"][0] < 0 or a["bbox"][1] < 0
        or a["bbox"][0] + a["bbox"][2] > image_by_id[a["image_id"]]["width"]
        or a["bbox"][1] + a["bbox"][3] > image_by_id[a["image_id"]]["height"]
    )
]

print("\nVERIFICATION CHECKS")

checks = [
    ("Every annotation points to an existing image", bad_image),
    ("Every annotation points to an existing category", bad_category),
    ("Every box has width > 0 and height > 0", bad_size),
    ("Every box lies inside its image", outside),
]

for check_name, bad_ids in checks:
    result = "PASS" if not bad_ids else f"FAIL {bad_ids[:5]}"
    print(f"{check_name:<50} {result}")
