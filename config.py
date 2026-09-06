import os
from dotenv import load_dotenv

load_dotenv(".env")

# Modify according to yours 
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")
TOKEN = os.getenv("TOKEN_GITHUB")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

COOKIES = {
        'csrftoken' : os.getenv("CSRFTOKEN"),
        'LEETCODE_SESSION' : os.getenv("LEETCODE_SESSION"),
}

DATABASE = "database/database.db"

URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/"

QUESTION_URL = f"https://leetcode.com/problems/"

GRAPHQL_URL = "https://leetcode.com/graphql"

EXTENSIONS = {
        "python": ".py",
        "python3": ".py",
        "java": ".java",
        "c": ".c",
        "c++": ".cpp",
        "cpp": ".cpp",
        "c#": ".cs",
        "javascript": ".js",
        "typescript": ".ts",
        "go": ".go",
        "kotlin": ".kt",
        "swift": ".swift",
        "rust": ".rs",
        "ruby": ".rb",
        "php": ".php",
        "dart": ".dart",
        "scala": ".scala",
        "elixir": ".ex",
        "erlang": ".erl",
        "racket": ".rkt",
        "mysql": ".sql",
    }

