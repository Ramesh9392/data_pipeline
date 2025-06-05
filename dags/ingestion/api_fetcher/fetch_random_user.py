import requests

def fetch_random_product(**kwargs):
    """Fetch a product from fakerapi.it and return JSON as XCom."""
    url = "https://fakerapi.it/api/v1/products"
    params = {
        "_quantity": 100,  # Fetch only 1 product
        "_type": "product",  # Specify the type as product
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()  # Raise an error for bad responses
    data = resp.json()
    print (data)
    return data  # This will be serialized by XCom in Airflow

