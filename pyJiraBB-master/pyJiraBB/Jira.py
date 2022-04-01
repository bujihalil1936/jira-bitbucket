
from jira import JIRA


class Jira:

    def __init__(self, jira_url, user, password):

        self.jira = JIRA(server=jira_url, basic_auth=(user, password))

    def set_project(self, project_key):

        self.project_key = project_key

    def get_projects(self):

        return self.jira.projects()

    def get_project_issues(self):

        return self.jira.search_issues("project=" + self.project_key)
