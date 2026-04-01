import urllib.parse

def build_google_url(address: str):
    query = urllib.parse.quote(f"{address} house for sale")
    return f"https://www.google.com/search?q={query}"

if __name__ == "__main__":
    address = "10535 Wilshire Blvd, Los Angeles, CA 90024"
    url = build_google_url(address)
    print("Generated Google URL:")
    print(url)