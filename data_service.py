import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from database.models import InstancesN8, InstancesN12, InstancesN16

# from typing import Union


def get_session() -> Session:
    # Connect to the SQLite database
    engine = create_engine("sqlite:///database/fair_sampling.db")

    # Create a configured "Session" class
    return sessionmaker(bind=engine)()


# METHOD STORE DATA IN FILES LOCALLY
def save_obj(database: str, path: str, filename: str, json_str_obj: dict):
    """
    Save json serializeable dict given location as json file.
    """

    directory_path = f"data/{database}/{path}"

    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)

    with open(f"{directory_path}/{filename}.json", "w") as json_file:
        json.dump(json_str_obj, json_file, indent=1)


def get_instance_class(N: int):
    return {8: InstancesN8, 12: InstancesN12, 16: InstancesN16}.get(N)
