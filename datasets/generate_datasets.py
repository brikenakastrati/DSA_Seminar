import random
import os

def generate_datasets():
    sizes = {"small": 5, "medium": 15, "large": 30}
    
    # Create the 'datasets' directory if it doesn't exist
    os.makedirs("datasets", exist_ok=True)
    
    for name, size in sizes.items():
        # Generate a random dataset of unique numbers
        dataset = random.sample(range(1, size * 10), size)
        
        # Ensure that the number 10 is in the dataset
        if 10 not in dataset:
            dataset[0] = 10  # Replace the first element with 10 to guarantee it appears in the dataset
        
        # Write the dataset to a text file
        with open(f"datasets/dataset_{name}.txt", "w") as f:
            f.write("\n".join(map(str, dataset)))

if __name__ == "__main__":
    generate_datasets()
