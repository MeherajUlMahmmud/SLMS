from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from user_control.models import User
from .models import DepartmentModel, BookModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *


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
    book = BookModel.objects.get(slug=slug)

    if request.GET.get('unavailableBook'):
        book.available = False
        book.save()
        return redirect('pub-book-detail', book.slug)

    if request.GET.get('availableBook'):
        book.available = True
        book.save()
        return redirect('pub-book-detail', book.slug)

    return render(request, 'publisher/pub-book-detail.html', {'book': book})


def stu_book_detail_view(request, slug):
    book = BookModel.objects.get(slug=slug)
    return render(request, 'student/stu-book-detail.html', {'book': book})


@login_required
def post_book_view(request):
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
            return render(request, 'publisher/publisher-dashboard.html')
        else:
            print("Error: Form Invalid")
            print(form.errors)
            context = {
                'task': task,
                'form': form
            }
            return render(request, 'publisher/post-update-book.html', context)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'publisher/post-update-book.html', context)


def update_book_view(request, pk):
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
                'form': form
            }
            return render(request, 'publisher/post-update-book.html', context)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'publisher/post-update-book.html', context)


def load_departments(request):
    university = request.GET.get('university')
    departments = DepartmentModel.objects.filter(university=university)
    return render(request, 'departments.html', {'departments': departments})


def load_courses(request):
    university = request.GET.get('university')
    departmentId = request.GET.get('department')
    department = DepartmentModel.objects.get(id=departmentId)
    courses = CourseModel.objects.filter(university=university, department=department)
    return render(request, 'courses.html', {'courses': courses})
