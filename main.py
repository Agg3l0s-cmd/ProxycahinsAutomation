import json
import sys
import datetime
import asyncio
from playwright.async_api import async_playwright

# Set the console encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Detect if Firefox is requested via command-line argument
USE_FIREFOX = "--firefox" in sys.argv


def log(message):
    # Open log file for logs
    file = open("logs.log", "a")
    file.write(message+"\n")


async def get_data():
    async with async_playwright() as p:
        # Choose browser based on argument
        browser_type = p.firefox if USE_FIREFOX else p.chromium
        # Set headless=False for debugging
        browser = await browser_type.launch(headless=True)

        page = await browser.new_page()

        # Fetch the API data
        # url = "https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc"
        url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/all/data.json"
        await page.goto(url, wait_until="networkidle")

        # Extract page content
        data = await page.evaluate("document.body.innerText")

        await browser.close()
        return json.loads(data)


async def main(path):
    try:
        data = await get_data()
        print(data[0])

        socks = ["socks4 127.0.0.1 9050 #tor\n"]

        for block in data:
            anonimity = block['anonymity']
            protocol = block['protocol']
            ip = block['ip']
            port = block['port']

            if anonimity.lower().strip() == 'elite' and protocol == 'http':
                socks.append(f"{protocol} {ip} {port}\n")

        try:
            file = open(path, "r+", encoding='utf-8')
            lines = file.readlines()
            file.close()
        except Exception as e:
            log(f"{datetime.datetime.now()} Error with reading from {path}! Error: {e}")

        cur = None
        for i, line in enumerate(lines):
            if line == "# defaults set to \"tor\"\n":
                cur = i+1
                break

        # Keep the lines only after tor socks4 ip
        lines = lines[:cur] + socks

        if cur is not None:
            try:
                file = open(path, "w", encoding='utf-8')
                file.writelines(lines)
                file.close()
            except Exception as e:
                log(f"{datetime.datetime.now()} Error with writing to {path}! Error: {e}")

    except Exception as e:
        log(f"{datetime.datetime.now()} Error with writing to {path}! Error: {e}")

# Run the script
if __name__ == "__main__":
    path = sys.argv[1]
    asyncio.run(main(path))
