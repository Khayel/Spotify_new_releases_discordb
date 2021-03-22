import config
from spotify import Spotify_API
from bot import create_bot
from database import Database

if __name__ == "__main__":
    api = Spotify_API(config.CLIENT_ID,
                      config.CLIENT_SECRET, db=Database())
    create_bot(api)
