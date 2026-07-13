from database.connection import getConnection

conn = getConnection()
cursor = conn.cursor()

# Creates a Table to store all the leetcode and Github values
cursor.execute("""
    CREATE TABLE IF NOT EXISTS solutions (
               
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status INT DEFAULT 0,

        title TEXT UNIQUE,
        frontend_id INTEGER DEFAULT NULL,
        title_slug TEXT DEFAULT NULL,
        topic_tags TEXT DEFAULT NULL,
        difficulty TEXT DEFAULT NULL,

        
        submission_id INTEGER DEFAULT NULL,
        language TEXT DEFAULT NULL,
        language_verbose TEXT DEFAULT NULL,
        memory TEXT DEFAULT NULL,
        runtime TEXT DEFAULT NULL,


        code TEXT DEFAULT NULL,

        question TEXT DEFAULT NULL,
        stats TEXT DEFAULT NULL,  

        solution_sha TEXT DEFAULT NULL,
        readme_sha TEXT DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
        
        retry_count INT DEFAULT 0,
        error_code TEXT DEFAULT NULL
    )""")

# Creates a table to store the root_readme_sha 
cursor.execute("""
CREATE TABLE IF NOT EXISTS root_sha (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    root_readme_sha TEXT DEFAULT NULL
)
""")

# Initialise
cursor.execute("""
INSERT OR IGNORE INTO root_sha (id)
VALUES (1)
""")

conn.commit()
