import os

# Your Data Pipeline Director
CATEGORIES = ["algorithms", "security", "devops", "languages", "architecture"]

def collect_data(category):
    print(f"Ingesting domain: {category}...")
    # Add your logic here to pull from HuggingFace datasets or local clones
    # Example: datasets.load_dataset("bigcode/the-stack", data_dir=category)

if __name__ == "__main__":
    for cat in CATEGORIES:
        collect_data(cat)
