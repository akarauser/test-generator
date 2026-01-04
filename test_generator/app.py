import argparse
import os
import random
import shutil

from .utils._logger import logger


def create_test_folders(train_folder, test_folder, test_ratio=0.2):
    """
    Creates test folders from a train folder, duplicating the folder structure
    and splitting the images randomly.

    Args:
        train_folder (str): Path to the main train folder.
        test_folder (str) : Path to the test folder.
        test_ratio (float):  Ratio of images to be moved to test folders (default: 0.2).
    """

    if not os.path.exists(train_folder):
        logger.error(f"Error: Train folder {train_folder} does not exist.")
        return

    # Get a list of subfolders
    subfolders = [
        d
        for d in os.listdir(train_folder)
        if os.path.isdir(
            # Exclude "." and ".."
            os.path.join(train_folder, d)
        )
        and d != "."
        and d != ".."
    ]

    # Create test folders
    for folder in subfolders:
        # Create a folder name for test folder
        test_folder_path = os.path.join(test_folder, folder)
        if not os.path.exists(test_folder_path):
            try:
                os.makedirs(test_folder_path)
            except OSError as e:
                logger.error(f"Error creating directory {test_folder_path}: {e}")
                return

    # Randomly select images to move to test folders
    for folder in subfolders:
        folder_path = os.path.join(train_folder, folder)
        images = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(
                os.path.join(
                    # Filter for image files
                    folder_path,
                    f,
                )
            )
            and f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        num_images_to_move = int(len(images) * test_ratio)

        if num_images_to_move > 0:
            random.shuffle(images)
            images_to_move = images[:num_images_to_move]

            for image in images_to_move:
                source_path = os.path.join(folder_path, image)
                destination_path = os.path.join(test_folder, folder, image)

                # Move the image
                try:
                    shutil.move(source_path, destination_path)
                    logger.info(
                        f"Moved {image} from {source_path} to {destination_path}"
                    )
                except Exception as e:
                    logger.error(f"Error moving {image}: {e}")
    print(f"{num_images_to_move} image moved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates test folders from a train folder."
    )
    parser.add_argument("-tr", "--train_folder", help="Path to the main train folder.")
    parser.add_argument(
        "-te", "--test_folder", help="Path to the destination test folder."
    )
    parser.add_argument(
        "-r",
        "--test_ratio",
        type=float,
        default=0.2,
        help="Ratio of images to be moved to test folders (default: 0.2)",
    )
    args: argparse.Namespace = parser.parse_args()

    create_test_folders(args.train_folder, args.test_folder, args.test_ratio)
