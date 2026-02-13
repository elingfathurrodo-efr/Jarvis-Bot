import telebot
import google.generativeai as genai
from metaapi_cloud_sdk import MetaApi
import asyncio
import threading
import time

# --- 1. DATA IDENTITAS TOTAL ---
TELEGRAM_TOKEN = "8237850543:AAGhbmzaTt4bYV6SFnQ4GEmCRN5VYx5jzTc"
GEMINI_API_KEY = "AIzaSyDQ29GupI81bB-uZYNcU1rRAzCJJ2cTii0"
META_API_TOKEN = "EyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI5MzdlNTQxNzkyZjcxNTA4ZTVkYzBjMmM1ZWUzOWFkMCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiw1170seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiOTM3ZTU0MTc5MmY3MTUwOGU1ZGMwYzJjNWVlMzlhZDAiLCJpYXQiOjE3NzA5Njc1ODd9.I8lWGvyQYmQEyOpjXp22KIk4HnyQXF7d0AwYtajU7AK_mW4w-IAOsCgVZX91g9POxKdFawvRUqekSXdnvsHshQ8mmsi2MUjHMV6xRICVPFyXXMGGUV6Ytt9PEOqhV3SSAjRs9v4kh6_PDXvv0K_tiyjWuhIMALvPNH0Ysp6LHbUL38AQNVHU_SVuONgC7_qVhEfA4IhL_BHc4yi0XYOYQuupiVetCt-IcAl3ap-Bp5ibocq7NzlzJrt136VbWQezYqjPwR972lqU42tXmWb-NBjLIF9Y0AVIk5ECOOLogvv01WCOXCuiEnV0hizMsqTjW5lCu3kwcLwSQpkD-HjwrmkvVleBwQ2OV9rEF8EpXw4fxM1hMQDab-ecZMIQBI_XSDa5fD_MoKR1DEmya-m7nM8_p1FLN8hzReTX4IVVw_Ia_GRdOFjZirUeBFocFAaAZoKA1LRpkipYD4Rti4FWh9V7cm1IqBYkJXnYwHUH5Hhch9OIvw7RgXkGQzAPjhNStq6Ymcw34eSDQPp76vCrA3o_enJzRHhkOfvmQzdOeJLZs9zh4bNZc5mzxchdhm1656H-GGUz8nIkhVI7wJDcPp0WsX3GGf-EDBBtW7JMcTE01SVATAwINQdwpg-jiNTUmPyH0krGJxCT409ud4zXMkbBRs6HmKxkHMmwt6n87ww"
META_ACCOUNT_ID = "988c34c6-fb12-408d-bc6d-e37cec96f482"

# DATA LOGIN MT5
MT5_ACCOUNT_ID = "211174033"
MT5_SERVER = "ValetaxIntl-Live2"
MT5_PASSWORD = "Yoi12345#"

# --- 2. KONFIGURASI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Ganti ke model yang lebih pintar
bot = telebot.TeleBot(TELEGRAM_TOKEN)
api = MetaApi(META_API_TOKEN)

# --- 3. FUNGSI INTI: HUNTER & PROTECTION (NYAWA AKUN) ---
async def hunter_engine():
    try:
        account = await api.metatrader_account_api.get_account(META_ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        print("🚀 JARVIS: Mesin Hunter Aktif!")
        
        while True:
            account_info = await connection.get_account_information()
            balance = account_info['balance']
            if balance >= 1200:
                print("🎯 Target Tercapai!")
                break
            await asyncio.sleep(20)
    except Exception as e:
        print(f"Mesin Error: {e}")

async def get_balance_real():
    try:
        account = await api.metatrader_account_api.get_account(META_ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        info = await connection.get_account_information()
        return info['balance']
    except:
        return "Gagal ambil data"

# --- 4. TELEGRAM HANDLER (AI + COMMAND) ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    msg = message.text.lower()
    
    # Deteksi bahasa manusia untuk cek saldo (tanpa /)
    if any(x in msg for x in ["saldo", "cek", "berapa"]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        balance = loop.run_until_complete(get_balance_real())
        response_text = f"⚔️ **LAPORAN KHUSUS BOS ELINO** ⚔️\n💰 Saldo: {balance} cent\n🎯 Target: 1200 cent\n🛡️ Status: Aman & Berburu!"
        bot.reply_to(message, response_text, parse_mode="Markdown")
        
    else:
        # Menjawab pertanyaan RANDOM dengan AI Gemini
        try:
            # Kita beri instruksi agar dia lebih manusiawi
            prompt = f"Kamu adalah Jarvis, AI asisten Elino. Kamu pintar, loyal, dan bisa menjawab apa saja dari internet. Jawab bos dengan santai: {message.text}"
            response = model.generate_content(prompt)
            bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "Aduh Bos, otak AI saya lagi refresh sebentar. Tapi tenang, saldo aman!")

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(hunter_engine())).start()
    bot.polling()
