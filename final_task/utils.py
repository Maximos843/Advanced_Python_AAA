import random
from copy import deepcopy
from telegram.ext import ContextTypes
from logger import CustomLogger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler
from dataclasses import dataclass


@dataclass
class GameVariables:
    TOKEN = '...'
    CROSS = 'X'
    ZERO = 'O'
    WINNER_USER = '❎'
    FREE_SPACE = '⋅'
    WINNER_COMP = '🟢'
    DEFAULT_STATE = [['⋅' for _ in range(3)] for _ in range(3)]


logger = CustomLogger().create_logger(__name__)


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(GameVariables.DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def bot_choose_position(context: ContextTypes.DEFAULT_TYPE) -> int | tuple:
    board = context.user_data['keyboard_state']
    free_positions = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == GameVariables.FREE_SPACE:
                free_positions.append((row, col))
    if free_positions == []:
        logger.debug('No free fields')
        return 0
    row, col = random.choice(free_positions)
    logger.debug(f'Chosen bot position is [{row, col}]')
    return row, col


def check_position(board: list[list[str]], row: int, col: int) -> bool:
    if board[row][col] == GameVariables.CROSS or board[row][col] == GameVariables.ZERO:
        logger.debug('Incorrect request')
        return False
    return True


def winner_positions(board: list[list[str]]) -> [str, list[tuple[int]]]:
    symb = GameVariables.CROSS
    for player in ['USER', 'COMPUTER']:
        if player == 'COMPUTER':
            symb = GameVariables.ZERO
        for i in range(3):
            if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[i][1] == symb:
                logger.debug(f'Vertical win of {player}')
                return player, [(0, i), (1, i), (2, i)]
            if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][1] == symb:
                logger.debug(f'Horizontal win of {player}')
                return player, [(i, 0), (i, 1), (i, 2)]
        if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] == symb:
            logger.debug(f'Main diagonal win of {player}')
            return player, [(0, 0), (1, 1), (2, 2)]
        if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[1][1] == symb:
            logger.debug(f'Second diagonal win of {player}')
            return player, [(0, 2), (1, 1), (2, 0)]
    return '', []


def check_winner(context: ContextTypes.DEFAULT_TYPE) -> tuple[str, list[int]]:
    winner, coords = winner_positions(context.user_data['keyboard_state'])
    text = ''
    if winner == 'USER':
        text = 'You won!'
    elif winner == 'COMPUTER':
        text = 'You lose bro...'
    return text, coords


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f'Put {GameVariables.CROSS} in empty field',
        reply_markup=reply_markup
    )
    return True


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    row, col = map(int, update.callback_query.data)
    flag = check_position(context.user_data['keyboard_state'], row, col)
    if not flag:
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.callback_query.message.text != 'Incorrect position':
            await update.callback_query.edit_message_text('Incorrect position', reply_markup=reply_markup)
        return True
    context.user_data['keyboard_state'][row][col] = GameVariables.CROSS
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup)
    text, coords = check_winner(context)
    if text:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        return await end(update, context, coords)
    bot_position = bot_choose_position(context)
    if not bot_position:
        await update.callback_query.edit_message_text('It\'s draw', reply_markup=reply_markup)
        return await end(update, context)
    context.user_data['keyboard_state'][bot_position[0]][bot_position[1]] = GameVariables.ZERO
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(reply_markup)
    text, coords = check_winner(context)
    if text:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        return await end(update, context, coords)
    return True


async def end(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE, coords: [list[tuple[int]]] = None) -> int:
    if coords is not None:
        for row, col in coords:
            wins = context.user_data['keyboard_state'][row][col]
            wins = wins.replace(GameVariables.CROSS, GameVariables.WINNER_USER)
            wins = wins.replace(GameVariables.ZERO, GameVariables.WINNER_COMP)
            context.user_data['keyboard_state'][row][col] = wins
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_reply_markup(reply_markup)
    await context.bot.send_message(update.effective_chat.id, text='Enter /start for new game')
    return ConversationHandler.END
