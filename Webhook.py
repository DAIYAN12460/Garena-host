from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from new import bot, dp
from aiogram import types
import asyncio

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
async def webhook():
    update = types.Update(**request.json)
    await dp.process_update(update)
    return jsonify({"ok": True})

@app.route("/")
def index():
    return "Bot is running!"
