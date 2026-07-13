import config
import base64
import requests
from datetime import date
from collections import Counter
import utils
import database.repository as repository




def upload_file(path, content, message, generate, new_current_id):

    TOKEN = config.TOKEN
    url = f"{config.URL}{path}"
    sha = None

    solution_sha, readme_sha = repository.get_sha(new_current_id)
    root_readme_sha = repository.get_root_sha()

    # Gets the sha if present in Database
    if generate.lower() == "root_readme":
        sha = root_readme_sha
    elif generate.lower() == "solution" :
        sha = solution_sha
    elif generate.lower() == "readme":
        sha = readme_sha
        
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
    }

    # Insert the SHA into data if present in Database
    if sha is not None:
        data["sha"] = sha
    


    headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
    }


    r = requests.put(url, headers=headers, json=data, timeout=60)

    # If SHA is not in Database but if it need to be updated it gets the SHA of it 
    if r.status_code == 422 or r.status_code == 409:

        sha = utils.get_sha(url, TOKEN) # Gets the SHA to update
        data["sha"] = sha
        r = requests.put(url, headers=headers, json=data, timeout=60)
    

    # Stores the Uploded files SHA
    if r.status_code == 200 or r.status_code == 201:
        new_sha = r.json()["content"]["sha"]

        if generate.lower() == "root_readme":
            repository.update_root_readme_sha(new_sha)
            

        elif generate.lower() == "solution" :
            repository.update_solution_sha(new_sha, new_current_id)

        elif generate.lower() == "readme":         
            repository.update_readme_sha(new_sha, new_current_id)
    else:
        print("Uploading files, Status code :", r.status_code)

    return r.status_code


