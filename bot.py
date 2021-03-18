import discord
from discord.ext import commands
import asyncio

artist_list = []
song_list = ['summer', 'let it be', 'run', 'sanctuary']
client = discord.Client()


def create_bot(spotify_api):
    bot = commands.Bot(command_prefix='-')

    async def check_new():  # 819320412118581311

        embed = discord.Embed(
            title="New Release in Spotify!",
            color=0xff0000,
            description=''
        )
        while True:
            new_releases = spotify_api.checkArtist()
            if new_releases != None:
                # new_releases shoould have a channel ID?
                # for channel in channels:
                #     try:
                #         await channel.send(embed=embed)
                #         break
                #     except:
                #         print('unable to send in', channel, guild
                # for list of new releases get the appropriate channel id to send it to  create embed then send
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
            await asyncio.sleep(10)

    @ bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

        bot.loop.create_task(check_new())

    @ bot.command()
    async def showlist(ctx):
        """Adds two numbers together."""
        await ctx.send(artist_list)

    @ bot.command()
    async def add(ctx, artist):
        print("DSADSSSSS)")
        status = spotify_api.new_artist(artist, str(ctx.channel.id))
        print(ctx.channel.id)
        if status:
            await ctx.send(f'Added {status} to watchlist')
            # add here
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

    bot.run('ODE5MzI3OTA2NzE0ODc3OTUy.YElAkw.UlunLmRovawVBe77brHWkbje6n0')
