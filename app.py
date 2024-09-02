import csv
import json
import requests
import time
import random


with open('1786unakuna@belift.id_17777638_calista all shop.txt', 'r') as file:
    cookie_data = json.load(file)

cookies = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookie_data])

# Read shop names from CSV file
shop_names = []
with open('shopnames.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        shop_names.append(row[0])

# Check availability of each shop
available_shops = []
for shop_name in shop_names:
    query = """
        query ValidateShop($domain: String, $shopName: String) {
            validateDomainShopName(domain: $domain, shopName: $shopName) {
                isValid
                error {
                    message
                    __typename
                }
                __typename
            }
        }
    """
    variables = {
        "shopName": shop_name,
        "domain": ""
    }
    headers = {
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "X-Version": "bd582a7",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "accept": "*/*",
        "Referer": "https://seller.tokopedia.com/",
        "X-Source": "tokopedia-lite",
        "X-Tkpd-Lite-Service": "icarus",
        "sec-ch-ua-platform": "\"Windows\"",
        "Cookie": cookies
    }
    data = {
        "operationName": "ValidateShop",
        "variables": variables,
        "query": query
    }
    response = requests.post("https://gql.tokopedia.com/graphql/ValidateShop", headers=headers, data=json.dumps(data))
    result = response.json()["data"]["validateDomainShopName"]
    if result["isValid"]:
        available_shops.append(shop_name)

    # Random delay
    delay_seconds = random.randint(1, 3)
    time.sleep(delay_seconds)

    print(f"Shop name: {shop_name}, available: {result['isValid']}")

# Save available shop names to CSV file
with open("availablename.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ShopName"])
    for shop_name in available_shops:
        writer.writerow([shop_name])