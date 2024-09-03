import requests

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
print(result)
