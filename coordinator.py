
from threading import Thread
import time

from services import api_service
from services import telegram_service

import config

class Coordinator:

    def __init__(self):
        self.api_service = api_service.ApiService(config.api_service)
        self.telegram_service = telegram_service.TelegramService(config.telegram)
        pass


    def run(self):
        self.get_threads = []
        self.get_threads.append(lambda: Thread(target=lambda: self.api_service.run()))
        self.get_threads.append(lambda: Thread(target=lambda: self.telegram_service.run()))

        self.threads = [get_thread() for get_thread in self.get_threads]

        while True:
            self._thread_start()
            time.sleep(30)

        return

    def _thread_start(self):
        for it, thread in enumerate(self.threads):
            if not thread.is_alive():
                try:
                    thread.start()
                except:
                    self.threads[it] = self.get_threads[it]()
                    self.threads[it].start()
        return

