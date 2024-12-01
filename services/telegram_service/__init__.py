# -*- coding: cp1251 -*-

import requests
import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


from ..abstract_service import AbstractService

import io
import asyncio


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Привет!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Помощь!")


async def message_helper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    await update.message.reply_text("Отправь мне файл с данными.")


async def file_helper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:

        await update.message.reply_text("Начинаю обработку")

        file = await context.bot.get_file(update.message.document)
        buf = await file.download_as_bytearray()
        io_buf = io.BytesIO(buf)
        io_buf.seek(0)

        file = pd.read_csv(io_buf)['value'].to_numpy().astype(np.float32).reshape(-1, 1)
        file = list(np.nan_to_num(file).reshape(-1).astype(float))

        response = await asyncio.to_thread(requests.post, 'http://localhost:8000/ai/generate_next_31', json=file)

        data = response.json()

        y = data['y']
        y_pred = data['y_pred']
        y_new = data['y_new']

        plt.figure(figsize=(22, 6))
        plt.plot(range(len(y)), y, color='green', label='Реальные')
        plt.plot(range(len(y_pred)), y_pred, color='blue', label='Генерация')

        plt.plot(range(len(y_pred), len(y_pred) + len(y_new)), y_new, color='red', label='Генерация новых значений')
    
        plt.xlabel('Индекс')
        plt.ylabel('Значение')
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        await update.message.reply_photo(buf)

        buf = io.BytesIO()
        pd.DataFrame(np.array(y_new).reshape(-1, 1).astype(np.int32)).to_csv(buf, index=False, header=['value'])
        buf.seek(0)

        await update.message.reply_document(buf, filename="Результат.csv")

        return
    except:
        pass

    await update.message.reply_text("Не удалось сформировать ответ")


class TelegramService(AbstractService):

    def __init__(self, config):
        super().__init__()
        self.app = Application.builder().token(config.token).build()
        
        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(CommandHandler("help", help_command))

        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_helper))
        self.app.add_handler(MessageHandler(filters.Document.FileExtension("csv"), file_helper))


    def run(self):
        asyncio.run(self._run())


    async def _run(self):

        await self.app.initialize()
        await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await self.app.start()
	
        while True:
            await asyncio.sleep(1)






