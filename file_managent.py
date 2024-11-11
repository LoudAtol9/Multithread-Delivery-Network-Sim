import threading

class multithread_file(threading.Thread):

    def __init__(self, filename: str):
        super().__init__()

        self.file_ptr = open(filename, "w")

        self.queue_semaphore = threading.Semaphore(1)
        self.lock = threading.Semaphore(0)

        self.print_queue: list[str] = []


    # Coloca uma string na fila de impressao 
    def queue_string(self, string: str):
        
        self.queue_semaphore.acquire()

        if string is None:
            self.print_queue.append(None)
        else:
            self.print_queue.append(string + "\n")

        self.lock.release()
        self.queue_semaphore.release()
        
    
    # Inicia a fila de impressao
    def run(self):

        string: str

        while True:
            # Espera requisicao da fila
            self.lock.acquire()

            string = self.print_queue.pop(0)

            # Recebeu sinal de interrupcao
            if string is None:
                break

            self.file_ptr.write(string)