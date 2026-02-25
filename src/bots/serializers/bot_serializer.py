from rest_framework import serializers

from systems.models import Bot
from systems.utils.token import PREFIX_BOT_TOKEN

class BotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ["bot_name"]

class BotReadSerializer(serializers.ModelSerializer):
    masked_token = serializers.SerializerMethodField()
    class Meta:
        model = Bot
        fields = ["id", "bot_name", "masked_token"]
    
    def get_masked_token(self, obj: Bot) -> str:
        return f"{PREFIX_BOT_TOKEN}{obj.prefix_token}****"

class BotResponseDeleteSerializer(serializers.Serializer):
    message: str
    deleted_id: str