from fore import TwitchAPI as API
from .constants import *


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Cursor(object):
    """
    Cursor for forward/backward pagination.
    Tells the server where to start fetching the next set of results, in a multi-page response.
    Avoid using the pagination cursor returned from one function as the parameter for another.
    """
    def __init__(self, value=None):
        self.__cursor = value

    def __set__(self, instance, value):
        self.__cursor = value

    def __get__(self, instance, owner):
        return self.__cursor


class Games:

    cursor = Cursor()

    @staticmethod
    def get_top(after=None, before=None, first=20):
        """
        Gets games sorted by number of current viewers on Twitch, most popular first.
        :param after: Cursor for forward pagination.
        :param before: Cursor for backward pagination.
        :param first: Number of objects to return. Maximum 100. Default 20.
        :return: List of games elements and sets the cursor field with information required
         to query for more games.
        """

        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')

        if after and before:
            raise TwitchAttributeException('Provide only one pagination direction')

        url = '{}/games/top'.format(HELIX)
        params = {'after': after, 'before': before, 'first': first}
        res = API.get(url, params)
        Games.cursor = res['pagination']['cursor']
        return res

    @staticmethod
    def get_by_id(game_id):
        """
        Gets game information by game ID.
        :param game_id: Game ID. At most 100 ID  values can be specified.
        :return: A list of elements containing game data.
        """

        if not game_id:
            raise TwitchAttributeException('Must provide at least one name or ID')
        if len(game_id) > 100:
            raise TwitchAttributeException('Malformed parameter "game_id": the value must be less than or equal to 100')

        url = '{}/games'.format(HELIX)
        params = {'id': game_id}
        res = API.get(url, params)
        return res['data']

    @staticmethod
    def get_by_name(game_name):
        """
        Gets game information by game name.
        :param game_name: Game name. The name must be an exact match. At most 100 name values can be specified.
        :return: A list of elements containing game data.
        """

        if not game_name:
            raise TwitchAttributeException('Must provide at least one name or ID')
        if len(game_name) > 100:
            raise TwitchAttributeException('Must limit "game_name" to 100 or less items.')

        url = '{}/games'.format(HELIX)
        params = {'name': game_name}
        res = API.get(url, params)
        return res['data']


class Streams:

    """
    Gets information about active streams.
    Streams are returned sorted by number of current
    viewers, in descending order. Across multiple pages
    of results, there may be duplicate or missing streams,
    as viewers join and leave streams.
    """

    cursor = Cursor()

    @staticmethod
    def get_by_user_id(user_id=None, stream_type='all'):
        """
        Returns streams broadcast by one or more specified user IDs. You can specify up to 100 IDs.
        :param user_id: ID of the user who is streaming.
        :param stream_type: Stream type: "all", "live", "vodcast". Default: "all".
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if len(user_id) > 100:
            raise TwitchAttributeException('Must limit "user_id" to 100 or less items')
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException('Invalid Stream Type. Valid types are %s' % STREAM_TYPES)

        url = '{}/streams'.format(HELIX)
        params = {'user_id': user_id, 'type': stream_type}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_by_user_name(user_name=None, stream_type='all'):
        """
        Returns streams broadcast by one or more specified user login names. You can specify up to 100 names.
        :param user_name: Login name of the user who is streaming.
        :param stream_type: Stream type: "all", "live", "vodcast". Default "all".
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if len(user_name) > 100:
            raise TwitchAttributeException('Must limit "user_name" to 100 or less items')
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException('Invalid Stream Type. Valid types are %s' % STREAM_TYPES)

        url = '{}/streams'.format(HELIX)
        params = {'user_login': user_name, 'type': stream_type}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_by_game_id(game_id=None, stream_type='all'):
        """
        Returns streams broadcasting one or more specified game IDs. You can specify up to 100 IDs.
        :param game_id: ID of the game being streamed.
        :param stream_type: Stream type: "all", "live", "vodcast". Default "all".
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if len(game_id > 100):
            raise TwitchAttributeException('Must limit "game_id to 100 or less items')
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException('Invalid Stream Type. Valid types are %s' % STREAM_TYPES)

        url = '{}/streams'.format(HELIX)
        params = {'game_id': game_id, 'type': stream_type}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_by_lang(language=None, stream_type='live', first=20):
        """
        Returns streams broadcasting one or more specified game IDs. You can specify up to 100 IDs.
        :param language: Stream language. You can specify up to 100 languages.
        :param stream_type: Stream type: "all", "live", "vodcast". Default: "all".
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')
        if language > 100:
            raise TwitchAttributeException()
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException('Invalid Stream Type. Valid types are %s' % STREAM_TYPES)

        url = '{}/streams'.format(HELIX)
        params = {'language': language, 'type': stream_type, 'first': first}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_live_streams(first=20):
        """
        Returns lives streams sorted by number of current viewers in decending order.
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')

        url = '{}/streams'.format(HELIX)
        params = {'type': STREAM_TYPE_LIVE, 'first': first}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_by_stream_type(stream_type='all', first=20):
        """
        Returns streams broadcasting specified stream type.
        :param stream_type: Stream type: "all", "live", "vodcast". Default: "all".
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException('Invalid Stream Type. Valid types are %s' % STREAM_TYPES)

        url = '{}/streams'.format(HELIX)
        params = {'type': stream_type, 'first': first}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_by_community(community_id=None, stream_type='live', first=20):
        """
        Returns streams in a specified community ID.
        :param community_id: Community ID of the stream. You can specify up to 100 IDs.
        :param stream_type: Stream type: "all", "live", "vodcast". Default: "all".
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams.
        """

        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')
        if len(community_id) > 100:
            raise TwitchAttributeException()
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException('Invalid Stream Type. Valid types are %s' % STREAM_TYPES)

        url = '{}/streams'.format(HELIX)
        params = {'community_id': community_id, 'type': stream_type, 'first': first}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_streams(after=None, before=None, community_id=None, first=20, game_id=None, language=None,
                    stream_type='all', user_id=None, user_login=None):
        """
        Gets information about active streams.
        :param after: Cursor for forward pagination.
        :param before: Cursor for backward pagination.
        :param community_id: Community ID of the user. You can specify up to 100 IDs.
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :param game_id: ID of the game being streamed. You can specify up to 100 IDs.
        :param language: Stream language. You can specify up to 100 languages.
        :param stream_type: Stream type: "all", "live", "vodcast". Default: "all".
        :param user_id: ID of the user streaming.
        :param user_login: Loging name of the user streaming.
        :return: List of elements containing stream information and sets the cursor field with information required
         to query for more streams
        """

        if before and after:
            raise TwitchAttributeException()

        if len(community_id) > 100:
            raise TwitchAttributeException("community_id: Too many values. Max 100")
        elif first > 100:
            raise TwitchAttributeException("first: Too many values. Max 100")
        elif len(game_id) > 100:
            raise TwitchAttributeException("game_id: Too many values. Max 100")
        elif len(language) > 100:
            raise TwitchAttributeException("language: Too many values. Max 100")
        elif len(user_id) > 100:
            raise TwitchAttributeException("user_id: Too many values. Max 100")
        elif len(user_login) > 100:
            raise TwitchAttributeException("user_login: Too many values. Max 100")

        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException()

        url = '{}/streams'.format(HELIX)
        params = {'after': after, 'before': before, 'community_id': community_id, 'first': first, 'game_id': game_id,
                  'language': language, 'stream_type': stream_type, 'user_id': user_id, 'user_login': user_login}

        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']


class Users:
    """
    Gets information about one or more specified Twitch users. Users are identified by optional user IDs and/or
    login name.
    """

    cursor = Cursor()

    @staticmethod
    def get_user_by_id(user_id=None):

        """
        Returns user information by ID.
        :param user_id: User ID. Multiple user IDs can be specified. Limit: 100.
        :return: A list containing user-information related elements.
        """

        if len(user_id) > 100:
            raise TwitchAttributeException()

        url = '{}/users'.format(HELIX)
        params = {'id': user_id}
        res = API.get(url, params)
        return res['data']

    @staticmethod
    def get_user_by_name(user_login=None):
        """
        Returns user information by login name.
        :param user_login: User login name. Multiple login names can be specified. Limit: 100.
        :return: A list containing user-information related elements.
        """

        if len(user_login) > 100:
            raise TwitchAttributeException()

        url = '{}/users'.format(HELIX)
        params = {'login': user_login}
        res = API.get(url, params)
        return res['data']

    @staticmethod
    def user_follows_user(from_id=None, to_id=None):
        """
        Gets information on follow relationships between two Twitch users.
        :param from_id: ID of the user following the "to_id" user.
        :param to_id: ID of the user being followed by the "from_id" user.
        :return: A list of follow relationship elements and sets the cursor
         field with information required to query for more follow information.
        """
        if not to_id and from_id:
            raise TwitchAttributeException('Must supply both "to_id" and "from_id" users.')

        url = '{}/users/follows'.format(HELIX)
        params = {'from_id': from_id, 'to_id': to_id}
        res = API.get(url, params)
        if res['total']:
            return res
        return False

    @staticmethod
    def get_following(after=None, before=None,
                      first=20, to_id=None):
        """
        Returns information on users who are following the "to_id" user.
        :param after: Cursor for forward pagination.
        :param before: Cursor for backward pagination.
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :param to_id: ID of the followed user.
        :return: A list of follow relationship elements and sets the cursor
         field with information required to query for more follow information.
        """

        if not to_id:
            raise TwitchAttributeException('Must supply a "to_id" user.')
        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')

        url = '{}/users/follows'.format(HELIX)
        params = {'after': after, 'before': before, 'first': first, 'to_id': to_id}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']

    @staticmethod
    def get_followers(after=None, before=None,
                      first=20, from_id=None):
        """
        Returns information on users who are being followed by the "from_id" user.
        :param after: Cursor for forward pagination.
        :param before: Cursor for backward pagination.
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :param from_id: ID of the following user.
        :return: A list of follow relationship elements and sets the cursor
         field with information required to query for more follow information.
        """
        if not from_id:
            raise TwitchAttributeException('Must supply a "from_id" user.')
        if first > 100:
            raise TwitchAttributeException('Malformed parameter "first": the value must be less than or equal to 100')
        url = '{}/users/follows'.format(HELIX)
        params = {'after': after, 'before': before, 'first': first, 'from_id': from_id}
        res = API.get(url, params)
        Streams.cursor = res['pagination']['cursor']
        return res['data']


class TwitchException(Exception):
    """Class for Twitch API non-exit exceptions."""
    pass


class TwitchAuthException(TwitchException):
    """Class for Twitch API Authorization exceptions."""
    pass


class TwitchAttributeException(TwitchException):
    """Class for Twitch API function parameter exceptions."""
    pass
