import os
from pathlib import Path
import fire
from pycocotools.coco import COCO
import json


cat_map = {"car": "vehicle", "freight_car": "vehicle",
           "truck": "vehicle", "bus": "vehicle", "van": "vehicle"}
cat_out = [{"name": "vehicle", "id": 1}]


def cat_id(cats, name):
    for cat in cats:
        if cat['name'] == name:
            return cat['id']
    return None


def convert_cat(coco, cat_out, cat_map):
    # get categories
    cats = coco.loadCats(coco.getCatIds())
    anns_out = []
    for cat in cats:
        cat_name = cat['name']
        if cat_name in cat_map:
            cat_name_out = cat_map[cat_name]
        elif cat_name in [co['name'] for co in cat_out]:
            cat_name_out = cat_name
        else:
            continue
        cat_id_out = cat_id(cat_out, cat_name_out)
        # get annotation filter by category
        anns = coco.loadAnns(coco.getAnnIds(catIds=cat['id']))
        # modify categery of annotation
        for ann in anns:
            ann['category_id'] = cat_id_out
            anns_out.append(ann)

    # get images
    imgs = coco.loadImgs(coco.getImgIds())

    # construct json dict
    dict_out = {}
    dict_out['images'] = imgs
    dict_out['annotations'] = anns_out
    dict_out['categories'] = cat_out

    return dict_out


def convert_file_cat(path, dir):
    path = Path(path)
    dir = Path(dir)
    if path.is_dir():
        print("input_dir = ", path)
        for p in path.glob("*"):
            convert_file_cat(p, dir)
    elif path.is_file() and path.suffix == '.json':
        print("input_path = ", path)

        coco = COCO(path)

        dict_out = convert_cat(coco, cat_out, cat_map)

        # dump json
        if not dir.exists():
            dir.mkdir(parents=True)
        with open(os.path.join(dir, path.stem + '_vehicle.json'), 'w') as f:
            json_out = json.dumps(dict_out)
            f.write(json_out)


if __name__ == "__main__":
    fire.Fire(convert_file_cat)
