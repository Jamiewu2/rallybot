from pyral import Rally


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def pprint_user(user):
    role = user.Role or '-No Role-'
    values = (user.Name, user.UserName, role)
    return values


class RallyClient:
    # default values
    server = "rally1.rallydev.com"
    user = ""
    password = ""

    def __init__(self, apikey, workspace, project):

        self.rally = Rally(RallyClient.server, RallyClient.user, RallyClient.password, apikey=apikey, workspace=workspace, project=project)

    def get_users(self):
        all_users = self.rally.getAllUsers()
        return map(pprint_user, all_users)
