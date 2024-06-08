import os
from pathlib import Path
import fire
import json


def clip_bbox(anns, width, height):
    anns_out = []
    for ann in anns:
        bbox = ann['bbox']
        if bbox[0] < 0:
            bbox[2] += bbox[0]
            bbox[0] = 0
        if bbox[1] < 0:
            bbox[3] += bbox[1]
            bbox[1] = 0
        if bbox[0] + bbox[2] > width:
            bbox[2] = width - bbox[0]
        if bbox[1] + bbox[3] > height:
            bbox[3] = height - bbox[1]
        ann['bbox'] = bbox
        anns_out.append(ann)
    return anns_out


def clip_file(path, dir, width=640, height=512):
    path = Path(path)
    dir = Path(dir)
    if path.is_dir():
        for p in path.glob("*"):
            clip_file(p, dir)
    elif path.is_file() and path.suffix == '.json':
        with open(path) as f:
            coco = json.load(f)
            coco["annotations"] = clip_bbox(coco['annotations'], width, height)
        # dump json
        if not dir.exists():
            dir.mkdir(parents=True)
        with open(os.path.join(dir, path.stem + '_clip.json'), 'w') as f:
            json_out = json.dumps(coco)
            f.write(json_out)


if __name__ == "__main__":
    fire.Fire(clip_file)
