from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import OrderNo, OrderInfo
from utils.decoratiors import login_required
from django.core.paginator import Paginator

# /order/checkNewOrder/ 查询是否有新的订单为处理
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def checkNewOrder(request):
    username = request.GET.get("username")
    try:
        if OrderNo.objects.check_new_order(username):
            return JsonResponse({"msg": True})
        else:
            return JsonResponse({"msg": False})
    except Exception as e:
        print(e)
    return JsonResponse({"msg":False})


# /order/finishOrder/ 完成订单结算
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def finishOrder(request):
    if request.method == "GET":
        orderId = request.GET.get("oid")
        try:
            OrderNo.objects.finish_one_obj(orderId)
        except Exception as e:
            print(e)
        return redirect("/order/orderManage")
    else:
        pass

# /order/orderManage/ 用户订单管理
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def orderManage(request):
    if request.method == "GET":
        userID = request.session.get("userID")
        startTime = request.GET.get("start_time")
        endTime = request.GET.get("end_time")
        keyWord = request.GET.get("key_word","")
        isPayed = request.GET.get("is_payed","")
        is_payed = True if isPayed == "true" else False if isPayed == "false" else None

        orderList = OrderNo.objects.get_order_list_by_user_and_sort(userID,startTime,endTime,keyWord,is_payed)
        orderInfoList = OrderInfo.objects.get_order_info_list(orderList)

        # 分页部分
        paginator = Paginator(orderInfoList, 5)  # 分页对象 每页显示5条
        # 制作最多包含5页的页码列表
        try:
            nextPage = int(request.GET.get("page", "1"))  # 当前要去的页码
        except:
            nextPage = 1

        curPaginator = paginator.page(nextPage)  # 下一页的paginator对象
        objList = curPaginator.object_list  # 要去的页码的所有数据
        pageCount = len(paginator.page_range)
        start = 1 if nextPage - 2 <= 1 else nextPage - 2
        end = pageCount if nextPage + 2 >= pageCount else nextPage + 2

        pageRange = range(start, end + 1)

        context = {
            "start_time":startTime,
            "end_time":endTime,
            "key_word":keyWord,
            "is_payed":isPayed,
            "orderInfoList":objList,
            "pageRange": [str(i) for i in pageRange],
            "curPaginator": curPaginator,
            "curPage": str(nextPage),
        }
        return render(request, "order/orderManage.html", context=context)
    else:
        pass