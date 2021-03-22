from database import Database
import config
import requests
import base64
import copy
import datetime
"""
Using client Credential flow authorization from Spotify API.
"""


class Spotify_API():
    def __init__(self, client_id, client_secret, db):
        self.db = db
        self.c_id = client_id
        self.c_secret = client_secret
        auth_str = '{}:{}'.format(client_id, client_secret)
        base64_auth = base64.b64encode(auth_str.encode()).decode()

        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={'grant_type': 'client_credentials'},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic {}'.format(base64_auth)

            }).json()
        print(response)
        self.access_header = {'Authorization': 'Bearer {}'.format(response['access_token']),
                              'Content-Type': 'application/json'}

    def refresh_token(self):
        """ Grab a new authentication token.
        """
        try:
            auth_str = '{}:{}'.format(self.c_id, self.c_secret)
            base64_auth = base64.b64encode(auth_str.encode()).decode()

            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={'grant_type': 'client_credentials'},
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic {}'.format(base64_auth)

                }).json()
            print(response)
            self.access_header = {'Authorization': 'Bearer {}'.format(response['access_token']),
                                  'Content-Type': 'application/json'}
        except:
            pass

    def spotify_search(self, artist):
        """Make a call to Spotify API and seach for an artist.

        Return artist JSON result. Used for auto-complete functionality.
        """

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=self.access_header,
            params={
                'type': "artist",
                'limit': 3,
                'q': artist}
        ).json()
        if not response['artists']['items']:
            return None
        return response['artists']['items'][0]

    def new_artist(self, artist, channel_id):
        items = self.spotify_search(artist)
        self.db.new_artist(
            items['id'],
            items['name'],
            self.check_artist_count(items['id'], 0, channel_id),
            items['images'][2]['url'],
            channel_id)
        print("TRY AGAIN ")
        return items['name']

    def sort_by_date(self, list):
        try:
            return sorted(list, key=lambda x: datetime.datetime.strptime(x['release_date'], '%Y-%m-%d') if x['release_date_precision'] == 'day' else datetime.datetime.strptime(x['release_date'], '%Y'), reverse=True)
        except:
            print(list)
            return sorted(list, key=lambda x: datetime.datetime.strptime(x['release_date'], '%Y')/print(x['release_date']), reverse=True)

    def check_artist_count(self, spotify_id, curr_count, channel_id, create=True):
        response = requests.get('https://api.spotify.com/v1/artists/{}/albums'.format(spotify_id),
                                headers=self.access_header,
                                params={
                                    'include_groups': 'album,single', 'market': 'US', 'limit': 50}
                                ).json()
        # creating an artist return initial count value
        if create:
            return response['total']

        # detection of new track
        else:

            # if total track is > than what is in database assume there is a new release
            if(response['total'] > curr_count):
                print("New release")
                # sort results by date. Assumes < 50 new releases and that most recent releases is within the first 50 results returned by Spotify
                result_list = self.sort_by_date(response['items'])
                new_releases = []
                item = {}

                # only return response['total'] - curr_count results
                for i in range(int(response['total']) - curr_count):
                    if result_list[i]['album_group'] == 'album':  # new Album
                        item = {
                            'type': 'Album',
                            'name': result_list[i]['name'],
                            'release_date': result_list[i]['release_date'],
                            'image': result_list[i]['images'][2]['url'],
                            'artist': result_list[i]['artists'][0]['name'],
                            'channel_id': channel_id
                        }

                    else:  # new Single
                        item = {
                            'type': 'Single',
                            'name': result_list[i]['name'],
                            'artist': result_list[i]['artists'][0]['name'],
                            'release_date': result_list[i]['release_date'],
                            'image': result_list[i]['images'][2]['url'],
                            'link': result_list[i]['external_urls']['spotify'],
                            'channel_id': channel_id
                        }

                    new_releases.append(copy.deepcopy(item))
                if new_releases == []:
                    return None
                self.db.update_count(spotify_id, response['total'])
                return new_releases

    def checkArtist(self):
        self.refresh_token()
        print('checking....')

        # for list of artist check tracks and total counts counts are the same good
        # check for updates
        items = self.db.get_id_count()
        results = []
        for id, count, channel_id in items:
            print(id, count)
            result = self.check_artist_count(id, count, channel_id, False)
            if result:
                results += result
            print("FINISHED")
        if results == []:
            return None
        return results

    def get_artists(self, channel_id):
        return self.db.get_artists(channel_id)
