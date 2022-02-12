# Spotify_new_releases_discordb
A discord bot that allows a server to add to a lists of artists. When an artist releases a song or album in Spotify, the bot will notify the channel that there has been a new release in spotify

Test out the bot [here](https://discord.com/api/oauth2/authorize?client_id=819327906714877952&permissions=2048&scope=bot)



Stack - Python, Discord.py, and SQlite database.

Commands
- add <artist> - add an artist to the watchlist in spotify. This command features an auto-complete using Spotify's search endpoint.
- show - displays a list of artist currently being watched for that channel.
- delete <artist> - remove artist from watchlist

Learned
- discord.py bot API library
- async programming
