from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='media/products/')

    def __str__(self):
        return self.name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Customer(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.email

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def verify_email(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        Order.objects.filter(customer=customer_id).order_by('-date')