import random

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MaxValueValidator, MinValueValidator


states = [
    "Abia",
    "Abuja",
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bayelsa",
    "Bauchi",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Edo",
    "Ebonyi",
    "Ekiti",
    "Enugu",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nassawara",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara",
]
states_long_lat = [
    (5.726664, 7.565156),
    (9.082473, 7.356269),
    (9.645162, 12.421864),
    (5.068420, 7.683476),
    (6.316646, 6.995496),
    (4.842071, 5.852486),
    (10.807842, 9.751328),
    (7.387295, 8.736775),
    (11.629788, 12.802802),
    (6.316806, 8.799662),
    (5.669369, 6.058477),
    (6.883155, 5.984382),
    (6.221285, 7.818528),
    (7.739940, 5.343869),
    (6.603331, 7.291178),
    (10.545474, 11.171589),
    (5.616333, 7.102473),
    (12.364066, 9.376286),
    (10.470247, 8.079514),
    (11.676993, 8.547603),
    (12.669475, 7.358564),
    (12.208350, 3.981469),
    (7.948534, 6.457488),
    (9.414218, 3.718773),
    (6.669684, 3.561586),
    (8.625961, 7.918797),
    (9.924713, 5.617843),
    (6.963726, 3.419530),
    (7.046053, 5.179615),
    (7.563343, 4.542657),
    (8.167863, 3.594321),
    (9.182326, 9.569508),
    (4.931917, 6.673922),
    (13.406813, 4.891265),
    (7.849436, 10.570253),
    (12.288096, 11.299737),
    (11.996030, 6.133369),
]



class VUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
    
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(None, email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists.")
        },
    )
    username = models.CharField(blank=True, null=True, max_length=150)
    role = models.CharField(
        max_length=256,
        choices=(("provider", "provider"), ("customer", "customer")),
        default="customer",
    )
    phone_number = models.CharField(blank=True, null=True, max_length=150)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = VUserManager()

class Location(models.Model):
    NIGERIAN_STATES = [('', 'Select State')] + [(x, x) for x in states]
    address = models.CharField(max_length=120)
    state = models.CharField(
        max_length=50,
        choices=NIGERIAN_STATES,
        null=True,
        blank=True,
        db_index=True,
    )
    vicinity = models.CharField(max_length=80, null=True, blank=True)
    vicinity_type = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True
    )
    latitude = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True
    )
    lga = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.state


class JobCategory(models.Model):
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from="name")
    image = models.ImageField(blank=True, null=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField()

    def __str__(self):
        return self.name

    image = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class JobType(models.Model):
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from="name")
    image = models.ImageField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Job Type"
        verbose_name_plural = "Job Types"


class Job(TimeStampedModel):
    position = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=256, blank=True, null=True)
    application_url = models.URLField(max_length=256, blank=True, null=True)
    featured = models.BooleanField(default=False)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.FloatField(blank=True, null=True)
    hours = models.FloatField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    filled = models.BooleanField(default=False)
    num_to_apply = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    service = models.ForeignKey(
        'api.Service', on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return "{} posting by {}".format(self.position, self.poster.username)


class UserIdentification(TimeStampedModel):
    IDENTITY = 'identity'
    DOCUMENT_TYPES = ((IDENTITY, 'identity'),)
    identity = CloudinaryField(
        max_length=100, verbose_name=_('Identification Document'), null=True
    )
    verified = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        verbose_name='user',
        related_name='identifications',
        on_delete=models.CASCADE,
    )
    doc_type = models.CharField(
        default=IDENTITY, choices=DOCUMENT_TYPES, max_length=30
    )
    require_modification = models.BooleanField(default=False)

    def __str__(self):
        return "ID for {}".format(self.user.username)


class Invoice(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    paid = models.BooleanField()
    order = models.CharField(max_length=256)
    discount = models.ForeignKey(
        'api.Coupon', on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.order

    def generate_code(cls, key='order'):

        def _generate_code():
            t = "ABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
            return "".join([random.choice(t) for i in range(12)])

        code = _generate_code()
        if key == 'slug':
            kwargs = {'slug': code}
        else:
            kwargs = {'order': code}
        while cls.objects.filter(**kwargs).exists():
            code = _generate_code()
        return code

    def save(self, *args, **kwargs):
        self.order = self.generate_code()
        super(Invoice, self).save(*args, **kwargs)


class JobApplication(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, models.CASCADE)
    selected = models.BooleanField()

    def __str__(self):
        return "{} applied for {} on {} ".format(
            self.applicant.first_name, self.job.position, self.created
        )


class Service(models.Model):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=70)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    description = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.name


class ServiceProvider(ActivatorModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="providers"
    )
    heading = models.CharField(max_length=256, null=True, db_index=True)
    slug = AutoSlugField(populate_from='heading', max_length=250)
    description = models.TextField()
    price = models.DecimalField(
        default=500.00, max_digits=10, decimal_places=2
    )
    booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "service")

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"{self.username} - {self.service}"


class Booking(TimeStampedModel):
    NOT_STARTED = 1
    STARTED = 2
    COMPLETED = 3
    PENDING = 4
    CANCELLED = 5
    BOOKING_STATUS = (
        (NOT_STARTED, 'not started'),
        (STARTED, 'started'),
        (COMPLETED, 'completed'),
        (CANCELLED, 'cancelled'),
    )
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='provider',
        null=True,
        blank=True,
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service',
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    status = models.IntegerField(default=PENDING, choices=BOOKING_STATUS)
    start = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_extras = models.ManyToManyField('api.ServiceExtra')

    @property
    def name(self):
        return self.service.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Rating(TimeStampedModel):
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)


class Coupon(TimeStampedModel):
    code = models.CharField(max_length=150)
    expires = models.DateTimeField()
    no_of_uses = models.IntegerField(default=5)
    used_by = models.ManyToManyField('api.User')


class ServiceExtra(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    unit = models.CharField(max_length=256, blank=True, null=True, default="")
    quantity = models.IntegerField(blank=True, null=True, default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    service = models.ForeignKey(
        'api.Service',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="extras",
    )
    serviceprovider = models.ForeignKey(
        'api.ServiceProvider', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} Extra of {self.service or self.serviceprovider}"


class Session(TimeStampedModel):
    NOT_STARTED = 1
    STARTED = 2
    COMPLETED = 3
    PENDING = 4
    CANCELLED = 5
    SESSION_STATUS = (
        (NOT_STARTED, 'not started'),
        (STARTED, 'started'),
        (COMPLETED, 'completed'),
        (CANCELLED, 'cancelled'),
        (PENDING, 'pending'),
    )
    start = models.DateField()
    time = models.TimeField()
    no_of_hours = models.IntegerField()
    status = models.IntegerField(default=NOT_STARTED, choices=SESSION_STATUS)
    booking = models.ForeignKey(
        'api.Booking',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='sessions',
    )
