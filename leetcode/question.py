import json
import config
import database.repository as repository
import requests
import leetcode.queries as querie

def get_question(title_slug, current_id):


    GRAPHQL_URL = config.GRAPHQL_URL
    QUERY = querie.QUESTION_QUERY

    r = requests.post(
        GRAPHQL_URL,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
        },
        json={
            "query": QUERY,
            "variables": {
                "titleSlug": title_slug
            }
        },
        timeout=60,
    )

    # updates only if the status is 200 
    if r.status_code == 200:
        data = r.json()
        
        question = data["data"]["question"]["content"]
        stats = data["data"]["question"]["stats"]

        # update the database
        repository.update_question(question, stats, current_id)

    print("(4/7) Done getting question", r.status_code)
    
