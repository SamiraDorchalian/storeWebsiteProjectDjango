from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from uuid import uuid4

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('Description'))
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', verbose_name=_('Top_product'))
    
    def __str__(self):
        return self.title


class Discount(models.Model):
    discount = models.FloatField(verbose_name=_('Discount'))
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    
    def __str__(self):
        return f'{str(self.discount)} {self.description}'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_('Category'))
    slug = models.SlugField(verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Unit_price'))
    inventory = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('Inventory'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('DateTime_Created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('DateTime_Modified'))
    discounts = models.ManyToManyField(Discount, blank=True, verbose_name=_('Discounts'))

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('User') )
    phone_number = models.CharField(max_length=255, verbose_name=_('Phone_Number'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Birth_Date'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        permissions = [
            ('send_private_email', 'Can send private email to user by the button')
        ]


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True, verbose_name=_('Customer'))
    province = models.CharField(max_length=255, verbose_name=_('Province'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))


class Order(models.Model):
    ORDER_STATUS_PAID = 'p' 
    ORDER_STATUS_UNPAID = 'u' 
    ORDER_STATUS_CANCELED = 'c' 
    ORDER_STATUS = [
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders', verbose_name=_('Customer'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('DateTime_Created'))
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID, verbose_name=_('Status'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name=_('Product'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity'))
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Unit_price'))

    class Meta:
        unique_together = [['order', 'product']]


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING , 'Waiting'),
        (COMMENT_STATUS_APPROVED , 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED , 'Not Approved'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Product'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    body = models.TextField(verbose_name=_('Body'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('DateTime_Created'))
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING, verbose_name=_('Status'))

    def __str__(self):
        return f'Order id={self.id}'


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, verbose_name=_('Id'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created_At'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name=_('Cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', verbose_name=_('Product'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity'))

    class Meta:
        unique_together = [['cart', 'product']]
