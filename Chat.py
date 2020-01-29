import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from GoogleSheets import GoogleSheets
import json
import pprint

boards = {}
bot = telebot.TeleBot('925758227:AAE3Og96C06CzvjGl8KrThu1NI875LhEPks')
scope = ['https://docs.google.com/spreadsheets/d/1wIyGRvHLc7ljy_9txoy-ec__ks4fapkP3HgYLVYHk2o/edit?usp=sharing']
user_information = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['googleSheets'])
def get_google_sheets(message):
    googleSheets = GoogleSheets()
    bot.send_message(message.chat.id, pprint.pformat(googleSheets.getAllLessons()))


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(-1001448834300, 'hello')
    bot.send_message(message.chat.id, 'you can use /googleSheets, /start,/order')


#


# we want to register more then 1 message, maybe it's form to register in postgres(next step)


@bot.message_handler(commands=['order'])
def step_one(message):
    send = bot.send_message(message.chat.id, 'Enter your email address')
    bot.register_next_step_handler(send, create_email_addrees)


def create_email_addrees(message):
    text = message.text.lower()
    if "@" in message.text:
        user_information[message.chat.id] = message.text
        send = bot.send_message(message.chat.id, 'Enter your first and second name,number phone and number order')
        bot.register_next_step_handler(send, createName)


def createName(message):
    text = message.text.lower
    mail = user_information.get(message.chat.id)
    user_information[message.chat.id] = mail + ' ' + message.text
    print(text)
    print(user_information)
    googleSheets = GoogleSheets()
    googleSheets.addNewPerson(user_information.get(message.chat.id))
    bot.send_message(message.chat.id, user_information.get(message.chat.id))


# share with google sheets


def draw_board(id):
    bot.send_message(id, "-" * 13)
    for i in range(3):
        bot.send_message(id, "|", boards.get(id)[0 + i * 3], "|", boards.get(id)[1 + i * 3], "|",
                         boards.get(id)[2 + i * 3], "|")
        bot.send_message(id, "-" * 13)


def take_input(player_token, id):
    valid = False
    while not valid:
        player_answer = bot.send_message(id, "Куда поставим " + player_token + "? ")
        try:
            player_answer = int(player_answer)
        except:
            print("Некорректный ввод. Вы уверены, что ввели число?")
            continue
        if player_answer >= 1 and player_answer <= 9:
            if (str(boards.get(id)[player_answer - 1]) not in "XO"):
                boards.setdefault(id)[player_answer - 1] = player_token
                valid = True
            else:
                bot.send_message(id, "Эта клеточка уже занята")
        else:
            bot.send_message(id, "Некорректный ввод. Введите число от 1 до 9 чтобы походить.")


def check_win(board):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False


@bot.message_handler(commands=['game'])
def start_game(message):
    counter = 0
    board = list(range(1, 10))
    boards[message.chat.id] = board = list(range(1, 10))
    win = False
    while not win:
        draw_board(board, )
        if counter % 2 == 0:
            take_input("X", message.chat.id)
        else:
            take_input("O", message.chat.id)
        counter += 1
        if counter > 4:
            tmp = check_win(board)
            if tmp:
                bot.send_message(message.chat.i, tmp, "выиграл!")
                win = True
                break
        if counter == 9:
            bot.send_message(message.chat.id, "Ничья!")
            break
    draw_board(board)


bot.polling()
