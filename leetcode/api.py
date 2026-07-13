import requests
import json
import config
import leetcode.queries as querie
import database.repository as repository


def set_problem_info(length):


    QUERY = querie.PROBLEM_INFO_QUERY
    cookies = config.COOKIES

    skip = 0
    total_questions = 0

    while True:

        json_data = {
            'query': QUERY,
            'variables': {
                'filters': {
                    'questionStatus': 'SOLVED',
                    'skip': skip,
                    'limit': 50,
                    'sortOrder': 'DESCENDING',
                    'sortField': 'NUM_SUBMITTED',
                },
            },
            'operationName': 'userProgressQuestionList',
        }
    
        response = requests.post(
            'https://leetcode.com/graphql/', 
            cookies=cookies, 
            json=json_data,
            timeout=60
        )

        result = response.json()["data"]["userProgressQuestionList"]

        total_questions = result["totalNum"]
        questions = result["questions"]
    
        # If no question break the loop
        if not questions:
            break
        
        # If Database has the same number of questions break
        if length >= total_questions:
            break

        # Update the database
        for question in questions:
            
            repository.insert_info_solutions(
                question["frontendId"], 
                question["title"], 
                question["titleSlug"], 
                question["difficulty"].capitalize(), 
                json.dumps(question["topicTags"])
            )
        
        # Ckecks if ther are more then 50 questions
        skip += 50
    
    # Update & Commit changes 
    repository.update_status_1()     
    repository.commit()
        
    print("\n(1/7) Done with the problems info")




def set_submission_info(current_id, title_slug):

    cookies = config.COOKIES
    QUERIE = querie.SUBMISSION_INFO

    json_data = {
        'query': QUERIE,
        'variables': {
            'questionSlug': title_slug,
            'offset': 0,
            'limit': 20,
            'lastKey': None,
        },
        'operationName': 'submissionList',
    }


    response = requests.post(
        'https://leetcode.com/graphql/', 
        cookies=cookies, 
        json=json_data,
        timeout=60
    )

    result = response.json()["data"]["questionSubmissionList"]["submissions"]

    # get the best solutions 
    id = 0
    iteration = 0

    if len(result) > 1:
        max_num = float("inf")    

        for i in range(0, len(result)):

            # checks if the solutions is accepted            
            if result[i]["statusDisplay"] == "Accepted":

                runtime_raw = result[i]["runtime"]
                runtime = int(runtime_raw.replace(" ms", ""))

                if max_num > runtime:
                    max_num = runtime
                    id = result[i]["id"]
                    iteration = i
    
    else:

        id = result[0]["id"]
    
    language_name = config.EXTENSIONS.get(result[iteration]["lang"].lower(), ".txt")

    # Updates the database
    repository.update_submisstion_solutions(
        id, 
        language_name, 
        result[iteration]["langName"], 
        result[iteration]["memory"], 
        result[iteration]["runtime"], 
        current_id
    )

    print("(2/7) Done with the submission info")


def set_code(current_id, submission_id):


    cookies = config.COOKIES

    json_data = {
        'query': '\n    query submissionDetails($submissionId: Int!) {\n  submissionDetails(submissionId: $submissionId) {\n    runtime\n    runtimeDisplay\n    runtimePercentile\n    runtimeDistribution\n    memory\n    memoryDisplay\n    memoryPercentile\n    memoryDistribution\n    code\n    timestamp\n    statusCode\n    aiJudgeMessage\n    isCompiledLang\n    aiRecheckSubmitted\n    user {\n      username\n      profile {\n        realName\n        userAvatar\n      }\n    }\n    lang {\n      name\n      verboseName\n    }\n    question {\n      questionId\n      titleSlug\n      hasFrontendPreview\n    }\n    notes\n    flagType\n    topicTags {\n      tagId\n      slug\n      name\n    }\n    runtimeError\n    compileError\n    lastTestcase\n    codeOutput\n    expectedOutput\n    totalCorrect\n    totalTestcases\n    fullCodeOutput\n    testDescriptions\n    testBodies\n    testInfo\n    stdOutput\n  }\n}\n    ',
        'variables': {
            'submissionId': submission_id, #1598230880
        },
        'operationName': 'submissionDetails',
    }


    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, json=json_data, timeout=60)

    data = response.json()["data"]["submissionDetails"]

    # updates the database
    repository.update_code_solutions(data["code"], current_id)

    print("(3/7) Done with the code")


