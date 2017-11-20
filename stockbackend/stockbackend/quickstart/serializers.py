from django.contrib.auth.models import User, Group
from rest_framework import serializers
from stockbackend.quickstart.models import Stock


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class StockSerializer(serializers.HyperlinkedModelSerializer):
    adjusted = serializers.CharField(source='adj_close')
    class Meta:
        model = Stock
        fields = ('symbol', 'date', 'open', 'close', 'high', 'low', 'volume','adjusted')