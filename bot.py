import discord
from discord.ext import commands
import asyncio
import config


def create_bot(spotify_api):
    """Wrapper for discord bot."""
    bot = commands.Bot(command_prefix='-')

    async def check_new():
        """ Function that invokes check in Spotify API and database for new releases.
        """
        embed = discord.Embed(
            title="New Release in Spotify!",
            color=0xff0000,
            description=''
        )
        while True:
            new_releases = spotify_api.checkArtist()
            if new_releases != None:
                for new_release in new_releases:
                    general_channel = bot.get_channel(
                        int(new_release['channel_id']))
                    print(new_release)
                    embed = discord.Embed(
                        title=new_release['name'], description=new_release['artist'], color=0xff0000)
                    embed.set_thumbnail(url=new_release['image'])
                    embed.set_author(
                        name=f"{new_release['artist']} has a new {new_release['type']} on Spotify!")
                    embed.set_footer(
                        text=f"Released on {new_release['release_date']}")
                    await general_channel.send(embed=embed)
            await asyncio.sleep(3600)

    @ bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

        # schedule check for new releases when bot is logged in
        bot.loop.create_task(check_new())

    @ bot.command()
    async def add(ctx, artist):
        status = spotify_api.new_artist(artist, str(ctx.channel.id))
        print(ctx.channel.id)
        if status:
            await ctx.send(f'Added {status} to watchlist')
        else:
            await ctx.send(f'Could not find artist {artist}')

    @ bot.command()
    async def show(ctx):
        # show artists followed on channel
        artist_list = spotify_api.get_artists(str(ctx.channel.id))
        send = "```\n ----Artists you are following----"
        for artist in artist_list:
            print(artist)
            send += artist['name']
            send += '\n'
        send += "```"
        await ctx.send(send)

    bot.run(config.BOT_TOKEN)
