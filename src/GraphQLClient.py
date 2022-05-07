import requests
import os


class GraphQLClient:
    def __init__(self, url, client_id, client_secret):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = ""
        if os.path.exists("../access_token"):
            with open("../access_token", "r") as f:
                self.access_token = f.readlines()[0].strip()
        else:
            self.generate_token()

    def get(self, query, retry=True):
        res = requests.post(url=self.url, json={"query": query}, headers=self.headers())
        if res.status_code != 200 or "errors" in res.json():
            print("Connection or formatting error")
            if retry:
                print("Trying to refresh token")
                self.generate_token()
                return self.get(query, False)

            else:
                print("Token refresh didn't solve the issue, here is the error and the query")
                print("Error", res.json())
                print("Query", query)
                print("Exiting")
                exit()
        return res.json()

    def generate_token(self):
        self.access_token = requests.post("https://www.esologs.com/oauth/token",
                                          auth=(self.client_id, self.client_secret),
                                          json={"grant_type": "client_credentials"}).json()["access_token"]
        with open("../access_token", "w") as f:
            print(self.access_token, file=f)

    def headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}
