from nextcord.ext import commands
from nextcord import Intents, SlashOption, ButtonStyle, Interaction, ui, Client, ClientUser, guild
from key import TOKEN
import os
import discord
from Database import get_Tamagotchi, set_Tamagotchi
from Tamagotchi import Tamagotchi
from Stats import update_stats
import time
tama = None

intents = Intents.all()
bot = commands.Bot(command_prefix="$", intents = intents)

@bot.slash_command(
    name = 'reload',
    description = "Reload a Cog",
    guild_ids = [972309726425653249]
)
async def reload(interaction, extension: str = SlashOption(
    name = "extension",
    description = "Cog name",
    required = True,
),
):
    bot.reload_extension(f"cogs.{extension}")

#######################################################################################################
class StatusView(ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.value = None
        self.Image = None

    @ui.button(label='Feed', style = ButtonStyle.green)
    async def feedButton(self, button, interaction):
        self.value = "feed"
        for child in self.children:
            child.disabled = True
        await interaction.edit(view=self)
        self.stop()

    @ui.button(label='Pet', style=ButtonStyle.green)
    async def petButton(self, button, interaction):
        self.value = "pet"
        for child in self.children:
            child.disabled = True
        await interaction.edit(view=self)
        self.stop()

    @ui.button(label='Wash', style=ButtonStyle.green)
    async def washButton(self, button, interaction):
        self.value = "wash"
        for child in self.children:
            child.disabled = True
        await interaction.edit(view=self)
        self.stop()

class SetupView(ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.value = None

    @ui.button(label='Yes', style=ButtonStyle.blurple)
    async def resetButtonYes(self, button, interaction):
        self.value = "reset"
        for child in self.children:
            child.disabled = True
        await interaction.edit(view=self)
        self.stop()

    @ui.button(label='No', style=ButtonStyle.blurple)
    async def resetButtonNo(self, button, interaction):
        self.value = "noReset"
        for child in self.children:
            child.disabled = True
        await interaction.edit(view=self)
        self.stop()

@bot.command()
async def check(ctx: commands.Context):
    """Displays the status of the Tamagotchi"""
    await ctx.send(f"============================================")
    id = str(ctx.message.author.id)
    tama = get_Tamagotchi(id)
    if (tama.name != "Error"):
        update_stats(tama)
        time.sleep(1)
        if (tama.state == "Dead" or tama.hunger == 0):
            await ctx.send(f"Your Tamagotchi {tama.name} has died from starvation.")
            with open(tama.image, 'rb') as fp:
                await ctx.send(file=discord.File(tama.image))
            set_Tamagotchi(id, Tamagotchi("Error"))
            return
        if(tama.state == 'sick' or tama.hygiene == 0):
            await ctx.send(f"Your Tamagotchi {tama.name} has died from sickness.")
            with open(tama.image, 'rb') as fp:
                await ctx.send(file=discord.File(tama.image))
            set_Tamagotchi(id, Tamagotchi("Error"))
            return
        if (tama.name == "Away" or tama.happy == 0):
            await ctx.send(f"Your Tamagotchi {tama.name} has run away from sadness.")
            with open(tama.image, 'rb') as fp:
                await ctx.send(file=discord.File(tama.image))
            set_Tamagotchi(id, Tamagotchi("Error"))
            return
        set_Tamagotchi(id, tama)
        view = StatusView()
        await ctx.send(f"Status of your Tamagotchi - {tama.name}:")
        await ctx.send(f"- Age: {int(tama.age)}")



        await ctx.send(f"- Hunger: {int(tama.hunger)} - " + ':pizza: '*(int(tama.hunger // 10)))
        await ctx.send(f"- Happiness: {int(tama.happy)} - " + ':smile: '*(int(tama.happy // 10)))
        await ctx.send(f"- Hygiene: {int(tama.hygiene)} - " + ':shower: '*(int(tama.hygiene // 10)))

        # put picture here
        with open(tama.image, 'rb') as fp:
            await ctx.send(file=discord.File(tama.image))
        await ctx.send(view=view)

        if ((tama.state != "Dead")and(tama.state != "Away")):
            await view.wait()
            if view.value is None:
                print("Timed out")
            elif view.value == "feed":
                await ctx.send(f"- {ctx.message.author} fed {tama.name}!")
                tama.feed()
                update_stats(tama)
                set_Tamagotchi(id, tama)
                ctx.command = bot.get_command("check")
                await bot.invoke(ctx)
            elif view.value == "pet":
                await ctx.send(f"- {ctx.message.author} pet {tama.name}!")
                tama.play()
                update_stats(tama)
                set_Tamagotchi(id, tama)
                ctx.command = bot.get_command("check")
                await bot.invoke(ctx)
            elif view.value == "wash":
                await ctx.send(f"- {ctx.message.author} washed {tama.name}!")
                tama.clean()
                update_stats(tama)
                set_Tamagotchi(id, tama)
                ctx.command = bot.get_command("check")
                await bot.invoke(ctx)
            else:
                print("Cancelled...")
    else:
        await ctx.send("Make a Tamagotchi first using $setup!")


@bot.command()
async def setup(ctx: commands.Context, name):
    if name.lower() == "error":
        await ctx.send('Sorry! That name is not allowed. Try using a different name')
        return
    id = str(ctx.message.author.id)
    tama = get_Tamagotchi(id)
    view = SetupView()
    await ctx.send("Do you want to setup a new Tamagotchi?")
    await ctx.send(view=view)
    await view.wait()
    if (view.value == "reset"):
        if (tama.name != 'Error'): #if your Tom exists
            await ctx.send(f"You already have a Tamagotchi named {tama.name}!")
            await ctx.send("Would you like to setup a new one? (Note that the previous one will flee)")
            view2 = SetupView()
            await ctx.send(view=view2)
            await view2.wait()
            if(view2.value == "reset"): #if your Tom exists but you wnat to
                ## prompt to input name
                await ctx.send("Creating your new Tamagotchi...")
                set_Tamagotchi(id, Tamagotchi(name))
                await ctx.send(f"Here's your new Tamagotchi named {get_Tamagotchi(id).name}")
                ctx.command = bot.get_command("check")
                await bot.invoke(ctx)
            elif (view2.value == "noReset"): #if your Tom exists and you dont want to reset
                await ctx.send(f"Request cancelled.")
        else: #if your Tom doesnt exist
            await ctx.send("Creating your new Tamagotchi....")
            set_Tamagotchi(id, Tamagotchi(name))
            await ctx.send(f"Here's your new Tamagotchi named {get_Tamagotchi(id).name}")
            ctx.command = bot.get_command("check")
            await bot.invoke(ctx)
    elif (view.value == "noReset"): #If you dont want to create a new Tom
        await ctx.send(f"Request cancelled.")

#######################################################################################################


bot.run(TOKEN)
