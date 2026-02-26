from rest_framework import serializers
from iam.models import Membership
from users.serializers.user_serializer import UserReadSerializer
        
class MembershipReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    group = serializers.StringRelatedField()
    class Meta:
        model = Membership
        fields = ["id", "group", "joined_at", "user"]
        
class MembershipListReadSerializer(serializers.ListSerializer):
    child = MembershipReadSerializer()
    
class MembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["user", "group"]