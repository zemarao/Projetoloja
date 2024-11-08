import xmltodict

# Função para processar o XML e extrair as informações desejadas
def processar_xml(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        data = xmltodict.parse(file.read())

    # Dicionário para armazenar as informações extraídas
    resultado = {
        'Nome Destinatário': '',
        'Produtos': [],
    }

    # Extraindo o nome do destinatário
    resultado['Nome Destinatário'] = data['nfeProc']['NFe']['infNFe']['dest']['xNome']

    # Extraindo informações de cada produto
    itens = data['nfeProc']['NFe']['infNFe']['det']
    if isinstance(itens, list):  # Caso haja vários produtos
        for item in itens:
            produto = extrair_detalhes_produto(item)
            resultado['Produtos'].append(produto)
    else:  # Caso haja apenas um produto
        produto = extrair_detalhes_produto(itens)
        resultado['Produtos'].append(produto)

    return resultado

# Função para extrair os detalhes do produto de um item
def extrair_detalhes_produto(item):
    produto = item['prod']
    detalhes_produto = {
        'Código do Produto': produto['cProd'],
        'Código EAN': produto['cEAN'],
        'Descrição do Produto': produto['xProd'],
        'Unidade Comercial': produto['uCom'],
        'Quantidade Comercial': produto['qCom'],
        'Valor Unitário Comercial': produto['vUnCom'],
        'Valor Total do Produto': produto['vProd'],
        'Valor do Desconto': produto.get('vDesc', '0.00'),  # Pode estar ausente
        'Indicador de Total': produto['indTot']
    }

    # Extraindo a data de vencimento, se disponível em duplicata
    duplicata = item.get('dup')
    if duplicata:
        detalhes_produto['Data de Vencimento'] = duplicata.get('dVenc')
    else:
        detalhes_produto['Data de Vencimento'] = 'N/A'  # Se não houver data de vencimento

    return detalhes_produto

# Função principal para exibir o resultado extraído
def main():
    # Caminho do arquivo XML
    xml_file = 'caminho/do/arquivo.xml'  # Altere para o caminho do arquivo XML

    # Processa o arquivo XML e obtém as informações
    resultado = processar_xml(xml_file)

    # Exibe o resultado
    print("Nome do Destinatário:", resultado['Nome Destinatário'])
    print("\nProdutos:")
    for produto in resultado['Produtos']:
        for chave, valor in produto.items():
            print(f"{chave}: {valor}")
        print("-" * 20)

# Executa a função principal
if __name__ == "__main__":
    main()
