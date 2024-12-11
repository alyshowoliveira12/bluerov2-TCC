# Exemplos de Utilização das Funções

Antes de começar, não esqueça de configurar corretamente o tipo de conexão para o BlueROV2.

---

## **1. Controle Manual**
Utilize o script `manual_control.py` para enviar comandos manuais de movimentação.

**Comando:**
```bash
python manual_control.py --conexao <tipo_de_conexao> --x <valor_x> --y <valor_y> --z <valor_z> --r <valor_yaw> --buttons <valor_botao>
```
```bash
python manual_control.py --conexao udp:localhost:14445 --x 500 --y 0 --z -500 --r 250 --buttons 0
```

## **2. Armar/Desarmar**
Utilize o script `arm.py` para armar e `disarm.py` para desarmar.

**Comando:**
```bash
python arm.py --conexao <tipo_de_conexao>
```
```bash
python arm.py --conexao udp:localhost:14445
```
## **2. Armar/Desarmar**
Utilize o script `arm.py` para armar e `disarm.py` para desarmar.

**Comando:**
```bash
python arm.py --conexao <tipo_de_conexao>
```
```bash
python arm.py --conexao udp:localhost:14445
```

## **3. Movimento NED**
Utilize o script `ned_movement.py` para enviar um único comando NED ao BlueROV2. **NECESSITA DE UM SISTEMA DE LOCALIZAÇÃO**.

**Comando:**
```bash
python ned_movement.py --conexao <tipo_de_conexao> --north <valor_north> --east <valor_east> --down <valor_down>
```
```bash
python ned_movement.py --conexao tcp:127.0.0.1:5763 --north 5 --east 0 --down -2
```

