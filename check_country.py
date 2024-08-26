from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import os
from dotenv import load_dotenv
import openai
from time import sleep

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

service = Service(executable_path=r"C:\chromedriver-win64\chromedriver.exe")   
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9030")
driver = webdriver.Chrome(service=service, options=options)

with open('1.json', 'r') as file:
    data = json.load(file)

gpt_country = []
for item_index, item in enumerate(data, start=1):
    if item['country'] == "{}":
        print(f"This element doesn't have country -------> {item_index}\n")
        driver.get(item['link'])
        sleep(0.5)

        address = ", ".join(driver.find_element(By.CLASS_NAME, 'ico-location-alt').text.split('\n'))

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"The country of the following address is: {address}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the country from the API response
        extracted_country = response.choices[0].text.strip()
        print(f"The country for the address '{address}' is:  {extracted_country}\n")
        item['country'] = extracted_country
    else:
        print(f"There is country : {item_index}\n")
        pass
    
    gpt_country.append({"link" : item["link"], "country" : item["country"]})

    with open("gpt.json", "w") as file:
        json.dump(gpt_country, file, indent=4)
