from datetime import timedelta, datetime

from pyral import Rally


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def pprint_user(user):
    role = user.Role or '-No Role-'
    values = (user.Name, user.UserName, role)
    return values


def pprint_user_story(user_story):
    name = user_story.Name
    author = user_story.CreatedBy.Name

    return "UserStory Name: {}, Author: {}".format(name, author)


class RallyClient:
    # default values
    server = "rally1.rallydev.com"
    user = ""
    password = ""

    def __init__(self, apikey, workspace, project):
        self.rally = Rally(RallyClient.server, RallyClient.user, RallyClient.password, apikey=apikey, workspace=workspace, project=project)
        self.rally.enableLogging('rally.log')

    def get_users(self):
        all_users = self.rally.getAllUsers()
        return map(pprint_user, all_users)

    def get_user_stories(self):
        """
        internally, rally uses HierarchicalRequirement for UserStories and Defects

        :return:
        """
        response = self.rally.get('HierarchicalRequirement', fetch=True, projectScopeDown=True)
        results = map(pprint_user_story, response)
        return results

    def get_changes(self):
        #build the query to get only the artifacts (user stories and defects) updated in the last day
        querydelta = timedelta(hours=-12)
        querystartdate = datetime.utcnow() + querydelta
        query = 'LastUpdateDate > ' + querystartdate.isoformat()

        response = self.rally.get('Artifact', fetch=True, projectScopeDown=True, query=query, order='LastUpdateDate desc')
        results = []

        #format of the date strings as we get them from rally
        format = "%Y-%m-%dT%H:%M:%S.%fZ"

        for artifact in response:
            include = False

            #start building the message string that may or may not be sent up to slack
            postmessage = '*' + artifact.FormattedID + '*'
            postmessage = postmessage + ': ' + artifact.Name + '\n'
            for revision in artifact.RevisionHistory.Revisions:
                print(revision.CreationDate)
                revisionDate = datetime.strptime(revision.CreationDate, format)
                age = revisionDate - datetime.utcnow()
                seconds = abs(age.total_seconds())
                #only even consider this story for inclusion if the timestamp on the revision is less than iterval seconds onld
                description = revision.Description
                items = description.split(',')

                for item in items:
                    item = item.strip()
                    #the only kinds of updates we care about are changes to OWNER and SCHEDULE STATE
                    #other changes, such as moving ranks around, etc, don't matter so much
                    if item.startswith('SCHEDULE STATE ') or item.startswith("OWNER added "):
                        postmessage = postmessage + "> " + item + ' \n'
                        include = True

            if include:
                postmessage = postmessage + 'https://rally1.rallydev.com/#/search?keywords=' + artifact.FormattedID + '\n'
                results.append(postmessage)

        return results
