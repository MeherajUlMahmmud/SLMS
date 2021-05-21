from user_control.models import StudentProfileModel
from django.db import models
from book_control.models import BookModel


class OrderModel(models.Model):
    student = models.ForeignKey(StudentProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(BookModel, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    additional_note = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    publisher_paid_approval = models.BooleanField(default=False)
    student_paid_approval = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderPaymentModel(models.Model):
    order = models.OneToOneField(OrderModel, null=True, blank=True, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
