# pyJiraBB
This is an assignment for learning JIRA, Bitbucket and using RestAPI with Python

## Assignment Details

### install a jira instance
* you need to use postgresql
* jira needs to run from an url like: http://localhost:8080/jira
 
### install a bitbucket instance
* you need to use postgresql
* bitbucket needs to run from an url like: http://localhost:8080/bitbucket
 
### create and configure jira project
* create a new jira project named "Bitbucket Request" with key "BR". You can use "Task Management" as project type/template.
* add a new custom field(type should be text field) named "Bitbucket Project Name" to all screens of BR.
* add a new custom field(type should be text field) named "Bitbucket Repository Name" to all screens of BR.
* project should have only one issue type: "Repository Request"
* project workflows should have only 2 status: "To Do", "Done"
* create a new issue and fill the fields: summary, Bitbucket Project Name, Bitbucket Repository Name. After creating issue, its status should be "To Do"
 
### write a script to create bitbucket project and repository with the information from jira. (Note: Project name should be same with Bitbucket project name and Repository name should be same with Bitbucket Repository Name.)
* script should select issues of jira with project key BR and status To Do.
* script should read values of Bitbucket Project Name, Bitbucket Repository Name fields
* script should open a new bitbucket project with Bitbucket Project Name if the project not exists
* script should open a new bitbucket repository with Bitbucket Repository Name under project with Bitbucket Project Name
* script should update(create transition) jira issue. After the process jira issue should have status "Done"

## Using

* Set variables in "config.py" file first
* Use as "python pyJiraBB.py BR 'To Do'"

