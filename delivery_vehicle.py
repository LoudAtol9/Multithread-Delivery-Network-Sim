from __future__ import annotations

import threading
import time
import random

import main
import monitor as m
import delivery_package as dp
import redistribution_point as rp
import consts as cn


class delivery_vehicle(threading.Thread):

    # A (espaços de carga) = spaces
    def __init__(self, id: int, total_spaces: int, starting_pos: int , S: int,
                  list_of_redis_point: list[rp.redistribution_point], direction=cn.RIGHT) -> None:
        
        # Chama o construtor da classe Thread
        super().__init__()

        # ID do veiculo
        self.id = id 

        # Suporte maximo de carga do veiculo
        self.total_spaces = total_spaces

        # Espaco Ocupado na carga
        self.used_spaces = 0

        # Carga (lista de pacotes)
        self.load_list : list[dp.delivery_package] = []

        # Semaphoro que controla a disponibilidade do veiculo
        self.lock = threading.Semaphore(0)

        # Tem copia das referencias de todos os pontos de redistribuicao
        self.list_rp: list[rp.redistribution_point] = list_of_redis_point

        # Direcao que o veiculo vai andar
        self.direction = direction

        # Em qual ponto ele vai iniciar
        self.starting_pos = starting_pos
        self.pos = starting_pos
        self.in_travel = False

        # Numero de pontos de redistribuicao
        self.S = S
    
    # Configura o Monitor
    def set_monitor(self, monitor: m.Monitor):
        self.monitor = monitor

    # Coloca uma encomenda no caminhao
    def load_package(self, package: dp.delivery_package) -> None:

        # Caso nao esteja cheio entao adicionar pacote
        if not (len(self.load_list) == self.total_spaces) :
            self.load_list.append(package)
            self.used_spaces = self.used_spaces + 1


    # Ve quais sao as encomendas que correspondem a aquele destino e as descarrega do caminhao
    def unload_packages(self, dest: int) -> list[dp.delivery_package] :

        # Quantos itens foram removidos 
        poped_itens = 0

        # Lista de encomendas que serao entregues nesse destino
        package_list : list[dp.delivery_package] = []

        # Percorre a lista de encomendas
        for i in range(0, len(self.load_list)) :

            # Caso seja pra esse destino 
            if self.load_list[i - poped_itens].dest == dest :

                # Remover do cargo e salvar na lista
                package_list.append(self.load_list.pop(i - poped_itens))
                # Atualiza qnts itens foram removidos para nao quebrar o contador
                poped_itens = poped_itens + 1

        self.used_spaces = self.used_spaces - poped_itens
        return package_list


    # Destrava o veiculo
    # Chamada pelo ponto de redistribuicao
    def unlock_vehicle(self) -> None:
        self.lock.release() # ------------- destrava -------------

    def condition_to_run(self):
        if self.monitor.num_packages_to_deliver == 0 and len(self.load_list) == 0:
            return False
        return self.monitor.get_num_packages_received() != main.packages_P

    # Loop que percorre todas os pontos de distribuicao recebendo e dando pacotes
    def run(self):

        # Enquanto tiver encomenda para entregar
        while (not (self.monitor.num_packages_to_deliver == 0 and len(self.load_list) == 0)):
            #print(f"[{self}] esta em [{self.list_rp[self.pos]}]\n")

            # Estaciona Veiculo no patio do ponto de redistribuicao
            self.list_rp[self.pos].add_vehicle(self) # -- acorda o rp --

            self.lock.acquire() # ------------- trava -------------
            # Enquanto nao terminar operacoes nao pode partir ao proximo destino
            self.in_travel = True
            time.sleep(random.randint(1, 10))

            # Avança pra proxima casa dependendo do sentido
            if self.direction == cn.RIGHT:
                self.pos = (self.pos + 1) % self.S
            else:
                if (self.pos - 1) < 0:
                    self.pos = self.S - 1
                else:
                    self.pos = self.pos - 1

            self.in_travel = False
            

    def __str__(self) -> str:
        return f"Veiculo: {self.id}"


    def debbug_info(self) -> str:
        print(f"[{self}] :")
        print(f"    total_spaces = {self.total_spaces}")
        print(f"    used_spaces = {self.used_spaces}")
        #print(f"    load_list = {self.load_list}")
        print(f"    len(load_list) = {len(self.load_list)}")
        print(f"    starting_pos = {self.starting_pos}")
        print(f"    list_rp = {self.list_rp}")
        print("-------------//-------------//-------------\n\n")
    
    def get_id(self) -> int:
        return self.id
    
    def get_total_spaces(self) -> int:
        return self.total_spaces
    
    def get_used_spaces(self) -> int:
        return self.used_spaces