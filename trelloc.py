from trello import TrelloClient


class TrelloBoard:
    def __init__(self, api_key, token, board_id):
        self.client = TrelloClient(api_key=api_key, token=token)
        self.board = self.client.get_board(board_id)

    def list_lists(self, list_filter=''):
        return self.board.list_lists()


class Members:
    def __init__(self, api_key, token):
        self.members = {}
        self.client = TrelloClient(api_key=api_key, token=token)

    def get_avatar_url(self, member_id):
        if member_id is None:
            return ''

        if member_id not in self.members:
            self.members[member_id] = self.__fetch_member(member_id)
        return self.members[member_id].get('avatar_url')

    def __fetch_member(self, member_id):
        json_obj = self.client.fetch_json(
            '/members/' + member_id,
            query_params={'badges': False})
        id = json_obj.get('id', '')
        username = json_obj.get('username', '')
        full_name = json_obj.get('fullName', '')
        avatar_url = json_obj.get('avatarUrl', '')
        if avatar_url is None:
            avatar_url = ''
        return {
            'id': id,
            'username': username,
            'full_name': full_name,
            'avatar_url': self.__avatar_url(username, avatar_url + '/30.png')
        }

    def __avatar_url(self, username, url):
        return '![{username}]({url})'.format(username=username, url=url)
