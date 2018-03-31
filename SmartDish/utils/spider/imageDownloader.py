import json
import requests
import os
i = 0

if os.path.exists("./spiderData/dish_list_with_image.json"):
    os.remove("./spiderData/dish_list_with_image.json")


f2 = open("./spiderData/dish_list_with_image.json","a")

with open("./spiderData/dishes.json","r") as f:
    line = f.readline()
    while line:
        line = line.rstrip("\n")
        obj = json.loads(line)
        image_url = obj["image"]
        image_name = "test_images/%s_"%i +image_url.split("/")[-1]
        image_path = "../../static/media/image/"+image_name
        html = requests.get(image_url).content
        f1 = open(image_path,"wb")
        f1.write(html)
        f1.close()
        obj["image_name"] = image_name

        f2.write(json.dumps(obj,ensure_ascii=False) +"\n")
        i+=1
        print("%s:%s"%(i,obj["name"]))


        line = f.readline()

f2.close()