from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .forms import *
from .models import *
from .decorators import *
from carts.utils import *


@unauthenticated_user
def home(request):
    return render(request, 'index.html')


@unauthenticated_user
def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_student:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('student-dashboard')
            elif user and user.is_publisher:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('publisher-dashboard')
            else:
                messages.error(request, 'Email or Password is incorrect.')
                return redirect('login')
        else:
            return render(request, 'login.html', {'form': form})

    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


@unauthenticated_user
def student_register_view(request):
    if request.method == 'POST':
        student_reg_form = StudentRegistrationForm(request.POST)
        if student_reg_form.is_valid():
            student_reg_form.save()
            email = student_reg_form.cleaned_data.get('email')
            raw_password = student_reg_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            StudentProfileModel.objects.create(user=user)
            login(request, user)
            return redirect('student-dashboard')
        else:
            return render(request, 'student/student-registration.html', {"student_reg_form": student_reg_form})

    student_reg_form = StudentRegistrationForm()
    context = {
        "student_reg_form": student_reg_form
    }
    return render(request, 'student/student-registration.html', context)


@unauthenticated_user
def publisher_register_view(request):
    if request.method == 'POST':
        publisher_reg_form = PublisherRegistrationForm(request.POST)
        if publisher_reg_form.is_valid():
            publisher_reg_form.save()
            email = publisher_reg_form.cleaned_data.get('email')
            raw_password = publisher_reg_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            PublisherProfileModel.objects.create(user=user)
            login(request, user)
            return redirect('publisher-dashboard')
        else:
            return render(request, 'publisher/publisher-registration.html', {"publisher_reg_form": publisher_reg_form})

    publisher_reg_form = PublisherRegistrationForm()
    context = {
        "publisher_reg_form": publisher_reg_form
    }
    return render(request, 'publisher/publisher-registration.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def student_dashboard_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    user = request.user
    student = StudentProfileModel.objects.get(user=user)
    department_found = False
    if student.department_name:
        department = student.department_name
        dept_name = DepartmentModel.objects.filter(department=department)
        if dept_name.exists():
            department_found = True
    if student.varsity_name:
        varsity = student.varsity_name

    # books = None
    # if student.department_name and student.varsity_name and department_found:
    #     books = BookModel.objects.filter(university=varsity, department=department)

    books = BookModel.objects.all()

    context = {
        'department': department,
        'varsity': varsity,
        'book_list': books,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'student/student-dashboard.html', context)


@login_required
def publisher_dashboard_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    current_user = request.user
    publisher = PublisherProfileModel.objects.get(user=current_user)
    books = BookModel.objects.filter(publisher=publisher)

    context = {
        'books': books,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'publisher/publisher-dashboard.html', context)


@login_required
def profile_view(request, pk):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    user = User.objects.get(id=pk)
    context = {
    }

    if user.is_publisher:
        profile = PublisherProfileModel.objects.get(user=user)
        books = BookModel.objects.filter(publisher=profile)
        orders = OrderModel.objects.filter(book__in=list(books), is_completed=True)

        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

        if profile.location is not None:
            locations = profile.location.split(' ')
            location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

            for location in locations:
                location_link += location + "%20"

            location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"

        context = {
            'user': user,
            'profile': profile,
            'books': books,
            'orders': orders,
            'location_link': location_link,

            'pending_orders': pending_orders,
            'unpaid_orders': unpaid_orders,
            'orders_to_deliver': orders_to_deliver,
            'completed_orders': completed_orders,
        }
    elif user.is_student:
        profile = StudentProfileModel.objects.get(user=user)
        orders = OrderModel.objects.filter(student=profile, is_completed=True)

        context = {
            'user': user,
            'profile': profile,
            'orders': orders,

            'pending_orders': pending_orders,
            'unpaid_orders': unpaid_orders,
            'orders_to_deliver': orders_to_deliver,
            'completed_orders': completed_orders,
        }

    return render(request, 'profile.html', context)


@login_required
def publisher_edit_profile(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    profile = PublisherProfileModel.objects.get(user=request.user)

    form = PublisherProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = PublisherProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)
        else:
            print(form.errors)
            return redirect('publisher-edit-profile')

    context = {
        'form': form,
        'profile': profile,
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'edit-profile.html', context)


@login_required
def student_edit_profile(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    profile = StudentProfileModel.objects.get(user=request.user)
    universities = UniversityModel.objects.all()

    form = StudentProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=profile)

        # varsityId = request.POST.get('varsity_name')
        # departmentId = request.POST.get('department_name')
        #
        # varsity = UniversityModel.objects.get(id=varsityId)
        # department = DepartmentModel.objects.get(id=departmentId)

        # print(request.POST)

        # print(varsity)
        # print(department)

        # form.fields['varsity_name'] = varsity
        # form.fields['department_name'] = department

        # print(form.fields['varsity_name'])
        # print(form.fields['department_name'])
        # print(form.fields['phone'])
        # print(form.fields['gender'])
        # print(form.fields['birth_date'])

        # updated_request = request.POST.copy()
        # updated_request.__setitem__('varsity_name', varsity.university)
        # updated_request.__setitem__('department_name', department.department)
        # form = StudentProfileUpdateForm(updated_request)
        #
        # print(request.POST)
        # print(updated_request)

        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)
        else:
            print(form.errors)
            return redirect('student-edit-profile')

    context = {
        'form': form,
        'universities': universities,
        'profile': profile,
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'edit-profile.html', context)


def about_view(request):
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
    return render(request, "about.html", context)


def contact_view(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    if request.method == 'POST':
        name = request.POST['name']
        email_add = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        # FeedbackModel.objects.create(name=name, email=email_add, subject=subject, message=message)

        messages.success(request, "Feedback sent successfully.")

        context = {
            'pending_orders': pending_orders,
            'unpaid_orders': unpaid_orders,
            'orders_to_deliver': orders_to_deliver,
            'completed_orders': completed_orders,
        }

        return render(request, 'contact.html', context)

    context = {
        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }

    return render(request, 'contact.html', context)


@login_required
def account_settings(request):
    pending_orders = get_pending_orders(request)
    unpaid_orders = get_unpaid_orders(request)
    orders_to_deliver = get_orders_to_deliver(request)
    completed_orders = get_completed_orders(request)

    user = request.user

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            slug_str = "%s %s" % (user.name, user.id)
            user.slug = slugify(slug_str)
            user.save()
            return redirect('settings')

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            context = {
                'information_form': information_form,
                'password_form': password_form,

                'pending_orders': pending_orders,
                'unpaid_orders': unpaid_orders,
                'orders_to_deliver': orders_to_deliver,
                'completed_orders': completed_orders,
            }
            return render(request, 'settings.html', context)
    context = {
        'information_form': information_form,
        'password_form': password_form,

        'pending_orders': pending_orders,
        'unpaid_orders': unpaid_orders,
        'orders_to_deliver': orders_to_deliver,
        'completed_orders': completed_orders,
    }
    return render(request, 'settings.html', context)
