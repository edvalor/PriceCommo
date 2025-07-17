import re
import requests
from datetime import date
from flask_cors import CORS
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template





#.......................................................................................................................................................
#.......................................................................................................................................................





app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

def extrair_price(texto):
    match = re.search(r'R\$[\s]*[\d.,]+', texto)
    return match.group(0).strip() if match else "N/A"

def limpar_texto(texto):
    texto = re.sub(r'\b(soja|milho|MILHO|SOJA)\b', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'[-\:\s\u200b]+', '', texto)  
    texto = texto.encode('utf-8').decode('utf-8') 
    return texto.strip()





#.......................................................................................................................................................
#.......................................................................................................................................................





def cotacao_agricolagemelli(): # DOIS SOUP
    url = 'https://agricolagemelli.com/historico-precos'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Agricolagemelli. {str(e)}", "url": url}
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('tr', class_='jet-dynamic-table__row')
        if len(price) > 1:
           dados = price[1].find_all('td')
           if len(dados) >= 3:
               soja = dados[1].get_text(strip=True) if price[1] else "N/A"
               milho = dados[2].get_text(strip=True) if price[2] else "N/A"
           else:
                soja = milho = "Valor não encotrado"
        else:
           soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Soja": soja,
           "Milho": milho,
           "url": url,
           "Fonte": "Agricolagemelli",
           "estado": "Paraná",
          "cidade": "Cascavel"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Agricolagemelli: {str(e)}", "url": url}


def cotacao_camposverdes():
    url = 'https://www.camposverdes.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Campos Verdes: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='col-xs-3 col-sm-6 col-md-5 col-lg-4')
        if len(price) >= 3:
            soja = price[0].get_text(strip=True) if price[0] else "N/A"
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Campos Verdes",
            "estado": "Rio Grande do Sul",
            "cidade": "Maringá"

        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Campos Verdes: {str(e)}", "url": url}
    

def cotacao_capaznet():
    url = 'https://www.capaznet.com/portal/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Capaznet: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('p')
        if len(price) >= 10:
            soja = price[1].get_text(strip=True) if price[1] else "N/A"
            milho = price[2].get_text(strip=True) if price[2] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Capaznet",
            "estado": "Rio Grande do Sul",
            "cidade": "Não-me-Toque"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Capaznet: {str(e)}", "url": url}


def cotacao_cepalcereais():
    url = 'https://www.cepalcereais.com.br/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cepalcereais. {str(e)}", "url": url}
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        data_hoje = date.today()
        data_hoje_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('p', style='text-shadow:#000 1px -1px, #000 -1px 1px, #000 1px 1px, #000 -1px -1px;')
        if len(price) >= 3:
            milho = limpar_texto(price[2].get_text(strip=True)) if price[2] else "N/A"
            soja = limpar_texto(price[0].get_text(strip=True)) if price[0] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_hoje_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Cepalcereais",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cepalcereais. {str(e)}", "url": url}


def cotacao_coagril():
    url = 'https://www.coagril-rs.com.br/cotacoes'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Coagril. {str(e)}", "url": url}
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        data_hoje = date.today()
        data_hoje_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('td', class_='alignright')
        if len(price) >= 3:
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
            soja = price[3].get_text(strip=True) if price[3] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_hoje_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Coagril",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Não foi possível acessar os dados da Coagril. {str(e)}", "url": url}


def cotacao_coopeagri():
    url = 'https://www.coopeagri.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Coopeagri. {str(e)}", "url": url}
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        data_hoje = date.today()
        data_hoje_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('span', style='font-size:18px;')
        if len(price) >= 3:
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
            soja = price[0].get_text(strip=True).replace("c/ DAP", "").strip() if price[0] else "N/A"
        else:
            soja = milho = "---"
        return {
            "Data": data_hoje_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Coopeagri",
            "estado": "Rio Grande do Sul",
            "cidade": "Não-me-Toque"
        }
    except Exception as e:
        return {"ERRO": f"Não foi possível acessar os dados da Coopeagri. {str(e)}", "url": url}


def cotacao_cotacoesmercado():
    url = 'https://www.cotacoesemercado.com/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cotações & Mercado: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('p', class_='font_8 wixui-rich-text__text')
        if len(price) >= 10:
            soja_balcao = extrair_price(price[1].get_text(strip=True)) if price[1] else "N/A"
            milho_balcao = extrair_price(price[2].get_text(strip=True)) if price[2] else "N/A"
            soja_disponivel = extrair_price(price[6].get_text(strip=True)) if price[6] else "N/A"
            milho_disponivel = extrair_price(price[7].get_text(strip=True)) if price[7] else "N/A"
        else:
            soja_balcao = milho_balcao = soja_disponivel = milho_disponivel = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Balcão": {
                "Soja": soja_balcao,
                "Milho": milho_balcao
            },
            "Disponível": {
                "Soja": soja_disponivel,
                "Milho": milho_disponivel
            },
            "url": url,
            "Fonte": "Cotacoesemercado",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cotações & Mercado: {str(e)}", "url": url}


def cotacao_cotriba():
    url = 'https://cotriba.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Não foi possível acessar os dados da Cotriba: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='content--value')
        if len(price) >= 3:
            milho = price[0].get_text(strip=True) if price[0] else "N/A"
            soja = price[1].get_text(strip=True) if price[1] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Cotriba",
            "estado": "Rio Grande do Sul",
            "cidade": "Não-me-Toque"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cotriba: {str(e)}", "url": url}


def cotacao_cotrijal():
    url = 'https://www.cotrijal.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Não foi possível acessar os dados da Cotrijal: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', style='line-height: 45px;')
        if len(price) >= 3:
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
            soja = price[0].get_text(strip=True) if price[0] else "N/A"
        else:
            soja = milho = "Mercado está fechado."
        return {
            "Data": data_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Cotrijal",
            "estado": "Rio Grande do Sul",
            "cidade": "Não-me-Toque"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cotrijal: {str(e)}", "url": url}


def cotacao_cotrirosa(): # ESSE TEM PREÇO PROXIMO, NÃO REAL
    url = 'https://cotrirosa.com/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestsException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cotrirosa: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='content--value')
        if len(price) >= 3:
            soja = price[1].get_text(strip=True) if price[1] else "N/A"
            milho = price[0].get_text(strip=True) if price[0] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Cotrirosa",
            "estado": "Rio Grande do Sul",
            "cidade": "Santa Rosa"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cotrirosa: {str(e)}", "url": url}
    

def cotacao_cotriel():
    url = 'https://www.cotriel.com.br/Home'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Não foi possível acessar os dados da Cotriba: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='well')
        if len(price) > 1:
            dados = price[1].find_all('p')
            if len(dados) >= 10:
                milho = dados[6].get_text(strip=True) if dados[6] else "N/A"
                soja = dados[4].get_text(strip=True) if dados[4] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Soja": soja,
            "Milho": milho,
            "url": url,
            "Fonte": "Cotriel",
            "estado": "Rio Grande do Sul",
            "cidade": "Não-me-Toque"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cotriba: {str(e)}", "url": url}


def cotacao_cotrisal():
    url = 'https://www.cotrisal.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Não foi possível acessar os dados da Cotrisal: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('p', class_='preco_cotacao')
        if len(price) >= 6:
            norte_soja = price[0].get_text(strip=True) if price[0] else "N/A"
            norte_milho = price[1].get_text(strip=True) if price[1] else "N/A"
            noroeste_soja = price[3].get_text(strip=True) if price[3] else "N/A"
            noroeste_milho = price[4].get_text(strip=True) if price[4] else "N/A"
        else:
            norte_soja = norte_milho = "Mercado está fechado"
            noroeste_soja = noroeste_milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Regiao Norte": {
                "Soja": norte_soja,
                "Milho": norte_milho,
            },
            "Regiao Noroeste": {
                "Soja": noroeste_soja,
                "Milho": noroeste_milho,
            },
            "url": url,
            "Fonte": "Cotrisal",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cotrisal: {str(e)}", "url": url}


def cotacao_cotrisoja():
    url = 'https://cotrisoja.com.br'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestsException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cotrisoja: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='item--value')
        if len(price) >= 3:
            soja = price[0].get_text(strip=True) if price[0] else "N/A"
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Cotrisoja",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cotrisoja: {str(e)}", "url": url}


def cotacao_grupopoletto():
    url = 'http://www.grupopoletto.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Grupo Poletto: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='col-xs-4')
        if len(price) >= 10:
            soja = price[4].get_text(strip=True) if price[4] else "N/A"
            milho = price[8].get_text(strip=True) if price[8] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Grupopoletto",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Não foi possível acessar os dados da Grupo Poletto: {str(e)}", "url": url}


def cotacao_plantarnet():
    url = 'https://www.plantarnet.com.br/agricola/cotacoes'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da PlantarNet: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('b')
        if len(price) >= 8:
            soja = limpar_texto(price[4].get_text(strip=True)) if price[4] else "N/A"
            milho = limpar_texto(price[5].get_text(strip=True)) if price[5] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Plantarnet",
            "estado": "Paraná",
            "cidade": "Cascavel"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da PlantarNet: {str(e)}", "url": url}
    

def cotacao_sebben():
    url = 'https://sebben.ind.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Sebben: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('span', class_='elementor-icon-list-text')
        if len(price) >= 8:
            soja = extrair_price(price[0].get_text(strip=True)).replace('-------------------------------------', '').strip() if price[0] else "N/A"
            milho = extrair_price(price[2].get_text(strip=True)).replace('-------------------------------------', '').strip() if price[2] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Sebben",
            "estado": "Rio Grande do Sul",
            "cidade": "Passo Fundo"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Sebben: {str(e)}", "url": url}



def cotacao_cooperoque():
    url = 'https://www.cooperoque.com.br/?pg=cotacoes'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Cooperoque: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='el_3')
        if len(price) >= 3:
            soja = price[0].get_text(strip=True) if price[0] else "N/A"
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Cooperoque",
            "estado": "Rio Grande do Sul",
            "cidade": "Ijuí"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Cooperoque: {str(e)}", "url": url}


def cotacao_lazarotto():
    url = 'https://www.lazarotto.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Lazarotto: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('span', class_='exchange-price')
        if len(price) >= 3:
            soja = price[0].get_text(strip=True) if price[0] else "N/A"
            milho = price[2].get_text(strip=True) if price[2] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Lazarotto",
            "estado": "Rio Grande do Sul",
            "cidade": "Ijuí"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Lazarotto: {str(e)}", "url": url}


def cotacao_grupouggeri():
    url = 'https://grupouggeri.com.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Grupouggeri: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='col-md-12 tcota')
        if len(price) >= 3:
            soja = price[0].get_text(strip=True) if price[1] else "N/A"
            milho = price[1].get_text(strip=True) if price[1] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Grupouggeri",
            "estado": "Rio Grande do Sul",
            "cidade": "Ijuí"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Grupouggeri: {str(e)}", "url": url}


def cotacao_vieraagrocereais():
    url = 'https://www.vieraagrocereais.com.br/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Vieraagrocereais: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('span', class_='cotvalor')
        if len(price) >= 3:
            soja = (price[0].get_text(strip=True)) if price[0] else "N/A"
            milho = (price[2].get_text(strip=True)) if price[2] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Vieraagrocereais",
            "estado": "Rio Grande do Sul",
            "cidade": "Ijuí"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Vieraagrocereais: {str(e)}", "url": url}


def cotacao_agropan():
    url = 'https://agropan.coop.br/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Agropan: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('div', class_='item--value')
        if len(price) >= 10:
            tarde_soja = limpar_texto(price[5].get_text(strip=True)) if price[5] else "N/A"
            tarde_milho = limpar_texto(price[2].get_text(strip=True)) if price[2] else "N/A"
            manha_soja = limpar_texto(price[1].get_text(strip=True)) if price[1] else "N/A"
            manha_milho = limpar_texto(price[6].get_text(strip=True)) if price[6] else "N/A"
        else:
            manha_soja = manha_milho = tarde_soja = tarde_milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Manhã" : {
                "Soja": manha_soja,
                "Milho": manha_milho
            },
            "Tarde" : {
                "Soja": tarde_soja,
                "Milho": tarde_milho
            },
            "Fonte": "Agropan",
            "url": url,
            "estado": "Rio Grande do Sul",
            "cidade": "Ijuí"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Agropan: {str(e)}", "url": url}


def cotacao_agriplanmga():
    url = 'http://www.agriplanmga.com.br/widgets/'
    try:
        response = requests.get(url, timeout=10 )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"ERRO": f"Não foi possível acessar os dados da Agriplanmga: {str(e)}", "url": url}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        data_hoje = date.today()
        data_ptBR = data_hoje.strftime("%d/%m/%Y")
        price = soup.find_all('span', class_='pull-left cotacaovalorsaca')
        if len(price) >= 3:
            milho = price[0].get_text(strip=True) if price[0] else "N/A"
            soja = price[1].get_text(strip=True) if price[1] else "N/A"
        else:
            soja = milho = "Mercado está fechado"
        return {
            "Data": data_ptBR,
            "Milho": milho,
            "Soja": soja,
            "url": url,
            "Fonte": "Agriplanmga",
            "estado": "Rio Grande do Sul",
            "cidade": "Maringá"
        }
    except Exception as e:
        return {"ERRO": f"Erro ao processar dados da Agriplanmga: {str(e)}", "url": url}





#.......................................................................................................................................................
#.......................................................................................................................................................





# Endpoints da API
@app.route('/')
def index():
    return render_template('HOME.html')

@app.route('/commodities')
def commodities():
    return render_template('COMMODITIES.html')

@app.route('/sites')
def sites():
    return render_template('INSIDE_SITES.html')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "API de Cotações Agrícolas",
        "endpoints": [

            # RIO GRANDE DO SUL
            #//////////////////////////////////////////////////////////////
            # PASSO FUNDO
            "/cotacao/cepalcereais", # RIO GRANDE DO SUL / Passo Fundo
            "/cotacao/coagril", # RIO GRANDE DO SUL / Passo Fundo
            "/cotacao/cotacoesmercado", # RIO GRANDE DO SUL / Passo Fundo
            "/cotacao/cotrisal", # RIO GRANDE DO SUL / Passo Fundo
            "/cotacao/cotrisoja", # RIO GRANDE DO SUL / Passo Fundo
            "/cotacao/grupopoletto", # RIO GRANDE DO SUL / Passo Fundo
            "/cotacao/sebben", # RIO GRANDE DO SUL / Passo Fundo
            # NÃO-ME-TOQUE
            "/cotacao/capaznet", # RIO GRANDE DO SUL / Não-me-Toque
            "/cotacao/cotriba", # RIO GRANDE DO SUL / Não-me-Toque
            "/cotacao/cotriel", # RIO GRANDE DO SUL / Não-me-Toque
            "/cotacao/cotrijal", # RIO GRANDE DO SUL / Não-me-Toque
            "/cotacao/coopeagri", # RIO GRANDE DO SUL / Não-me-Toque
            # SANTA ROSA
            "/cotacao/cotrirosa", # RIO GRANDE DO SUL / Santa Rosa
            # IJUÍ
            "/cotacao/cooperoque", # RIO GRANDE DO SUL / Ijuí
            "/cotacao/lazarotto", # RIO GRANDE DO SUL / Ijuí
            "/cotacao/grupouggeri", # RIO GRANDE DO SUL / Ijuí
            "/cotacao/vieraagrocereais", # RIO GRANDE DO SUL / Ijuí
            "/cotacao/agropan", # RIO GRANDE DO SUL / Ijuí
            #///////////////////////////////////////////////////////////////

            # PARANÁ
            #///////////////////////////////////////////////////////////////
            # CASCAVEL
            "/cotacao/agricolagemelli", # PARANÁ / Cascavel
            "/cotacao/plantarnet", # PARANÁ / Cascavel
            # MARINGÁ
            "/cotacao/agriplanmga", # PARANÁ / Maringá
            #///////////////////////////////////////////////////////////////

            # OUTROS
            "/cotacao/camposverdes",

            # COTAÇÕES DE OUTROS ESTADOS
            "/cotacao/rio_grande_do_sul",
            "/cotacao/parana",
            "/cotacao/rio_grande_do_sul/passo_fundo",
            "/cotacao/rio_grande_do_sul/nao_me_toque",
            "/cotacao/rio_grande_do_sul/santa_rosa",
            "/cotacao/rio_grande_do_sul/ijui",
            "/cotacao/parana/cascavel",
            "/cotacao/parana/maringa",
            "/cotacao/todas"
        ]
    })





#.......................................................................................................................................................
#.......................................................................................................................................................





@app.route('/cotacao/agricolagemelli', methods=['GET'])
def api_cotacao_agricolagemelli():
    resultado = cotacao_agricolagemelli()
    return jsonify(resultado)


@app.route('/cotacao/camposverdes', methods=['GET'])
def api_cotacao_camposverdes():
    resultado = cotacao_camposverdes()
    return jsonify(resultado)


@app.route('/cotacao/cepalcereais', methods=['GET'])
def api_cotacao_cepalcereais():
    resultado = cotacao_cepalcereais()
    return jsonify(resultado)


@app.route('/cotacao/capaznet', methods=['GET'])
def api_cotacao_capaznet():
    resultado = cotacao_capaznet()
    return jsonify(resultado)


@app.route('/cotacao/coagril', methods=['GET'])
def api_cotacao_coagril():
    resultado = cotacao_coagril()
    return jsonify(resultado)


@app.route('/cotacao/cotrijal', methods=['GET'])
def api_cotacao_cotrijal():
    resultado = cotacao_cotrijal()
    return jsonify(resultado)


@app.route('/cotacao/cotacoesmercado', methods=['GET'])
def api_cotacao_cotacoesmercado():
    resultado = cotacao_cotacoesmercado()
    return jsonify(resultado)


@app.route('/cotacao/cotriba', methods=['GET'])
def api_cotacao_cotriba():
    resultado = cotacao_cotriba()
    return jsonify(resultado)


@app.route('/cotacao/cotriel', methods=['GET'])
def api_cotacao_cotriel():
    resultado = cotacao_cotriel()
    return jsonify(resultado)


@app.route('/cotacao/cotrisal', methods=['GET'])
def api_cotacao_cotrisal():
    resultado = cotacao_cotrisal()
    return jsonify(resultado)


@app.route('/cotacao/cotrisoja', methods=['GET'])
def api_cotacao_cotrisoja():
    resultado = cotacao_cotrisoja()
    return jsonify(resultado)


@app.route('/cotacao/cotrirosa', methods=['GET'])
def api_cotacao_cotrirosa():
    resultado = cotacao_cotrirosa()
    return jsonify(resultado)


@app.route('/cotacao/coopeagri', methods=['GET'])
def api_cotacao_coopeagri():
    resultado = cotacao_coopeagri()
    return jsonify(resultado)


@app.route('/cotacao/grupopoletto', methods=['GET'])
def api_cotacao_grupopoletto():
    resultado = cotacao_grupopoletto()
    return jsonify(resultado)


@app.route('/cotacao/plantarnet', methods=['GET'])
def api_cotacao_plantarnet():
    resultado = cotacao_plantarnet()
    return jsonify(resultado)


@app.route('/cotacao/sebben', methods=['GET'])
def api_cotacao_sebben():
    resultado = cotacao_sebben()
    return jsonify(resultado)


@app.route('/cotacao/cooperoque', methods=['GET'])
def api_cotacao_cooperoque():
    resultado = cotacao_cooperoque()
    return jsonify(resultado)


@app.route('/cotacao/lazarotto', methods=['GET'])
def api_cotacao_lazarotto():
    resultado = cotacao_lazarotto()
    return jsonify(resultado)


@app.route('/cotacao/grupouggeri', methods=['GET'])
def api_cotacao_grupouggeri():
    resultado = cotacao_grupouggeri()
    return jsonify(resultado)


@app.route('/cotacao/vieraagrocereais', methods=['GET'])
def api_cotacao_vieraagrocereais():
    resultado = cotacao_vieraagrocereais()
    return jsonify(resultado)


@app.route('/cotacao/agropan', methods=['GET'])
def api_cotacao_agropan():
    resultado = cotacao_agropan()
    return jsonify(resultado)


@app.route('/cotacao/agriplanmga', methods=['GET'])
def api_cotacao_agriplanmga():
    resultado = cotacao_agriplanmga()
    return jsonify(resultado)





#.......................................................................................................................................................
#.......................................................................................................................................................



@app.route('/cotacao/rio_grande_do_sul', methods=['GET'])
def api_cotacao_rio_grande_do_sul():
    return jsonify({
        "cepalcereais": cotacao_cepalcereais(), # RIO GRANDE DO SUL / Passo Fundo
        "coagril": cotacao_coagril(), # RIO GRANDE DO SUL / Passo Fundo
        "cotacoesmercado": cotacao_cotacoesmercado(), # RIO GRANDE DO SUL / Passo Fundo
        "cotrisal": cotacao_cotrisal(), # RIO GRANDE DO SUL / Passo Fundo
        "cotrisoja": cotacao_cotrisoja(), # RIO GRANDE DO SUL / Passo Fundo
        "grupopoletto": cotacao_grupopoletto(), # RIO GRANDE DO SUL / Passo Fundo
        "sebben": cotacao_sebben(), # RIO GRANDE DO SUL / Passo Fundo
        "capaznet": cotacao_capaznet(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotriba": cotacao_cotriba(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotriel": cotacao_cotriel(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotrijal": cotacao_cotrijal(), # RIO GRANDE DO SUL / Não-me-Toque
        "coopeagri": cotacao_coopeagri(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotrirosa": cotacao_cotrirosa(), # RIO GRANDE DO SUL / Santa Rosa
    })





@app.route('/cotacao/parana', methods=['GET'])
def api_cotacao_parana():
    return jsonify({
        "agricolagemelli": cotacao_agricolagemelli(), # PARANÁ / Cascavel
        "plantarnet": cotacao_plantarnet(), # PARANÁ / Cascavel
        "agriplanmga": cotacao_agriplanmga() # PARANÁ / Maringá
    })








@app.route('/cotacao/rio_grande_do_sul/passo_fundo', methods=['GET']) #OK, 1º
def api_cotacao_passo_fundo():
    return jsonify({ 
        "cepalcereais": cotacao_cepalcereais(), # RIO GRANDE DO SUL / Passo Fundo
        "coagril": cotacao_coagril(), # RIO GRANDE DO SUL / Passo Fundo
        "cotacoesmercado": cotacao_cotacoesmercado(), # RIO GRANDE DO SUL / Passo Fundo
        "cotrisal": cotacao_cotrisal(), # RIO GRANDE DO SUL / Passo Fundo
        "cotrisoja": cotacao_cotrisoja(), # RIO GRANDE DO SUL / Passo Fundo
        "grupopoletto": cotacao_grupopoletto(), # RIO GRANDE DO SUL / Passo Fundo
        "sebben": cotacao_sebben() # RIO GRANDE DO SUL / Passo Fundo
    })






@app.route('/cotacao/rio_grande_do_sul/nao_me_toque', methods=['GET']) #OK, 2º
def api_cotacao_nao_me_toque():
    return jsonify({
        "capaznet": cotacao_capaznet(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotriba": cotacao_cotriba(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotriel": cotacao_cotriel(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotrijal": cotacao_cotrijal(), # RIO GRANDE DO SUL / Não-me-Toque
        "coopeagri": cotacao_coopeagri() # RIO GRANDE DO SUL / Não-me-Toque
    })





@app.route('/cotacao/rio_grande_do_sul/santa_rosa', methods=['GET']) #OK, 3º
def api_cotacao_santa_rosa():
    return jsonify({
        "cotrirosa": cotacao_cotrirosa() # RIO GRANDE DO SUL / Santa Rosa
    })






@app.route('/cotacao/rio_grande_do_sul/ijui', methods=['GET']) #OK, 4º
def api_cotacao_ijui():
    return jsonify({
        "cooperoque": cotacao_cooperoque(), # RIO GRANDE DO SUL / Ijuí
        "lazarotto": cotacao_lazarotto(), # RIO GRANDE DO SUL / Ijuí / TEM HORÁRIO DE PREÇO
        "grupouggeri": cotacao_grupouggeri(), # RIO GRANDE DO SUL / Ijuí / TEM HORÁRIO DE PREÇO
        "vieraagrocereais": cotacao_vieraagrocereais(), # RIO GRANDE DO SUL / Ijuí
        "agropan": cotacao_agropan() # RIO GRANDE DO SUL / Ijuí
    })






@app.route('/cotacao/parana/cascavel', methods=['GET']) #OK, 5º
def api_cotacao_cascavel():
    return jsonify({
        "agricolagemelli": cotacao_agricolagemelli(), # PARANÁ / Cascavel
        "plantarnet": cotacao_plantarnet() # PARANÁ / Cascavel
    })





@app.route('/cotacao/parana/maringa', methods=['GET']) #OK, 6º
def api_cotacao_maringa():
    return jsonify({
        "agriplanmga": cotacao_agriplanmga(), # PARANÁ / Maringá
        "camposverdes": cotacao_camposverdes() # PARANÁ / Maringá
    })







#.......................................................................................................................................................
#.......................................................................................................................................................





@app.route('/cotacao/todas', methods=['GET'])
def api_cotacao_todas():
    """Endpoint que retorna todas as cotações de uma vez"""
    return jsonify({
        # RIO GRANDE DO SUL
        "cepalcereais": cotacao_cepalcereais(), # RIO GRANDE DO SUL / Passo Fundo
        "coagril": cotacao_coagril(), # RIO GRANDE DO SUL / Passo Fundo
        "cotacoesmercado": cotacao_cotacoesmercado(), # RIO GRANDE DO SUL / Passo Fundo
        "cotrisal": cotacao_cotrisal(), # RIO GRANDE DO SUL / Passo Fundo
        "cotrisoja": cotacao_cotrisoja(), # RIO GRANDE DO SUL / Passo Fundo
        "grupopoletto": cotacao_grupopoletto(), # RIO GRANDE DO SUL / Passo Fundo
        "sebben": cotacao_sebben(), # RIO GRANDE DO SUL / Passo Fundo
        "capaznet": cotacao_capaznet(), #RIO GRANDE DO SUL / Não-me-Toque
        "cotriba": cotacao_cotriba(), #RIO GRANDE DO SUL / Não-me-Toque
        "cotriel": cotacao_cotriel(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotrijal": cotacao_cotrijal(), # RIO GRANDE DO SUL / Não-me-Toque
        "coopeagri": cotacao_coopeagri(), # RIO GRANDE DO SUL / Não-me-Toque
        "cotrirosa": cotacao_cotrirosa(), # RIO GRANDE DO SUL / Santa Rosa
        "cooperoque": cotacao_cooperoque(), # RIO GRANDE DO SUL / Ijuí
        "lazarotto": cotacao_lazarotto(), # RIO GRANDE DO SUL / Ijuí
        "grupouggeri": cotacao_grupouggeri(), # RIO GRANDE DO SUL / Ijuí
        "vieraagrocereais": cotacao_vieraagrocereais(), # RIO GRANDE DO SUL / Ijuí
        "agropan": cotacao_agropan(), # RIO GRANDE DO SUL / Ijuí
        # PARANÁ
        "agricolagemelli": cotacao_agricolagemelli(), # PARANÁ / Cascavel
        "plantarnet": cotacao_plantarnet(), # PARANÁ / Cascavel
        "agriplanmga": cotacao_agriplanmga(), # PARANÁ / Maringá
        "camposverdes": cotacao_camposverdes() # PARANÁ / Maringá

    })

if __name__ == '__main__':
   app.run(debug=True)

#.......................................................................................................................................................
#.......................................................................................................................................................