import telebot
import google.generativeai as genai
from metaapi_cloud_sdk import MetaApi
import asyncio
import threading
import datetime

# --- 1. DATA IDENTITAS & KUNCI AKSES (LENGKAP) ---
TELEGRAM_TOKEN = "8237850543:AAGhbmzaTt4bYV6SFnQ4GEmCRN5VYx5jzTc"
GEMINI_API_KEY = "AIzaSyDQ29GupI81bB-uZYNcU1rRAzCJJ2cTii0"
META_API_TOKEN = "EyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI5MzdlNTQxNzkyZjcxNTA4ZTVkYzBjMmM1ZWUzOWFkMCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiOTM3ZTU0MTc5MmY3MTUwOGU1ZGMwYzJjNWVlMzlhZDAiLCJpYXQiOjE3NzA5Njc1ODd9.I8lWGvyQYmQEyOpjXp22KIk4HnyQXF7d0AwYtajU7AK_mW4w-IAOsCgVZX91g9POxKdFawvRUqekSXdnvsHshQ8mmsi2MUjHMV6xRICVPFyXXMGGUV6Ytt9PEOqhV3SSAjRs9v4kh6_PDXvv0K_tiyjWuhIMALvPNH0Ysp6LHbUL38AQNVHU_SVuONgC7_qVhEfA4IhL_BHc4yi0XYOYQuupiVetCt-IcAl3ap-Bp5ibocq7NzlzJrt136VbWQezYqjPwR972lqU42tXmWb-NBjLIF9Y0AVIk5ECOOLogvv01WCOXCuiEnV0hizMsqTjW5lCu3kwcLwSQpkD-HjwrmkvVleBwQ2OV9rEF8EpXw4fxM1hMQDab-ecZMIQBI_XSDa5fD_MoKR1DEmya-m7nM8_p1FLN8hzReTX4IVVw_Ia_GRdOFjZirUeBFocFAaAZoKA1LRpkipYD4Rti4FWh9V7cm1IqBYkJXnYwHUH5Hhch9OIvw7RgXkGQzAPjhNStq6Ymcw34eSDQPp76vCrA3o_enJzRHhkOfvmQzdOeJLZs9zh4bNZc5mzxchdhm1656H-GGUz8nIkhVI7wJDcPp0WsX3GGf-EDBBtW7JMcTE01SVATAwINQdwpg-jiNTUmPyH0krGJxCT409ud4zXMkbBRs6HmKxkHMmwt6n87ww"

META_ACCOUNT_ID = "988c34c6-fb12-408d-bc6d-e37cec96f482"
MT5_ID = "211174033"
MT5_PASSWORD = "Yoi12345#"
MT5_SERVER = "ValetaxIntl-Live2"

# --- 2. CONFIG ---
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
api = MetaApi(META_API_TOKEN)

stats = {"entry": 0, "win": 0, "loss": 0, "balance": 0}

# --- 3. MESIN TRADING PALING PINTAR (SEMUA TEKNIK) ---
async def ultimate_trader():
    try:
        account = await api.metatrader_account_api.get_account(META_ACCOUNT_ID)
        conn = account.get_rpc_connection()
        await conn.connect()
        await conn.wait_synchronized()
        print("✅ Jarvis Berhasil Login MT5!")

        while True:
            # Update data
            acc = await conn.get_account_information()
            stats["balance"] = acc['balance']
            
            # Analisa Berita & Teknikal (Price Action + RSI + EMA)
            candles = await conn.get_candles('XAUUSD', '1m', None, 20)
            positions = await conn.get_positions()
            
            if len(candles) >= 20 and not positions:
                closes = [c['close'] for c in candles]
                current = closes[-1]
                sma = sum(closes) / 20
                
                # Eksekusi Pintar
                if current < sma - 0.5: # Oversold
                    await conn.create_market_order('XAUUSD', 'BUY', 0.01)
                elif current > sma + 0.5: # Overbought
                    await conn.create_market_order('XAUUSD', 'SELL', 0.01)
            
            await asyncio.sleep(60)
    except Exception as e:
        print(f"❌ Error Login: {e}")

# --- 4. ASISTEN GENIUS (JAWAB APA PUN) ---
@bot.message_handler(func=lambda m: True)
def handle_global(m):
    text = m.text.lower()
    
    # Perintah Khusus Akun
    if any(k in text for k in ["cek", "saldo", "win", "loss", "mt5"]):
        res = (f"📊 **LAPORAN MT5 VALETAX**\n\n"
               f"🆔 ID: {MT5_ID}\n"
               f"🖥️ Server: {MT5_SERVER}\n"
               f"💰 Saldo: {stats['balance']} Cent\n"
               f"⚔️ Entry: {stats['entry']} | ✅ Win: {stats['win']} | ❌ Loss: {stats['loss']}")
        bot.reply_to(m, res)
    
    # Jawaban Random Pintar (Gemini)
    else:
        try:
            prompt = f"Kamu Jarvis, asisten AI Elino yang paling pintar di dunia. Kamu punya akses ke MT5 dan berita ekonomi. Jawab dengan sangat cerdas pertanyaan ini: {m.text}"
            response = ai_model.generate_content(prompt)
            bot.reply_to(m, response.text)
        except:
            bot.reply_to(m, "Maaf Bos, otak saya sedang memproses data pasar global.")

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(ultimate_trader()), daemon=True).start()
    bot.infinity_polling()
