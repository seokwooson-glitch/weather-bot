import requests
import os
from datetime import datetime

BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"

SKY_CODE = {"1": "☀️ 맑음", "3": "⛅ 구름많음", "4": "☁️ 흐림"}
PTY_CODE = {"0": "", "1": "🌧 비", "2": "🌨 비/눈", "3": "❄️ 눈", "4": "🌦 소나기"}

GRID_COORDS = {
    "서울": (60, 127),
    "부산": (99, 75),
    "대구": (89, 90),
    "인천": (54, 124),
    "광주": (58, 74),
    "대전": (67, 100),
    "분당": (63, 123),
}

def get_grid(city="분당"):
    return GRID_COORDS.get(city, GRID_COORDS["분당"])

def get_weather(city="분당"):
    API_KEY = os.getenv("WEATHER_API_KEY")
    nx, ny = get_grid(city)
    now = datetime.now()

    params = {
        "serviceKey": API_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "base_date": now.strftime("%Y%m%d"),
        "base_time": now.strftime("%H00"),
        "nx": nx,
        "ny": ny,
    }

    res = requests.get(f"{BASE_URL}/getUltraSrtNcst", params=params)
    items = res.json()["response"]["body"]["items"]["item"]
    data = {item["category"]: item["obsrValue"] for item in items}

    return {
        "city": city,
        "temp": data.get("T1H", "N/A"),
        "humidity": data.get("REH", "N/A"),
        "rain": data.get("RN1", "0"),
        "pty": PTY_CODE.get(data.get("PTY", "0"), ""),
        "wind_speed": data.get("WSD", "N/A"),
    }

def format_weather(w):
    pty = w["pty"]
    rain_info = f"\n🌂 강수량: {w['rain']}mm" if w["rain"] != "0" else ""
    return (
        f"📍 {w['city']} 현재 날씨\n"
        f"🌡 기온: {w['temp']}°C\n"
        f"💧 습도: {w['humidity']}%\n"
        f"💨 풍속: {w['wind_speed']}m/s\n"
        f"{f'🌧 강수: {pty}' if pty else '☀️ 강수 없음'}"
        f"{rain_info}"
    ) 
