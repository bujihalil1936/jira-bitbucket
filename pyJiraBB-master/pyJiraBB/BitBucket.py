
from bitbucket.bitbucket import Bitbucket
import requests
from requests.auth import HTTPBasicAuth
import json


class BitBucket:

    def __init__(self, bb_url, user, password):

        self.bb_url = bb_url
        self.user = user
        self.password = password

    def check_status(self):

        if self.req.status_code == 200:
            return True
        else:
            return "Error : Status Code : " + str(self.req.status_code)

    def check_errors(self):

        if "errors" in json.loads(self.req.content):
            return json.loads(self.req.content)["errors"][0]["message"]
        else:
            return False

    def ask_request(self, url):

        self.req = requests.get(url,
                                auth=HTTPBasicAuth(self.user, self.password))

    def get_projects(self):

        self.ask_request(self.bb_url + "projects/")
        if self.check_status():
            return json.loads(self.req.content)["values"]
        else:
            return self.check_status()

    def get_project(self, project_key):

        self.ask_request(self.bb_url + "projects/" + str(project_key))
        if self.check_status():
            if self.check_errors() is False:
                return json.loads(self.req.content)
            else:
                return self.check_errors()
        else:
            return False

    def get_project_repos(self, project_key):

        self.ask_request(self.bb_url + "projects/" + project_key + "/repos/")
        if self.check_status():
            if self.check_errors() is False:
                return json.loads(self.req.content)
            else:
                return self.check_errors()
        else:
            return False

    def get_project_key(self, project_name):

        projects = self.get_projects()
        for project in projects:
            if project["name"] == project_name:
                return project["key"]
        return False

    def ask_post_request(self, url, data):

        header = {"X-Atlassian-Token": "nocheck",
                  "content-type": "application/json"}
        self.req = requests.post(url,data=data,
                                auth=HTTPBasicAuth(self.user, self.password),
                                headers=header)

    def create_project(self, data):

        self.req = self.ask_post_request(self.bb_url + "projects/",data=data)

    def create_repo(self, data, project_key):
        
        self.req = self.ask_post_request(self.bb_url + "projects/" + project_key
                                + "/repos",
                                data=data)

    def project_exists(self, project_name, search_key="name"):
        projects = self.get_projects()
        for project in projects:
            if project[search_key].lower() == project_name.lower():
                return True
        return False

    def repo_exists(self, project_key, repo_name):
        repos = self.get_project_repos(project_key)
        if repos is not False and type(repos) != str:
            for repo in repos["values"]:
                if repo["name"].lower() == repo_name.lower():
                    return True
            return False
        else:
            return False

    # Create meaningful project key for created projects
    def create_project_key(self,project_name):
        word_list = project_name.split(" ")
        pk = ""
        for word in word_list:
            pk = pk + word[0]
        return pk

    # Prevent project key conflicts
    def random_project_key(self,pk):
        x = True
        i = 0
        while x:
            if self.project_exists(pk, search_key="key") is True:
                pk = pk + str(i)
                i = i + 1
            else:
                return pk
