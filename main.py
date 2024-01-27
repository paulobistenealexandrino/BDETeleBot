import credentials
import telebot
import mercadopago
import time

bot = telebot.TeleBot(credentials.TELEGRAM_TOKEN)

def main():

  @bot.message_handler(commands = members_commands)
  def send_message(message):
    
    photo_path = 'fotos' + message.text + '.png'
    member_photo = open(photo_path, "rb")
    bot.send_photo(chat_id = message.chat.id, photo = member_photo)

    member_name = member_names[message.text][1]
    personal_message = f"""
O mano DJ {member_name} é um cara talibã
Virou o teu cunhado
E tá pegando a tua irmã
  """
    bot.reply_to(message, personal_message)
    time.sleep(3)
    send_welcome(message)

  @bot.message_handler(commands = ['doar'])
  def send_donation(message):
    sdk = mercadopago.SDK(credentials.MERCADOPAGO_TOKEN)
    payment_data = {
    "transaction_amount": 5,
    "description": "descrição",
    "payment_method_id": 'pix',
    "installments": 1,
    "payer": {
        "email": credentials.MY_EMAIL
    }}
    result = sdk.payment().create(payment_data)
    pix_copia_cola = result['response']['point_of_interaction']['transaction_data']['qr_code']
    bot.reply_to(message,"""
    Obrigado por contribuir para o BDE comprar sua lancha. Copie o código pix abaixo e cole no aplicativo do seu banco para realizar uma contribuição de R$5.
    """)
    bot.send_message(message.chat.id, pix_copia_cola)

  @bot.message_handler(func = lambda message: True)
  def send_welcome(message):
    bot.send_message(message.chat.id, """
Este é o Telegram Bot do BDE! Escolha um membro para conhecer o bonde:

/biro
/paulo
/joao
/saulo
/bruno
/pedro
/victor

Caso queira ajudar o BDE a comprar sua lancha contribuindo com R$5, clique (ou envie) /doar para obter um código pix copia-e-cola.
""")

  bot.polling()

member_names = {
    '/biro':['biro','Biro'],
    '/paulo':['paulo','Paulo'],
    '/joao':['joao','João'],
    '/saulo':['saulo','Saulo'],
    '/bruno':['bruno','Bruno'],
    '/pedro':['pedro','Pedro'],
    '/victor':['victor','Victor']
}

members_commands = [value[0] for value in member_names.values()]

if __name__ == '__main__':
    main()