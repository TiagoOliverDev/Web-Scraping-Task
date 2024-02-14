from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

import json
import pandas as pd
import pytz


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
    def __init__(self):
        self.driver = self.init_chrome_driver()

    def convert_date_to_utc_iso(self, date_str: str):
        try:
            et_tz = pytz.timezone('US/Eastern')

            date_hour = datetime.strptime(date_str, '%I:%M %p ET (%m/%d/%Y)')

            date_hour_et = et_tz.localize(date_hour)

            ddate_hour_utc = date_hour_et.astimezone(pytz.utc)

            date_hour_iso = ddate_hour_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

            return date_hour_iso
        except Exception as e:
            print(f"Error in convert_date_to_utc_iso(). CODE: {e}")
            return None

    def convert_to_float(self, value_for_convert: str):
        try:
            s_numeric = ''.join(c for c in value_for_convert if c.isdigit() or c in ['-', '.'])
            
            value_float = float(s_numeric)
            
            return value_float
        except Exception as e:
            value_float = 0
            return value_float

    def create_df_and_json(self, data: str):
        try:
            df = pd.DataFrame(data)

            data_dict = {}
            data_dict['Dados'] = df.to_dict('records')

            js = json.dumps(data_dict)
            fp = open('dados_bet.json', 'w')
            fp.write(js)
            fp.close()
                
        except Exception as e:
            print(f"Error in create_df_and_json(). CODE: {e}")
            return None

    def init_chrome_driver(self):
        try:
            driver_path = ChromeDriverManager().install()

            service = webdriver.chrome.service.Service(driver_path)

            options = webdriver.ChromeOptions()

            driver = webdriver.Chrome(service=service, options=options)

            return driver
        
        except Exception as e:
            print(f"Error in init_chrome_driver(). CODE: {e}")
            return None

    def go_to_page(self, url: str):
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Error in go_to_page(). CODE: {e}")
            return None

    def click_btn(self, xpath_btn: str):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_btn))
            )

            botao = self.driver.find_element(By.XPATH, xpath_btn)
            botao.click()
        except Exception as e:
            print(f"Error in click_btn(). CODE: {e}")
            return None

    def wait_for_element(self, timeout: int, xpath: str):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def capture_number_games(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]/span'))
            )

            value = int(element.text)

            return value
        except Exception as e:
            print(f"Error in capture_number_games(). CODE: {e}")
            return None

    def data_extract_bet(self, xpath_base: str):
        print('web scraping started...')
        self.go_to_page(url='https://veri.bet/odds-picks?filter=upcoming')

        qtd_iterator = self.capture_number_games()
        calc_for_iterator = qtd_iterator / 2 + 2

        self.click_btn(xpath_btn='/html/body/div[2]/div/div/div[1]/div/div[3]/div/a[1]')
        self.wait_for_element(10, xpath_base)

        values_bet = []
        try:
            print('downloading data, please wait!')
            for i in range(2, int(calc_for_iterator)):
                xpath_elemento_tr = f'{xpath_base}/tr[{i}]'
                elemento_tr = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_elemento_tr))
                )

                for x in range(1,3):
                    item = Item()

                    item.sport_league = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[4]/td[1]/table/tbody/tr/td/span[1]/a').text
                    date = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[4]/td[1]/table/tbody/tr/td/span[2]').text
                    date_formated = self.convert_date_to_utc_iso(date_str=date)
                    item.event_date_utc = date_formated
                    item.team1 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                    item.team2 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                    item.period = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
                    item.price = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/span').text
                    item.side = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                    item.team = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
                    spread_for_float = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span').text
                    spread_conveted = self.convert_to_float(value_for_convert=spread_for_float)
                    item.spread = spread_conveted
                    # item.n2 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[2]/span').text
                    # item.title_spread = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[3]/span').text
                    # item.n4 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[1]/td[4]/span').text
                    # item.n8 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[2]/td[4]/table/tbody/tr/td/span').text
                    # item.n10 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[2]/table/tbody/tr/td/span').text
                    # item.n11 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[3]/table/tbody/tr/td/span').text
                    # item.n12 = elemento_tr.find_element(By.XPATH, f'./td/div/div/div/div[{x}]/div/div/div/div/table/tbody/tr[3]/td[4]/table/tbody/tr/td/span').text

                    values_bet.append(item)
            # print(values_bet)
            df = pd.DataFrame([vars(item) for item in values_bet])
            data_dict = {}
            data_dict['Data bet'] = df.to_dict('records')
            # print(df)
            json_file_path = 'data/data_bet.json'
            js = json.dumps(data_dict)
            with open(json_file_path, 'w') as fp:
                fp.write(js)
                fp.close()

            with open(json_file_path, 'r') as fp:
                json_bet = json.load(fp)
                print(json.dumps(json_bet, indent=2))
            
            return values_bet

        except Exception as e:
            print(f"Error scraping data. CODE: {e}")
            return None
        finally:
            self.close_browser()

    def close_browser(self):
        print('downloading completed...')
        print('browser closed! Check the "data" folder in the project root')
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error close_browser(). CODE: {e}")
            return None


