import telebot
import google.generativeai as genai
from metaapi_cloud_sdk import MetaApi
import asyncio
import threading

# --- 1. DATA IDENTITAS ---
TELEGRAM_TOKEN = "8237850543:AAGhbmzaTt4bYV6SFnQ4GEmCRN5VYx5jzTc"
GEMINI_API_KEY = "AIzaSyDQ29GupI81bB-uZYNcU1rRAzCJJ2cTii0"
META_API_TOKEN = "EyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI5MzdlNTQxNzkyZjcxNTA4ZTVkYzBjMmM1ZWUzOWFkMCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiw1170seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiOTM3ZTU0MTc5MmY3MTUwOGU1ZGMwYzJjNWVlMzlhZDAiLCJpYXQiOjE3NzA5Njc1ODd9.I8lWGvyQYmQEyOpjXp22KIk4HnyQXF7d0AwYtajU7AK_mW4w-IAOsCgVZX91g9POxKdFawvRUqekSXdnvsHshQ8mmsi2MUjHMV6xRICVPFyXXMGGUV6Ytt9PEOqhV3SSAjRs9v4kh6_PDXvv0K_tiyjWuhIMALvPNH0Ysp6LHbUL38AQNVHU_SVuONgC7_qVhEfA4IhL_BHc4yi0XYOYQuupiVetCt-IcAl3ap-Bp5ibocq7NzlzJrt136VbWQezYqjPwR972lqU42tXmWb-NBjLIF9Y0AVIk5ECOOLogvv01WCOXCuiEnV0hizMsqTjW5lCu3kwcLwSQpkD-HjwrmkvVleBwQ2OV9rEF8EpXw4fxM1hMQDab-ecZMIQBI_XSDa5fD_MoKR1DEmya-m7nM8_p1FLN8hzReTX4IVVw_Ia_GRdOFjZirUeBFocFAaAZoKA1LRpkipYD4Rti4FWh9V7cm1IqBYkJXnYwHUH5Hhch9OIvw7RgXkGQzAPjhNStq6Ymcw34eSDQPp76vCrA3o_enJzRHhkOfvmQzdOeJLZs9zh4bNZc5mzxchdhm1656H-GGUz8nIkhVI7wJDcPp0WsX3GGf-EDBBtW7JMcTE01SVATAwINQdwpg-jiNTUmPyH0krGJxCT409ud4zXMkbBRs6HmKxkHMmwt6n87ww"

# DATA MT5 NYATA
META_ACCOUNT_ID = "988c34c6-fb12-408d-bc6d-e37cec96f482"
MT5_ACCOUNT = "211174033"
MT5_SERVER = "ValetaxIntl-Live2"
MT5_PASSWORD = "Yoi12345#"

# --- 2. KONFIGURASI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
api = MetaApi(META_API_TOKEN)

async def connect_to_mt5():
    try:
        account = await api.metatrader_account_api.get_account(META_ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        return connection
    except Exception as e:
        print(f"❌ Login Gagal: {e}")
        return None

# --- 3. ENGINE HUNTER (AUTO ENTRY & TARGET 1200) ---
async def hunter_engine():
    conn = await connect_to_mt5()
    if not conn: return
    print(f"🚀 JARVIS: Mesin Hunter Aktif di Akun {MT5_ACCOUNT}")
    
    while True:
        try:
            info = await conn.get_account_information()
            balance = info['balance']
            
            if balance >= 1200:
                print("🎯 Target Tercapai! Operasi Berhenti.")
                break
            
            # Cek posisi: Jika kosong, Entry BUY Gold 0.01
            positions = await conn.get_positions()
            if len(positions) == 0:
                print("⚔️ Jarvis: Entry BUY XAUUSD...")
                await conn.create_market_order('XAUUSD', 'BUY', 0.01)
            
            await asyncio.sleep(60) 
        except Exception as e:
            print(f"⚠️ Reconnecting... {e}")
            conn = await connect_to_mt5()
            await asyncio.sleep(15)

# --- 4. TELEGRAM HANDLER ---
@bot.message_handler(func=lambda message: True)
def main_handler(message):
    txt = message.text.lower()
    
    if any(k in txt for k in ["saldo", "cek", "status"]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        conn = loop.run_until_complete(connect_to_mt5())
        if conn:
            info = loop.run_until_complete(conn.get_account_information())
            teks = (
                f"🛡️ **LAPORAN UNIT JARVIS** 🛡️\n"
                f"💰 Saldo: {info['balance']} cent\n"
                f"🎯 Target: 1200 cent\n"
                f"📈 Status: {'Berburu' if info['balance'] < 1200 else 'Selesai'}"
            )
            bot.reply_to(message, teks, parse_mode="Markdown")
        else:
            bot.reply_to(message, "Gagal konek ke MT5!")
    else:
        try:
            prompt = f"Kamu Jarvis, asisten AI Elino. Jawab dengan cerdas: {message.text}"
            res = model.generate_content(prompt)
            bot.reply_to(message, res.text)
        except:
            bot.reply_to(message, "Sistem AI sedang refresh!")

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(hunter_engine())).start()
    bot.polling(none_stop=True)
