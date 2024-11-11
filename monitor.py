from __future__ import annotations

import os
import threading
import time
import pandas as pd

import main

def clear():
    # Limpa a tela no Windows ou Linux/macOS
    comando = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando)

class Monitor(threading.Thread):

    def __init__(self):
        super().__init__()
        self.num_packages_to_deliver: int = main.packages_P
        self.num_packages_received: int = 0
        self.num_packages_on_travel: int = 0

    def set_lists(self, list_rp: list[main.rp.redistribution_point], list_dv: list[main.dv.delivery_vehicle]):
        self.list_rp = list_rp
        self.list_dv = list_dv

    def get_num_packages_received(self) -> int:
        return self.num_packages_received
    
    #
    def run(self):

        dv_id_list: list[int] = list(range(len(self.list_dv)))
        dv_pos_list: list[str] = list(range(len(self.list_dv)))
        dv_load_list: list[int] = list(range(len(self.list_dv)))

        rp_id_list: list[int] = list(range(len(self.list_rp)))
        rp_to_deliver: list[int] = list(range(len(self.list_rp)))
        rp_received: list[int] = list(range(len(self.list_rp)))
        rp_parking_lot: list[list[int]] = list(range(len(self.list_rp)))
        rp_vehicles_id: list[int] = []

        # Enquanto tiver algo a ser entregue
        while self.num_packages_received != main.packages_P:

            # Percorre as Threads de Veiculo para coletar informacoes
            for vehicle in self.list_dv:
                if vehicle.in_travel == True:
                    dv_pos_list[vehicle.id] = str(vehicle.pos) + " --> " + str((vehicle.pos + 1) % main.redistribution_point_S)
                else:
                    dv_pos_list[vehicle.id] = str(vehicle.pos)

                dv_load_list[vehicle.id] = len(vehicle.load_list)

            # Cria tabela
            vehicle_data = {
                "Veículo": dv_id_list,
                "Localização": dv_pos_list,
                "Carga": dv_load_list
            }
            vehicle_dataframe = pd.DataFrame(vehicle_data)

            # Percorre as Threads de ponto de redistribuicao para coletar informacoes
            for redis in self.list_rp:
                rp_received[redis.id] = redis.get_num_packages_received()
                rp_to_deliver[redis.id] = redis.get_num_packages_to_deliver()

                rp_parking_lot[redis.id] = []

                for vehicle in redis.parking_lot:
                    rp_parking_lot[redis.id].append(vehicle.id)

            # Cria tabela
            rp_data = {
                "Ponto de Redistribuicao": rp_id_list,
                "Pacotes a serem entregues": rp_to_deliver,
                "Pacotes recebidos": rp_received,
                "Estacionamento": rp_parking_lot
            }
            rp_dataframe = pd.DataFrame(rp_data)

            # Atualiza os estados das variaveis globais
            self.num_packages_received = sum(rp_received)
            self.num_packages_to_deliver = sum(rp_to_deliver)
            self.num_packages_on_travel = sum(dv_load_list)

            clear()

            print("Pacotes a receber = ", self.num_packages_received )
            print("Pacotes a serem entregues = ", self.num_packages_to_deliver)
            print("Pacotes em transporte = ", self.num_packages_on_travel)
            print("\n\n")

            print(vehicle_dataframe.to_string(index=False))
            print("\n\n")
            print(rp_dataframe.to_string(index=False))

            time.sleep(0.5)



    # Atualiza os estados das variaveis globais
    def update_stats(self, list_rp: list[main.rp.redistribution_point]) -> None:

        sum_pd = sum_r = 0

        for rp in list_rp:
            sum_pd = sum_pd + rp.get_num_packages_to_deliver()
            sum_r = sum_r + rp.get_num_packages_received()

        self.num_packages_to_deliver = sum_pd
        self.num_packages_received = sum_r

        print("Packages Received = ", self.num_packages_received )
        print("Packages to Deliver = ", self.num_packages_to_deliver)

    
