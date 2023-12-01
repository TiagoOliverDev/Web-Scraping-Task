from utils.web_scraping_aux import Web_scraping_aux


class Parse_veri_bet:

    robot_scraping = Web_scraping_aux()

    def start_robot(self):
        xpath_base = '//*[@id="odds-picks"]/tbody'
        self.robot_scraping.data_extract_bet(xpath_base)

if __name__ == "__main__":
    parser = Parse_veri_bet()
    parser.start_robot()