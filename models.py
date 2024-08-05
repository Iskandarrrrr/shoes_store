from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Kategoriya nomi')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Rasm')
    slug = models.SlugField(unique=True, null=True)  # So'zlarni dublikat qiladi
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Kategoriya',
                               related_name='subcategories')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=900"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Kategoriya: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Kategoriya nomlanishi')
    price = models.FloatField(verbose_name='Narxi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Qo`shilgan vaqti')
    quantity = models.IntegerField(default=0, verbose_name='Soni')
    description = models.TextField(default='Tez orada batafsil', verbose_name='Tarifi')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriya', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.CharField(max_length=40, verbose_name='Razmer')
    color = models.CharField(max_length=40, default='Kumush', verbose_name='Rangi/Material')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=900"
        else:
            return "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=900"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Maxsulot: pk={self.pk}, title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Mahsulot '
        verbose_name_plural = 'Mahsulotlar'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Rasm')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'


class Review(models.Model):
    text = models.TextField(verbose_name='Izoh qoldirish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'


class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Foydalanuvchi')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Mahsulot')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Sevimli mahsulot'
        verbose_name_plural = 'Sevimli mahsulotlar'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Xaridor')
    first_name = models.CharField(max_length=255, verbose_name='Xaridor ismi', default='')
    last_name = models.CharField(max_length=255, verbose_name='Xaridor familiyiasi', default='')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Xaridor'
        verbose_name_plural = 'Xaridorlar'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Xaridor')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Buyurtma vaqti')
    shipping = models.BooleanField(default=True, verbose_name='Kuryer')

    def __str__(self):
        return str(self.pk) + ' '

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Mahsulot')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Buyurtma')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Soni')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Buyurtmadagi mahsulot'
        verbose_name_plural = 'Buyurtmadagi mahsulotlar'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Buyurtma manzili'
        verbose_name_plural = 'Buyurtmalar manzili'
