from logger import CustomLogger
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)
from utils import start, game, GameVariables


logger = CustomLogger().create_logger(__name__)


def main() -> None:
    logger.info('Start bot')
    application = Application.builder().token(GameVariables.TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            True: [
                CallbackQueryHandler(game, pattern='^' + f'{row}{col}' + '$')
                for row in range(3) for col in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info('End bot')


if __name__ == '__main__':
    main()
