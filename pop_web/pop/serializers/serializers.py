from rest_framework import serializers
from pop import models


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class TestimonialsSerializers(serializers.Serializers):
    class Meta:
        model = models.Testimonials
        fields = "__all__"


class BlogsSerializers(serializers.Serializers):
    class Meta:
        model = models.Blogs
        fields = "__all__"


class SubscriptionSerializers(serializers.Serializers):
    class Meta:
        model = models.Subscription
        fields = "__all__"


class DemoSerializers(serializers.Serializers):
    class Meta:
        model = models.Demo
        fields = "__all__"


class BannerNumbersSerializers(serializers.Serializers):
    class Meta:
        model = models.BannerNumber
        fields = "__all__"
