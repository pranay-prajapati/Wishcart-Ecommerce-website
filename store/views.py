from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views import View

from store.models import Product, Category, Customer, Order


# Create your views here.
class Index(View):
    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1

                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print("cart:", request.session['cart'])
        return redirect('homepage')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.objects.all()

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'templates/index.html', data)


class Signup(View):
    def get(self, request):
        return render(request, 'templates/signup.html')

    def post(self, request):
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
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name,
                            email=email, mobile=mobile, password=password)
        error_message = self.validateCustomer(customer)
        # saving user data
        if not error_message:
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

    def validateCustomer(self, customer):
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


class Login(View):
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'templates/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password incorrect'
        else:
            error_message = 'Email or Password incorrect'

        print(email, password)
        return render(request, 'templates/login.html', {'error': error_message})


def Logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'templates/cart.html', {'products': products})


class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')


class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'templates/orders.html', {'orders': orders})
