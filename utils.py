import config
import requests
import database.repository as repository
from ai.translator import translate_solution
from github.api import uplode_codes 
from datetime import datetime, date, timedelta


# Get the SHA to update
def get_sha(url, token):

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers, timeout=60)

    if r.status_code == 200:
        return r.json()["sha"]
    
    return None



# Average Runtime and Memory to the README
def avg_runtime_memory(memory_runtime):

    memory_sum = runtime_sum = 0
    memory_count = runtime_count = 1

    for i in memory_runtime:
        
        if i[0].endswith(" MB"):
            mem = float(i[0].replace(" MB", ""))
        memory_sum += mem
        memory_count += 1

        run = float(i[1].replace(" ms", ""))
        runtime_sum += run
        runtime_count += 1
    
    return f"{memory_sum/memory_count:.2f} MB", f"{runtime_sum/runtime_count:.2f} ms"


# Give the current time
def get_date_time():

    ist_time = datetime.now()
    return ist_time.strftime("%d %B %Y")


# Error Handling
def run_step(retry_code, current_id, func, *args):

    try:
        result = func(*args)
        if retry_code > 0:
            repository.reset_error(current_id)
        return result
    
    except Exception as e:
        repository.rollback()
        repository.updated_time(current_id)
        repository.update_error(retry_code + 1, str(e), current_id)

def run_step_code(func, *args):

    try:
        result = func(*args)
        return result
    
    except Exception as e:
        print("Error in genrating codes with AI")
    

def current_streak():
    dates = repository.streak(date)

    today = date.today()
    streak = 0

    if today not in dates:
        today -= timedelta(days=1)

    while today in dates:
        streak += 1
        today -= timedelta(days=1)

    return streak

def multiply_codes(code, org_language, path, frontend_id, title_slug):

    org_language.lower()
    result = translate_solution(code, org_language)

    solutions = {
        "python": result["python"],
        "cpp": result["cpp"],
        "javascript": result["javascript"],
        "typescript": result["typescript"],
        "java": result["java"],
    }

    for language, code in solutions.items():

        if language == org_language:
            print(f"      {org_language} Done ✓")

        elif language != org_language:

            language_ext = config.EXTENSIONS.get(language.lower(), ".txt")
            temp_path = f"{path}/Solution{language_ext}"

            status_code = uplode_codes(
                path=temp_path,
                code=code,
                message=f"Added {language} Solution for {frontend_id:04}_{title_slug}"
            )

            print(f"      {language} Done ✓")
