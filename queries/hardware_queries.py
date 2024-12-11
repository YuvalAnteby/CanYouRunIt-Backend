from pymongo import MongoClient

"""
All function for handling the hardware in the DB will be here for ease of use and maintainability.
For example: adding new hardware, fetching hardware, and more.
"""

# Assuming MongoDB instance running locally
client = MongoClient('mongodb://localhost:27017')
db = client['game_db']

def add_gpu(brand, model, fullname):
    """
    Adding a new GPU to the collection.
    :param brand: brand of the GPU. E.G: Nvidia
    :param model: GPU model. E.G RTX 4090
    :param fullname: name of the GPU model. E.G: RTX 4070 TI super
    """
    # Make sure the input isn't empty
    if brand.empty() or model.empty() or fullname.empty():
        return
    # Standardize ids for the GPUs
    gpu_id = brand.lower() + "_" + model.lower().replace(' ', '_')
    # Check if the GPU already exists to avoid duplicates
    existing_gpu = db.hardware.find_one({"hardware_id": gpu_id, "type": "gpu"})
    if existing_gpu:
        print(f"GPU '{fullname}' already exists in the database.")
        return
    # Insert the new GPU to the DB
    db.hardware.insert_one(
        {"hardware_id": gpu_id, "brand": brand, "model": model, "fullname": fullname, "type": "gpu_" + brand.lower()})

def add_cpu(brand, model, fullname):
    """
    Adding a new CPU to the collection.
    :param brand: brand of the CPU. E.G: AMD
    :param model: CPU model without spaces. E.G RYZEN3600
    :param fullname: full name of the CPU model. E.G RYZEN R5 3600
    """
    # Make sure the input isn't empty
    if brand.strip() == "" or model.strip() == "" or fullname.strip() == "":
        return
    # Standardize ids for the CPUs
    cpu_id = brand.lower() + "_" + model.lower().replace(' ', '_')
    # Check if the CPU already exists to avoid duplicates
    existing_cpu = db.hardware.find_one({"hardware_id": cpu_id, "type": "cpu"})
    if existing_cpu:
        print(f"CPU '{fullname}' already exists in the database.")
        return
    # Insert the new CPU to the DB
    db.hardware.insert_one(
        {"hardware_id": cpu_id, "brand": brand, "model": model, "fullname": fullname, "type": "cpu_" +brand.lower()})

async def get_all_gpus():
    """
    Retrieve all GPUs from the database.
    :return: List of all GPUs as dictionaries.
    """
    return list(db.hardware.find({"type": "GPU"}))  # Assuming "type" is a field to differentiate GPUs

async def get_all_cpus():
    """
    Retrieve all CPUs from the database.
    :return: List of all CPUs as dictionaries.
    """
    return list(db.hardware.find({"type": "CPU"}))  # Assuming "type" is a field to differentiate CPUs