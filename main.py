import json
import sys
import os
import datetime


def log(message):
    file = open("logs.log", "a")
    file.write(message+"\n")


def main(path):
    os.system("node  main.js")

    # Set the console encoding to UTF-8
    sys.stdout.reconfigure(encoding='utf-8')

    socks = ["socks4 127.0.0.1 9050 #tor\n"]

    try:
        file = open('data.json', 'r', encoding='utf-8')
    except Exception:
        log(f"{datetime.datetime.now()} Error opening json!")
    data = json.load(file)
    file.close()

    for block in data['data']:
        anonimity = block['anonymityLevel']
        latency = block['latency']
        protocols = block['protocols']
        ip = block['ip']
        port = block['port']
        city = block['city']

        if anonimity.lower().strip() == 'elite' and latency < 70 and 'socks5' in protocols:
            socks.append(f"socks5 {ip} {port} #{city}\n")

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

    lines = lines[:cur] + socks

    if cur is not None:
        try:
            file = open(path, "w", encoding='utf-8')
            file.writelines(lines)
            file.close()
        except Exception as e:
            log(f"{datetime.datetime.now()} Error with writing to {path}! Error: {e}")


if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
