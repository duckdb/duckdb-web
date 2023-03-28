import os
import duckdb 
import json
import requests

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
STACK_OVERFLOW_API_URL = 'https://api.stackexchange.com/2.3/questions'

def post_to_discord(title, url, profile_image):
    payload = {
        "username": "Stack Overflow",
        "embeds": [
            {
                "title": title,
                "color": 16023588,
                "thumbnail": {"url": profile_image},
                "description": url
            }
        ]
    }
    with requests.post(DISCORD_WEBHOOK_URL, json=payload) as response:
        print(response.status_code)

if __name__ == '__main__':
    params = {
        'tagged': 'duckdb',
        'sort': 'creation',
        'order': 'desc',
        'site': 'stackoverflow'
    }
    response = requests.get(STACK_OVERFLOW_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        so_duckdb_tag = response.json()['items']
        with open("so.json", "w") as f:
            for item in so_duckdb_tag:
                f.write(json.dumps(item) + '\n')

        duckdb.sql('''
                CREATE OR REPLACE TABLE SO AS 
                SELECT * FROM read_ndjson_auto('./so.json')
                ORDER BY creation_date DESC
                Limit 30
        ''')

        new_duckdb_questions = duckdb.sql('''
            SELECT title, link, owner.profile_image,
                TO_TIMESTAMP(creation_date::BIGINT) create_time,
            FROM SO 
            WHERE create_time > NOW() - INTERVAL 1 DAY
            LIMIT 5
        ''')
 
        new_duckdb_questions.project('title, create_time').show()

        for title, link, image, _ in new_duckdb_questions.fetchall():
            post_to_discord(title, link, image)

    else:
        print(f'Request failed with status code {response.status_code}')

