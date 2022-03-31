#!/usr/bin/env python

import json
import sys
from Jira import Jira
from BitBucket import BitBucket
from config import *


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("ERROR : Use as JiraBitBucket.py PK issueStatus ")
        exit()
    pk = args[1]
    status = args[2]

    jira = Jira(JIRA_URL, JIRA_USER, JIRA_PASS)
    bb = BitBucket(BB_API_URL,
                   BB_USER,BB_PASS)
    jira.set_project(pk)
    issues = jira.get_project_issues()
    for issue in issues:
        if str(issue.fields.status) == status:
            """
            # Uncomment these 3 lines to get 'Done ID' and comment others after
            transitions = jira.jira.transitions(issue)
            x= [(t["id"], t['name']) for t in transitions]
            print(x)
            """
            project_name = issue.fields.customfield_10100
            repo_name = issue.fields.customfield_10101
            # if both project and repo don't exist, add them
            if bb.project_exists(project_name) is False:
                project_k = bb.create_project_key(project_name)
                project_key = bb.random_project_key(project_k)
                p_data = {
                    "key" : project_key,
                    "name" : project_name
                }
                bb.create_project(json.dumps(p_data))
                print("Project Created on BitBucket")
                r_data ={
                    "name" : repo_name
                }
                bb.create_repo(json.dumps(r_data), project_key)
                print("Repository Created on BitBucket")
                jira.jira.transition_issue(issue, 21)
                print("Issue updated to Done on JIRA")
            else:
                # if project exists but repo doesn't, add repo
                print("Project Exists on BitBucket")
                project_key = bb.get_project_key(project_name)
                if bb.repo_exists(project_key, repo_name) is False:
                    r_data ={
                        "name" : repo_name
                    }
                    bb.create_repo(json.dumps(r_data), project_key)
                    print("Repository Created on BitBucket")
                    jira.jira.transition_issue(issue, 21)
                    print("Issue updated to Done on JIRA")