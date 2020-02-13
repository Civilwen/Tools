import pandas as pd
import os
import json

root = 'E:/Project/COCOEval'
csv_path = root + "/result/"
testset_GT_json = root + "/data/test/wmm_thz_coco_0502_testset.json"
test_img_path = root + "/data/test/test_img"
csv_name="X-101-FPN-5x"
df_all = pd.read_csv(csv_path + csv_name+'.csv')
# print(df_all)
print(len(df_all))

cate_dict = {"defect0": 1, "defect1": 2, "defect2": 3, "defect3": 4, "defect4": 5}

img_id_dict = {}
with open(testset_GT_json, 'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict)
    for image in load_dict["images"]:
        img_id_dict[image["file_name"]] = image["id"]
# print(img_id_dict)

all_result_list = []
for index, file in df_all.iterrows():
    all_result_dict = {
        "image_id": int,
        "category_id": int,
        "bbox": [],
        "score": float
    }
    all_result_dict["image_id"] = img_id_dict[file["filename"]]
    all_result_dict["category_id"] = cate_dict[file["classes"]]
    width = file["xmax"] - file["xmin"]
    height = file["ymax"] - file["ymin"]
    all_result_dict["bbox"] = [file["xmin"], file["ymin"], width, height]
    all_result_dict["score"] = file["confidence"]
    all_result_list.append(all_result_dict)

jsObject = json.dumps(all_result_list)
fileObject = open(csv_path+csv_name+'.json', 'w')
fileObject.write(jsObject)
fileObject.close()
