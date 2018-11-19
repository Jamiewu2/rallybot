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
        return "\n".join(results)
