import json
from datetime import date
from collections import Counter
import utils
import database.repository as repository



def gen_readme(new_current_id):

    frontend_id, title, title_slug, difficulty, language, runtime, memory, topic_tags, question, stats = repository.get_readme_solutions(new_current_id)

    readme = f"""
# {frontend_id}.  {title}

{"🟢 Easy" if difficulty == "Easy" else ("🟡 Medium"if difficulty == "Medium" else "🔴 Hard")} &nbsp;&nbsp;&nbsp; ⚙️ {language} &nbsp;&nbsp;&nbsp; ⏱ {runtime} &nbsp;&nbsp;&nbsp; 💾 {memory}



{"&nbsp;&nbsp;&nbsp;".join(f"`{topic_tags[i]["name"]}`" for i in range(0, len(topic_tags)))}


## Overview

<div align="center">
<table>
<tr>

<td valign="top">

<h3> Problem</h3>

|Property            |Value        |
|--------------------|-------------|
|Problem ID          |**{frontend_id}**|
|Difficulty          |**{difficulty}**|
|Leetcode Link       |[link!](https://leetcode.com/problems/{title_slug}/description/)

</td>

<td valign="top">
<h3> Community Stats</h3>


| Metric          | Count                         |
|-----------------|------------------------------:|
|Acceptance Rate  |**{stats["acRate"]}**          |
|Total Submission |**{stats["totalSubmission"]}** |
|Total Accepted   |**{stats["totalAccepted"]}**   |



</td>


</tr>
</table>
</div>


## Question
{question}

<br>
<p align="right">Last Sync: {date.today()} &nbsp;</p>
"""
    
    return readme


def root_gen_readme(new_current_id):

    counter = Counter()

    new = repository.get_table_rootReadme()
    language_table = repository.get_language_by_group()
    tags = repository.get_tags()
    memory_runtime = repository.avg_mem_run()
    avg_memory, avg_runtime = utils.avg_runtime_memory(memory_runtime)
    easy, medium, hard, total = repository.group_difficulty()
    frontend_id, title_slug, difficulty = repository.get_root_readme_solutions(new_current_id)
    

    # Gets the TOP 4 tags witht he higest number 
    for row in tags:

        if row and row[0]:
            tag_list = json.loads(row[0])
            cleaned_list = [tag["name"] for tag in tag_list]
            counter.update(cleaned_list)

    updated_counter = counter.most_common(4)

    # Makes a table of all Uploded questions
    table = f"\n".join(
    f"| {index} | {i[0]:04} | [{i[1]}]({i[2]}/{i[0]:04}_{i[6]}) | {f"🟢&nbsp;Easy" if i[2] == "Easy" else (f"🟡&nbsp;Medium" if i[2] == "Medium" else f"🔴&nbsp;Hard")} | {i[3]} | {i[4]} | {i[5]} | [Link!](https://leetcode.com/problems/{i[6]}) |"
    for index, i in enumerate(new, start=1)
    )

    # Gets top 10 most used tags a batch
    tags_batch = "&nbsp;".join(
        f"<code>{i[0]}</code>" for i in counter.most_common(10)
    ) 

    readme = f"""
# Leetcode Solutions

<div align="right">
    <h3>🔥 {utils.current_streak()} Day Streak</h3>
</div>


This repository is automatically synchronized using **LeetCode Sync**. View the [**source code**](https://github.com/Charanreddy0007/LeetCode-Sync.git).

---

<div align="center">
{tags_batch}

<h2> Dashboard </h2>

<table>
<tr>
<td valign="top">

<h3> Statistics</h3>

| Metric | Value |
|-------|-------------:|
|Total  | **{total}**  |
|Easy   | **{easy}**   |
|Medium | **{medium}** |
|Hard   | **{hard}**   |

</td>

<td valign="top">

<h3> Top Topics</h3>

| Topic | Value |
|-------|------:|
| {updated_counter[0][0]} | **{updated_counter[0][1]}** |
{f"| {updated_counter[1][0]} | **{updated_counter[1][1]}** |" if len(updated_counter) >= 2 else ""}
{f"| {updated_counter[2][0]} | **{updated_counter[2][1]}** |"if len(updated_counter) >= 3 else ""}
{f"| {updated_counter[3][0]} | **{updated_counter[3][1]}** |"if len(updated_counter) == 4 else ""}


</td>

<td valign="top">

<h3> Languages</h3>

| Language | # |
|----------|------:|
| {language_table[0][0]} | **{language_table[0][1]}** |
{f"| {language_table[1][0]} | **{language_table[1][1]}** |" if len(language_table) >= 2 else ""}
{f"| {language_table[2][0]} | **{language_table[2][1]}** |"if len(language_table) >= 3 else ""}
{f"| {language_table[3][0]} | **{language_table[3][1]}** |"if len(language_table) == 4 else ""}

</td>

<td valign="top">

<h3> Repository Info</h3>

| Metric          | Value              |
|-----------------|-------------------:|
| Runtime    | **{avg_runtime}**  |
| Memory  | **{avg_memory}**   |
| Latest  | **[{frontend_id}]({difficulty}/{frontend_id:04}_{title_slug})**|
| Updated    | **{date.today()}** |  


</td>
</tr>
</table>

> **Note:** Repository statistics include all accepted submissions. Runtime and memory averages include SQL solutions, which may affect the reported averages.
---

Auto-generated using **LeetCode Sync**

| # | Id | Problem |   Difficulty  | Language | Runtime | Memory | Leetcode Link |
|---|----|---------|---------------|----------|---------|--------|:-------------:|
{table}
---

</div>

<div align="center">
<p> Powered by LeetCode Sync • GitHub Actions • Last Sync: {date.today()} </p>
</div>


"""
    return readme


