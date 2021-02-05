from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from store.models import Product, Category, Customer


# Create your views here.
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'templates/index.html', data)


def validateCustomer(customer):
    error_message = None

    if not customer.first_name:
        error_message = 'First Name Required!!!'
    elif len(customer.first_name) < 4:
        error_message = 'First Name must me 4 character long'
    elif not customer.last_name:
        error_message = 'Last Name Required!!!'
    elif len(customer.last_name) < 4:
        error_message = 'Last Name must me 4 character long'
    elif not customer.mobile:
        error_message = 'Mobile number required'
    elif len(customer.mobile) < 10:
        error_message = 'Mobile number must be 10 digits'
    elif not customer.password:
        error_message = 'Password Required'
    elif len(customer.password) < 8:
        error_message = 'Password must be 8 Character long'

    return error_message


def registerUser(request):
    post_data = request.POST
    first_name = post_data.get('firstname')
    last_name = post_data.get('lastname')
    email = post_data.get('email')
    mobile = post_data.get('mobile')
    password = post_data.get('password')

    # validation
    values = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'mobile': mobile
    }
    error_message=None
    # saving user data
    if not error_message:
        customer = Customer(first_name=first_name, last_name=last_name,
                            email=email, mobile=mobile, password=password)
        # password hashing
        customer.password = make_password(customer.password)
        customer.save()
        return redirect('homepage')

    else:
        data = {
            'error': error_message,
            'value': values
        }
        return render(request, 'templates/signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'templates/signup.html')
    else:
        return registerUser(request)


def login(request):
    if request.method == 'GET':
        return render(request, 'templates/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = 'Email or Password incorrect'
        else:
            error_message='Email or Password incorrect'

        print(email, password)
        return render(request, 'templates/login.html', {'error':error_message})