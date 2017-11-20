from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from stockbackend.quickstart.models import Stock
from rest_framework import viewsets
from stockbackend.quickstart.serializers import UserSerializer, GroupSerializer,StockSerializer
from rest_framework.response import Response
from django.db.models.query import QuerySet


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stock to be viewed or edited.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    def list(self, request):


        startDate = request.query_params.get('start_date')
        endDate = request.query_params.get('end_date')
        print(startDate)
        print(endDate)
        # if make:
        #     self.queryset = uploadobject.objects.filter(make=make)
        #     return self.queryset
        # else:
        #     return self.queryset
        # print(request.params)
        if startDate:
            queryset = Stock.objects.filter(date__gte=startDate, date__lte=endDate)
        else:
            queryset = Stock.objects.order_by('-idstock_detail')[:50].all()

        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data)