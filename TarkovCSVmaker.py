import requests
import csv

def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


new_query = """
{
  traders {
    id
    name
    cashOffers {
      priceRUB
      item {
        name
        buyFor {
          vendor {
            name
            normalizedName
          }
          priceRUB
        }
        sellFor {
          priceRUB
          vendor {
            normalizedName
            name
          }
        }
      }
    }
  }
}
"""

result = run_query(new_query)

filtered_items = []

for trader in result['data']['traders']:
    for offer in trader['cashOffers']:
        item = offer['item']
        
        # Filter out Flea Market offers
        buy_offers = [buy for buy in item['buyFor'] if buy['vendor']['normalizedName'] != 'flea-market']
        sell_offers = [sell for sell in item['sellFor'] if sell['vendor']['normalizedName'] != 'flea-market']

        # Check if any trader both buys and sells the item
        for buy_offer in buy_offers:
            for sell_offer in sell_offers:
                if buy_offer['vendor']['normalizedName'] == sell_offer['vendor']['normalizedName']:
                    ratio = sell_offer['priceRUB'] / buy_offer['priceRUB']
                    filtered_items.append({
                        'item_name': item['name'],
                        'vendor_name': buy_offer['vendor']['name'],
                        'buy_price': buy_offer['priceRUB'],
                        'sell_price': sell_offer['priceRUB'],
                        'ratio': ratio
                    })

# Write the filtered items to a CSV file
with open('filtered_items.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Item Name', 'Vendor Name', 'Buy Price (RUB)', 'Sell Price (RUB)', 'Buy-to-Sell Ratio'])
    for item in filtered_items:
        writer.writerow([item['item_name'], item['vendor_name'], item['buy_price'], item['sell_price'], item['ratio']])

print("Filtered items have been written to filtered_items.csv")
