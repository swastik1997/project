from rest_framework import serializers
from os.path import dirname, abspath
from .models import Stock

class StockSerializer(serializers.ModelSerializer):

	class Meta:
		model=Stock
		fields='__all__'
