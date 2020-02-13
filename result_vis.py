import pandas as pd
import cv2
import json

color_bar = {"red": (0, 0, 255),
             "blue": (255, 0, 0),
             "green": (0, 255, 0),
             "orange": (0, 165, 255),
             "deeppink": (147, 25, 255),
             "yellow": (0, 255, 255)}

color = {"defect0": color_bar["yellow"],
         "defect1": color_bar["blue"],
         "defect2": color_bar["deeppink"],
         "defect3": color_bar["orange"],
         "defect4": color_bar["red"]}

classes_rename = {"defect0": "human",
                  "defect1": "bottle",
                  "defect2": "knife",
                  "defect3": "rifle",
                  "defect4": "gun"}


def vis_csv(
        image_file, result
):
    df = pd.read_csv(result)
    for index, file in df.iterrows():
        if file[6] == 'defect0':
            continue
        img = cv2.imread(image_file + '/' + file[0])
        boxcolor = color[file["classes"]]
        # src_RGB = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img_rect = cv2.rectangle(img, (file[1], file[2]), (file[3], file[4]), boxcolor, 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        prob = round(file[5], 2)
        img_text = cv2.putText(img_rect, classes_rename[file[6]] + ' ' + str(prob), (file[1], file[2] - 5), font, 2,
                               boxcolor, 3)
        cv2.imwrite(img_file + '/' + file[0], img_rect)


def vis_gt(
        image_file, coco_gt,
):
    with open(coco_gt) as load_json:
        load_dict = json.load(load_json)

    for anno in load_dict['annotations']:
        image_name = load_dict['images'][anno['image_id'] - 1]['file_name']
        img = cv2.imread(image_file + '/' + image_name)
        boxcolor = color_bar['green']
        # boxcolor = color[file["classes"]]
        # src_RGB = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        x1 = anno['bbox'][0]
        y1 = anno['bbox'][1]
        x2 = x1 + anno['bbox'][2]
        y2 = y1 + anno['bbox'][3]
        img_rect = cv2.rectangle(img, (x1, y1), (x2, y2), boxcolor, 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        categ_name = load_dict['categories'][anno['category_id'] - 1]['name']
        img_text = cv2.putText(img_rect, categ_name, (x1, y2 + 30), font, 2,
                               boxcolor, 3)
        cv2.imwrite(img_file + '/' + image_name, img_rect)


if __name__ == '__main__':
    img_file = 'E:/Wen/vis_result/testset/test_img'
    result = 'E:/Wen/vis_result/result/summary_for_testsets.csv'
    coco_gt = 'E:/Wen/testset/TestSet_THz_1110.json'
    vis_csv(img_file, result)
    vis_gt(img_file, coco_gt)
