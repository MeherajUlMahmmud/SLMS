from .models import OrderModel
from user_control.models import StudentProfileModel, PublisherProfileModel
from book_control.models import BookModel


def get_pending_orders(request):
    pending_orders = []
    if request.user.is_authenticated and request.user.is_student:
        student = StudentProfileModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(student=student)
        order_list = list(order_queryset)
        pending_orders = [item for item in order_list
                          if item.student.user == request.user
                          and not item.is_approved
                          and not item.is_canceled
                          and not item.publisher_paid_approval
                          and not item.student_paid_approval
                          and not item.is_completed]
    elif request.user.is_authenticated and request.user.is_publisher:
        publisher = PublisherProfileModel.objects.get(user=request.user)
        book_queryset = BookModel.objects.filter(publisher=publisher)
        book_list = list(book_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list if item.book in book_list]
        pending_orders = [item for item in final_order_list
                          if not item.is_approved
                          and not item.is_canceled
                          and not item.publisher_paid_approval
                          and not item.student_paid_approval
                          and not item.is_completed]

    return pending_orders


def get_unpaid_orders(request):
    unpaid_orders = []
    if request.user.is_authenticated and request.user.is_student:
        student = StudentProfileModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(student=student)
        order_list = list(order_queryset)
        unpaid_orders = [item for item in order_list
                         if item.student.user == request.user
                         and item.is_approved
                         and not item.is_canceled
                         and not item.student_paid_approval
                         and not item.publisher_paid_approval
                         and not item.is_completed]
    elif request.user.is_authenticated and request.user.is_publisher:
        publisher = PublisherProfileModel.objects.get(user=request.user)
        book_queryset = BookModel.objects.filter(publisher=publisher)
        book_list = list(book_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list if item.book in book_list]
        unpaid_orders = [item for item in final_order_list
                         if item.is_approved
                         and not item.is_canceled
                         and not item.publisher_paid_approval
                         and not item.student_paid_approval
                         and not item.is_completed]
    return unpaid_orders


def get_orders_to_deliver(request):
    orders_to_deliver = []
    if request.user.is_authenticated and request.user.is_student:
        student = StudentProfileModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(student=student)
        order_list = list(order_queryset)
        orders_to_deliver = [item for item in order_list
                             if item.student.user == request.user
                             and item.is_approved
                             and not item.is_canceled
                             and not item.publisher_paid_approval
                             and item.student_paid_approval
                             and not item.is_completed]
    elif request.user.is_authenticated and request.user.is_publisher:
        publisher = PublisherProfileModel.objects.get(user=request.user)
        book_queryset = BookModel.objects.filter(publisher=publisher)
        book_list = list(book_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list if item.book in book_list]
        orders_to_deliver = [item for item in final_order_list
                             if item.is_approved
                             and not item.is_canceled
                             and not item.publisher_paid_approval
                             and item.student_paid_approval
                             and not item.is_completed]
    return orders_to_deliver


def get_completed_orders(request):
    completed_orders = []
    if request.user.is_authenticated and request.user.is_student:
        student = StudentProfileModel.objects.get(user=request.user)
        order_queryset = OrderModel.objects.filter(student=student)
        order_list = list(order_queryset)
        completed_orders = [item for item in order_list
                            if item.student.user == request.user
                            and item.is_approved
                            and not item.is_canceled
                            and item.publisher_paid_approval
                            and item.student_paid_approval
                            and item.is_completed]
    elif request.user.is_authenticated and request.user.is_publisher:
        publisher = PublisherProfileModel.objects.get(user=request.user)
        book_queryset = BookModel.objects.filter(publisher=publisher)
        book_list = list(book_queryset)
        order_queryset = OrderModel.objects.all()
        order_list = list(order_queryset)
        final_order_list = [item for item in order_list if item.book in book_list]
        completed_orders = [item for item in final_order_list
                            if item.is_approved
                            and not item.is_canceled
                            and item.publisher_paid_approval
                            and item.student_paid_approval
                            and item.is_completed]
    return completed_orders
