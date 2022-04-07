import requests


class GraphQLClient:
    def __init__(self, url, access_token):
        # TODO manage token rotation
        self.url = url
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get(self, query):
        res = requests.post(url=self.url, json={"query": query}, headers=self.headers)
        if res.status_code != 200:
            print("Connection error")
            exit()
        elif "errors" in res:
            print("Formatting error?")
            print(res.json())
            exit()
        return res.json()