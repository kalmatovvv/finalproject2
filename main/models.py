from django.db import models

# Create your models here.
from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cars')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')
    description = models.TextField()
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(MyUser, related_name='likers', blank=True, symmetrical=False)

    def __str__(self):
        return self.title

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    review = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='reviews')


    def __str__(self):
        return self.review

class CarImage(models.Model):
    image = models.ImageField(upload_to='cars', blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')

class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='carts')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='carts')
    cart = models.BooleanField(default=False)
