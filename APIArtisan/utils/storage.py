import os
import json
import aiofiles
import aiofiles.os

from ..constants import storage_constants


def create_if_doesnt_exist() -> None:
    if not os.path.exists(storage_constants.LOCAL_APP_DATA):
        os.makedirs(storage_constants.LOCAL_APP_DATA)

    if not os.path.exists(storage_constants.SETTINGS_JSON):
        with open(storage_constants.SETTINGS_JSON, "w") as f:
            f.write(json.dumps(storage_constants.DEFAULT_SETTINGS, indent=4))

    if not os.path.exists(storage_constants.SECRETS_DIR):
        os.makedirs(storage_constants.SECRETS_DIR)

    if not os.path.exists(storage_constants.CONFIGS_DIR):
        os.makedirs(storage_constants.CONFIGS_DIR)


def load_settings_from_file() -> dict:
    with open(storage_constants.SETTINGS_JSON, "r") as f:
        return json.load(f)


class Storage:
    """
    A class that provides methods for storing and retrieving data from files.
    """

    def __init__(self, directory: str):
        """
        Initializes a Storage object.

        Args:
            directory (str): The directory where the storage is located.
        """
        self.directory = directory

    async def write_to_file(self, json: str, name_of_file:str) -> None:
            """
            Write the given JSON string to a file with the specified name.

            Args:
                json (str): The JSON string to write to the file.
                name_of_file (str): The name of the file to write to.

            Raises:
                FileExistsError: If a file with the same name already exists.

            Returns:
                None
            """
            file = os.path.join(self.directory, f"{name_of_file}.json")
            if os.path.exists(file):
                raise FileExistsError(f"{name_of_file} already exists!")
            async with aiofiles.open(file, "w") as f:
                await f.write(json)

    async def update_file(self, json: str, name_of_file: str) -> None:
            """
            Update the contents of a file with the provided JSON data.

            Args:
                json (str): The JSON data to write to the file.
                name_of_file (str): The name of the file to update.

            Raises:
                FileNotFoundError: If the specified file does not exist.

            Returns:
                None
            """
            file = os.path.join(self.directory, f"{name_of_file}.json")
            if not os.path.exists(file):
                raise FileNotFoundError(f"{name_of_file} does not exist!")
            async with aiofiles.open(file, "w") as f:
                await f.write(json)

    async def delete_file(self, name: str) -> None:
        """
        Deletes a file from the storage directory.

        Args:
            name (str): The name of the file to delete.

        Raises:
            FileNotFoundError: If the file does not exist.

        Returns:
            None
        """
        file = os.path.join(self.directory, f"{name}.json")
        if not os.path.exists(file):
            raise FileNotFoundError(f"{name} does not exist!")
        await aiofiles.os.remove(file)

    def read_from_file(self, file_name: str) -> "dict":
        """
        Reads data from a file and returns it as a dictionary.

        Args:
            file_name (str): The name of the file to read from.

        Returns:
            dict: The data read from the file as a dictionary.
        """
        with open(os.path.join(self.directory, file_name), "r") as f:
            return json.load(f)

    def read_all_from_file(self) -> list["dict"]:
        """
        Reads data from all files in the specified directory and returns a list of dictionaries.

        Returns:
            A list of dictionaries containing the data read from each file.
        """
        files = os.listdir(self.directory)
        return [self.read_from_file(file_name) for file_name in files]


class Secrets(Storage):
    pass


class Configs(Storage):
    pass


secrets = Secrets(storage_constants.SECRETS_DIR)
configs = Configs(storage_constants.CONFIGS_DIR)
