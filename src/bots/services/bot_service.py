from systems.models import Bot
from bots.repositories.bot_repository import BotRepository

from utils.logger import get_logger


logger = get_logger(__name__)


class BotService:

    @staticmethod
    def update_bot(bot: Bot, data: dict):
        logger.debug(f"Starting service update_bot - bot_id: {bot.id}")

        for field, value in data.items():
            setattr(bot, field, value)

        return BotRepository.save_bot(bot)

    @staticmethod
    def destroy_bot(bot: Bot):
        logger.debug(f"Starting service destroy_bot - bot_id: {bot.id}")
        return BotRepository.delete_bot(bot)