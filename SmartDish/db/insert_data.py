

FEATURES = {
    "类型": ["硬菜", "小吃", "正餐", "方便", ],
    "冷热": ["冷", "热", "烫", "拔凉", ],
    "口味": ["酸", "甜", "辣", "麻辣", "香辣", "咸", "苦", ],
    "口感": ["清淡", "重口", "鲜香", "爽口", "嫩", "酥脆", ],
    "比例": ["肉多", "蔬菜多", "海鲜", ],
    "做法": ["炒菜", "炖菜", "油炸", "烘烤", "蒸", "煮", "汤", "传统面食", "带陷", "甜点", "面条", ],
    "地域": ["川菜", "湘菜", "粤菜", "东北菜", "西北菜", "淮南菜", "西餐", "清真", ],

    "营养":["高蛋白", "低脂肪", "营养均衡", "高维生素", "低热量", "低碳水", "低胆固醇", ],
    "受众":["增肌", "减脂", "适合糖尿病人", "适合高血压患者", ],
}

'''
把上面字典中 没有的健 和值 插入到数据库中~

已经做好了过滤,已经在数据库的值不会发生重复
'''
def insert_into_dish_feature():

    from dish.models import DishFeatureType
    from dish.models import DishFeature

    for typeName in FEATURES.keys():
        fnList = FEATURES[typeName]

        featureType = DishFeatureType.objects.filter(typeName=typeName)
        # 如果分类名称没有存到数据库 就把这个key存到数据库DishFeatureType
        if not featureType:
            featureType = DishFeatureType(typeName=typeName)
            featureType.save()
        # 否则这个key 已经在DishFeatureType里
        else:
            featureType = featureType[0]
        # 到这里 拿到当前key对应的 标签特点类型

        for f in fnList:
            feature = DishFeature.objects.filter(featureType=featureType,featureName=f)
            if feature:
                continue
            else:
                feature = DishFeature(featureType=featureType,featureName=f)
                feature.save()

def go():
    insert_into_dish_feature()


if __name__ == '__main__':
    go()