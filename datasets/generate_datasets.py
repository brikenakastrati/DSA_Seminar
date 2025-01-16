import random

def generate_datasets():
    sizes = {"small": 5, "medium": 15, "large": 30}
    for name, size in sizes.items():
        dataset = random.sample(range(1, size * 10), size)
        with open(f"datasets/dataset_{name}.txt", "w") as f:
            f.write("\n".join(map(str, dataset)))

if __name__ == "__main__":
    generate_datasets()
