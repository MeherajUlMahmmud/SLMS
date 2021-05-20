from django.urls import path

from .views import *

urlpatterns = [
    path('order-details/<str:pk>', order_details_view, name='order-details'),

    path('publisher/unchecked-orders/', publisher_unchecked_order_view, name='publisher-unchecked-orders'),
    path('publisher/unpaid-orders/', publisher_unpaid_order_view, name='publisher-unpaid-orders'),
    path('publisher/orders-to-deliver/', publisher_orders_to_deliver_view, name='publisher-orders-to-deliver'),
    path('publisher/completed-orders/', publisher_completed_orders_view, name='publisher-completed-orders'),

    path('student/pending-orders/', student_pending_order_view, name='student-pending-orders'),
    path('student/unpaid-orders/', student_unpaid_order_view, name='student-unpaid-orders'),
    path('student/orders-to-deliver/', student_orders_to_deliver_view, name='student-orders-to-deliver'),
    path('student/completed-orders/', student_completed_orders_view, name='student-completed-orders'),
]
