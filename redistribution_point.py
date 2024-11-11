from __future__ import annotations

import threading
import time
import random

import delivery_vehicle as dv
import delivery_package as dp

import file_managent as fm


class redistribution_point(threading.Thread):

    def __init__(self, id: int, file: fm.multithread_file):
        # Chama construtor da classe Thread
        super().__init__()
        self.id = id
        # Numero de Pacotes a serem entregues
        self.num_packages_to_deliver = 0
        # Numero de Pacotes ja recebidos
        self.num_packages_received: int = 0
        # Pacotes a serem entregues
        self.packages_to_deliver: list[dp.delivery_package] = []
        # Pacotes recebidos
        self.packages_received: list[dp.delivery_package] = []
        # Fila do Estacionamento
        self.parking_lot: list[dv.delivery_vehicle] = []
        # Semaforo para controlar acesso a lista
        self.parking_semaphore: threading.Semaphore = threading.Semaphore(1)
        # Semaforo para acordar o ponto de redis
        self.semaphore: threading.Semaphore = threading.Semaphore(0)
        # Arquivo de log
        self.log_file = file
        # Para encerrar a thread com o programa principal
        self.daemon = True  


    # Adiciona um pacote no estoque, apenas usado na inicializacao
    def add_package_to_stock(self, package: dp.delivery_package):
        self.packages_to_deliver.append(package)
        self.num_packages_to_deliver = self.num_packages_to_deliver + 1


    # Enche o caminhao de pacotes
    # Caso nao caiba, nem um pacote ele nao faz nada
    def give_packages(self, vehicle: dv.delivery_vehicle) -> None:

        free_spaces : int = vehicle.get_total_spaces() - vehicle.get_used_spaces()
        if free_spaces > self.num_packages_to_deliver : free_spaces = self.num_packages_to_deliver

        self.log_file.queue_string(f"[{vehicle}] recebeu {free_spaces} pacotes de [{self}]\n")

        for _ in range(free_spaces):
            package = self.packages_to_deliver.pop()
            package.start()
            vehicle.load_package(package)
            self.num_packages_to_deliver = self.num_packages_to_deliver - 1


    # Recebe todos os pacotes do caminhao direcionados a esse posto
    # Se nao tiver nenhum pacote ele nao faz nada
    def receive_packages(self, vehicle: dv.delivery_vehicle) -> None:

        package_list : list[dp.delivery_package] = vehicle.unload_packages(self.id)

        self.log_file.queue_string(f"[{vehicle}] entregou {len(package_list)} pacotes para [{self}]\n")

        for package in package_list :
            package.end_delivery()
            self.packages_received.append(package)
            self.num_packages_received = self.num_packages_received + 1


    # Adiciona um veiculo a lista e acorda e libera a thread
    # Chamada pelo veiculo
    def add_vehicle(self, vehicle: dv.delivery_vehicle) -> None:
        self.parking_semaphore.acquire()
        self.parking_lot.append(vehicle)
        self.parking_semaphore.release() 
        self.semaphore.release() # ------------- destrava -------------


    # Maquina de estados do Ponto de Redistribuicao
    # Loop continou para processar veiculos a medida que chegam
    def run(self) -> None:

        # Sempre
        while True:
            # Bloqueia ate ter um veiculo na lista de espera
            self.semaphore.acquire() # ------------- trava -------------

            # Remove o próximo veículo
            vehicle = self.parking_lot.pop(0)

            # Sinal para encerrar a thread
            if vehicle is None:
                break  

            # Processa o veiculo recebido
            self.log_file.queue_string(f"[{self}] Processando [{vehicle}]\n")
            self.receive_packages(vehicle)
            self.give_packages(vehicle)
            time.sleep(random.randint(1,3))

            # Libera o veiculo do patio
            self.log_file.queue_string(f"[{self}] Liberou [{vehicle}]\n")
            vehicle.unlock_vehicle() # -- libera o veiculo --


    def __str__(self) -> str:
        return f"Ponto de Distribuicao {self.id}"
    
    def debbug_info(self) -> str:
        print("\n-------------//-------------//-------------")
        print(f"[{self}] :")
        print(f"    num_packages_to_deliver = {self.num_packages_to_deliver}")
        print(f"    num_packages_received = {self.num_packages_received}")
        #print(f"    packages_to_deliver = {self.packages_to_deliver}")
        #print(f"    packages_received = {self.packages_received}")
        print(f"    parking_lot = {self.parking_lot}")
        print("-------------//-------------//-------------")
        
    
    def get_id(self) -> int:
        return self.id
    
    def get_num_packages_to_deliver(self) -> int:
        return self.num_packages_to_deliver
    
    def get_num_packages_received(self) -> int:
        return self.num_packages_received
