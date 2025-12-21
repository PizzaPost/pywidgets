import requests
def check_update():
    response = requests.get("https://github.com/PizzaPost/pywidgets/info")
    data = response.json()
    latest_version = data["version"]

    if latest_version == "0.1.0":
        print("pywidgets is on the latest version")
    else:
        print("An update is available. Download it now with 'pip install --upgrade pywidgets'")
