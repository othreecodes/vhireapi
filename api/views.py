from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework.compat import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import json


class UserViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    @list_route(methods=['POST'])
    def login(self, request, *args, **kwargs):
        attrs = request.data
        email = attrs.get('email')
        password = attrs.get('password')
        # import pdb; pdb.set_trace()
        if email and password:
            user = authenticate(
                request=request, email=email, password=password
            )
            if not user:
                return Response(
                    {"error": "Invalid Login Credentials"}, status=400
                )

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'role': user.role})

        return Response(
            {"error": "Please Input an email and password"}, status=400
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'role': user.role})

        else:
            return Response(data=serializer.errors, status=400)


class LocationViewset(viewsets.ModelViewSet):
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class JobCategoryViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = ()
    serializer_class = serializers.JobCategorySerializer
    queryset = models.JobCategory.objects.all()

    def retrieve(self, request, pk=None):
        services = models.Service.objects.filter(category=self.get_object())
        return Response(
            serializers.ServiceSerializer(services, many=True).data
        )


class JobTypeViewset(viewsets.ModelViewSet):
    serializer_class = serializers.JobTypeSerializer
    queryset = models.JobType.objects.all()


class JobViewset(viewsets.ModelViewSet):
    serializer_class = serializers.JobSerializier
    queryset = models.Job.objects.all()


class BookingViewset(viewsets.ModelViewSet):
    serializer_class = serializers.BookingSerializier
    queryset = models.Booking.objects.all()

    def create(self, request, *args, **kwargs):
        we = json.loads(request.data)


        booking = models.Booking()
        booking.service_id = we[0]['booking']['service']
        booking.customer = request.user
        booking.start = f"{we[0]['start']} {we[0]['time']}"
        booking.price = 500
        booking.save()
        sessions = []
        for x in we:
            sessions.append(
                models.Session(
                    start=x['start'],
                    time=x['time'],
                    no_of_hours=x['no_of_hours'],
                    booking=booking,
                )
            )
        models.Session.objects.bulk_create(sessions)
        # import pdb; pdb.set_trace()
        return Response(
            serializers.BookingSerializier(
                request.user.bookings, many=True
            ).data,
            status=200,
        )

    def list(self,request,*args,**kwargs):
        return Response(
            serializers.BookingSerializier(
                request.user.bookings, many=True
            ).data,
            status=200,
        )
        
# def create(self, request)
class UserIdViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UserIDSerializer
    queryset = models.UserIdentification.objects.all()


class InvoiceViewset(viewsets.ModelViewSet):
    serializer_class = serializers.InvoiceSerializer
    queryset = models.Invoice.objects.all()


class JobApplicationViewset(viewsets.ModelViewSet):
    serializer_class = serializers.JobApplicationSerializer
    queryset = models.JobApplication.objects.all()

class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SessionsSerializer
    queryset = models.Session.objects.all()

    @detail_route(methods=['POST'])
    def cancel(self, request, *args, **kwargs):
        session = self.get_object()

        session.status = models.Session.CANCELLED
        session.save()

        return Response(
            serializers.SessionsSerializer(
                session).data, status=status.HTTP_202_ACCEPTED
        )
        
    @detail_route(methods=['POST'])
    def submit(self, request, *args, **kwargs):
        session = self.get_object()

        session.status = models.Session.COMPLETED
        session.save()

        return Response(
            serializers.SessionsSerializer(
                session).data, status=status.HTTP_202_ACCEPTED
        )
    
    @detail_route(methods=['POST'])
    def start(self, request, *args, **kwargs):
        session = self.get_object()

        session.status = models.Session.STARTED
        session.save()

        return Response(
            serializers.SessionsSerializer(
                session).data, status=status.HTTP_202_ACCEPTED
        )

    
class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = ()
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

