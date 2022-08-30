from ast import Index
from io import FileIO
from operator import concat, index
from pickletools import long1, long4
import html
import string
import time
import traceback
import re
from turtle import position
import httplib2
import difflib
import requests
import json
import webbrowser
import requests as requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# produto, id_categoria, id_subcategoria, preco, stock, descricao

global browser
option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome()
action = webdriver.ActionChains


def Organizar_Texto(texto, palavras_excecao):
    a = 1
    while (a == 1):
        try:                
            text = str(texto).split(' ')
            exec = str(palavras_excecao).split(',')

            nome_produto = ""

            for i in range(len(text)):
                if(exec.__contains__(text[i].strip()) == False):
                    text[i] = str(text[i]).strip().lower()
                    text[i] = str(text[i]).strip().replace(str(text[i]).__getitem__(0), str(text[i]).__getitem__(0).upper())
                nome_produto += str(text[i]) + " "
                
            a = 0
            return str(nome_produto).strip()
        except:
            print(traceback.print_exc())
            a = 1

def Selecionar_Produto(endereco_produto, categorias_produto, palavras_excecao):
    descricao = ""
    url = ""
    element4 = ""
    element5 = ""
    
    a = 1
    while (a == 1):
        try:                
            browser.get(endereco_produto)
            index = (browser.current_url).index('produto/') + 8
            codigo_produto = str(browser.current_url)[index:]

            url = "https://www.pauta.com.br/buildingBlock/" + codigo_produto + ".png"

            time.sleep(30)
            #element = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[4]/div[2]/h4")
            #element2 = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[4]/div[2]/div/table")
            #element3 = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[4]/div[2]")
            
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[4]')))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/produto-box/div/div[3]/h4[2]')))
            
            element4 = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[4]')
            element5 = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/produto-box/div/div[3]/h4[2]')
            
            #element4 = browser.find_element_by_xpath('//*[@id="sec-produtos"]/div/div/div[2]')
            #element5 = browser.find_element_by_xpath('//*[@id="sec-produtos"]/div/div/div[2]/div[2]/div[5]/div/div/produto-box/div/div[3]/h4[2]')
            
            #element6 = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[4]/div[1]")
            #element7 = browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]")

            descricao = str(element4.get_attribute('innerHTML')).replace('<p>', '').replace('</p>', '') \
                .replace('¿', '').replace('14,0¿', '14"').replace('14,0 ¿', '14"').replace('14¿', '14"'). \
                replace('14 ¿', '14"').replace('15,6¿', '15,6"').replace('15,6 ¿', '15,6"'). \
                replace('a Pauta', 'o Distribuidor').replace('Dia/Dias', 'Dias').replace('Kg', ' Kg'). \
                replace('/buildingBlock', 'www.pauta.com.br/buildingBlock')    
            a = 0
        except:
            a = 1
            print(traceback.print_exc())
            

    informacoes_produto = str(descricao)[str(descricao).index(
        '<p ng-bind-html="renderHtml(produto.proEspecificacao)" class="ng-binding">') + 74:str(descricao).index(
        '</div>')]

    index_1 = str(descricao).index('id="nomefabri" value="') + 22
    index_2 = str(descricao).index('"', index_1)
    nomefabri = str(descricao)[index_1:index_2]

    index_3 = str(descricao).index('id="partnumber" value="') + 23
    index_4 = str(descricao).index('"', index_3)
    partnumber = str(descricao)[index_3:index_4]


    if (informacoes_produto.isspace() == True):
        descricao = str(descricao)[str(descricao).index('<div class="product-info-box">'):]

    h = httplib2.Http()
    resp = h.request(url, 'HEAD')

    index2 = str(descricao).index('<div id="css-feature-icons"></div>')
    descricao = str(descricao)[:index2 + 35]

    if (str(descricao).__contains__('<div id="inline-') == True):
        index3 = str(descricao).index('<div id="inline-')
        descricao = str(descricao)[:index3]

    if (int(resp[0]['status']) < 400):
        img = '<p><img alt="Image" class="img-responsive" src="url" style="box-sizing: border-box; border: 0px; vertical-align: middle; display: block; max-width: 100%; height: auto; color: rgb(41, 45, 48); font-family: &quot;Roboto Condensed&quot;, sans-serif; font-size: 12px; text-align: -webkit-center; background-color: rgb(238, 238, 238);" /></p>'.replace(
                'url', url)
        descricao = descricao + img
    '''
    nome_produto = Organizar_Texto(str(element5.get_attribute('innerHTML')).strip(), palavras_excecao)
    marca_produto = Organizar_Texto(str(nomefabri).strip(), "")
    partnumber_produto = str(partnumber).strip()
    '''

    nome_produto = str(element5.get_attribute('innerHTML')).strip()
    if(nome_produto.__contains__('&') == True):
        nome_produto = nome_produto.replace(nome_produto[nome_produto.index('&'):nome_produto.index(' ', nome_produto.index('&'))], '').strip()

    nome_produto = nome_produto.replace('  ', ' ')
            
    marca_produto = str(nomefabri).strip()
    partnumber_produto = str(partnumber).strip()

    #print(partnumber_produto)
    if Checar_Se_Produto_Existe(str(partnumber_produto)) == False:
        Adicionar_Produto(nome_produto, "0", "0.00", "0.00", descricao, categorias_produto, codigo_produto, marca_produto, partnumber_produto)
                
def Checar_Se_Produto_Existe(sku_partnumber):
   token_url = "https://www.nuvemshop.com.br/apps/authorize/token"
            
   client_id = '3516'
   client_secret = '70ngJHVEXROFfJnYkl0rYPJCrHastsjDf5qP9HYYb2onpXtq'

   access_token = '414fe30b65b85dc3ab419370f1e364f74879230d'
   user_id = '1827299'

   api_call_headers = {
      'Authentication': 'bearer ' + access_token,
      'Content-Type': 'application/json',
      'User-Agent': 'AdcProdutos (geovanibarbosa@live.com)'
   }
    
   test_api_url = "https://api.nuvemshop.com.br/v1/1827299/products/?q={sku}".replace('{sku}', str(sku_partnumber).strip())
   api_call_response = requests.get(test_api_url, headers=api_call_headers)
   
   if api_call_response.status_code == 200:
      vet = json.loads(api_call_response.text)
      for i in range(len(vet)):
         if str(sku_partnumber).strip() == vet[i]['variants'][0]['sku']:
            return True
            break
         elif i == len(vet) -1: 
            return False            
   else: 
      return False

def Checar_Se_Produto_Existe2(sku_partnumber):
    token_url = "https://www.nuvemshop.com.br/apps/authorize/token"
            
    client_id = '3516'
    client_secret = '70ngJHVEXROFfJnYkl0rYPJCrHastsjDf5qP9HYYb2onpXtq'

    access_token = '414fe30b65b85dc3ab419370f1e364f74879230d'
    user_id = '1827299'

    api_call_headers = {
    'Authentication': 'bearer ' + access_token,
    'Content-Type': 'application/json',
    'User-Agent': 'AdcProdutos (geovanibarbosa@live.com)'
    }
    
    test_api_url = "https://api.nuvemshop.com.br/v1/1827299/products/sku/{sku}".replace('{sku}', str(sku_partnumber).strip())
    api_call_response = requests.get(test_api_url, headers=api_call_headers)
    vet = json.loads(api_call_response.text)

    try:
        if vet['code'] == 404:
            return False
    except: 
        return True

def Checar_Se_Produto_Existe3(nome_produto):
    token_url = "https://www.nuvemshop.com.br/apps/authorize/token"
            
    client_id = '3516'
    client_secret = '70ngJHVEXROFfJnYkl0rYPJCrHastsjDf5qP9HYYb2onpXtq'

    access_token = '414fe30b65b85dc3ab419370f1e364f74879230d'
    user_id = '1827299'

    api_call_headers = {
    'Authentication': 'bearer ' + access_token,
    'Content-Type': 'application/json',
    'User-Agent': 'AdcProdutos (geovanibarbosa@live.com)'
    }

    vet_nomes_produtos = []
    for i in range(1, 10):
        test_api_url = "https://api.nuvemshop.com.br/v1/1827299/products?page={i}&per_page=200".replace('{i}', str(i))
        api_call_response = requests.get(test_api_url, headers=api_call_headers)
        vet = json.loads(api_call_response.text)
        for j in range(len(vet)):
            vet_nomes_produtos.append(vet[j]['name']['pt'])

    nomeproduto_correspondente = difflib.get_close_matches(str(nome_produto).strip(), vet_nomes_produtos)
    if (len(nomeproduto_correspondente) > 0 and vet_nomes_produtos.__contains__(str(nomeproduto_correspondente[0]).strip()) == True):
        return True
    else: 
        return False

def Atualizar_Estoque_Preço():
    texto = str(browser.find_element_by_xpath('/html/body/div[2]/section[1]/div/div').text)
    qnt = int(texto.count("Código:"))
    print(texto)

def Adicionar_Produto(produto, stock, prom_preco, preco, descricao, categorias, codigo, marca, partnumber):
    a = 1
    while (a == 1):
        try:                        
            vet_categorias = categorias.split(',')
            ids_categorias = []

            token_url = "https://www.nuvemshop.com.br/apps/authorize/token"
            test_api_url = "https://api.nuvemshop.com.br/v1/1827299/products"
            test_api_url2 = "https://api.nuvemshop.com.br/v1/1827299/categories?page=1&per_page=200"

            client_id = '3516'
            client_secret = '70ngJHVEXROFfJnYkl0rYPJCrHastsjDf5qP9HYYb2onpXtq'

            access_token = '414fe30b65b85dc3ab419370f1e364f74879230d'
            user_id = '1827299'

            api_call_headers = {
            'Authentication': 'bearer ' + access_token,
            'Content-Type': 'application/json',
            'User-Agent': 'AdcProdutos (geovanibarbosa@live.com)'
            }

            api_call_response2 = requests.get(test_api_url2, headers=api_call_headers)
            vet = json.loads(api_call_response2.text)
                
            for i in range(len(vet)):
                if (vet_categorias.__contains__(vet[i]['handle']['pt'])):
                    ids_categorias.append(vet[i]['id'])

                
            list_images = []
            position = 1
            for t in range(1, 5):
                url = "https://www.pauta.com.br/img/" + codigo + "/1.png".replace("1", str(t))
                request_response = requests.head(url)
                status_code = request_response.status_code
                if (status_code == 200):
                    list_images.append(
                        dict({
                            "src": str(url), 
                            "position": int(position)
                            })
                    )
                position+=1

            Peso = 0.0
            Altura = 0.0
            Profundidade = 0.0
            Largura = 0.0
            EAN = 10

            try:    
                APL = str(descricao).index('"ng-binding">', str(descricao).index("Dimensão da Embalagem (A / P / L)"))
                string_APL = str(descricao)[APL + 13:str(descricao).index('</span', APL)]
                string_APL = str(string_APL).replace('.0mm', '').replace('/', '')
                
                time.sleep(2)
                Peso = str(descricao).index('"ng-binding">', str(descricao).index("Peso do produto com embalagem"))
                string_Peso = str(descricao)[Peso + 13:str(descricao).index('</span', Peso)]
                string_Peso = str(string_Peso).replace('Kg', '').strip()

                time.sleep(2)
                Peso = float(str(string_Peso).replace('Kg', '').strip()) * 1.0
                Altura = float(str(string_APL.split('  ')[0]).replace('mm', '').strip())/10.0
                Profundidade = float(str(string_APL.split('  ')[1]).replace('mm', '').strip())/10.0
                Largura = float(str(string_APL.split('  ')[2]).replace('mm', '').strip())/10.0
            except:
                Peso = 0.0
                Altura = 0.0
                Profundidade = 0.0
                Largura = 0.0
                #print(traceback.print_exc())
                
            time.sleep(2)
            try:
                index_texto = str(descricao).index('"ng-binding">', str(descricao).index("EAN"))
                string_EAN = str(descricao)[index_texto + 13:str(descricao).index('</span', index_texto)]
                EAN = int(string_EAN)
            except:
                EAN = 10
                #print(traceback.print_exc())

            api_call_payload = json.dumps(
            {
            "images": list_images,
            "categories": ids_categorias,
            "name": {
            "pt": produto
            },
            "description": {
                "pt": descricao
            },
            "variants": [
                {
                    "promotional_price": prom_preco,
                    "price": preco,
                    "weight": str(Peso),
                    "height": str(Altura),
                    "depth": str(Profundidade),
                    "width": str(Largura),
                    "stock_management": True,
                    "stock": int(stock),
                    "brand": marca,
                    "sku": partnumber,
                    "barcode": EAN
                }
            ]})
            
            api_call_response = requests.post(test_api_url, data=api_call_payload, headers=api_call_headers)
            if(str(api_call_response == "<Response [201]>")):
                print("Código: " + codigo + ", Nome: " + produto + ", Stock: " + stock + ", Categorias: " + categorias)            
            a = 0
        except:
            a = 1
            print(traceback.print_exc())

def buscar_subcategoria_correspondente(nome_subcategoria_aproximada):
    a = 1
    while (a == 1):
        try:
            test_api_url = "https://api.nuvemshop.com.br/v1/1827299/categories?fields=name,id,handle,subcategories&page=1&per_page=200"

            client_id = '3516'
            client_secret = '70ngJHVEXROFfJnYkl0rYPJCrHastsjDf5qP9HYYb2onpXtq'

            access_token = '414fe30b65b85dc3ab419370f1e364f74879230d'
            user_id = '1827299'

            api_call_headers = {
            'Authentication': 'bearer ' + access_token,
            'Content-Type': 'application/json',
            'User-Agent': 'AdcProdutos (geovanibarbosa@live.com)'
            }
            
            api_call_response = requests.get(test_api_url, headers=api_call_headers)

            vet_name_subcategorias = []
            vet_handle_subcategorias = []
            vet = json.loads(api_call_response.text)

            for i in range(len(vet)):
                vet_name_subcategorias.append(vet[i]['name']['pt'])
                vet_handle_subcategorias.append(vet[i]['handle']['pt'])
                
            subcategoria_correspondente = difflib.get_close_matches(str(nome_subcategoria_aproximada), vet_name_subcategorias)
            if (len(subcategoria_correspondente) > 0):
                a = 0
                return vet_handle_subcategorias[vet_name_subcategorias.index(str(subcategoria_correspondente[0]))]
                #return subcategoria_correspondente[0]
            else:
                return ""
        except:
            a = 1
            print(traceback.print_exc())
            
def func_main(codigos_produto, categorias_produto):

    #endereco_categoria = input("Digite o link da categoria: ")
    #palavras_excecao = input("Digite as palavras de exceção da categoria: ")
    #codigos_produto = input("Digite os códigos dos produtos: ")
    #categorias_produto = input("Digite todas as categorias: ")
    #print("\n")

    #links_produtos = codigos_produto.split(',')
    #links_produtos = []
    #links_produtos = codigos_produto
            
    '''
    browser.get(endereco_categoria)
                    
    time.sleep(50)
    element0 = browser.find_element_by_xpath('//*[@id="sec-produtos"]/div/div/div[2]/div[2]')
    texto_produtos = str(element0.get_attribute('innerHTML'))
    index_links_produtos = [m.start() for m in re.finditer('/produto/', texto_produtos)]
                    
    for i in range(len(index_links_produtos)):
        if (links_produtos.__contains__("https://pauta.com.br" + texto_produtos[index_links_produtos[i]:texto_produtos.index('"', index_links_produtos[i])]) == False): 
            links_produtos.append("https://pauta.com.br" + texto_produtos[index_links_produtos[i]:texto_produtos.index('"', index_links_produtos[i])])
    '''
    for j in range(len(codigos_produto)):    
        browser.get("https://pauta.com.br/produto/" + str(codigos_produto[j]).replace("'", "").replace('"', ''))
        #time.sleep(50)
        Selecionar_Produto("https://pauta.com.br/produto/" + str(codigos_produto[j]).replace("'", "").replace('"', ''), str(categorias_produto), "")

  
def func_main2(categoria_master):

    #endereco_categoria = input("Digite o link da categoria: ")
    #palavras_excecao = input("Digite as palavras de exceção da categoria: ")

    vet_codigo_produtos = []

    links_informatica = ["https://pauta.com.br/pesquisamenu/Software_OEM", "https://pauta.com.br/pesquisamenu/Software_Seguran%C3%A7a%20Digital", "https://pauta.com.br/pesquisamenu/Software_ESD", "https://pauta.com.br/pesquisamenu/Software_FPP", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_Acess%C3%B3rios%20para%20Notebook", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_Notebook", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_Servidor", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_All%20in%20One", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_Mini%20PC", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_Tablet", "https://pauta.com.br/pesquisamenu/Computa%C3%A7%C3%A3o_Computador", "https://pauta.com.br/pesquisamenu/Impress%C3%A3o_Impressora", "https://pauta.com.br/pesquisamenu/Impress%C3%A3o_Impress%C3%A3o%203D", "https://pauta.com.br/pesquisamenu/Impress%C3%A3o_Multifuncional","https://pauta.com.br/pesquisamenu/Energia_Estabilizador", "https://pauta.com.br/pesquisamenu/Energia_No-Break", "https://pauta.com.br/pesquisamenu/Energia_Acess%C3%B3rios%20de%20energia", "https://pauta.com.br/pesquisamenu/Energia_Protetor", "https://pauta.com.br/pesquisamenu/Energia_Filtro%20de%20Linha", "https://pauta.com.br/pesquisamenu/Imagem_Scanner", "https://pauta.com.br/pesquisamenu/Imagem_Monitor", "https://pauta.com.br/pesquisamenu/Imagem_Televisor", "https://pauta.com.br/pesquisamenu/Imagem_Projetor", "https://pauta.com.br/pesquisamenu/Conectividade_Roteador", "https://pauta.com.br/pesquisamenu/Conectividade_Switch", "https://pauta.com.br/pesquisamenu/Conectividade_Placa%20de%20Rede", "https://pauta.com.br/pesquisamenu/Conectividade_Repetidores", "https://pauta.com.br/pesquisamenu/Conectividade_Modem%20ADSL", "https://pauta.com.br/pesquisamenu/Conectividade_Conversor", "https://pauta.com.br/pesquisamenu/Conectividade_Rede%20Wireless", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Caixa%20de%20Som", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Cabo", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Mouse%20Pad", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Acess%C3%B3rios%20para%20Notebook", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Leitor%20Biom%C3%A9trico", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Webcam", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Fonte%20de%20Alimenta%C3%A7%C3%A3o", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Fone%20de%20Ouvido%20e%20Headset", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Controle%20para%20Jogos", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Mouse", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Teclado", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Kit%20Teclado%20e%20Mouse", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Cooler", "https://pauta.com.br/pesquisamenu/Acess%C3%B3rios_Cadeira", "https://pauta.com.br/pesquisamenu/Componentes_SSD", "https://pauta.com.br/pesquisamenu/Componentes_Fonte%20de%20Alimenta%C3%A7%C3%A3o", "https://pauta.com.br/pesquisamenu/Componentes_DVD-RW", "https://pauta.com.br/pesquisamenu/Componentes_Mem%C3%B3ria", "https://pauta.com.br/pesquisamenu/Componentes_Placa%20m%C3%A3e", "https://pauta.com.br/pesquisamenu/Componentes_HD%20para%20Notebook", "https://pauta.com.br/pesquisamenu/Componentes_HD", "https://pauta.com.br/pesquisamenu/Componentes_HD%20Externo", "https://pauta.com.br/pesquisamenu/Componentes_Processador", "https://pauta.com.br/pesquisamenu/Componentes_Placa%20de%20V%C3%ADdeo", "https://pauta.com.br/pesquisamenu/Componentes_Gabinete", "https://pauta.com.br/pesquisamenu/Armazenamento_Cart%C3%A3o%20de%20Mem%C3%B3ria", "https://pauta.com.br/pesquisamenu/Armazenamento_HD%20Externo", "https://pauta.com.br/pesquisamenu/Armazenamento_HD%20para%20Servidor", "https://pauta.com.br/pesquisamenu/Armazenamento_Pen%20Drive", "https://pauta.com.br/pesquisamenu/Armazenamento_SSD", "https://pauta.com.br/pesquisamenu/Armazenamento_Storage", "https://pauta.com.br/pesquisamenu/Suprimentos_Acess%C3%B3rios%20para%20Suprimentos", "https://pauta.com.br/pesquisamenu/Suprimentos_Bast%C3%A3o%20de%20Cera", "https://pauta.com.br/pesquisamenu/Suprimentos_Toners", "https://pauta.com.br/pesquisamenu/Suprimentos_Kits", "https://pauta.com.br/pesquisamenu/Suprimentos_Garrafas", "https://pauta.com.br/pesquisamenu/Suprimentos_Revelador", "https://pauta.com.br/pesquisamenu/Suprimentos_Fitas", "https://pauta.com.br/pesquisamenu/Suprimentos_Cilindro", "https://pauta.com.br/pesquisamenu/Suprimentos_Unidade%20de%20Imagem", "https://pauta.com.br/pesquisamenu/Suprimentos_Fotorreceptor", "https://pauta.com.br/pesquisamenu/Suprimentos_Cartucho", "https://pauta.com.br/pesquisamenu/Digitaliza%C3%A7%C3%A3o_Mesa%20Digitalizadora"]
    links_seguranca = ["https://pauta.com.br/pesquisamenu/CFTV_DVR", "https://pauta.com.br/pesquisamenu/CFTV_Câmera%20HD", "https://pauta.com.br/pesquisamenu/CFTV_NVR", "https://pauta.com.br/pesquisamenu/CFTV_Câmera%20IP", "https://pauta.com.br/pesquisamenu/Termografia", "https://pauta.com.br/pesquisamenu/Automatizador", "https://pauta.com.br/pesquisamenu/Controle%20de%20Acesso_Controladora", "https://pauta.com.br/pesquisamenu/Controle%20de%20Acesso_Leitor%20Biom%C3%A9trico", "https://pauta.com.br/pesquisamenu/Controle%20de%20Acesso_Leitor%20Facial", "https://pauta.com.br/pesquisamenu/Controle%20de%20Acesso_Leitor%20Escravo", "https://pauta.com.br/pesquisamenu/Controle%20de%20Acesso_Botoeira", "https://pauta.com.br/pesquisamenu/Controle%20de%20Acesso_Tags%20e%20Cartões", "https://pauta.com.br/pesquisamenu/Interfonia_Central%20de%20Condom%C3%ADnio", "https://pauta.com.br/pesquisamenu/Interfonia_Porteiro%20IP", "https://pauta.com.br/pesquisamenu/Interfonia_Interfone%20residencial", "https://pauta.com.br/pesquisamenu/Interfonia_Cabo%20para%20Interfone", "https://pauta.com.br/pesquisamenu/Interfonia_Acess%C3%B3rios%20para%20Interfonia", "https://pauta.com.br/pesquisamenu/Fechadura_Fechadura", "https://pauta.com.br/pesquisamenu/Fechadura_Fechadura%20Digital", "https://pauta.com.br/pesquisamenu/Fechadura_Fechadura%20Eletromagn%C3%A9tica", "https://pauta.com.br/pesquisamenu/Fechadura_Fechadura%20Solenoide", "https://pauta.com.br/pesquisamenu/Fechadura_Fechadura%20El%C3%A9trica%20(Porta%20de%20Vidro)", "https://pauta.com.br/pesquisamenu/Fechadura_Fechadura%20Mecânica", "https://pauta.com.br/pesquisamenu/Fechadura_Acess%C3%B3rios%20para%20Fechadura", "https://pauta.com.br/pesquisamenu/Ilumina%C3%A7%C3%A3o", "https://pauta.com.br/pesquisamenu/Alarme_Central%20de%20Alarme", "https://pauta.com.br/pesquisamenu/Alarme_Sensor", "https://pauta.com.br/pesquisamenu/Alarme_Sirene", "https://pauta.com.br/pesquisamenu/Alarme_Controle%20Remoto", "https://pauta.com.br/pesquisamenu/Alarme_Bateria%20de%20Alarme", "https://pauta.com.br/pesquisamenu/Alarme_Cabo%20para%20Alarme", "https://pauta.com.br/pesquisamenu/Alarme_Acess%C3%B3rios%20para%20Alarme", "https://pauta.com.br/pesquisamenu/Prote%C3%A7%C3%A3o%20Perimetral_Central%20de%20Choque", "https://pauta.com.br/pesquisamenu/Prote%C3%A7%C3%A3o%20Perimetral_Haste%20de%20Cerca", "https://pauta.com.br/pesquisamenu/Prote%C3%A7%C3%A3o%20Perimetral_Cabo%20de%20Alta%20Isola%C3%A7%C3%A3o", "https://pauta.com.br/pesquisamenu/Prote%C3%A7%C3%A3o%20Perimetral_Sensor", "https://pauta.com.br/pesquisamenu/Prote%C3%A7%C3%A3o%20Perimetral_Fio%20de%20Arame", "https://pauta.com.br/pesquisamenu/Prote%C3%A7%C3%A3o%20Perimetral_Acess%C3%B3rios%20para%20Prote%C3%A7%C3%A3o%20Perimetral", "https://pauta.com.br/pesquisamenutelecom/Fechadura_Fechadura%20Digital"]
    links_telecom = ["https://pauta.com.br/pesquisamenutelecom/ONU", "https://pauta.com.br/pesquisamenutelecom/Conectividade_Roteador", "https://pauta.com.br/pesquisamenutelecom/Conectividade_Switch", "https://pauta.com.br/pesquisamenutelecom/Conectividade_Rack%20Servidor"]
    
    links = links_informatica

    for i in range(len(links)): 
        a = 1
        while (a == 1): 
            try:
                request_response = requests.head(str(links[i]))
                status_code = request_response.status_code
                if (status_code == 200):
                    browser.get(str(links[i]))
                    
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[1]/div/div')))
                    texto = str(browser.find_element_by_xpath('/html/body/div[2]/section[1]/div/div').text)
                    #texto = str(browser.find_element_by_xpath('//*[@id="sec-produtos"]/div/div/div[2]/div[2]/div[1]/div/div/produto-box/div/div[4]/p').text)
                    qnt = int(texto.count("Código:"))
                    barra_de_dados = ""
                    cod_produto = ""
                    index_Código = 0
                    index_Maisdetalhes = 0
                            
                    for j in range(qnt):
                        index_Código = texto.index("Código:", index_Código)
                        index_Maisdetalhes = texto.index("Mais detalhes", index_Maisdetalhes)
                        barra_de_dados = str(texto[index_Código:index_Maisdetalhes]).strip()
                        cod_produto = str(barra_de_dados)[str(barra_de_dados).index('Código:') +7:str(barra_de_dados).index('Marca:')].strip()
                        vet_codigo_produtos.append(cod_produto)
            
                        index_Código +=7
                        index_Maisdetalhes +=13

                    vet_caracters = ['%C3%A7;ç', '%20; ', '%C3%A3;ã', '%C3%B3;ó', '%C3%A9;é', '%C3%AD;í', '%C3%B4;ô']
                    url = str(browser.current_url).replace(str(vet_caracters[0]).split(';')[0], str(vet_caracters[0]).split(';')[1]) \
                                                .replace(str(vet_caracters[1]).split(';')[0], str(vet_caracters[0]).split(';')[1]) \
                                                .replace(str(vet_caracters[2]).split(';')[0], str(vet_caracters[0]).split(';')[1]) \
                                                .replace(str(vet_caracters[3]).split(';')[0], str(vet_caracters[0]).split(';')[1]) \
                                                .replace(str(vet_caracters[4]).split(';')[0], str(vet_caracters[0]).split(';')[1]) \
                                                .replace(str(vet_caracters[5]).split(';')[0], str(vet_caracters[0]).split(';')[1]) \
                                                .replace(str(vet_caracters[6]).split(';')[0], str(vet_caracters[0]).split(';')[1])

                    texto_categoria_subcategoria_produto = str(url).replace('https://pauta.com.br/pesquisamenu/','').replace('https://pauta.com.br/pesquisamenutelecom/','').strip()
                                    
                    if (len(str(texto_categoria_subcategoria_produto).split('_')) > 1 and str(texto_categoria_subcategoria_produto).__contains__('_') == True):
                        categoria_produto = str(texto_categoria_subcategoria_produto).split('_')[0]
                        sub_categoria_produto = str(texto_categoria_subcategoria_produto).split('_')[1]
                    elif (browser.current_url == "https://pauta.com.br/pesquisamenutelecom/Mesa%20Digitalizadora"):
                        categoria_produto_correspondente = "digitalizacao"
                        sub_categoria_produto_correspondente = "mesa-digitalizadora"
                    elif (browser.current_url == "https://pauta.com.br/pesquisamenutelecom/ONU"):
                        categoria_produto_correspondente = "materiais"
                        sub_categoria_produto_correspondente = "onu"
                    elif (browser.current_url == "https://pauta.com.br/pesquisamenuseg/Fechadura_Fechadura%20Digital"):
                        categoria_produto_correspondente = "fechadura"
                        sub_categoria_produto_correspondente = "fechadura-digital"

                    if(len(vet_codigo_produtos) > 0):
                        time.sleep(5)
                        if (browser.current_url != "https://pauta.com.br/pesquisamenu/Energia_No-Break" and browser.current_url != "https://pauta.com.br/pesquisamenutelecom/CFTV_Nobreak" and browser.current_url != "https://pauta.com.br/pesquisamenutelecom/No-Break"):
                            categoria_produto_correspondente = str(buscar_subcategoria_correspondente(categoria_produto))
                            sub_categoria_produto_correspondente = str(buscar_subcategoria_correspondente(sub_categoria_produto))
                        elif (browser.current_url == "https://pauta.com.br/pesquisamenu/Energia_No-Break"): 
                            categoria_produto_correspondente = "energia"
                            sub_categoria_produto_correspondente = "no-break"
                        elif (browser.current_url == "https://pauta.com.br/pesquisamenutelecom/CFTV_Nobreak"): 
                            categoria_produto_correspondente = "cftv"
                            sub_categoria_produto_correspondente = "nobreak"
                        elif (browser.current_url == "https://pauta.com.br/pesquisamenutelecom/No-Break"): 
                            categoria_produto_correspondente = "conectividade"
                            sub_categoria_produto_correspondente = "nobreak1"
                                                 
                                                 
                        if (str(categoria_produto_correspondente).strip() != "" and str(sub_categoria_produto_correspondente).strip() != ""):
                            func_main(vet_codigo_produtos, str(categoria_master) + "," + str(categoria_produto_correspondente).strip() + "," + str(sub_categoria_produto_correspondente).strip())
                        vet_codigo_produtos.clear()
                a = 0        
            except: 
                a = 1
                print(traceback.print_exc())         


# Press the green button in the gutter to run the script.
if __name__ == '__main__': 
    func_main2("informatica")