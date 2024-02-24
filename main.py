from bs4 import BeautifulSoup
import requests


url = "https://www.zdravlje.gov.rs/view_file.php?file_id=2967&cache=sr"
html_response = requests.get(url)


with open("cene.xlsx", "wb") as f:
    f.write(html_response.content)

print("File je sačuvan.")