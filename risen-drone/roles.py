import random

from rated import *
from globals import *
from database import *
from utility import send_followup

def PrepareRoles(roles):
    for role in roles:
        #morphable
        if role.name in MORPHABLE_ROLES:
            MORPHABLE_ROLES[role.name][0] = role
            continue
        #chat killer
        if role.id == EXTRA_ROLES['ckr']:
            EXTRA_ROLES['ckr'] = role
            SPECIAL_ROLES["Ultimate"][0] = role
            continue
        #necromancer - gone, reduced into atoms
        # if role.id == EXTRA_ROLES['necromancer']:
        #     EXTRA_ROLES['necromancer'] = role
        #     SPECIAL_ROLES['Necromancer'][0] = role
        #     continue
        #discord admin
        if role.name == 'The Illuminati':
            SPECIAL_ROLES['The Illuminati'][0] = role
            continue
        #basically Splicer, roles with color and icons
        if role.name in APPROVED_ROLES:
            APPROVED_ROLES[role.name] = role

               
#chat killer function
# async def WAIT_FOR_CHAT_KILLER(msg):
#     if msg.channel == CHANNELS["general"]:
#         CHAT_KILLER['last'] = msg.created_at
        
#         #wait 2 hours
#         await asyncio.sleep(CHAT_KILLER['wait'])
        
#         if msg.created_at == CHAT_KILLER['last'] and not EXTRA_ROLES['ckr'] in msg.author.roles:
#             #thirdkill = None # Nick - i have removed this, seems to be unused - sleazel #Sleazel - it seems i have used it for something and then forgot to delete - rolo
#             CHAT_KILLER['reviveChat'] = True
#             NECROMANCY['awarded'] = False
#             print("new chat killer")
#             await SEND(CHANNELS["general"],msg.author.mention + " do not worry, I can talk with you if no one else will.")
#             UPDATE_CKR()
#             for member in EXTRA_ROLES['ckr'].members:
#                 await REMOVE_ROLES(member,EXTRA_ROLES['ckr'])
#             await asyncio.sleep(5)
#             await ADD_ROLES(msg.author,EXTRA_ROLES['ckr'])
#             await asyncio.sleep(1)

#             if EXTRA_ROLES['ckr'].name != "Ultimate Chat Killer":
#                 await EDIT_ROLE(EXTRA_ROLES['ckr'], "Ultimate Chat Killer", "New chat killer. They are not Professionals yet.")
#             return

#         elif msg.created_at == CHAT_KILLER['last'] and EXTRA_ROLES['ckr'] in msg.author.roles:
#             CHAT_KILLER['reviveChat'] = True

#             if EXTRA_ROLES['ckr'].name != "Ultimate Chat Killer":
#                 NECROMANCY['awarded'] = False
#                 await SEND(CHANNELS["general"], msg.author.mention + " this is infinitely saddening. Nobody wants to talk with you.")
#                 await asyncio.sleep(1)

#                 await EDIT_ROLE(EXTRA_ROLES['ckr'], "The Awkward One", "Awkward.")

#             if EXTRA_ROLES['ckr'].name == "Ultimate Chat Killer":
#                 NECROMANCY['awarded'] = False
#                 await SEND(CHANNELS["general"], msg.author.mention + " I must insist. I am here for you if you wish.")
#                 await asyncio.sleep(1)

#                 await EDIT_ROLE(EXTRA_ROLES['ckr'], "Professional Chat Murderer", "Yikes, they have killed the chat again.")
      
    
