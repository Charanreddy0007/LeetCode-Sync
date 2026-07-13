QUESTION_QUERY = """
query selectProblem($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        boundTopicId
        title
        titleSlug
        content
        translatedTitle
        translatedContent
        isPaidOnly
        difficulty
        likes
        dislikes
        isLiked
        similarQuestions
        exampleTestcases
        contributors {
            username
            profileUrl
            avatarUrl
        }
        topicTags {
            name
            slug
            translatedName
        }
        companyTagStats
        codeSnippets {
            lang
            langSlug
            code
        }
        stats
        hints
        solution {
            id
            canSeeDetail
            paidOnly
            hasVideoSolution
            paidOnlyVideo
        }
        status
        sampleTestCase
        metaData
        judgerAvailable
        judgeType
        mysqlSchemas
        enableRunCode
        enableTestMode
        enableDebugger
        envInfo
        libraryUrl
        adminUrl
        challengeQuestion {
            id
            date
            incompleteChallengeCount
            streakCount
            type
        }
        note
    }
}
"""

PROBLEM_INFO_QUERY = """
query userProgressQuestionList($filters: UserProgressQuestionListInput) {
    userProgressQuestionList(filters: $filters) {    
        totalNum    
        questions {
            translatedTitle      
            frontendId      
            title      
            titleSlug      
            difficulty      
            lastSubmittedAt      
            numSubmitted      
            questionStatus      
            lastResult      
            topicTags {        
                name        
                nameTranslated        
                slug      
                }    
            }  
        }
    }    
"""

SUBMISSION_INFO = """
    query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: Int, $status: Int) {  
        questionSubmissionList(    offset: $offset    limit: $limit    lastKey: $lastKey    questionSlug: $questionSlug    lang: $lang    status: $status  ) {
            lastKey    
            hasNext    
            submissions {      
                id      
                title      
                titleSlug      
                status      
                statusDisplay      
                lang      
                langName      
                runtime      
                timestamp      
                url      
                isPending      
                memory      
                hasNotes      
                notes      
                flagType      
                frontendId      
                topicTags {        
                    id      
                }    
            }  
        }
    }    
"""