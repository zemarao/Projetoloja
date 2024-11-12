import xml.etree.ElementTree as ET

def extrair_informacoes(xml_content):
    # Namespaces necessários para acessar os elementos no XML
    namespaces = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe',
    }

    # Parseia o conteúdo do XML
    root = ET.fromstring(xml_content)

    # Extrai o nome do emitente
    emitente = root.find('.//nfe:emit/nfe:xNome', namespaces).text

    # Lista para armazenar os produtos
    produtos = []

    # Itera sobre os elementos <det> que contêm informações dos produtos
    for det in root.findall('.//nfe:det', namespaces):
        prod = det.find('nfe:prod', namespaces)

        # Extraindo valores necessários e convertendo para números
        qCom = float(prod.find('nfe:qCom', namespaces).text)
        vProd = float(prod.find('nfe:vProd', namespaces).text)
        vUnCom = float(prod.find('nfe:vUnCom', namespaces).text)
        vDesc = float(prod.find('nfe:vDesc', namespaces).text)

        # Calculando o valor ajustado
        valor_ajustado = vUnCom - (vDesc / qCom)

        # Montando o dicionário do produto
        produto_info = {
            'cProd': prod.find('nfe:cProd', namespaces).text,
            'xProd': prod.find('nfe:xProd', namespaces).text,
            'qCom': qCom,
            'vProd': vProd,
            'vUnCom': vUnCom,
            'vDesc': vDesc,
            'valor_ajustado': valor_ajustado,
        }

        produtos.append(produto_info)

    return emitente, produtos
