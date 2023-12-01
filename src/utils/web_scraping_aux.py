from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import  Service
from dataclasses import dataclass, asdict
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
from typing import List
import pandas as pd

import time

@dataclass
class Item:
    sport_league: str = ''     # sport as we classify it, e.g. baseball, basketball, football
    event_date_utc: str = ''   # date of the event, in UTC, ISO format
    team1: str = ''            # team 1 name
    team2: str = ''            # team 2 name
    pitcher: str = ''          # optional, pitcher for baseball
    period: str = ''           # full time, 1st half, 1st quarter and so on
    line_type: str = ''        # whatever site reports as line type, e.g. moneyline, spread, over/under
    price: str = ''            # price site reports, e.g. '-133' or '+105'
    side: str = ''             # side of the bet for over/under, e.g. 'over', 'under'
    team: str = ''             # team name, for over/under bets this will be either team name or total
    spread: float = 0.0        # for handicap and over/under bets, e.g. -1.5, +2.5

class Web_scraping_aux:
    # def __init__(self, caminho_driver):
    #     self.driver = webdriver.Chrome(executable_path=caminho_driver)

        
    def __init__(self):
        self.driver = self.init_chrome_driver()

    def create_df_and_json(self, data: str):
        df = pd.DataFrame(data)

        data_dict = {}
        data_dict['Dados'] = df.to_dict('records')

        js = json.dumps(data_dict)
        fp = open('dados_bet.json', 'w')
        fp.write(js)
        fp.close()

    def clean_html(self, html):
        # Utiliza o BeautifulSoup para extrair o texto do HTML sem as tags
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(strip=True)
    
    def remover_tabs(self, texto):
        # Remove caracteres de tabulação (\t)
        return texto.replace('\t', '')

    def init_chrome_driver(self):
        # Use ChromeDriverManager para instalar e obter o caminho do chromedriver automaticamente
        driver_path = ChromeDriverManager().install()

        # Inicialize o serviço do Chrome
        service = webdriver.chrome.service.Service(driver_path)

        # Configurar as opções do Chrome, se necessário
        options = webdriver.ChromeOptions()

        # Inicializar o driver do Chrome
        driver = webdriver.Chrome(service=service, options=options)

        return driver
        # service = Service()                 # Classe usada para iniciar uma instância de chrome webdriver
        # options = webdriver.ChromeOptions() # preferências do browser do chrome
        # options.add_argument('--incognito')
        # # options.add_argument('--enable-mobile-emulation')
        # options.add_argument("--disable-infobars");
        # # options.AddUserProfilePreference("credentials_enable_service", false);
        # # options.AddUserProfilePreference("profile.password_manager_enabled", false);
        # driver = webdriver.Chrome(service=service, options=options)
        # return driver

    def go_to_page(self, *, url: str):
        # driver = self.init_chrome_driver()
        self.driver.get(url)
        # time.sleep(3)

    def clicar_em_botao(self, xpath_botao):
        # teste = xpath_botao
        # btns = self.driver.find_elements(By.TAG_NAME, 'a')[0].text
        # print(btns)
        # time.sleep(5)
        # # driver = self.init_chrome_driver()
        # Aguarde até que o botão esteja presente
        self.esperar_elemento_aparecer(timeout=10, xpath=xpath_botao)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_botao))
        )

        # # Encontre o botão pelo XPath e clique nele
        botao = self.driver.find_element(By.XPATH, xpath_botao)
        botao.click()
        print('botao clicado')

    def esperar_elemento_aparecer(self, timeout, xpath):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def teste(self, xpath_base, num_linhas): 
        print('1')
        self.go_to_page(url='https://veri.bet/odds-picks?filter=upcoming')
        # time.sleep(13)
        print('2')
        self.clicar_em_botao(xpath_botao='/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]')
        self.esperar_elemento_aparecer(10, xpath_base)
        print('3')
        try:
            dados_tabela = []

            for i in range(2, num_linhas + 1):
                xpath_elemento = f'{xpath_base}/tr[{i}]'
                elemento = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_elemento))
                )
                dados_tabela.append(elemento.text)
                print(dados_tabela)
            return dados_tabela

        finally:
            # Fechar o navegador
            self.driver.quit()

    def teste2(self, xpath_base, num_linhas): 
        print('1')
        self.go_to_page(url='https://veri.bet/odds-picks?filter=upcoming')
        # time.sleep(13)
        print('2')
        self.clicar_em_botao(xpath_botao='/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]')
        self.esperar_elemento_aparecer(10, xpath_base)
        print('3')
        try:
            valores_td = []

            for i in range(2, num_linhas + 1):
                xpath_elemento_td = f'{xpath_base}/tr[{i}]/td/div/div/div/div[1]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span'
                elemento_td = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_elemento_td))
                )
                valor_td = elemento_td.text
                valores_td.append(valor_td)
                print(valores_td)
            return valores_td

        finally:
            # Fechar o navegador
            self.driver.quit()

    def teste3(self, xpath_base, num_linhas): 
        print('1')
        self.go_to_page(url='https://veri.bet/odds-picks?filter=upcoming')
        # time.sleep(13)
        print('2')
        self.clicar_em_botao(xpath_botao='/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]')
        self.esperar_elemento_aparecer(10, xpath_base)
        print('3')
        try:
            valores_td = []

            for i in range(2, num_linhas + 1):
                xpath_elemento_tbody_1 = f'{xpath_base}/tr[{i}]/td/div/div/div/div[1]/div/div/div/div/table/tbody'
                xpath_elemento_tbody_2 = f'{xpath_base}/tr[{i}]/td/div/div/div/div[2]/div/div/div/div/table/tbody'

                elemento_tbody_1 = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_elemento_tbody_1))
                )
                elemento_tbody_2 = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_elemento_tbody_2))
                )

                valor_tbody_1 = self.clean_html(elemento_tbody_1.get_attribute("outerHTML"))
                valor_tbody_2 = self.clean_html(elemento_tbody_2.get_attribute("outerHTML"))

                # Remover caracteres de tabulação
                valor_tbody_1 = self.remover_tabs(valor_tbody_1)
                valor_tbody_2 = self.remover_tabs(valor_tbody_2)


                valores_td.append((valor_tbody_1, valor_tbody_2))
                print(valores_td)
                print("#########################################################################################################")
            return valores_td

        finally:
            # Fechar o navegador
            self.driver.quit()


    def obter_valores_colunas(self, xpath_base):
        print('1')
        self.go_to_page(url='https://veri.bet/odds-picks?filter=upcoming')
        # time.sleep(13)
        print('2')
        self.clicar_em_botao(xpath_botao='/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]')
        self.esperar_elemento_aparecer(10, xpath_base)
        print('3')
        try:
            # Esperar o elemento aparecer 
            xpath_elemento_tr = f'{xpath_base}/tr[2]'
            elemento_tr = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_elemento_tr))
            )


            item = Item()

            values_Bet = []
            for x in range(1,3):
                # Criar uma instância fora do loop

                # Atribuir valores à instância
                item.sport_league = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[4]/td[1]/table/tbody/tr/td/span[1]/a').text
                item.event_date_utc = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[4]/td[1]/table/tbody/tr/td/span[2]').text
                item.team1 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                item.team2 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                item.period = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
                item.price = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/span').text
                item.n2 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[2]/span').text
                item.title_spread = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[3]/span').text
                item.n4 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[4]/span').text
                item.n8 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[4]/table/tbody/tr/td/span').text
                item.n10 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[2]/table/tbody/tr/td/span').text
                item.n11 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[3]/table/tbody/tr/td/span').text
                item.n12 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[4]/table/tbody/tr/td/span').text
                item.side = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                item.team = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                item.spread = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span').text

                # Adicionar à lista
                values_Bet.append(item)

            self.create_df_and_json(data=values_Bet)

            print(item.sport_league)
            print(item.event_date_utc)
            print(item.team1)
            print(item.team2)
            print(item.period)
            print(item.price)
            print(item.side)
            print(item.team)
            print(item.spread)

            # Retornar os valores em um array
            return values_Bet

        except Exception as e:
            print(f"Erro ao obter valores das colunas: {e}")
            return None




    def data_extract(self, *, table_xpatch: str):
        print('1')
        self.go_to_page(url='https://veri.bet/odds-picks?filter=upcoming')
        # time.sleep(13)
        print('2')
        self.clicar_em_botao(xpath_botao='/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]')
        # print('3')
        # Aguarde até que a tabela esteja presente
        self.esperar_elemento_aparecer(10, table_xpatch)
        print('3')

        time.sleep(5)
        # Encontre a tabela pelo XPath
        tabela = self.driver.find_element(By.XPATH, table_xpatch)
        # Obtenha todas as linhas da tabela
        linhas_tabela = tabela.find_elements(By.TAG_NAME, 'tr')

        dados = []

        # Itera sobre as linhas da tabela e extrai os dados
        for linha in linhas_tabela:
            colunas = linha.find_elements(By.TAG_NAME, 'td')
            dados_linha = [coluna.text for coluna in colunas]
            dados.append(dados_linha)
            print(dados)
        return dados

    def encontrar_elemento_por_id(self, element_id):
        return self.driver.find_element(By.ID, element_id)

    def clicar_elemento(self, elemento):
        elemento.click()

    def preencher_campo(self, elemento, texto):
        elemento.send_keys(texto)

    # def esperar_elemento_aparecer(self, timeout, element_id):
    #     WebDriverWait(self.driver, timeout).until(
    #         EC.presence_of_element_located((By.ID, element_id))
    #     )

    def fechar_navegador(self):
        self.driver.quit()


cmd  = Web_scraping_aux()
# test = cmd.data_extract(table_xpatch='//*[@id="odds-picks"]/tbody/tr[1]/td/div[2]')
test = cmd.obter_valores_colunas(xpath_base = '//*[@id="odds-picks"]/tbody')
print(test) 
# //*[@id="odds-picks"]/tbody/tr[2]/td
