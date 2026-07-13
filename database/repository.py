import json
from database.connection import getConnection

conn = getConnection()
cursor = conn.cursor()


def commit():
    conn.commit()

def insert_info_solutions(frontend_id, title, title_slug, difficulty, topic_tags):
    cursor.execute(
        """
        INSERT OR IGNORE INTO solutions (
        frontend_id, 
        title, 
        title_slug, 
        difficulty, 
        topic_tags
        ) 
        VALUES (?, ?, ?, ?, ?)
        """,
        (frontend_id, title, title_slug, difficulty, topic_tags, )
    )


def update_submisstion_solutions(submission_id, language_verbose, language, memory, runtime, current_id):
    cursor.execute(
        """
        UPDATE solutions

        SET submission_id = ?,
        language_verbose = ?,
        language = ?,
        memory = ?,
        runtime = ?,
        status = 2

        WHERE id = ?
        AND status = 1
        """, 
        (submission_id, language_verbose, language, memory, runtime, current_id)
    )

def update_code_solutions(code, current_id):
    cursor.execute(
        """
        UPDATE solutions 
        
        SET code = ?, 
        status = 3
        
        WHERE id = ?
        AND status = 2
        """, 
        (code, current_id)
    )

def get_length():
    cursor.execute(
        """
            SELECT COUNT(*) 
            FROM solutions
        """
    )
    return cursor.fetchone()[0]

def get_current_id_retry():
    cursor.execute(
        """
        SELECT id, retry_count
        FROM solutions
        WHERE status < 7
          AND retry_count < 3
        ORDER BY id ASC
        LIMIT 1
        """
    )
    return cursor.fetchone()

def get_submission_info(current_id):
    cursor.execute(
        """
        SELECT 
        title_slug, 
        status
        FROM solutions 
        WHERE id = ?
        LIMIT 1
        """, (current_id,)
    )
    result = cursor.fetchone()

    return result[0], result[1]

def get_code_info(current_id):

    cursor.execute(
        """
        SELECT submission_id,
        status
        FROM solutions 
        WHERE id = ?
        LIMIT 1
        """, 
        (current_id,)
    )

    data = cursor.fetchone()

    return data[0], data[1]


def get_sha(current_id):

    cursor.execute(
        """
        SELECT 
        solution_sha,
        readme_sha
        FROM solutions
        WHERE id = ?
        LIMIT 1
        """,
        (current_id,)    
    )

    data = cursor.fetchone()

    return data[0], data[1]

def get_root_sha():
    cursor.execute(
        """
        SELECT root_readme_sha 
        FROM root_sha 
        WHERE id = 1
        LIMIT 1
        """
    )
    
    return cursor.fetchone()[0]
    
def update_root_readme_sha(new_sha):
    cursor.execute(
        """
            UPDATE root_sha 
            SET root_readme_sha = ? 
            WHERE id = 1
        """ , (new_sha, )
    )  

def update_solution_sha(new_sha, current_id):
    cursor.execute(
        """
        UPDATE solutions 
        SET solution_sha = ?, 
        status = 6 
        WHERE id = ? 
          AND status = 5
        """ , (new_sha, current_id,)
    )  

def update_readme_sha(new_sha, current_id):
    cursor.execute(
        """
        UPDATE solutions 
        SET readme_sha = ?, 
        status = 5 
        WHERE id = ? 
          AND status = 4
        """ , (new_sha, current_id)
    )  
 

def get_readme_solutions(current_id):
    cursor.execute(
        """
        SELECT
        frontend_id, 
        title, 
        title_slug,
        difficulty, 
        language, 
        runtime, 
        memory, 
        topic_tags,
        question,
        stats
        FROM solutions
        WHERE id = ?
        LIMIT 1
        """,(current_id,))
    
    data = cursor.fetchone()
    return data[0], data[1], data[2], data[3], data[4], data[5], data[6], json.loads(data[7]), data[8], json.loads(data[9])


def get_table_rootReadme():
    cursor.execute(
        """
        SELECT 
        frontend_id, 
        title, 
        difficulty, 
        language, 
        runtime, 
        memory, 
        title_slug, 
        id 
        FROM solutions 
        WHERE status = 7 
        ORDER BY frontend_id
        """)
    return cursor.fetchall()

def get_language_by_group():
    cursor.execute(
        """
        SELECT 
        language, 
        COUNT(id) 
        FROM solutions 
        WHERE status = 7 
        GROUP BY language 
        ORDER BY COUNT(id) DESC LIMIT 4
        """)
    return cursor.fetchall()

def get_tags():
    cursor.execute(
        """
        SELECT 
        topic_tags 
        FROM solutions 
        WHERE status = 7
        """)
    return cursor.fetchall()

def avg_mem_run():
    cursor.execute(
        """
        SELECT 
        memory,
        runtime
        FROM solutions 
        WHERE status = 7
        """
    )
    return cursor.fetchall()
    

def group_difficulty():
    cursor.execute(
        """
        SELECT 
        difficulty, COUNT(*)
        FROM solutions
        WHERE status = 7
        GROUP BY difficulty
        """
    )

    counts = dict(cursor.fetchall())

    easy = counts.get("Easy", 0)
    medium = counts.get("Medium", 0)
    hard = counts.get("Hard", 0)
    total = easy + medium + hard

    return easy, medium, hard, total

def get_root_readme_solutions(current_id):
    cursor.execute(
        """
        SELECT frontend_id, title_slug, difficulty
        FROM solutions
        WHERE id = ?
        LIMIT 1
        """,(current_id,))
    
    data = cursor.fetchone()
    return data[0], data[1], data[2]

def get_path(current_id):
    cursor.execute(
        """
        SELECT difficulty, 
        frontend_id, 
        title_slug, 
        language_verbose, 
        code, 
        status
        
        FROM solutions
        WHERE id = ?
        LIMIT 1 
        """,(current_id,)
    )

    data = cursor.fetchone()
    return data[0], data[1], data[2], data[3], data[4], data[5]


def update_question(question, stats, current_id):

    cursor.execute("""
        UPDATE solutions
        SET question = ?, 
        stats = ?,
        status = 4
                       
        WHERE id = ?
        AND status = 3
        """, (question, stats, current_id)
    )

def update_status_1():
    cursor.execute(
        """
        UPDATE solutions 
        SET status = 1 
        WHERE status = 0
    """
    )

def update_status_7(current_id):
    cursor.execute(
        """
        UPDATE solutions 
        SET status = 7 
        WHERE id = ? 
          AND status = 6
        """, (current_id,)
    )


def get_status(current_id):
    cursor.execute(
        """
        SELECT status 
        FROM solutions 
        WHERE ID = ?
        LIMIT 1
        """, (current_id, )
    )
    
    return cursor.fetchone()[0]


def update_error(retry_code, error_code, current_id):
    cursor.execute(
        """
        UPDATE solutions
        SET retry_count = ?,
        error_code = ?
        WHERE id = ?
        """, (retry_code, error_code, current_id, )
    )

def reset_error(current_id):
    cursor.execute(
        """
        UPDATE solutions
        SET retry_count = 0,
        error_code = NULL
        WHERE id = ?
        """, (current_id, )
    )

def updated_time(current_id):
    cursor.execute(
        """
        UPDATE solutions
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (current_id, )
    )

def rollback():
    conn.rollback()