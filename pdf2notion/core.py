# -*- coding: utf-8 -*-
import json
import os
import shutil
from pathlib import Path

from notion.block import FileBlock, ImageBlock
from notion.client import NotionClient
from pdf2image import convert_from_path

image_dir = Path.cwd() / Path("pdf2notion") / Path("image")


def convert_pdf2image(pdf_path_obj):
    """convert pdf to image.

    convert pdf to image that is png format.
    images will deleted by this program after uploading.

    Args:
        pdf_path_obj (Path): PDF Path object.
    """
    pdf = convert_from_path(str(pdf_path_obj))

    for index, page in enumerate(pdf):
        image_path = image_dir / Path(
            pdf_path_obj.stem + "_" + "{:0>4}".format(index) + ".png"
        )
        page.save(str(image_path), "png")


def upload2notion(page, name, tags):
    """upload images to Notion.
    Args:
        page : from notion
        name (Path): pdf path
        tags (list): page tags
    """
    row = page.collection.add_row()
    row.name = str(name.stem)
    row.Tags = tags
    for image_path in image_dir.iterdir():
        image = row.children.add_new(ImageBlock)
        image.upload_file(str(image_path))
    pdf = row.children.add_new(FileBlock)
    pdf.upload_file(str(name))


def read_json():
    """read a json file for setting.

    the json must be located like '~/pdf2notion.json'
    Returns:
        dict: data from json file for setting.
    """
    json_path = Path.home() / Path("pdf2notion.json")
    if json_path.exists():
        try:
            with open(json_path) as f:
                json_data = json.load(f)
                return json_data
        except json.decoder.JSONDecodeError as e:
            print(e)
            print(type(e))


def remove_images():
    shutil.rmtree(str(image_dir))
    os.mkdir(str(image_dir))


def main():
    json_data = read_json()
    if json_data is None:
        return
    client = NotionClient(token_v2=json_data["token_v2"])
    page = client.get_collection_view(json_data["url"])
    for data in json_data["pdf_dir"]:
        for d in Path(data["dir"]).iterdir():
            if d.suffix == ".pdf":
                convert_pdf2image(d)
                upload2notion(page, d, data["tags"])
                remove_images()


if __name__ == "__main__":
    main()
