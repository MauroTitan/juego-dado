from telegram.ext import *
import random

puntajes = {}  # Diccionario para almacenar los puntajes de los usuarios
usuarios_unidos = []  # Lista para almacenar los usuarios que se han unido al juego

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Bienvenido al juego.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe /unirte para unirte al juego.")

def join(update, context):
    user_id = update.message.from_user.id
    if user_id not in usuarios_unidos:
        usuarios_unidos.append(user_id)
        puntajes[user_id] = 0
        context.bot.send_message(chat_id=update.effective_chat.id, text="Te has unido al juego.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe /jugar para comenzar.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ya te has unido al juego.")

def play(update, context):
    user_id = update.message.from_user.id
    if user_id in usuarios_unidos:
        puntaje_actual = puntajes[user_id]
        dado = random.randint(1, 6)
        puntajes[user_id] = puntaje_actual + dado
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Has lanzado el dado y has obtenido un {dado}.")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tu puntaje actual es {puntajes[user_id]}.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Primero debes unirte al juego.")

def leaderboard(update, context):
    if len(puntajes) > 0:
        sorted_puntajes = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
        leaderboard_text = "Puntuaciones:\n"
        for idx, (user_id, puntaje) in enumerate(sorted_puntajes):
            user_name = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id).user.username
            leaderboard_text += f"{idx+1}. {user_name}: {puntaje}\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=leaderboard_text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No hay puntuaciones para mostrar.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Comandos disponibles:\n/unirte: Unirte al juego.\n/jugar: Lanzar el dado y obtener un puntaje.\n/puntuaciones: Ver las puntuaciones de los jugadores.\n/ayuda: Ver los comandos disponibles.")

def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ha ocurrido un error. Por favor, intenta nuevamente más tarde.")

if __name__ == '__main__':
    updater = Updater(token='6496171159:AAF5F6RMiodCOhCkre2OznSiVrKwipCJj18', use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('unirte', join))
    dispatcher.add_handler(CommandHandler('jugar', play))
    dispatcher.add_handler(CommandHandler('puntuaciones', leaderboard))
    dispatcher.add_handler(CommandHandler('ayuda', help))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()