from django.db import models
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(models.Model):
    username = models.CharField(
        max_length=20, unique=True, blank=False, validators=[MinLengthValidator(3)]
    )
    password = models.CharField(
        max_length=20, blank=False, validators=[MinLengthValidator(3)]
    )
    email = models.EmailField(
        blank=False,
        validators=[EmailValidator(message="Enter Valid Email")],
        unique=True,
    )
    phone_number = (
        models.CharField(
            max_length=10,
            validators=[
                RegexValidator(
                    regex=r"^\d{10}$",
                    message="Phone number must be exactly 10 digits.",
                    code="invalid_phone_number",
                )
            ],
            blank=False,
        ),
    )
    country_code = (
        models.CharField(
            max_length=4,
            validators=[
                RegexValidator(regex=r"^\+\d{3}$", message="Invalid Country Code")
            ],
            blank=False,
        ),
    )
    first_name = models.CharField(
        max_length=30, blank=False, validators=[MinLengthValidator(3)]
    )
    last_name = models.CharField(
        max_length=30, blank=False, validators=[MinLengthValidator(3)]
    )
    middle_name = models.CharField(max_length=30, validators=[MinLengthValidator(1)])


class Testimonials(models.Model):
    company_icon = models.BinaryField()
    company_name = models.CharField(
        max_length=255, blank=False, validators=[MinLengthValidator(2)]
    )
    testimonial = models.TextField(blank=False)
    writer_name = models.CharField(max_length=50, blank=False)
    writer_post = models.CharField(max_length=30, blank=False)


class Blogs(models.Model):
    blog_image = models.BinaryField(blank=False)
    title = models.TextField(
        blank=False, max_length=50, validators=[MinLengthValidator(8)]
    )
    sub_title = models.TextField(blank=False, validators=[MinLengthValidator(15)])
    created_at = models.DateTimeField(auto_now_add=True)
    read_duration = models.TimeField(blank=False)


class Subscription(models.Model):
    email = models.EmailField(blank=False)
    created_at = models.DateTimeField(auto_now=True)


class Demo(models.Model):
    demo_time = models.TimeField(blank=False)
    date = models.DateField(blank=False)

    def validate_model_data(self):
        if self.date < timezone.now().date:
            raise ValidationError("Date cannot be in the past")

    def save(self, *args, **kwargs):
        self.validate_model_data()
        super.save(*args, **kwargs)


class BannerNumber(models.Model):
    """
    BANNER NUMBERS NEEDS JOB EVERY 1 WEEK
    """

    installed_capacity_monitored = models.IntegerField(
        validators=[MinValueValidator(0)], blank=False
    )
    sites_active_on_platform = models.IntegerField(
        validators=[MinValueValidator(0)], blank=False
    )
    mwh_monitored = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    tons_of_co2_offset = models.IntegerField(
        validators=[MinValueValidator(0)], blank=False
    )
