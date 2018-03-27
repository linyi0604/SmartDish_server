from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from .models import DishType, DishInfo, DishFeature
from utils.decoratiors import login_required
from django.core.paginator import Paginator

# Create your views here.

# /dish/dish/ 用户菜品管理
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def dishManage(request):
    if request.method == "GET":
        userID = request.session.get("userID")
        # 查询条件
        dishTypeID = request.GET.get("dishTypeID")
        dishTypeID = int(dishTypeID) if dishTypeID != "all" and dishTypeID is not None else "all"
        dishName = request.GET.get("dishName")

        # 该餐厅菜品分类列表
        typeList = DishType.objects.get_type_list(userID=userID)
        # 该餐厅所有菜品
        dishList = DishInfo.objects.get_dish_by_condition(userID=userID,dishTypeID=dishTypeID,dishName=dishName)

        # 分页部分
        paginator = Paginator(dishList, 5) # 分页对象 每页显示5条
        # 制作最多包含5页的页码列表
        try:
            nextPage = int(request.GET.get("page", "1")) # 当前要去的页码
        except:
            nextPage = 1

        curPaginator = paginator.page(nextPage) # 下一页的paginator对象
        objList = curPaginator.object_list # 要去的页码的所有数据
        pageCount = len(paginator.page_range)
        start = 1 if nextPage-2 <= 1 else nextPage-2
        end = pageCount if nextPage+2 >= pageCount else nextPage + 2

        pageRange = range(start,end+1)



        context = {
            "typeList": typeList,
            "dishList": objList,
            "dishTypeID":dishTypeID,
            "pageRange":[ str(i) for i in pageRange],
            "curPaginator":curPaginator,
            "curPage":str(nextPage),
        }
        if dishName is not None:
            context["dishName"] = dishName
        return render(request, "dish/dishManage.html",context=context)
    else:
        pass

# /dish/typeManage  用户菜品分类管理
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def typeManage(request):
    if request.method == "GET":
        userID = request.session.get("userID")
        typeList = DishType.objects.get_type_list(userID=userID)
        context = {"typeList":typeList}

        return render(request, "dish/typeManage.html", context=context)
    else:
        pass


# /dish/addType  餐厅用户添加菜品分类
@login_required
@require_http_methods(['GET'])  # 限制访问请求类型
def addType(request):
    typename = request.GET.get("typename")
    userID = request.session.get("userID")
    try:
        DishType.objects.add_one_object(userID=userID,typename=typename)
    except Exception as e:
        return JsonResponse({"info": "发生错误:"+str(e)})

    return JsonResponse({"info":"OK"})


# /dish/deleteType  删除菜品分类
@login_required
@require_http_methods(['GET'])  # 限制访问请求类型
def deleteType(request):
    typeID = request.GET.get("typeID")
    try:
        DishType.objects.delete_one_object(tid=typeID)
    except Exception as e:
        return JsonResponse({"info": "发生错误:"+str(e)})

    return JsonResponse({"info":"OK"})


# /dish/changeTypeName  修改菜品分类名称
@login_required
@require_http_methods(['GET'])  # 限制访问请求类型
def changeTypeName(request):
    typeID = request.GET.get("typeID")
    typeName = request.GET.get("value")
    try:
        DishType.objects.change_one_object(typeID=typeID,typeName=typeName)
    except Exception as e:
        return JsonResponse({"info": "发生错误:"+str(e)})

    return JsonResponse({"info":"OK"})

# /dish/addDish  添加菜品
@login_required
@require_http_methods(['GET','POST'])  # 限制访问请求类型
def addDish(request):
    if request.method == "GET":
        userID = request.session.get("userID")
        typeList = DishType.objects.get_type_list(userID=userID)

        featureTable = DishFeature.objects.get_feature_table()

        context = {
            "typeList": typeList,
            "featureTable" : featureTable,
        }
        return render(request, "dish/addDish.html",context=context)
    else:
        dishName = request.POST.get("dishName")
        dishType = request.POST.get("dishType")
        dishPrice = request.POST.get("dishPrice")
        dishImage = request.FILES.get("dishImage")
        dishDetail = request.POST.get("dishDetail")
        dishFeature = request.POST.getlist("dishFeature")
        try:
            obj = DishInfo.objects.add_one_object(dishName=dishName,dish_type=dishType,
                                            dishPrice=dishPrice,dishImage=dishImage,
                                            dishDetail=dishDetail,dishFeature=dishFeature)
        except Exception as e:
            print(str(e))
        return redirect("/dish/dishManage")


# /dish/editDish?did=id 编辑菜品
@login_required
@require_http_methods(["GET","POST"])
def editDish(request):
    '''get返回编辑菜品页面 post保存修改'''
    if request.method == "GET":
        userID = request.session.get("userID")
        dishID = request.GET.get("did")
        dish = DishInfo.objects.get(id=dishID)
        typeList = DishType.objects.get_type_list(userID=userID)
        featureTable = DishFeature.objects.get_feature_table()
        context = {
            "dish":dish,
            "typeList":typeList,
            "featureTable":featureTable,
            "featureList":[int(i) for i in dish.dishFeature.split(",") if "," in dish.dishFeature],  # 已选的特征id列表
        }
        return render(request,"dish/editDish.html",context=context)
    else:
        dishID = request.POST.get("dishID")
        dishName = request.POST.get("dishName")
        dishType = request.POST.get("dishType")
        dishImage = request.FILES.get("dishImage")
        dishPrice = request.POST.get("dishPrice")
        dishDetail = request.POST.get("dishDetail")
        dishFeature = request.POST.getlist("dishFeature")
        try:
            DishInfo.objects.update_one_object(dishID,dishName,dishType,dishImage,dishPrice,dishDetail,dishFeature)
        except Exception as e:
            print(str(e))

        return redirect("/dish/dishManage/")