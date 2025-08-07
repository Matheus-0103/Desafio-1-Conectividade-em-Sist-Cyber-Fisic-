# modelo_osi.py

def camada_aplicacao(dados):
    etiqueta = "[APLICAÇÃO]"
    print(f"{etiqueta}: Enviando a letra '{dados}'")
    return etiqueta, dados

def camada_apresentacao(dados):
    etiqueta = "[APRESENTAÇÃO]"
    dados_encapsulados = f"{etiqueta} {dados}"
    print(f"{etiqueta}: Encapsulando dados... -> {dados_encapsulados}")
    return dados_encapsulados

def camada_sessao(dados):
    etiqueta = "[SESSÃO]"
    dados_encapsulados = f"{etiqueta} {dados}"
    print(f"{etiqueta}: Gerenciando a sessão... -> {dados_encapsulados}")
    return dados_encapsulados

def camada_transporte(dados, porta_origem, porta_destino):
    etiqueta = "[TRANSPORTE]"
    header_transporte = f"Porta Origem: {porta_origem}, Porta Destino: {porta_destino}"
    dados_encapsulados = f"{etiqueta} [{header_transporte}] {dados}"
    print(f"{etiqueta}: Adicionando cabeçalho de transporte... -> {dados_encapsulados}")
    return dados_encapsulados

def camada_rede(dados, ip_origem, ip_destino):
    etiqueta = "[REDE]"
    header_rede = f"IP Origem: {ip_origem}, IP Destino: {ip_destino}"
    dados_encapsulados = f"{etiqueta} [{header_rede}] {dados}"
    print(f"{etiqueta}: Adicionando cabeçalho de rede... -> {dados_encapsulados}")
    return dados_encapsulados

def camada_enlace(dados, mac_origem, mac_destino):
    etiqueta = "[ENLACE]"
    header_enlace = f"MAC Origem: {mac_origem}, MAC Destino: {mac_destino}"
    trailer_enlace = "[CRC]"
    dados_encapsulados = f"{etiqueta} [{header_enlace}] {dados} {trailer_enlace}"
    print(f"{etiqueta}: Criando o quadro com cabeçalho e trailer... -> {dados_encapsulados}")
    return dados_encapsulados

def camada_fisica(quadro):
    etiqueta = "[FÍSICA]"
    print(f"{etiqueta}: Convertendo o quadro para binário...")
    quadro_binario = ' '.join(format(ord(char), '08b') for char in quadro)
    print(f"{etiqueta}: Dado binário pronto para transmissão -> {quadro_binario}")
    return quadro_binario

def desencapsular(quadro):
    print("\n===== SIMULAÇÃO DE RECEPÇÃO =====")
    quadro_texto = ''.join(chr(int(byte, 2)) for byte in quadro.split())
    print(f"[FÍSICA]: Quadro recebido em texto -> {quadro_texto}")

    partes = quadro_texto.split("[ENLACE] [")
    payload_enlace = partes[1].split("] ")[1].split(" [CRC]")[0]
    print(f"[ENLACE]: Removendo cabeçalho e trailer... -> {payload_enlace}")

    partes = payload_enlace.split("[REDE] [")
    payload_rede = partes[1].split("] ")[1]
    print(f"[REDE]: Removendo cabeçalho de rede... -> {payload_rede}")

    partes = payload_rede.split("[TRANSPORTE] [")
    payload_transporte = partes[1].split("] ")[1]
    print(f"[TRANSPORTE]: Removendo cabeçalho de transporte... -> {payload_transporte}")

    partes = payload_transporte.split("[SESSÃO] ")
    payload_sessao = partes[1]
    print(f"[SESSÃO]: Removendo etiqueta de sessão... -> {payload_sessao}")

    partes = payload_sessao.split("[APRESENTAÇÃO] ")
    payload_apresentacao = partes[1]
    print(f"[APRESENTAÇÃO]: Removendo etiqueta de apresentação... -> {payload_apresentacao}")

    partes = payload_apresentacao.split("[APLICAÇÃO] ")
    dados_finais = partes[1]
    print(f"[APLICAÇÃO]: O dado original é '{dados_finais}'")

    print(f"\n🎯 Dispositivo de destino recebeu com sucesso a letra: '{dados_finais}'")


# ===============================
# INÍCIO DA SIMULAÇÃO
# ===============================
print("===== SIMULAÇÃO DO ENVIO =====")
print("📨 Dados a serem enviados: 'A'")
print("-" * 50)

mac_origem = "#B"
mac_destino = "9g"
ip_origem = "%s"
ip_destino = "9g"
porta_origem = 8080
porta_destino = 80

etiqueta_app, dados_app = camada_aplicacao("A")
dados_ap = camada_apresentacao(f"{etiqueta_app} {dados_app}")
dados_sessao = camada_sessao(dados_ap)
dados_transporte = camada_transporte(dados_sessao, porta_origem, porta_destino)
dados_rede = camada_rede(dados_transporte, ip_origem, ip_destino)
quadro = camada_enlace(dados_rede, mac_origem, mac_destino)
quadro_binario = camada_fisica(quadro)

print("-" * 50)
print(f"📡 Enviando para dispositivo de destino: {mac_destino}")

if mac_destino == "9g":
    desencapsular(quadro_binario)
else:
    print("❌ O quadro foi descartado: não era destinado a este dispositivo.")
