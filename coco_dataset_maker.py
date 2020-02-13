import os
import json
import datetime
import xml.etree.cElementTree as ET

# trainset
# label_path = 'E:/Wen/trainset/train_label'
# label_json_path = 'E:/Wen/trainset/'
# ===========================================================================

# testset
label_path = 'E:/Wen/testset/test_label'
label_json_path = "E:/Wen/testset/"

# 完全体的info
info = {
    "year": 2019,
    "version": "0.2.0",
    "description": "THz Dataset 11-10",
    "contributor": "waspinator",
    "url": "https://github.com/waspinator/pycococreator",
    "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}
# 完全体的licenses
licenses = [{
    "id": 1,
    "name": "Attribution-NonCommercial-ShareAlike License",
    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
}]
# 完全体的categories
categories = [{"id": 1, "name": "human", "supercategory": "restricted_obj"},
              {"id": 2, "name": "bottle", "supercategory": "restricted_obj"},
              {"id": 3, "name": "knife", "supercategory": "restricted_obj"},
              {"id": 4, "name": "rifle", "supercategory": "restricted_obj"},
              {"id": 5, "name": "gun", "supercategory": "restricted_obj"}]

# 为了便于确定categories_id编号创建的字典
cate_dict = {"human": 1, "bottle": 2, "knife": 3, "rifle": 4, "gun": 5}

img_id = 0
ann_id = 0
images = []
annotations = []
for xml_file in os.listdir(label_path):
    tree = ET.ElementTree(file=label_path + "/" + xml_file)
    root = tree.getroot()
    for child_of_root in root:
        if child_of_root.tag == "filename":
            image = {
                "id": int,
                "file_name": str,
                "width": int,
                "height": int,
            }

            img_id = img_id + 1
            filename = child_of_root.text
            image["id"] = img_id
            image["file_name"] = filename
            image["width"] = 1000
            image["height"] = 1900
            images.append(image)

        if child_of_root.tag == "object":

            # n = 1

            # 对不同类别的被检测目标进行过采样，使得每种被检测目标的数量趋于一致
            if child_of_root[0].text == "bottle":
                n = 8
            elif child_of_root[0].text == "knife":
                n = 14
            elif child_of_root[0].text == "rifle":
                n = 16
            elif child_of_root[0].text == "gun":
                n = 8
            else:
                n = 1

            for i in range(n):
                annotation = {
                    "id": int,
                    "image_id": int,
                    "category_id": int,
                    "segmentation": [[]],
                    "area": float,
                    "bbox": [],
                    "iscrowd": int,
                }
                cate_name = child_of_root[0].text
                cate_id = cate_dict[cate_name]
                xmin = int(child_of_root[4][0].text)
                ymin = int(child_of_root[4][1].text)
                xmax = int(child_of_root[4][2].text)
                ymax = int(child_of_root[4][3].text)
                width = xmax - xmin
                height = ymax - ymin
                area = width * height
                ann_id = ann_id + 1

                annotation["id"] = ann_id
                annotation["image_id"] = img_id
                annotation["category_id"] = cate_id
                annotation["bbox"] = [xmin, ymin, width, height]
                annotation["area"] = area
                annotation["segmentation"] = [[xmax, ymax, xmin, ymax, xmin, ymin, xmax, ymin, xmax, ymax]]
                annotation["iscrowd"] = 0
                annotations.append(annotation)
print("images:", images)
print("annotations:", annotations)

thz_coco = {
    "info": info,
    "licenses": licenses,
    "categories": categories,
    "images": images,
    "annotations": annotations,
}

print("ann_wmm", thz_coco)

# 将数据集写入json文件
wmm_thz_coco = json.dumps(thz_coco)

# trainset
# with open(label_json_path + "TrainSet_THz_1110.json", "w") as f:
#     f.write(wmm_thz_coco)

# with open(label_json_path + "TrainSet_THz_1110_MultiSample.json", "w") as f:
#     f.write(wmm_thz_coco)

# testset
with open(label_json_path + "TestSet_THz_1110.json", "w") as f:
    f.write(wmm_thz_coco)
