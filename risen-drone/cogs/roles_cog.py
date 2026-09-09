import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import datetime
from roles import DemorphFrom, MorphTo, MorphTo, SubTo, UnsubFrom
from utility import send_followup, command_check
from globals import EVENTS, EXTRA_ROLES, PING_ROLES, RIG_LIST, MORPHABLE_ROLES, SPECIAL_ROLES, EX_CLIMBERS, MAX_EGGS, BOT_BLACKLIST
from rated import DEFER, FOLLOWUP, INTERACTION, SEND, REMOVE_ROLES, ADD_ROLES
from database import list_decoded_entries, add_entry_with_check