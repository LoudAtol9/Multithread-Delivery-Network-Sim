from __future__ import annotations

import os
import random
import threading
import time

import delivery_vehicle as dv
import delivery_package as dp
import redistribution_point as rp

import monitor as m
import file_managent as fm


# Inputs Iniciais
cargo_spaces_A: int = 4
redistribution_point_S: int = 5
vehicle_C: int = 7
packages_P: int = 40
 
# Monitor: 
#   - controla as variaveis globais
#   - imprime informações na tela
monitor = m.Monitor()

# Controlador de Impressao:
#   - Faz uma fila para uma impressao nao 
# sair por cima da outra
file = fm.multithread_file("actions.log")

# Lista com todos as threads necessarias
list_rp: list[rp.redistribution_point] = []
list_dv: list[dv.delivery_vehicle] = []
list_dp: list[dp.delivery_package] = []



# Condicoes exigidas pelo enunciado
def initial_conditions(A: int, C: int, P: int) -> None:
    assert P > A > C, "Parâmetros de entrada inválidos, P >> A >> C"


def main():

    index: int = 0

    global monitor

    global list_dp
    global list_dv
    global list_rp

    # Incializa os pacotes
    for i in range(packages_P):
        origin = random.randint(0, redistribution_point_S - 1)
        dest = random.randint(0, redistribution_point_S - 1)
        if origin == dest : origin = origin + 1
        list_dp.append(dp.delivery_package(i, origin, dest, file))

    # Inicializa os pontos de redistribuicao
    for i in range(redistribution_point_S):
        list_rp.append(rp.redistribution_point(i, file))
        
    # Incializa o estoque nos pontos de redistribuicao
    while len(list_dp) != 0 :
        if list_dp[0].dest != index:
            list_rp[index].add_package_to_stock(list_dp.pop(0))
        index = (index + 1) % redistribution_point_S

    # Inicializa os veiculos
    for i in range(vehicle_C):
        list_dv.append(dv.delivery_vehicle(i, cargo_spaces_A, random.randint(0, redistribution_point_S - 1), redistribution_point_S, list_rp))

    # Inicia as threads dos pontos de redistribuicao
    for redis_point in list_rp:
        redis_point.start()   

    # Inicia o controlador de impressao
    file.start()

    # Inicia nosso monitor e atualizador das variaveis
    monitor.set_lists(list_rp, list_dv)
    monitor.start()

    # Inicia as threads dos veiculos
    for vehicle in list_dv:
        vehicle.set_monitor(monitor)
        vehicle.start()

    # Espera os veiculos desligarem
    for vehicle in list_dv:
        vehicle.join()
    
    # Emite sinal para desligar os pontos de redistribuição
    for redis_point in list_rp:
        redis_point.add_vehicle(None)
        redis_point.join()

    # Emite sinal para desligar a fila
    file.queue_string(None)

    
if __name__ == '__main__' :
    main()