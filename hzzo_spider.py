import scrapy
import pandas as pd

class HZZOSpider(scrapy.Spider):
    name = 'hzzo'
    start_urls = ['https://hzzo.hr/zdravstvena-zastita/lijekovi/objavljene-liste-lijekova']

    def parse(self, response):
        # Pronađi link ka prvom Excel fajlu
        first_excel_link = response.xpath('//a[contains(@href, ".xlsx")]/@href').extract_first()
        self.logger.info("Link ka Excel fajlu: %s", first_excel_link)
        yield scrapy.Request(response.urljoin(first_excel_link), callback=self.parse_excel)

    def parse_excel(self, response):
        self.logger.info("Otvaram Excel datoteku...")
        # Otvaranje Excel datoteke
        excel_file = pd.ExcelFile(response.body)

        self.logger.info("Lista listova u Excel datoteci: %s", excel_file.sheet_names)

        # Čitanje određenih listova iz Excel datoteke
        df_oll_1 = pd.read_excel(excel_file, sheet_name='OLL-1. dio')
        df_oll_2 = pd.read_excel(excel_file, sheet_name='OLL-2. dio')
        df_oll_3 = pd.read_excel(excel_file, sheet_name='OLL-3. dio')
        df_oll_4 = pd.read_excel(excel_file, sheet_name='OLL-4. dio')

        self.logger.info("Prvi redovi OLL-1.dio:\n%s", df_oll_1.head())
        self.logger.info("Prvi redovi OLL-2.dio:\n%s", df_oll_2.head())
        self.logger.info("Prvi redovi OLL-3.dio:\n%s", df_oll_3.head())
        self.logger.info("Prvi redovi OLL-4.dio:\n%s", df_oll_4.head())

        # Spajanje svih DataFrame-ova u jedan
        merged_df = pd.concat([df_oll_1, df_oll_2, df_oll_3, df_oll_4], ignore_index=True)

        # Pretvaranje u JSON format
        json_data = merged_df.to_json(orient='records')

        # Čuvanje JSON-a u datoteku
        with open('merged_data.json', 'w') as f:
            f.write(json_data)

        self.log('Svi listovi su uspešno spojeni i sačuvani u merged_data.json fajlu.')


# Pycharm je otvoren, u konzoli smo instalirali uz komande pip install pandas, scrapy, 
#zatim smo u konzolu uneli scrapy startproject myproject, posle tog smo usli u spider podfolder i tu kreirali
#hzzo.py i u njemu smo napravili ovaj kod, pokrenuli kod u konzoli uz komandu scrapy crawl hzzo i spremili prva 4 excell sheeta u json.
