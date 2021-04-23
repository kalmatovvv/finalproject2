from django.contrib import admin

from .models import CarImage, Car, Category, Review


class CarImageInline(admin.TabularInline):
    model = CarImage
    min_num = 1
    max_num = 10


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [ CarImageInline,]

class ReviewInline(admin.TabularInline):
    model = Review


admin.site.register(Category)
