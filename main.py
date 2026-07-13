import sys
import time
import config
import database.schema
import database.repository as repository

from utils import run_step
from github.api import upload_file
from leetcode.question import get_question
from github.readme import root_gen_readme, gen_readme
from leetcode.api import set_problem_info, set_submission_info, set_code

total_start_time = time.time() # Starts the timer

# Problem info
try: 
    set_problem_info(repository.get_length()) 
except Exception as e:
    print("Error in getting questions", str(e))
    repository.rollback()
    sys.exit(0)

# IF all the questions are done exits ELSE continue
current_id_error = repository.get_current_id_retry()
if current_id_error == None:
    print("No new questions found")
    sys.exit(0)
else:
    current_id, retry_code = current_id_error[0], current_id_error[1]


# Submission info
title_slug, status = repository.get_submission_info(current_id)
if status == 1:
    run_step(
        retry_code, 
        current_id, 
        set_submission_info, 
        current_id, 
         title_slug
        )


# Code 
submission_id, status = repository.get_code_info(current_id)
if status == 2:
    run_step(
        retry_code,
        current_id,
        set_code,
        current_id,
         submission_id
    )


# Question
status = repository.get_status(current_id)
if status == 3:
    run_step(
        retry_code,
        current_id,
        get_question,
        title_slug,
         current_id
    )


# Initialize For GIT
difficulty, frontend_id, title_slug, language_verbose, code, status = repository.get_path(current_id)
solution_path = f"{difficulty}/{frontend_id:04}_{title_slug}/Solution{language_verbose}"
readme_path   = f"{difficulty}/{frontend_id:04}_{title_slug}/README.md"


# Uplode Problem README
if  status == 4: 
    readme_status = run_step(
        retry_code,
        current_id,
        upload_file,
         readme_path,
         gen_readme(current_id),
         f"Added README for {frontend_id:04}_{title_slug}", 
         "readme", 
         current_id
    )

    print(f"(5/7) Done gen_readme: {readme_status}")


# Uplodes Problem Code
status = repository.get_status(current_id)
if status == 5:
    code_status = run_step(
        retry_code,
        current_id,
        upload_file,
         solution_path,
         code,
         f"Added Solution for {frontend_id:04}_{title_slug}", 
         "solution", 
         current_id
    )

    print(f"(6/7) Done code: {code_status}")


# Uplodes Root README
status = repository.get_status(current_id)
if status == 6:
    repository.update_status_7(current_id)
    root_readme_status = run_step(
        retry_code,
        current_id,
        upload_file,
         "README.md",
         root_gen_readme(current_id),
         f"Updated README", 
         "root_readme", 
         current_id
    )
    print(f"(7/7) Done root_gen_readme: {root_readme_status}")

# ALL DONE
status = repository.get_status(current_id)
if status == 7:
    repository.updated_time(current_id)
    total_end_time = time.time()
    print("\n--------------Done--------------\n")
    print(f"Total Time: {(total_end_time - total_start_time):.2f} S")


# FINAL COMMIT
repository.commit()