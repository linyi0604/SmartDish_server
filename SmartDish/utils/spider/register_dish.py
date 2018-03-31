import json
from re_user.models import ReUserInfo
from dish.models import DishInfo,DishType,DishFeature,DishFeatureType
import random

'''
from utils.spider.register_dish import run
'''


def run():
    feature_type_id = 10
    res_id = 9
    re_user = ReUserInfo.objects.get(id=res_id)
    dish_type = DishType.objects.filter(re_user=re_user)
    default_type = dish_type[0]

    with open("./utils/spider/spiderData/dish_list_with_image.json","r") as f:
        line = f.readline()
        while line:
            try:
                json_obj = line.rstrip("\n")
                con = json.loads(json_obj)
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

            line = f.readline()


if __name__ == '__main__':
    run()