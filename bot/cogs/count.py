import discord

import config as c
import datastoragefunctions as dsf
from discord.ext import commands

class Count(commands.Cog):
    """
    Cog for counting channel functionality.
    """
    def __init__(self, bot):
        self.bot = bot 
        self._last_member = None
    
    @commands.command()
    async def record(self, ctx):
        """
        Shows the current count channel record.
        """
        print(f"User {ctx.author.id} used record. args: None")
        record = dsf.dataStorageRead()["count"]["record"]
        await ctx.send(f"The current count channel record is {record}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Function for handling counting channel messages and functions
        """
        if message.author.bot: return # bots could interfere
        if message.channel.id != c.counting_channel: return # this handler is only for counting channel

        print(f"User {message.author.id} triggered cogs.Count.on_message(). message: {message.content}")
        c_channel = message.channel # counting channel
        complete_data = dsf.dataStorageRead()
        lc_data = complete_data["count"]['last-count'] # last count data
        userdata = dsf.userStorage("r", message.author.id)

        await message.delete() # Security measure to prevent people from unsending their message & breaking count 

        fail_code = None
        if not message.content.startswith(str(lc_data['number'] + 1)): fail_code = 1 # wrong next number fail
        if message.author.id == lc_data['member']: fail_code = 2 # same member twice fail

        if fail_code is not None:
            print(f"User {message.author.id} has a non-zero fail_code. fail_code: {fail_code}")
            reason = {
                1: "That wasn't the next number!", 
                2: "You aren't allowed to send two numbers in a row."
            }.get(fail_code) # Fail code translator

            embed = discord.Embed(title = reason, description = f"The next number was {(lc_data['number'] + 1)}. Restarting at 1.", color = 0x000000) \
            .set_author(name = message.author.name, icon_url = message.author.avatar_url) \
            .set_thumbnail(url = message.author.avatar_url) \
            .set_footer(text = c.embed_footer_text) # Fail embed

            complete_data["count"]["last-count"] = { "number": 0, "member": 0 } # Reset last-count

            if lc_data['number'] > complete_data["count"]["record"]:
                difference = lc_data['number'] - complete_data["count"]["record"]
                embed.add_field(name = "This was a new record!", value = f"It beat the previous one by {difference}.")
                complete_data["count"]["record"] = lc_data["number"]
            
            userdata["count"]["fails"] += 1    
        else:
            lc_data['number'] += 1 # Increment number
            lc_data['member'] = message.author.id # Set last user
            userdata["count"]["number"] += 1 
            complete_data["count"]["last-count"] = lc_data # Save last count data to complete data

            embed = discord.Embed(title = "Count", description = message.content, color = c.embed_color) \
            .set_author(name = message.author.name, icon_url = message.author.avatar_url) \
            .set_thumbnail(url = message.author.avatar_url) \
            .set_footer(text = c.embed_footer_text) # Construct an embed for the correct number 

        dsf.userStorage("w", message.author.id, data = userdata) # Write updated userdata
        dsf.dataStorageWrite(complete_data) # Write the complete data
        await c_channel.send(embed = embed) # Send to count channel
