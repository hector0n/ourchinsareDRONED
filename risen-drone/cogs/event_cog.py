import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands

from globals import EDIBLE_EGGS, EGG_EATER, EVENTS, EXTRA_ROLES, MAX_EGGS, MEGA_SECRET_LAUNCHER, MORPHABLE_ROLES, BUTTONS, BOT_BLACKLIST, SPECIAL_ROLES
from rated import ADD_ROLES, DEFER, FOLLOWUP, INTERACTION, REMOVE_ROLES, SEND
from database import check_full_egg_conditions, check_perfect_egg_conditions, delete_entry_by_value, list_decoded_entries
from utility import launch_egg, command_check

class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="launch", description="Launch an egg with your trusty Egg Launcher!")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Max", value="max"),
        discord.app_commands.Choice(name="Full", value="full"),
        discord.app_commands.Choice(name="Perfect", value="perfect"),
        discord.app_commands.Choice(name="Mega Secret", value="mega"),
        discord.app_commands.Choice(name="Admin (Admins Only)", value="admin"),
        discord.app_commands.Choice(name="??? (??? Only)", value="someone"),
    ])
    # , priority: discord.Member = None
    async def launch(self, interaction: discord.Interaction, type: str = None):
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        usr = interaction.user
        ch = interaction.channel

        await DEFER(interaction)

        try:
            if (not EVENTS["Easter"] and ch.id != 813882658156838923) or type == "someone":
                await FOLLOWUP(f"{usr.mention} threw the Sleazy Egg! ...But it fell on the ground and broke.", interaction)
                return

            from views import ButtonEgg_Throw
            view = ButtonEgg_Throw(timeout=30)
            view.thrower = usr.id
            view.disabled = False
            view.type = None
            # view.priority = priority.id if priority else None

            if SPECIAL_ROLES["The Illuminati"][0] in usr.roles and type == "the illuminati":
                BUTTONS["easterStaffStatus"] = True
                view.type = "The Illuminati"
            elif 1 == 1 and type == "someone":
                BUTTONS["easterStaffStatus"] = True
                view.type = "???"
            else:
                if BUTTONS["easterStatus"]:
                    await FOLLOWUP("The Egg Launcher is charging. This stuff takes time.", interaction)
                    return
                
                BUTTONS["easterStatus"] = True

                for role in reversed(usr.roles):
                    if role.name.title() in MAX_EGGS:
                        view.type = role.name
                        break

                if type:
                    if type.title() == "Max" and str(view.thrower) in list_decoded_entries(f"{view.type.title()} Egg"):
                        view.type = MAX_EGGS[view.type.title()]
                    elif type.title() == "Max":
                        await FOLLOWUP("To launch that egg, you must first have the base one.", interaction)
                        BUTTONS["easterStatus"] = False
                        return

                    if (type.title() == "Full" and check_full_egg_conditions(usr)):
                        view.type = type.title()
                    elif type.title() == "Full":
                        await FOLLOWUP("Aren't you full of yourself? Or perhaps not full enough.", interaction)
                        BUTTONS["easterStatus"] = False
                        return

                    if (type.title() == "Perfect" and check_perfect_egg_conditions(usr)):
                        view.type = type.title()
                    elif type.title() == "Perfect":
                        await FOLLOWUP(f"Nobody's perfect, but you aren't even close.", interaction)
                        BUTTONS["easterStatus"] = False
                        return
                    
                    if (type.title() == "Mega" and (MEGA_SECRET_LAUNCHER["user"] == usr.id or MEGA_SECRET_LAUNCHER["user"] == None)):
                        view.type = "Mega Secret"
                    elif type.title() == "Mega":
                        await FOLLOWUP("The Mega Secret Egg Launcher can only be used once, and by the person who found it. Maybe that person is you... someday.", interaction)
                        BUTTONS["easterStatus"] = False
                        return
                    
            if random.randint(1, 11) == 1:
                view.type = "Super Secret"

            if view.type == None:
                await FOLLOWUP("The Egg Launcher is confused... It doesn't know which Egg to launch!", interaction)
                BUTTONS["easterStatus"] = False
                return
            
            if view.type == BUTTONS["easterLast"]:
                await FOLLOWUP("The Egg Launcher refuses to launch the same egg twice in a row! It seems to be craving some variety.", interaction)
                BUTTONS["easterStatus"] = False
                return
                    
            BUTTONS["easterLast"] = view.type
            view.channel = ch
            view.toolate = True
            viewMsg = ""

            if view.type == "Super Secret":
                viewMsg = f"{usr.mention}'s Egg Launcher malfunctioned and threw a strange looking egg!"
            else:
                viewMsg = f"{usr.mention} threw the {view.type} Egg!"

            view.message = await FOLLOWUP(viewMsg, interaction, False, view)
            await asyncio.sleep(1.7)
            await view.wait()
            await view.too_late()

            if BUTTONS["easterStatus"] and not BUTTONS["easterStaffStatus"]:
                await asyncio.sleep(BUTTONS["easterTimer"])
                await SEND(ch, "The egg launcher is ready!")
                BUTTONS["easterStatus"] = False

            if BUTTONS["easterStaffStatus"]:
                BUTTONS["easterStaffStatus"] = False
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/launch`: {exc}", interaction)
            BUTTONS["easterStatus"] = False
            BUTTONS["easterStaffStatus"] = False
            raise

    @discord.app_commands.command(name="talk", description="I will relay your message to the person of your choice.")
    @discord.app_commands.choices(who=[
        discord.app_commands.Choice(name="Janitor", value="janitor"),
        discord.app_commands.Choice(name="Broken Drone", value="bd"),
        discord.app_commands.Choice(name="Sleazel", value="sleazel"),
    ])
    async def talk(self, interaction: discord.Interaction, who: str):
        stopMsg = command_check(interaction)
        if stopMsg:
            await INTERACTION(interaction, stopMsg, True)
            return

        usr = interaction.user
        ch = interaction.channel

        await DEFER(interaction)

        try:
            if who == "janitor":
                await FOLLOWUP("Janitor is a bit on the edge due to the excessive amount of eggs they have to clean, you'd better not disturb them.", interaction)
            elif who == "ad":
                await FOLLOWUP("...Me? You can speak to me anytime.", interaction)
            elif who == "sleazel":
                await FOLLOWUP("I asked Sleazel and they said they will get back to you soon.", interaction)
            elif who == "archon":
                await FOLLOWUP("Archon says they can tell you, but a portal must be made to the Aether first.", interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/talk`: {exc}", interaction)
            raise