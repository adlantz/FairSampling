import json
import os


def save_obj(database: str, path: str, filename: str, json_str_obj: dict):
    """
    Save json serializeable dict to given location as json file.
    """

    directory_path = f"data/{database}/{path}"

    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)

    with open(f"{directory_path}/{filename}.json", "w") as json_file:
        json.dump(json_str_obj, json_file, indent=1)
