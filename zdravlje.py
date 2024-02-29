import scrapy
import os
import json
import pandas as pd
from datetime import datetime


class ZdravljeSpider(scrapy.Spider):
    name = 'zdravlje'
    start_urls = ['https://www.zdravlje.gov.rs/tekst/335366/najvise-cene-lekova.php']
    download_delay = 10

    def parse(self, response):

        excel_folder = 'excel_data'
        pdf_folder = 'pdf_data'
        json_folder = 'json_data'

        if not os.path.exists(excel_folder):
            os.makedirs(excel_folder)

        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

        if not os.path.exists(json_folder):
            os.makedirs(json_folder)


        excel_links = response.css('a[title="Excel"]::attr(href)').extract()
        print("Excel links:", excel_links)
        for link in excel_links:
            absolute_url = response.urljoin(link)
            print("Downloading Excel file from:", absolute_url)
            yield scrapy.Request(url=absolute_url, callback=self.save_excel)


        pdf_links = response.css('a[title="PDF"]::attr(href)').extract()
        print("PDF links:", pdf_links)
        for link in pdf_links:
            absolute_url = response.urljoin(link)
            print("Downloading PDF file from:", absolute_url)
            yield scrapy.Request(url=absolute_url, callback=self.save_pdf)

    def save_excel(self, response):

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        excel_filename = os.path.join('excel_data', f'sr_{timestamp}.xlsx')
        print("Saving Excel file as:", excel_filename)
        with open(excel_filename, 'wb') as f:
            f.write(response.body)


        json_filename = os.path.join('json_data', f'sr_{timestamp}.json')
        print("Converting Excel file to JSON:", json_filename)
        excel_df = pd.read_excel(excel_filename)
        excel_df.to_json(json_filename, orient='records')

    def save_pdf(self, response):

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        filename = os.path.join('pdf_data', f'sr_{timestamp}.pdf')
        print("Saving PDF file as:", filename)
        with open(filename, 'wb') as f:
            f.write(response.body)
