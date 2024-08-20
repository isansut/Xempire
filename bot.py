import requests
import json
import time
from datetime import datetime
import telebot
import threading

def claim_bonus():
    # URL endpoint
    url = 'https://api.xempire.io/hero/bonus/offline/claim'

    # Membaca data dari file data.json
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: File data.json tidak ditemukan.")
        exit()
    except json.JSONDecodeError:
        print("Error: File data.json tidak valid atau rusak.")
        exit()

    # Mengganti nilai dalam headers
    headers['api-hash'] = data['api-hash']
    headers['api-key'] = data['api-key']
    headers['api-time'] = data['api-time']

    # Membuat permintaan POST
    response = requests.post(url, headers=headers, json={})

    # Menangani respons
    if response.status_code == 200:
        print("Bonus claimed successfully!")
        data = response.json()
        hero_money = data["data"]["hero"]["money"]
        print("Money:", hero_money)

        # Kirim pesan ke Telegram
        message = f"Bonus Offline berhasil diklaim!\nJumlah Uang : {hero_money}"
        bot.send_message(CHAT_ID, message) 

    else:
        print(f"Error claiming bonus. Status code: {response.status_code}")
        print(response.text)

# Header HTTP
headers = {
    'accept-language': 'en-US,en;q=0.9',
    'api-hash': '',  # Akan diganti dari data.json
    'api-key': '',  # Akan diganti dari data.json
    'api-time': '',  # Akan diganti dari data.json
    'content-length': '2',
    'content-type': 'application/json',
    'is-beta-server': 'null',
    'origin': 'https://game.xempire.io',
    'priority': 'u=1, i',
    'referer': 'https://game.xempire.io/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
}

# Inisialisasi bot Telegram
bot = telebot.TeleBot('7408982748:AAEafamevEJXpm1dWr0QNmA_d8G3xTxpDX8')  # Ganti dengan token bot Anda
CHAT_ID = '6550828209' # Ganti dengan ID chat Anda

def claim_bonus_thread():
    while True:
        claim_bonus()

        # Hitung mundur selama 1 jam
        for remaining_seconds in range(3600, 0, -1):
            minutes, seconds = divmod(remaining_seconds, 60)
            print(f"Waktu berikutnya: {minutes:02d}:{seconds:02d} tersisa", end='\r')
            time.sleep(1)
        print("\n")

# Inisialisasi bot Telegram dan mulai polling di thread terpisah
bot = telebot.TeleBot('7408982748:AAEafamevEJXpm1dWr0QNmA_d8G3xTxpDX8')
CHAT_ID = '6550828209'

# Mulai thread untuk claim_bonus
claim_thread = threading.Thread(target=claim_bonus_thread)
claim_thread.start()

# Mulai polling bot Telegram di thread utama
bot.polling()