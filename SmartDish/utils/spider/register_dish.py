import json
from re_user.models import ReUserInfo
from dish.models import DishInfo,DishType,DishFeature,DishFeatureType
import random

'''
from utils.spider.register_dish import run
'''


def run():
    i = 1
    res_no = 0

    re_user = ReUserInfo.objects.add_one_object(username="res%s" % res_no, password=str(res_no))
    re_user.save()
    default_type = DishType.objects.add_one_object(userID=re_user.id, typename="默认")
    default_type.save()
    feature_type_id = 10

    image_url = ""

    with open("./utils/spider/spiderData/dish_list_with_image.json","r") as f:
        line = f.readline()
        while line:
            if i % 100 == 0:
                res_no+=1
                re_user = ReUserInfo.objects.add_one_object(username="res%s" % res_no, password=str(res_no))
                re_user.name = "测试餐厅%s"%res_no
                re_user.phone = res_no
                re_user.image = image_url
                re_user.save()
                default_type = DishType.objects.add_one_object(userID=re_user.id, typename="默认")
                default_type.save()

            try:
                json_obj = line.rstrip("\n")
                con = json.loads(json_obj)
                image_url = con["image_name"]
                features = []
                if con["labels"]:
                    features += con["labels"]
                if con["features"]:
                    features += con["features"]
                if con["method"] :
                    features.append(con["method"])

                feature_id_list = []
                for fea in features:
                    df = DishFeature.objects.filter(featureName=fea)
                    if df:
                        df = df[0]
                        feature_id_list.append(str(df.id))
                    else:
                        df = DishFeature(featureName=fea,featureType_id=feature_type_id)
                        df.save()
                        feature_id_list.append(str(df.id))
                dish = DishInfo(
                            dish_type=default_type,
                            dishName=con["name"],
                            dishPrice=random.randint(5,30),
                            dishImage=con["image_name"],
                            dishDetail=con["detail"],
                            dishFeature=",".join(feature_id_list)
                        )
                dish.save()

            except Exception as e:
                print(e)

            i += 1
            line = f.readline()


if __name__ == '__main__':
    run()