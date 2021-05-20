from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from carts.forms import ConfirmOrderForm
from user_control.models import User
from .models import DepartmentModel, BookModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from carts.utils import *


# @login_required
# def book_list(request, department_slug=None):
#     departments = DepartmentModel.objects.all()
#     department = None
#     books = BookModel.objects.filter(available=True)
#     paginator = Paginator(books, 8)
#     page = request.GET.get('page')
#     paged_products = paginator.get_page(page)
#     if department_slug:
#         department = get_object_or_404(DepartmentModel, slug=department_slug)
#         books = books.filter(department=department)
#         paginator = Paginator(books, 8)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#
#     return render(request, 'student/books.html',
#                   {'department': department,
#                    'departments': departments,
#                    'books': paged_products})


def pub_book_detail_view(request, slug):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    book = BookModel.objects.get(slug=slug)

    if request.GET.get('unavailableBook'):
        book.available = False
        book.save()
        return redirect('pub-book-detail', book.slug)

    if request.GET.get('availableBook'):
        book.available = True
        book.save()
        return redirect('pub-book-detail', book.slug)

    if request.GET.get('deleteBook'):
        book.delete()
        return redirect('publisher-dashboard')

    context = {
        'book': book,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }

    return render(request, 'publisher/pub-book-detail.html', context)


def stu_book_detail_view(request, slug):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    student = StudentProfileModel.objects.get(user=request.user)
    book = BookModel.objects.get(slug=slug)

    form = ConfirmOrderForm()
    if request.method == 'POST':
        form = ConfirmOrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.student = student
            new_order.book = book

            new_order.price_rate = book.price

            form.save()
            return redirect('home')
        else:
            context = {
                'book': book,
                'form': form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'orders_to_deliver': orders_to_deliver,
                'completed_orders': completed_orders,
            }
            return render(request, 'user_control/customer/confirm-order.html', context)
    context = {
        'book': book,
        'form': form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'student/stu-book-detail.html', context)


@login_required
def post_book_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    task = "Post New"
    form = PostBookForm()

    if request.method == 'POST':
        form = PostBookForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            current_user = request.user
            obj.publisher = PublisherProfileModel.objects.get(user=current_user)
            slug_str = "%s %s" % (obj.name, obj.edition)
            obj.slug = slugify(slug_str)
            obj.save()
            return redirect('publisher-dashboard')
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'orders_to_deliver': orders_to_deliver,
                'completed_orders': completed_orders,
            }
            return render(request, 'publisher/post-update-book.html', context)

    context = {
        'task': task,
        'form': form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }

    return render(request, 'publisher/post-update-book.html', context)


def update_book_view(request, pk):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    task = "Update"
    book = BookModel.objects.get(id=pk)
    form = PostBookForm(instance=book)

    if request.method == 'POST':
        form = PostBookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            obj = form.save()
            return redirect('pub-book-detail', obj.slug)
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'orders_to_deliver': orders_to_deliver,
                'completed_orders': completed_orders,
            }
            return render(request, 'publisher/post-update-book.html', context)

    context = {
        'task': task,
        'form': form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }

    return render(request, 'publisher/post-update-book.html', context)


def load_departments(request):
    university = request.GET.get('university')
    print(university)
    departments = DepartmentModel.objects.filter(university=university)
    return render(request, 'departments.html', {'departments': departments})


def load_courses(request):
    university = request.GET.get('university')
    departmentId = request.GET.get('department')
    department = DepartmentModel.objects.get(id=departmentId)
    courses = CourseModel.objects.filter(university=university, department=department)
    return render(request, 'courses.html', {'courses': courses})
