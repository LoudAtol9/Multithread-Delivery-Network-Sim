# Simulador de Rede de Entregas Concorrente

Este projeto implementa uma aplicação concorrente para simular o comportamento de uma rede de entregas. O objetivo é modelar a interação entre encomendas, veículos de transporte e pontos de redistribuição, utilizando conceitos de **concorrência** e **sincronização** abordados na disciplina **Sistemas Operacionais I**.

---

## 🛠 Funcionalidades

- Simulação de uma rede de entregas com **pontos de redistribuição** conectados sequencialmente.
- Criação de **threads** para encomendas, veículos e pontos de redistribuição.
- Sincronização com **semafóros** e **variáveis de trava** para garantir acesso exclusivo aos recursos compartilhados.
- Monitoramento em tempo real do status da simulação.
- Geração de logs detalhados para rastreamento de cada encomenda.

---

## 📂 Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

### 1. **`delivery_package.py`**
- Representa as **encomendas** efetivamente.
- Cada encomenda é uma thread que registra seu trajeto (ponto de origem e destino) e os tempo ao carregar e descarregar.
- Utiliza semáforos para dormir e não usar recurso desnecessariamente.

### 2. **`delivery_vehicle.py`**
- Representa os **veículos** que transportam as encomendas.
- Cada veículo gerencia uma lista de encomendas (limitada pela capacidade de carga do veículo) e segue uma rota circular pelos pontos de redistribuição.
- Realiza sincronização para carregar/descarregar encomendas e mover entre pontos de redistribuição usando um semaphoro.

### 3. **`redistribution_point.py`**
- Representa os **pontos de redistribuição**.
- Gerencia filas de encomendas e veículos, controlando a transferência de cargas.
- Usa um semáforo (Mutex) para garantir que apenas um veículo é processado por vez e para garantir e usa outro para dormir o processo enquanto não há carros na espera.

### 4. **`monitor.py`**
- Fornece monitoramento em tempo real da simulação.
- Exibe tabelas mostrando o status de cada veículo e ponto de redistribuição, como localização, carga e pacotes processados.
- Faz a comunicação entre as threads e compartilha dados globais do processo entre elas.

### 5. **`file_managent.py`**
- Gerencia a gravação de logs em arquivos de forma um por vez, como se fosse uma fila de impressão.
- Utiliza uma fila protegida por semáforos para registrar eventos como carregamento, descarregamento e movimentação das encomendas.

---

## 🚀 Como Executar

### Pré-requisitos:
- **Python 3.9** ou superior.
- Biblioteca adicional: `pandas`.

### Execução:
Execute o programa principal, alterando no código os seguintes argumentos:
- `S`: Número de pontos de redistribuição.
- `C`: Número de veículos.
- `P`: Número de encomendas.
- `A`: Capacidade de carga por veículo.

Exemplo de comando:
```bash
$ python main.py
```
## 📤 Saídas

### 1. **Console**
- Exibição em tempo real do status dos veículos, encomendas e pontos de redistribuição.

### 2. **Logs**
- Arquivos detalhados com os rastros das encomendas, incluindo os pontos de redistribuição acessados e tempos de cada etapa.

#### Exemplo de log:
```text
[Pacote 1] saiu de [Ponto de Distribuicao 0] as 1234567890s
[Pacote 1] chegou em [Ponto de Distribuicao 3] as 1234567895s
```
## 🔑 Conceitos Aplicados

### **Concorrência e Threads**
- Cada elemento da simulação (encomendas, veículos, pontos) opera como uma thread independente, utilizando o módulo `threading` do Python.

### **Sincronização**
- Semáforos são usados para controlar o acesso aos pontos de redistribuição e coordenar a interação entre veículos e encomendas.

### **Sincronização Circular**
- Veículos circulam pelos pontos de redistribuição em um ciclo contínuo, implementando filas circulares.

### **Gerenciamento de Recursos**
- A capacidade limitada de carga dos veículos é controlada dinamicamente, simulando restrições reais.

---

## 👥 Contribuidores

Este projeto foi desenvolvido por **André Mendonça Morato Pupin e Gabriel Freitas Carucce** como parte da disciplina **Sistemas Operacionais I**.


