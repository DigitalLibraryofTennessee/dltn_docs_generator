from github import Github
import yaml
import argparse


class QuarterlyReport:
    """Class to generate a quarterly report for DLTN work.

    Attributes:
        milestone (str): The milestone the report is associated with.
        issues (list): A list of all closed issues from the milestone.

    """

    def __init__(self, gh_user, gh_pass, gh_token, milestone):
        self.milestone = milestone
        self.gh_connection = self.__authenticate(gh_user, gh_pass, gh_token)
        self.issues = (
            self.gh_connection.get_user("DigitalLibraryofTennessee")
            .get_repo("DLTN_XSLT")
            .get_issues(state="closed")
        )

    @staticmethod
    def __authenticate(user, password, token):
        if token != "":
            return Github(token)
        else:
            return Github(user, password)

    def process_issues(self):
        completed_issues = []
        for issue in self.issues:
            try:
                if issue.milestone.title == self.milestone:
                    completed_issues.append(
                        f"`{issue.assignee.login} <https://github.com/{issue.assignee.login}>`_: "
                        f"`{issue.title} <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT/issues/{issue.number}>`_"
                    )
            except AttributeError:
                pass
        return self.__create_rst_doc(completed_issues)

    def __create_rst_doc(self, issues):
        with open(
            f"../docs/progress_reports/{self.milestone}.rst", "w+"
        ) as milestone_report:
            milestone_report.write(f"{self.milestone}\n")
            milestone_report.write(f'{"="*len(self.milestone)}\n\n')
            milestone_report.write(
                "This report shows all work completed during the quarter according to the "
                "`DLTN_XSLT issue tracker <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT/issues/>`_.\n\n"
            )
            i = 1
            for issue in issues:
                milestone_report.write(f"{i}. {issue}\n")
                i += 1
        return


if __name__ == "__main__":
    settings = yaml.safe_load(open("../config.yml", "r"))
    parser = argparse.ArgumentParser(description="Quarterly report parser")
    parser.add_argument("-m", "--milestone", dest="milestone", required=True)
    parser.add_argument(
        "-u", "--user", dest="username", required=False, default=settings["gh_user"]
    )
    parser.add_argument(
        "-p", "--password", dest="password", required=False, default=settings["gh_pass"]
    )
    parser.add_argument(
        "-a", "--access_token", dest="access_token", required=False, default=settings["gh_accesstoken"]
    )
    args = parser.parse_args()
    report = QuarterlyReport(args.username, args.password, args.access_token, args.milestone)
    report.process_issues()
