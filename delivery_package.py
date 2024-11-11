from __future__ import annotations

import threading
import time
import file_managent as fm


class delivery_package(threading.Thread):

    def __init__(self, id: int, origin: int, dest: int, file: fm.multithread_file) -> None:
        super().__init__()
        self.id = id
        self.origin = origin
        self.dest = dest
        self.lock = threading.Semaphore(0)
        self.time: float = 0.0
        self.file = file

    # Libera a thread para terminar de medir o tempo
    def end_delivery(self):
        self.lock.release()

    # Cronometra o tempo para entrega
    def run(self):

        time_start = time.time()
        self.lock.acquire()
        self.time = time.time() - time_start

        self.file.queue_string(f"[Pacote {self.id}] foi de [Ponto de Distribuicao {self.origin}] a [Ponto de Distribuicao {self.dest}] em {self.time}s\n")
        