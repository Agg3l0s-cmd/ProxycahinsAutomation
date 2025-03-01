import json
import sys

# Set the console encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

lines = []

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

    for block in data['data']:
        anonimity = block['anonymityLevel']
        latency = block['latency']
        protocols = block['protocols']
        ip = block['ip']
        port = block['port']
        city = block['city']

        if anonimity.lower().strip() == 'elite' and latency < 70 and 'socks5' in protocols:
            lines.append(f"socks5 {ip} {port} #{city}")

    file.close()

print(lines)