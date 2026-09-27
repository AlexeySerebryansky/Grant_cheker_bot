from client.client import Client

client = Client()

code = client.get_html("https://fundinghub.com.ua/grants")

with open("test.html", "w", encoding="utf-8") as f:
    f.write(code)

print(len(code))
