import json
import os

def get_dish_list():
    dish_list = []
    with open("./spiderData/dishes.json","r") as f:
        line = f.readline()
        while line:
            line = line.rstrip("\n")
            con = json.loads(line)
            dish_list.append(con)
            line = f.readline()
    return dish_list

def get_label_list(dish_list):
    label_list = []
    for con in dish_list:
        labels = con["labels"]
        for i in labels:
            if i not in label_list:
                label_list.append(i)
    return label_list

def split_dish_list(dish_list,label_list):
    for label in label_list:
        with open("./spiderData/splitData/"+label+".json","a") as f:
            for dish in dish_list:
                if label in dish["labels"]:
                    f.write(json.dumps(dish,ensure_ascii=False)+"\n")


if __name__ == '__main__':
    dish_list = get_dish_list()
    label_list = get_label_list(dish_list)
    for label in label_list:
        if os.path.exists("./spiderData/splitData/"+label+".json"):
            os.remove("./spiderData/splitData/"+label+".json")
    split_dish_list(dish_list, label_list)