from systems.models import Bot
from utils.logger import get_logger

logger = get_logger(__name__)

class BotRepository:

    @staticmethod
    def save_bot(bot:Bot):
        logger.debug(f"Starting repository save_bot - bot_id: {bot.id}")
        bot.save()
        return bot

    @staticmethod
    def delete_bot(bot: Bot):
        logger.debug(f"Starting repository delete_bot - bot_id: {bot.id}")
        return bot.delete()