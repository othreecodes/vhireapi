from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email') + (
            'is_staff', 'is_active', 'date_joined', 'role', 'phone_number'
        )
        read_only_fields = ('is_staff', 'is_active', 'date_joined')


class JobCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobCategory
        fields = "__all__"


class JobTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobType
        fields = "__all__"


class JobSerializier(serializers.ModelSerializer):

    class Meta:
        model = models.Job
        fields = "__all__"
        read_only_fields = ('created', 'modified')


class SessionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Session
        fields = "__all__"
        depth = 1


class BookingSerializier(serializers.ModelSerializer):
    sessions = SessionsSerializer(many=True)

    class Meta:
        model = models.Booking
        fields = [
            'id',
            'created',
            'modified',
            'status',
            'price',
            'start',
            'provider',
            'service',
            'customer',
            'sessions',
            'name',
            'service_extras',
        ]
        read_only_fields = ('created', 'modified')

    def name(self, object):
        return "ola"


class UserIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserIdentification
        fields = "__all__"
        read_only_fields = ('created', 'modified')


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice
        fields = "__all__"
        read_only_fields = ('created', 'modified')


class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice
        fields = "__all__"
        read_only_fields = ('created', 'modified')


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = "__all__"


class ServiceExtraSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceExtra
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    extras = ServiceExtraSerializer(many=True)

    class Meta:
        model = models.Service
        fields = "__all__"


class ServiceProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceProvider
        fields = "__all__"
