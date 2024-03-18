import requests
import sqlite3

threatfox_url = "https://threatfox-api.abuse.ch/api/v1/"
payload = {
    "query": "get_iocs",
    "days": 1
}

response = requests.post(threatfox_url, json=payload)
if response.status_code == 200:
    ioc_data = response.json().get("data", [])

    conn = sqlite3.connect("ioc_database.db")
    cursor = conn.cursor()

    # Create the 'iocs' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iocs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ioc TEXT,
            threat_type TEXT,
            malware TEXT,
            first_seen TEXT,
            tags TEXT
        )
    ''')
    conn.commit()

    for ioc in ioc_data:
        tags = ', '.join(ioc['tags']) if isinstance(ioc['tags'], list) else ioc['tags']
        cursor.execute(
            "INSERT INTO iocs (ioc, threat_type, malware, first_seen, tags) VALUES (?, ?, ?, ?, ?)",
            (ioc['ioc'], ioc['threat_type_desc'], ioc['malware_printable'], ioc['first_seen'], tags)
        )

    conn.commit()
    conn.close()
else:
    print("Failed to fetch IOCs from ThreatFox")
