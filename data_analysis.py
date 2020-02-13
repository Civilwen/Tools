import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# print(matplotlib.matplotlib_fname())


# 用于统计数据集中每种类型的数量
def get_class(load_dict):
    for image in load_dict["annotations"]:
        class_dict[str(image["category_id"])] = class_dict[str(image["category_id"])] + 1;


# 输入两个长度相等的list,返回两个list中对应元素的比值,比值=两个list中较大元素/两个list中较小元素
def make_ratio(height, width):
    ratio = []
    for i in range(len(height)):
        if height[i] >= width[i]:
            ratio.append(np.divide(height[i], width[i]))
        else:
            ratio.append(np.divide(width[i], height[i]))
    return ratio


def width_height_statistic(load_dict, ann_height, ann_width):
    for image in load_dict["annotations"]:
        ann_height[ann_class[image["category_id"]]].append(image["bbox"][3])
        ann_width[ann_class[image["category_id"]]].append(image["bbox"][2])


def area_statistic(load_dict, ann_area):
    for image in load_dict["annotations"]:
        ann_area[ann_class[image["category_id"]]].append(image['area'])
        if image['category_id'] == 1 and image['area'] < 200000:
            print(image['id'])


# 画直方图，输入类别categ_name和对应长宽比数组data_array
def plot_hist(date_array, categ_name, bin=15):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.12)
    plt.title(chinese_dict[categ_name] + "的长宽比分布", size=15)
    plt.xlabel("长宽比", size=15)
    plt.ylabel("数量", size=15)
    plt.xticks(fontsize=13)
    # plt.yticks([0, 4, 8, 12, 16, 20], fontsize=13)
    # weights = np.ones_like(date_array) / float(len(date_array))
    # plt.hist(date_array, weights=weights, bins=bin, color='slategray', histtype='bar', align='left', rwidth=0.97)
    plt.hist(date_array, bins=bin, color='tan', histtype='bar', align='left', rwidth=0.97)
    plt.show()


# 面积直方图
def plot_hist_area(date_array, categ_name, bin=15):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.12)
    plt.title(chinese_dict[categ_name] + "的面积分布", size=20)
    plt.xlabel("面积", size=20)
    plt.ylabel("数量", size=20)
    plt.xticks(fontsize=13)
    # plt.yticks([0, 4, 8, 12, 16, 20], fontsize=13)
    area = np.array(date_array[categ_name])
    area = area * (16 / 25)
    plt.hist(area, bins=bin, color='olive', histtype='bar', align='left', rwidth=0.97)
    plt.show()


# 所有对象的长宽比
def plot_hist_all(date_array, bin=10):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.1)
    plt.title("过采样后的长宽比统计")
    plt.xlabel("长宽比")
    plt.ylabel("对象的数量")
    # weights = np.ones_like(date_array) / float(len(date_array))
    # plt.hist(date_array, weights=weights, bins=bin, color='slategray', histtype='bar', align='left', rwidth=0.97)
    plt.hist(date_array, bins=bin, color='darkslateblue', histtype='bar', align='left', rwidth=0.97)
    plt.show()


def get_ann_aspect_ratio(categ_name, ann_height, ann_width):
    ratio = make_ratio(ann_height[categ_name], ann_width[categ_name])
    plot_hist(ratio, categ_name)


if __name__ == '__main__':
    # 标注文件的绝对路径
    # trainset
    json_path_train = "E:/Wen/trainset/TrainSet_THz_1110.json"
    # # testset
    json_path_test = "E:/Wen/testset/TestSet_THz_1110.json"

    # 用于类别统计计数
    class_dict = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}

    # annotation字段中相应的分类
    ann_class = {1: "human", 2: "bottle", 3: "knife", 4: "rifle", 5: "gun"}
    chinese_dict = {'human': '人体', 'bottle': '水瓶', 'knife': '刀具', 'rifle': '步枪', 'gun': '手枪'}
    # 用于统计各类物品的width和height
    ann_height = {"human": [], "bottle": [], "knife": [], "rifle": [], "gun": []}
    ann_width = {"human": [], "bottle": [], "knife": [], "rifle": [], "gun": []}
    # 用于统计各类物品的面积
    ann_area = {"human": [], "bottle": [], "knife": [], "rifle": [], "gun": []}

    # =========================================================
    # 导入训练集和测试集

    with open(json_path_train) as load_json:
        load_dict_train = json.load(load_json)
    with open(json_path_test) as load_json:
        load_dict_test = json.load(load_json)

    # =========================================================
    # 对训练集和测试集的危险物品数目进行统计，结果保存在class_dict

    get_class(load_dict_train)
    get_class(load_dict_test)  # 这里既有TrainSet，也有TestSet

    # =========================================================
    # 对训练集和测试集的危险物品 长与宽 进行统计，结果保存在ann_width和ann_height

    width_height_statistic(load_dict_train, ann_height, ann_width)  # 填充ann_w和ann_h
    width_height_statistic(load_dict_test, ann_height, ann_width)  # 这里既有TrainSet，也有TestSet

    # =========================================================
    # 对训练集和测试集的危险物品的 面积 进行统计，结果保存在ann_area

    area_statistic(load_dict_train, ann_area)  # 填充ann_w和ann_h
    area_statistic(load_dict_test, ann_area)  # 这里既有TrainSet，也有TestSet

    # =========================================================
    # 输出各类危险物品的 长宽比 统计直方图

    for i in {1, 2, 3, 4, 5}:
        get_ann_aspect_ratio(ann_class[i], ann_height, ann_width)

    # =========================================================
    # 输出各类危险物品的 面积 统计直方图

    for i in {1, 2, 3, 4, 5}:
        plot_hist_area(ann_area, ann_class[i])

    # ==================================================
    # # 所有类别合计的长宽比
    # all_height = []
    # all_width = []
    # for i in {1, 2, 3, 4, 5}:
    #     if i == 1:
    #         n = 1
    #     elif i == 2:
    #         n = 8
    #     elif i == 3:
    #         n = 13
    #     elif i == 4:
    #         n = 13
    #     else:
    #         n = 8
    #     print(n * len(ann_width[ann_class[i]]))
    #     for j in range(n):
    #         all_height += ann_height[ann_class[i]]
    #         all_width += ann_width[ann_class[i]]
    # ratio_all = make_ratio(all_height, all_width)
    # plot_hist_all(ratio_all)
    # =====================================================================
