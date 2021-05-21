from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from book_control.forms import *
# from .forms import *
from user_control.models import *
from book_control.models import *
from .models import *
from .utils import *


@login_required
def order_details_view(request, pk):
    order_item = OrderModel.objects.get(id=pk)
    order_payment_item = None
    try:
        order_payment_item = OrderPaymentModel.objects.get(order=order_item)
    except:
        order_payment_item = None
    book = order_item.book

    is_student = False
    if request.user.is_student:
        is_student = True

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)
    print(order_payment_item)

    if request.GET.get('confirmPayment'):
        order_item.publisher_paid_approval = True
        order_item.save()
        return redirect('publisher-unpaid-orders')

    context = {
        'order_item': order_item,
        'order_payment_item': order_payment_item,
        'book': book,
        'is_student': is_student,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'order-details.html', context)


@login_required
def publisher_unchecked_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    if request.GET.get('acceptOrder'):
        item_id = int(request.GET.get('orderID'))
        print(item_id)
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_approved = True
        order_item.save()
        return redirect('publisher-unchecked-orders')

    if request.GET.get('rejectOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.delete()
        return redirect('publisher-unchecked-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'publisher/unchecked-orders.html', context)


@login_required
def publisher_unpaid_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'publisher/unpaid-orders.html', context)


@login_required
def publisher_orders_to_deliver_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    if request.GET.get('deliverOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.is_completed = True
        order_item.save()
        return redirect('publisher-orders-to-deliver')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'publisher/orders-to-deliver.html', context)


@login_required
def publisher_completed_orders_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'publisher/completed-orders.html', context)


@login_required
def student_pending_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    if request.GET.get('cancelOrder'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.delete()
        return redirect('student-pending-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'student/pending-orders.html', context)


@login_required
def student_unpaid_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    if request.GET.get('submitPayment'):
        item_id = int(request.GET.get('orderID'))
        order_item = OrderModel.objects.get(id=item_id)
        order_item.student_paid_approval = True
        order_item.save()

        transactionID = request.GET.get('transactionID')
        phoneNumber = request.GET.get('phoneNumber')
        OrderPaymentModel.objects.create(order=order_item, transaction_id=transactionID,
                                         phone_number=phoneNumber)
        return redirect('student-unpaid-orders')

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'student/unpaid-orders.html', context)


@login_required
def student_orders_to_deliver_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'student/orders-to-deliver.html', context)


@login_required
def student_completed_orders_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'student/completed-orders.html', context)
