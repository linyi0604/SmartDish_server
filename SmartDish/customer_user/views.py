from django.http import JsonResponse, HttpResponse
from dish.models import DishInfo, DishFeature
from re_user.models import ReUserInfo
from utils.common import BASE_IMAGE_URL, TIME_DELAY
from utils.decoratiors import phone_required
from utils.get_hash import get_hash
from .models import CustomerUserInfo, Cart, Favorite, CustomerRecord
from order.models import OrderInfo, OrderNo
from django.db.models import Q
import time
import math

def getDishPage(request):
    '''手机端菜品主页所有数据'''
    username = request.GET.get("username")

    channel_info = DishFeature.objects.all()[0:11]
    dishList = DishInfo.objects.all().order_by("-dishSellCount")[0:10]
    recommendList = CustomerRecord.objects.get_recommend_list(username)

    try:
        recommend_info = recommendList[0:12]
        banner_info = recommendList[12:20]
        act_info = recommendList[20:30]
        secKill_info = recommendList[30:35]
        hot_info = recommendList[35:41]


    except Exception as e:
        print(e)
        banner_info = dishList
        recommend_info = dishList
        act_info = dishList
        secKill_info = dishList
        hot_info = dishList

    t = math.floor(time.time() * 1000)
    context = {
        # banner 广告横幅
        "banner_info": [
                {
                    "price_origin":"",
                    "price": i.dishPrice,
                    "image_url": BASE_IMAGE_URL + i.dishImage,
                    "name": i.dishName,
                    "restaurant": i.dish_type.re_user.name,
                    "restaurant_id": i.dish_type.re_user.id,
                    "detail": i.dishDetail,
                    "features": DishFeature.objects.get_name_str_list_from_id_str_list(i.dishFeature),
                    "id": i.id,
                } for i in banner_info
            ],
        # 入口按钮信息
        "channel_info":[
            {
                "image_url":"/static/media/image/customer/channel/00"+str(i.id-1)+".png",
                "name":i.featureName,
                "id":i.id,
            } for i in channel_info
        ],
        # 活动信息
        "act_info":[
                {
                    "price_origin":"",
                    "price": i.dishPrice,
                    "image_url": BASE_IMAGE_URL + i.dishImage,
                    "name": i.dishName,
                    "restaurant": i.dish_type.re_user.name,
                    "restaurant_id": i.dish_type.re_user.id,
                    "detail": i.dishDetail,
                    "features": DishFeature.objects.get_name_str_list_from_id_str_list(i.dishFeature),
                    "id": i.id,
                } for i in act_info
            ],
        # secKill 秒杀部分数据
        "secKill_info":{
            "end_time":t+1000*60*60*2,
            "start_time":t+1000*60,
            "list":[
                {
                    "price_origin":"",
                    "start_time":"",
                    "end_time":"",
                    "price": i.dishPrice,
                    "image_url": BASE_IMAGE_URL + i.dishImage,
                    "name": i.dishName,
                    "restaurant": i.dish_type.re_user.name,
                    "restaurant_id": i.dish_type.re_user.id,
                    "detail": i.dishDetail,
                    "features": DishFeature.objects.get_name_str_list_from_id_str_list(i.dishFeature),
                    "id": i.id,
                } for i in secKill_info
            ]
        },

        # recommend 推荐数据
        "recommend_info":[
            {
                "price": i.dishPrice,
                "image_url": BASE_IMAGE_URL + i.dishImage,
                "name": i.dishName,
                "restaurant": i.dish_type.re_user.name,
                "restaurant_id": i.dish_type.re_user.id,
                "detail": i.dishDetail,
                "features": DishFeature.objects.get_name_str_list_from_id_str_list(i.dishFeature),
                "id": i.id,
            } for i in recommend_info
        ],
        # hot 热卖信息
        "hot_info": [
            {
                "price": i.dishPrice,
                "image_url": BASE_IMAGE_URL + i.dishImage,
                "name": i.dishName,
                "restaurant": i.dish_type.re_user.name,
                "restaurant_id": i.dish_type.re_user.id,
                "detail": i.dishDetail,
                "features": DishFeature.objects.get_name_str_list_from_id_str_list(i.dishFeature),
                "id": i.id,
            } for i in hot_info
        ],

    }
    return JsonResponse(context)

# /customer_user/addStep
# 添加用户浏览一个商品的轨迹
def addStep(request):
    dish_id = request.GET.get("dish_id")
    username = request.GET.get("username")
    try:
        CustomerRecord.objects.add_one_step(dish_id,username)
    except Exception as e:
        print(e)
    try:
        recommendList = CustomerRecord.objects.get_recommend_list_from_dish_id(dish_id)
        recommend_info = recommendList[0:9]
    except Exception as e:
        print(e)
        dishList = DishInfo.objects.all().order_by("-dishSellCount")[0:9]
        recommend_info = dishList

    context = {
        # recommend 推荐数据
        "recommend_info": [
            {
                "price": i.dishPrice,
                "image_url": BASE_IMAGE_URL + i.dishImage,
                "name": i.dishName,
                "restaurant": i.dish_type.re_user.name,
                "restaurant_id": i.dish_type.re_user.id,
                "detail": i.dishDetail,
                "features": DishFeature.objects.get_name_str_list_from_id_str_list(i.dishFeature),
                "id": i.id,
            } for i in recommend_info
        ],
    }
    return JsonResponse(context)

def getDishList(request):
    '''获取所有菜品列表'''
    dishList = DishInfo.objects.get_dish_list()
    list = []
    for dish in dishList:
        list.append({
            "dishID":dish.id,
            "dishResName":dish.dish_type.re_user.name,
            "dishResID":dish.dish_type.re_user.id,
            "dishName":dish.dishName,
            "dishDetail":dish.dishDetail,
            "dishImage":"/static/media/image/"+dish.dishImage,
        })
    context = {
            "imageList":[
                "/static/media/image/customer/banner/banner1.png",
                "/static/media/image/customer/banner/banner2.png",
            ],
            "dishList":list,
        }
    return JsonResponse(context)

# /customer_user/getOrderInfo
# 获取某条订单详情信息
def getOrderInfo(request):
    from datetime import timedelta
    orderNoId = request.GET.get("order_id")
    try:
        order = OrderNo.objects.get(id=orderNoId)
        order_info_list = OrderInfo.objects.filter(order=order)
        context = {
                    "id":order.id,
                    "time":(order.create_time+timedelta(hours=TIME_DELAY)).strftime("%Y-%m-%d %H:%M:%S"),
                    "restaurant":order.re_user.name,
                    "restaurant_id":order.re_user.id,
                    "is_payed":"未支付" if order.is_payed is False else "已支付",
                    "dish_count":order.count,
                    "total_price":order.price,
                    "dish_list":[{
                        "id":order_info.dish.id,
                        "name":order_info.dish.dishName,
                        "image_url":BASE_IMAGE_URL+order_info.dish.dishImage,
                        "price":order_info.dish.dishPrice,
                        "detail":order_info.dish.dishDetail,
                        "grade":order_info.dish.dishGrade,
                        "sell_count":order_info.dish.dishSellCount,
                        "restaurant_id":order_info.dish.dish_type.re_user.id,
                        "restaurant":order_info.dish.dish_type.re_user.name,
                        "features":DishFeature.objects.get_name_str_list_from_id_str_list(order_info.dish.dishFeature),
                        "count":order_info.count,
                    } for order_info in order_info_list],
                }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

# /customer_user/getOrder
# 获取订单列表
def getOrder(request):
    username = request.GET.get("username")
    try:
        order_list = OrderNo.objects.filter(customer__username=username).order_by("-create_time")
        order_info_list = {order:OrderInfo.objects.filter(order=order) for order in order_list}
        from functools import reduce
        from datetime import timedelta
        context = {"list":[
            {
                "id":order.id,
                "time":(order.create_time+timedelta(hours=TIME_DELAY)).strftime("%Y-%m-%d %H:%M:%S"),
                "restaurant":order.re_user.name,
                "restaurant_id":order.re_user.id,
                "is_payed":"未支付" if order.is_payed is False else "已支付",
                "dish_count":reduce(lambda x,y:x+y,[i.count for i in order_info_list[order]]),
                "total_price":reduce(lambda x,y:x+y,[i.count*i.dish.dishPrice for i in order_info_list[order]]),
                "dish_list":[{
                    "id":order_info.dish.id,
                    "name":order_info.dish.dishName,
                    "image_url":BASE_IMAGE_URL+order_info.dish.dishImage,
                    "price":order_info.dish.dishPrice,
                    "detail":order_info.dish.dishDetail,
                    "grade":order_info.dish.dishGrade,
                    "sell_count":order_info.dish.dishSellCount,
                    "restaurant_id":order_info.dish.dish_type.re_user.id,
                    "restaurant":order_info.dish.dish_type.re_user.name,
                    "features":DishFeature.objects.get_name_str_list_from_id_str_list(order_info.dish.dishFeature),
                    "count":order_info.count,
                } for order_info in order_info_list[order]],
            } for order in order_list
        ]}
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


# /customer_user/addOrder
# 购物车结算到订单
def addOrder(request):
    username = request.GET.get("username")
    dish_id_list = request.GET.get("id_list").split(",")
    try:
        cart_list = Cart.objects.filter(customer__username=username,dish_id__in=dish_id_list)
        order = OrderNo.objects.add_one_order(username=username,cart_list=cart_list)
        OrderInfo.objects.add_by_order_and_cart_list(order=order, cart_list=cart_list)
        Cart.objects.delete_by_username_and_dish_id_list(username,dish_id_list)
        return HttpResponse("OK")
    except Exception as e:
        print(e)
        return HttpResponse(e)


# /customer_user/getTypeDishInfo
# 获取餐厅菜单  分类 餐品 信息
def getTypeDishInfo(request):
    res_id = request.GET.get("res_id")
    try:
        type_list = ReUserInfo.objects.get_type_dish_list(res_id)
        context = {"list":[
            {
                "typeId":t.id,
                "typeName":t.typeName,
                "dishList":[{
                    "id":dish.id,
                    "name":dish.dishName,
                    "image_url":BASE_IMAGE_URL+dish.dishImage,
                    "price":dish.dishPrice,
                    "detail":dish.dishDetail,
                    "grade":dish.dishGrade,
                    "sell_count":dish.dishSellCount,
                    "restaurant_id":dish.dish_type.re_user.id,
                    "restaurant":dish.dish_type.re_user.name,
                    "features":DishFeature.objects.get_name_str_list_from_id_str_list(dish.dishFeature),
                } for dish in DishInfo.objects.filter(dish_type=t)]
            } for t in type_list
        ]}
        return JsonResponse(context)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))

# /customer_user/getResInfo
# 获取餐厅详细信息
def getResInfo(request):
    res_id = request.GET.get("res_id")
    try:
        res = ReUserInfo.objects.get(id=res_id)
        context = {
            "id": res.id,
            "username": res.username,
            "name": res.name,
            "address": res.address,
            "phone": res.phone,
            "detail": res.detail,
            "grade":res.grade,
            "sellCount":res.sellCount,
            "image_url": BASE_IMAGE_URL + res.image,
        }

        return JsonResponse(context)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


# /customer_user/searchRes
# 搜索餐厅列表
def searchRes(request):
    keyWord = request.GET.get("key_word")
    sort = request.GET.get("sort")
    try:
        res_list = ReUserInfo.objects.filter(name__contains=keyWord).order_by(sort)
        context = {
            "list": [{
                "id": res.id,
                "username": res.username,
                "name": res.name,
                "address": res.address,
                "phone": res.phone,
                "detail": res.detail,
                "grade":res.grade,
                "sellCount":res.sellCount,
                "image_url": BASE_IMAGE_URL + res.image,
            } for res in res_list]
        }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

# /customer_user/searchDish
# 搜索菜品列表
def searchDish(request):
    key_word = request.GET.get("key_word")
    sort = request.GET.get("sort")
    result_list = DishInfo.objects.filter(Q(dishName__contains=key_word)
                                          |Q(dishDetail__contains=key_word)).order_by(sort)

    context = {"list":[{
            "id":dish.id,
            "name":dish.dishName,
            "image_url":BASE_IMAGE_URL+dish.dishImage,
            "price":dish.dishPrice,
            "detail":dish.dishDetail,
            "grade":dish.dishGrade,
            "sell_count":dish.dishSellCount,
            "restaurant_id":dish.dish_type.re_user.id,
            "restaurant":dish.dish_type.re_user.name,
            "features":DishFeature.objects.get_name_str_list_from_id_str_list(dish.dishFeature),
        }for dish in result_list]}
    return JsonResponse(context)


# /customer_user/deleteFavorite
# 删除收藏夹中某一商品
def deleteFavorite(request):
    event_id = request.GET.get("event_id")
    try:
        Favorite.objects.delete_by_id(event_id)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))
    return HttpResponse("OK")

# /customer_user/getFavorite
# 获取收藏夹所有商品
def getFavorite(request):
    username = request.GET.get("username")
    try:
        favorite_list = Favorite.objects.filter(customer__username=username)
        context = {
            "list":[{
                "id":obj.dish.id,
                "price":obj.dish.dishPrice,
                "detail":obj.dish.dishDetail,
                "image_url":BASE_IMAGE_URL+obj.dish.dishImage,
                "name":obj.dish.dishName,
                "grade":obj.dish.dishGrade,
                "sell_count":obj.dish.dishSellCount,
                "restaurant":obj.dish.dish_type.re_user.name,
                "restaurant_id":obj.dish.dish_type.re_user.id,
                "features":DishFeature.objects.get_name_str_list_from_id_str_list(obj.dish.dishFeature),
                "event_id":obj.id,
            } for obj in favorite_list ]
        }
        return JsonResponse(context)

    except Exception as e:
        print(e)
        return HttpResponse(str(e))

# /customer_user/checkFavorite
# 检查该商品是否在自己的收藏夹里
def checkFavorite(request):
    username = request.GET.get("username")
    dish_id = request.GET.get("dish_id")
    try:
        if Favorite.objects.filter(customer__username=username,dish_id=dish_id):
            return HttpResponse("true")
        else:
            return HttpResponse("false")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

# /customer_user/addFavorite
# 手机用户添加到收藏夹
def addFavorite(request):
    dish_id = request.GET.get("dish_id")
    username = request.GET.get("username")
    # 检查一下是否已经在购物车了
    try:
        obj = Favorite.objects.filter(dish_id=dish_id,customer__username=username)
        if obj:
            return HttpResponse("该商品您已经收藏过了!")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))
    try:
        Favorite.objects.add_one_object(dish_id,username)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

    return HttpResponse("OK")


# /customer_user/updateCustomerInfo
# 手机用户修改个人信息
def updateCustomerInfo(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    name = request.GET.get("name")
    phone = request.GET.get("phone")
    detail = request.GET.get("detail")
    try:
        CustomerUserInfo.objects.update_one_object(username,password,name,phone,detail)
    except Exception as e:
        print(e)
        return HttpResponse(str(e))
    return HttpResponse("OK")

# /customer_user/deleteCartInfo
# 删除购物车中某商品
def deleteCartInfo(request):
    id_list = request.GET.get("id_list")
    id_list = id_list.lstrip("[").rstrip("]").split(",")
    try:
        Cart.objects.delete_by_id_list(id_list)
    except Exception as e:
        print(e)
        return HttpResponse("notOK:"+str(e))
    return HttpResponse("OK")

# /customer_user/updateCartDishCount
# 更改购物车中某商品数量
def updateCartDishCount(request):
    cart_id = request.GET.get("cart_id")
    count = request.GET.get("count")
    try:
        Cart.objects.update_one_object(cart_id=cart_id,count=count)
    except Exception as e:
        print(e)
        return HttpResponse("notOK")
    return HttpResponse("OK")

# /customer_user/getCart
# 手机用户申请购物车数据
def getCart(request):
    username = request.GET.get("username")
    try:
        cart_info = Cart.objects.get_cart_info(username)
        if not cart_info:
            raise Exception
        context={"list":[
            {
                "event_id":i.id,    # 该条申请的id 在这里是购物车id
                "id":i.dish_id,     # 菜品的id
                "name":i.dish.dishName, # 菜品名称
                "detail":i.dish.dishDetail, # 菜品的介绍
                "count":i.count,    # 菜品的数量
                "price":i.dish.dishPrice,   # 菜品的价格
                "image_url":BASE_IMAGE_URL+i.dish.dishImage,    # 图片地址
                "restaurant_id":i.dish.dish_type.re_user.id,    # 所属餐厅的id
                "restaurant":i.dish.dish_type.re_user.name, # 所属餐厅名称
                "features":DishFeature.objects.get_name_str_list_from_id_str_list(i.dish.dishFeature), # 菜品特点
            } for i in cart_info
        ]}
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return HttpResponse(e)


# /customer_user/addCart
# 手机用户添加商品到购物车
def addCart(request):
    username = request.GET.get("username")
    dish_id = request.GET.get("dish_id")
    # 1 先检查目前购物车当中有没有不是当前商家的菜品
    cart_list = Cart.objects.filter(customer__username=username,is_payed=False)
    re_user = DishInfo.objects.get(id=dish_id).dish_type.re_user
    if cart_list:
        if cart_list[0].dish.dish_type.re_user.id != re_user.id:
            return HttpResponse("Unique")

    # 2 购物车当中都是该商家的菜品,就添加到购物车当中
    try:
        Cart.objects.add_to_cart(username,dish_id)
        return HttpResponse("OK")
    except Exception as e:
        print(e)
        return HttpResponse(e)


# /customer_user/login
# 手机用户进行登陆
@phone_required
def login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    old_username = request.GET.get("old_username")
    try:
        # 查询数据库看是否有重复
        user = CustomerUserInfo.objects.get_one_object_by_username(username)
        if not user or user.password != get_hash(password):
            return HttpResponse("notOK")
        else:
            CustomerRecord.objects.login(old_username,user)
            return JsonResponse({
                "username":user.username,
                "name":user.name,
                "phone":user.phone,
                "detail":user.detail,
            })

    except Exception as e:
        print(e)
        return HttpResponse(str(e))


# /customer_user/register
# 手机用户进行注册逻辑
@phone_required
def register(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    try:
        # 查询数据库看是否有重复
        user = CustomerUserInfo.objects.get_one_object_by_username(username)
        if user:
            return HttpResponse("notOK")
        else:
            CustomerUserInfo.objects.add_one_object(username,password)
            return HttpResponse("OK")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))


