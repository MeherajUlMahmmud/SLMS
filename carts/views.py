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
    book = order_item.book

    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    context = {
        'order_item': order_item,
        'book': book,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'user_control/order-details.html', context)


@login_required
def publisher_unchecked_order_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    if request.GET.get('acceptOrder'):
        item_id = int(request.GET.get('orderID'))
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
        order_item.advertiser_paid_approval = True
        order_item.is_running = True
        order_item.is_running = True
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
        order_item.customer_paid_approval = True
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
