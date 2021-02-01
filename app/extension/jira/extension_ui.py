import random

from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, PopupManager, Issue, Project, Search, ProjectsList, \
    BoardsList, Board, Dashboard, Logout

from util.api.jira_clients import JiraRestClient
from util.conf import JIRA_SETTINGS

client = JiraRestClient(JIRA_SETTINGS.server_url, JIRA_SETTINGS.admin_login, JIRA_SETTINGS.admin_password)
rte_status = client.check_rte_status()

KANBAN_BOARDS = "kanban_boards"
SCRUM_BOARDS = "scrum_boards"
USERS = "users"
ISSUES = "issues"
CUSTOM_ISSUES = "custom_issues"
JQLS = "jqls"
PROJECTS = "projects"

def create_issue(webdriver, dataset):
    issue_modal = Issue(webdriver)

    @print_timing("selenium_create_issue")
    def measure():

        @print_timing("selenium_create_issue:open_quick_create")
        def sub_measure():
            issue_modal.open_create_issue_modal()
        sub_measure()

        @print_timing("selenium_create_issue:fill_and_submit_issue_form")
        def sub_measure():
            issue_modal.fill_summary_create()  # Fill summary field
            issue_modal.fill_description_create2(rte_status)  # Fill description field
            issue_modal.assign_to_me()  # Click assign to me
            issue_modal.set_resolution()  # Set resolution if there is such field
            issue_modal.set_issue_type()  # Set issue type, use non epic type

            @print_timing("selenium_create_issue:fill_and_submit_issue_form:submit_issue_form")
            def sub_sub_measure():
                issue_modal.submit_issue()
            sub_sub_measure()
        sub_measure()
    measure()
    PopupManager(webdriver).dismiss_default_popup()

def view_issue(webdriver, datasets):
    issue_page = Issue(webdriver, issue_key=datasets['issue_key'])

    @print_timing("selenium_view_issue")
    def measure():
        issue_page.go_to()
        issue_page.wait_for_page_loaded()
    measure()