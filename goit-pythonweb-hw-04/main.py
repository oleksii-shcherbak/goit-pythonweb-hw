import argparse
import asyncio
import logging
from pathlib import Path

import aiofiles

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


async def copy_file(file: Path, output_folder: Path) -> None:
    """Copy a single file into a subfolder named after its extension.

    Args:
        file: The source file to copy.
        output_folder: The root destination folder.
    """
    extension = file.suffix.lstrip(".").lower() or "no_extension"
    destination_dir = output_folder / extension

    try:
        await asyncio.to_thread(destination_dir.mkdir, parents=True, exist_ok=True)
        destination_file = destination_dir / file.name

        async with aiofiles.open(file, "rb") as src:
            content = await src.read()

        async with aiofiles.open(destination_file, "wb") as dst:
            await dst.write(content)

    except Exception as e:
        logging.error("Failed to copy %s: %s", file, e)


async def read_folder(source_folder: Path, output_folder: Path) -> None:
    """Recursively read all files in source_folder and copy them to output_folder.

    Args:
        source_folder: The folder to scan recursively.
        output_folder: The root destination folder.
    """
    try:
        entries = await asyncio.to_thread(lambda: list(source_folder.rglob("*")))
    except Exception as e:
        logging.error("Failed to read source folder %s: %s", source_folder, e)
        return

    tasks = []
    for entry in entries:
        if entry.is_file():
            tasks.append(copy_file(entry, output_folder))

    await asyncio.gather(*tasks)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Namespace with source and output folder paths.
    """
    parser = argparse.ArgumentParser(
        description="Asynchronously sort files into subfolders by extension."
    )
    parser.add_argument("source", type=str, help="Path to the source folder.")
    parser.add_argument("output", type=str, help="Path to the output folder.")
    return parser.parse_args()


async def main() -> None:
    """Entry point: validate paths and launch the sorting process."""
    args = parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.exists():
        logging.error("Source folder does not exist: %s", source_folder)
        return

    if not source_folder.is_dir():
        logging.error("Source path is not a directory: %s", source_folder)
        return

    await asyncio.to_thread(output_folder.mkdir, parents=True, exist_ok=True)
    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    asyncio.run(main())
