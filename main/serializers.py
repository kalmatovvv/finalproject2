from rest_framework import serializers

from main.models import CarImage, Category, Car, Review, Cart


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('image', 'id')

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        review = Review.objects.create(author=author, **validated_data)
        return review


class CarSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y %H:%M",
                                        read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ('id', 'title', 'price', 'description', 'images',
                   'created_at', 'owner', 'category', 'number_of_likes', 'liked_by_me')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        owner = request.user
        car = Car.objects.create(
            owner=owner, **validated_data
        )
        for image in images_data.getlist('images'):
            CarImage.objects.create(car=car,
                                     image=image)
        return car

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        # print(instance.images.all())
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            CarImage.objects.create(
                car=instance, image=image
            )
        return instance

    def get_liked_by_me(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

    def to_representation(self, instance):
        representation = super(CarSerializer, self).to_representation(instance)
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        return representation

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'car', 'user', 'cart')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('user')
            fields.pop('cart')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('car')
        favorite = Cart.objects.get_or_create(user=user, car=post)[0]
        favorite.cart = True if favorite.cart == False else False
        favorite.save()
        return favorite