from highrise import BaseBot, __main__
from highrise.models import (User, Position,
                              GetMessagesRequest,GetRoomPrivilegeRequest, GetWalletRequest,AnchorPosition, 
                              GetUserOutfitRequest,GetInventoryRequest, GetBackpackRequest,GetRoomUsersRequest, 
                              GetConversationsRequest,CurrencyItem, Item, Reaction, SessionMetadata,SetOutfitRequest)
import asyncio
import random
import json  # Import JSON for file handling
from datetime import datetime, timezone, timedelta
import logging
import os
from collections import deque
import re
from typing import Any, Dict, Union
from typing import List
from pathlib import Path
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define emote list
emote_list = {
    "model": {
        "id": "emote-model",
        "duration": 6.490173,
        "is_free": True
    },
    "1": {
        "id": "emote-model",
        "duration": 6.490173,
        "is_free": True
    },
    "dont start now": {
        "id": "dance-tiktok2",
        "duration":  10.392353,
        "is_free": True
    },
    "2": {
        "id": "dance-tiktok2",
        "duration":  10.392353,
        "is_free": True
    },
    "russian dance": {
        "id": "dance-russian",
        "duration":  10.252905,
        "is_free": True
    },
    "3": {
        "id": "dance-russian",
        "duration":  10.252905,
        "is_free": True
    },
    "teleport": {
        "id": "emote-teleporting",
        "duration":  11.7676,
        "is_free": True
    },
    "4": {
        "id": "emote-teleporting",
        "duration":  11.7676,
        "is_free": True
    },
    "curtsy": {
        "id": "emote-curtsy",
        "duration":  2.425714,
        "is_free": True
    },
    "5": {
        "id": "emote-curtsy",
        "duration":  2.425714,
        "is_free": True
    },
    "lets go shopping": {
        "id": "dance-shopping",
        "duration":  4.316035,
        "is_free": True
    },
    "6": {
        "id": "dance-shoppingcart",
        "duration":  4.316035,
        "is_free": True
    },
    "greedy": {
        "id": "emote-greedy",
        "duration":  4.316035,
        "is_free": True
    },
    "7": {
        "id": "emote-greedy",
        "duration":  4.316035,
        "is_free": True
    },
    "flex": {
        "id": "emoji-flex",
        "duration":  2.099351,
        "is_free": True
    },
    "8": {
        "id": "emoji-flex",
        "duration":  2.099351,
        "is_free": True
    },
    "sing along": {
        "id": "idle_singing",
        "duration":  10.260182,
        "is_free": True
    },
    "9": {
        "id": "idle_singing",
        "duration":  10.260182,
        "is_free": True
    },
    "pennys dance": {
        "id": "dance-pennywise",
        "duration":  1.214349,
        "is_free": True
    },
    "10": {
        "id": "dance-pennywise",
        "duration":  1.214349,
        "is_free": True
    },
    "bow": {
        "id": "emote-bow",
        "duration":  3.344036,
        "is_free": True
    },
    "11": {
        "id": "emote-bow",
        "duration":  3.344036,
        "is_free": True
    },
    "snowball fight": {
        "id": "emote-snowball",
        "duration":  5.230467,
        "is_free": True
    },
    "12": {
        "id": "emote-snowball",
        "duration":  5.230467,
        "is_free": True
    },
    "confused": {
        "id": "emote-confused",
        "duration":  8.578827,
        "is_free": True
    },
    "13": {
        "id": "emote-confused",
        "duration":  8.578827,
        "is_free": True
    },
    "charging": {
        "id": "emote-charging",
        "duration":  8.025079,
        "is_free": True
    },
    "14": {
        "id": "emote-charging",
        "duration":  8.025079,
        "is_free": True
    },
    "floating": {
        "id": "emote-float",
        "duration": 8.995302,
        "is_free": True
    },
    "15": {
        "id": "emote-float",
        "duration": 8.995302,
        "is_free": True
    },
    "frog": {
        "id": "emote-frog",
        "duration": 14.55257,
        "is_free": True
    },
    "16": {
        "id": "emote-frog",
        "duration": 14.55257,
        "is_free": True
    },
    "enthused": {
        "id": "idle-enthusiastic",
        "duration": 15.941537,
        "is_free": True
    },
    "17": {
        "id": "idle-enthusiastic",
        "duration": 15.941537,
        "is_free": True
    },
    "grave dance": {
        "id": "dance-weird",
        "duration": 21.556237,
        "is_free": True
    },
    "18": {
        "id": "dance-weird",
        "duration": 21.556237,
        "is_free": True
    },
    "lambi pose": {
        "id": "emote-superpose",
        "duration": 4.530791,
        "is_free": True
    },
    "19": {
        "id": "emote-superpose",
        "duration": 4.530791,
        "is_free": True
    },
    "sword fight": {
        "id": "emote-swordfight",
        "duration": 5.914365,
        "is_free": True 
    },
    "20": {
        "id": "emote-swordfight",
        "duration": 5.914365,
        "is_free": True 
    },
    "do the worm": {
        "id": "emote-snake",
        "duration": 5.262578,
        "is_free": True
    },
    "21": {
        "id": "emote-snake",
        "duration": 5.262578,
        "is_free": True
    },
    "viral groove": {
        "id": "idle-dance-tiktok4",
        "duration": 15.500708,
        "is_free": True
    },
    "22": {
        "id": "idle-dance-tiktok4",
        "duration": 15.500708,
        "is_free": True
    },
    "shuffle dance": {
        "id": "dance-tiktok10",
        "duration": 8.225648,
        "is_free": True
    },
    "23": {
        "id": "dance-tiktok10",
        "duration": 8.225648,
        "is_free": True
    },
    "cursing": {
        "id": "emoji-cursing",
        "duration": 2.382069,
        "is_free": True
    },
    "24": {
        "id": "emoji-cursing",
        "duration": 2.382069,
        "is_free": True
    },
    "raise the roof": {
        "id": "emoji-celebrate",
        "duration": 3.412258,
        "is_free": True
    },
    "25": {
        "id": "emoji-celebrate",
        "duration": 3.412258,
        "is_free": True
    },
    "emote cute": {
        "id": "emote-cute",
        "duration": 6.170464,
        "is_free": True
    },
    "26": {
        "id": "emote-cute",
        "duration": 6.170464,
        "is_free": True
    },
    "telekinesis": {
        "id": "emote-telekinesis",
        "duration": 10.492032,
        "is_free": True
    },
    "27": {
        "id": "emote-telekinesis",
        "duration": 10.492032,
        "is_free": True
    },
    "energy ball": {
        "id": "emote-energyball",
        "duration": 7.575354,
        "is_free": True
    },
    "28": {
        "id": "emote-energyball",
        "duration": 7.575354,
        "is_free": True
    },
    "maniac": {
        "id": "emote-maniac",
        "duration": 4.906886,
        "is_free": True
    },
    "29": {
        "id": "emote-maniac",
        "duration": 4.906886,
        "is_free": True
    },
    "snow angel": {
        "id": "emote-snowangel",
        "duration": 6.218627,
        "is_free": True
    },
    "30": {
        "id": "emote-snowangel",
        "duration": 6.218627,
        "is_free": True
    },
    "sweating": {
        "id": "emote-hot",
        "duration": 4.353037,
        "is_free": True
    },
    "hot": {
        "id": "emote-hot",
        "duration": 4.353037,
        "is_free": True
    },
    "31": {
        "id": "emote-hot",
        "duration": 4.353037,
        "is_free": True
    },
    "kpop dance": {
        "id": "dance-blackpink",
        "duration": 7.150958,
        "is_free": True
    },
    "32": {
        "id": "dance-blackpink",
        "duration": 7.150958,
        "is_free": True
    },
    "flirty wave": {
        "id": "emote-lust",
        "duration": 4.655965,
        "is_free": True
    },
    "33": {
        "id": "emote-lust",
        "duration": 4.655965,
        "is_free": True
    },
    "cutey": {
        "id": "emote-cutey",
        "duration": 3.26032,
        "is_free": True
    },
    "34": {
        "id": "emote-cutey",
        "duration": 3.26032,
        "is_free": True
    },
    "casual dance": {
        "id": "idle-dance-casual",
        "duration": 9.079756,
        "is_free": True
    },
    "35": {
        "id": "idle-dance-casual",
        "duration": 9.079756,
        "is_free": True
    },
    "pose 1": {
        "id": "emote-pose1",
        "duration": 2.825795,
        "is_free": True
    },
    "36": {
        "id": "emote-pose1",
        "duration": 2.825795,
        "is_free": True
    },
    "pose 3": {
        "id": "emote-pose3",
        "duration": 5.10562,
        "is_free": True
    },
    "37": {
        "id": "emote-pose3",
        "duration": 5.10562,
        "is_free": True
    },
    "pose 5": {
        "id": "emote-pose5",
        "duration": 4.621532,
        "is_free": True
    },
    "38": {
        "id": "emote-pose5",
        "duration": 4.621532,
        "is_free": True
    },
    "pose 7": {
        "id": "emote-pose7",
        "duration": 4.655283,
        "is_free": True
    },
    "39": {
        "id": "emote-pose7",
        "duration": 4.655283,
        "is_free": True
    },
    "pose 8": {
        "id": "emote-pose8",
        "duration": 4.808806,
        "is_free": True
    },
    "40": {
        "id": "emote-pose8",
        "duration": 4.808806,
        "is_free": True
    },
    "gagging": {
        "id": "emoji-gagging",
        "duration": 5.500202,
        "is_free": True
    },
    "41": {
        "id": "emoji-gagging",
        "duration": 5.500202,
        "is_free": True
    },
    "savage dance": {
        "id": "dance-tiktok8",
        "duration": 10.938702,
        "is_free": True
    },
    "42": {
        "id": "dance-tiktok8",
        "duration": 10.938702,
        "is_free": True
    },
    "say so dance": {
        "id": "dance-tiktok9",
        "duration": 11.892918,
        "is_free": True
    },
    "43": {
        "id": "dance-tiktok9",
        "duration": 11.892918,
        "is_free": True
    },
    "fashion": {
        "id": "emote-fashionista",
        "duration": 5.606485,
        "is_free": True
    },
    "44": {
        "id": "emote-fashionista",
        "duration": 5.606485,
        "is_free": True
    },
    "gravity": {
        "id": "emote-gravity",
        "duration": 8.955966,
        "is_free": True
    },
    "45": {
        "id": "emote-gravity",
        "duration": 8.955966,
        "is_free": True
    },
    "uwu": {
        "id": "idle-uwu",
        "duration": 24.761968,
        "is_free": True
    },
    "46": {
        "id": "idle-uwu",
        "duration": 24.761968,
        "is_free": True
    },
     "wrong": {
        "id": "dance-wrong",
        "duration": 12.422389,
        "is_free": True
    },
    "47": {
        "id": "dance-wrong",
        "duration": 12.422389,
        "is_free": True
    },
    "sleigh": {
        "id": "emote-sleigh",
        "duration": 11.333165,
        "is_free": True
    },
    "48": {
        "id": "emote-sleigh",
        "duration": 11.333165,
        "is_free": True
    },
    "hyped": {
        "id": "emote-hyped",
        "duration": 7.492423,
        "is_free": True
    },
    "49": {
        "id": "emote-hyped",
        "duration": 7.492423,
        "is_free": True
    },
    "zombie ": {
        "id": "emote-zombierun",
        "duration": 9.182984,
        "is_free": True
    },
    "50": {
        "id": "emote-zombierun",
        "duration": 9.182984,
        "is_free": True
    },
    "punk guitar": {
        "id": "emote-punkguitar",
        "duration": 9.365807,
        "is_free": True
    },
    "51": {
        "id": "emote-punkguitar",
        "duration": 9.365807,
        "is_free": True
    },
    "shy": {
        "id": "emote-shy",
        "duration": 4.477567,
        "is_free": True
    },
    "52": {
        "id": "emote-shy",
        "duration": 4.477567,
        "is_free": True
    },
    "icecream": {
        "id": "dance-icecream",
        "duration": 14.769573,
        "is_free": True
    },
    "53": {
        "id": "dance-icecream",
        "duration": 14.769573,
        "is_free": True
    },
    "timejump": {
        "id": "emote-timejump",
        "duration": 4.007305,
        "is_free": True
    },
    "54": {
        "id": "emote-timejump",
        "duration": 4.007305,
        "is_free": True
    },
    "touch": {
        "id": "dance-touch",
        "duration": 11.7,
        "is_free": True
    },
    "55": {
        "id": "dance-touch",
        "duration": 11.7,
        "is_free": True
    },
    "guitar": {
        "id": "idle-guitar",
        "duration": 13.229398,
        "is_free": True
    },
    "56": {
        "id": "idle-guitar",
        "duration": 13.229398,
        "is_free": True
    },
    "kawaii": {
        "id": "dance-kawai",
        "duration": 10.290789,
        "is_free": True
    },
    "57": {
        "id": "dance-kawai",
        "duration": 10.290789,
        "is_free": True
    },
    "scritchy": {
        "id": "idle-wild",
        "duration": 26.422824,
        "is_free": True
    },
    "58": {
        "id": "idle-wild",
        "duration": 26.422824,
        "is_free": True
    },
    "celebration": {
        "id": "emote-celebrationstep",
        "duration": 3.353703,
        "is_free": True
    },
    "59": {
        "id": "emote-celebrationstep",
        "duration": 3.353703,
        "is_free": True
    },
    "surprise": {
        "id": "emote-pose6",
        "duration": 5.375124,
        "is_free": True
    },
    "60": {
        "id": "emote-pose6",
        "duration": 5.375124,
        "is_free": True
    },
    "bashful": {
        "id": "emote-shy2",
        "duration": 4.989278,
        "is_free": True
    },
    "61": {
        "id": "emote-shy2",
        "duration": 4.989278,
        "is_free": True
    },
    "creepycute": {
        "id": "emote-creepycute",
        "duration": 7.902453,
        "is_free": True
    },
    "62": {
        "id": "emote-creepycute",
        "duration": 7.902453,
        "is_free": True
    },
    "pose 10": {
        "id": "emote-pose10",
        "duration": 3.989871,
        "is_free": True
    },
    "63": {
        "id": "emote-pose10",
        "duration": 3.989871,
        "is_free": True
    },
    "repose": {
        "id": "sit-relaxed",
        "duration": 1.118455,
        "is_free": True
    },
    "64": {
        "id": "sit-relaxed",
        "duration": 1.118455,
        "is_free": True
    },
    "boxer": {
        "id": "emote-boxer",
        "duration": 5.555702,
        "is_free": True
    },
    "65": {
        "id": "emote-boxer",
        "duration": 5.555702,
        "is_free": True
    },
    "creepy puppet": {
        "id": "dance-creepypuppet",
        "duration": 6.416121,
        "is_free": True
    },
    "66": {
        "id": "dance-creepypuppet",
        "duration": 6.416121,
        "is_free": True
    },
    "penguin dance": {
        "id": "dance-pinguin",
        "duration": 11.58291,
        "is_free": True
    },
    "67": {
        "id": "dance-pinguin",
        "duration": 11.58291,
        "is_free": True
    },
    "yes": {
        "id": "emote-yes",
        "duration": 2.565001,
        "is_free": True
    },
    "68": {
        "id": "emote-yes",
        "duration": 2.565001,
        "is_free": True
    },
    "tired": {
        "id": "emote-tired",
        "duration": 4.61063,
        "is_free": True
    },
    "69": {
        "id": "emote-tired",
        "duration": 4.61063,
        "is_free": True
    },
    "sad": {
        "id": "emote-sad",
        "duration": 5.411073,
        "is_free": True
    },
    "70": {
        "id": "emote-sad",
        "duration": 5.411073,
        "is_free": True
    },
    "kiss": {
        "id": "emote-kiss",
        "duration": 2.387175,
        "is_free": True
    },
    "71": {
        "id": "emote-kiss",
        "duration": 2.387175,
        "is_free": True
    },
    "tummy ache": {
        "id": "emoji-gagging",
        "duration": 5.500202,
        "is_free": True
    },
    "72": {
        "id": "emoji-gagging",
        "duration": 5.500202,
        "is_free": True
    },
    "jingle": {
        "id": "dance-jinglebell",
        "duration": 11,
        "is_free": True
    },
    "73": {
        "id": "dance-jinglebell",
        "duration": 11,
        "is_free": True
    },
    "nervous": {
        "id": "idle-nervous",
        "duration": 21.714221,
        "is_free": True
    },
    "74": {
        "id": "idle-nervous",
        "duration": 21.714221,
        "is_free": True
    },
    "toilet": {
        "id": "idle-toilet",
        "duration": 32.174447,
        "is_free": True
    },
    "75": {
        "id": "idle-toilet",
        "duration": 32.174447,
        "is_free": True
    },
    "astronaut": {
        "id": "emote-astronaut",
        "duration": 13.791175,
        "is_free": True
    },
    "76": {
        "id": "emote-astronaut",
        "duration": 13.791175,
        "is_free": True
    },
    "anime dance": {
        "id": "dance-anime",
        "duration": 8.46671,
        "is_free": True
    },
    "77": {
        "id": "dance-anime",
        "duration": 8.46671,
        "is_free": True
    },
    "ice skating": {
        "id": "emote-iceskating",
        "duration": 7.299156,
        "is_free": True
    },
    "78": {
        "id": "emote-iceskating",
        "duration": 7.299156,
        "is_free": True
    },
    "head blowup": {
        "id": "emote-headblowup",
        "duration": 11.667537,
        "is_free": True
    },
    "79": {
        "id": "emote-headblowup",
        "duration": 11.667537,
        "is_free": True
    },
    "ditzy pose": {
        "id": "emote-pose9",
        "duration": 4.583117,
        "is_free": True
    },
    "80": {
        "id": "emote-pose9",
        "duration": 4.583117,
        "is_free": True
    },
    "gift": {
        "id": "emote-gift",
        "duration": 5.8,
        "is_free": True
    },
    "81": {
        "id": "emote-gift",
        "duration": 5.8,
        "is_free": True
    },
    "push it": {
        "id": "dance-employee",
        "duration": 8,
        "is_free": True
    },
    "82": {
        "id": "dance-employee",
        "duration": 8,
        "is_free": True
    },
    "launch": {
        "id": "emote-launch",
        "duration": 11,
        "is_free": True
    },
    "83": {
        "id": "emote-launch",
        "duration": 11,
        "is_free": True
    },
    "salute": {
        "id": "emote-salute",
        "duration": 3,
        "is_free": True
    },
    "84": {
        "id": "emote-salute",
        "duration": 3,
        "is_free": True
    },
    "cute salute": {
        "id": "emote-cutesalute",
        "duration": 3,
        "is_free": True
    },
    "85": {
        "id": "emote-cutesalute",
        "duration": 3,
        "is_free": True
    },
    "fairy twirl": {
        "id": "emote-looping",
        "duration": 15,
        "is_free": True
    },
    "86": {
        "id": "emote-looping",
        "duration": 10,
        "is_free": True
    },
    "fairy float": {
        "id": "idle-floating",
        "duration": 10,
        "is_free": True
    },
    "87": {
        "id": "idle-floating",
        "duration": 10,
        "is_free": True
    },
    "smooch": {
        "id": "emote-kissing-bound",
        "duration": 5,
        "is_free": True
    },
    "88": {
        "id": "emote-kissing-bound",
        "duration": 5,
        "is_free": True
    },
    "fishing pull": {
        "id": "fishing-pull-small",
        "duration": 1,
        "is_free": True
    },
    "89":{
        "id": "fishing-pull-small",
        "duration": 1,
        "is_free": True
    },
    "fishing cast": {
        "id": "fishing-cast",
        "duration": 1.5,
        "is_free": True
    },
    "90": {
        "id": "fishing-cast",
        "duration": 1.5,
        "is_free": True
    },
    "fishing": {
        "id": "fishing-idle",
        "duration": 16,
        "is_free": True
    },
    "91": {
        "id": "fishing-idle",
        "duration": 16,
        "is_free": True
    },
    "mining": {
        "id": "mining-mine",
        "duration": 3,
        "is_free": True
    },
    "92": {
        "id": "mining-mine",
        "duration": 3,
        "is_free": True
    },
    "mine success": {
        "id": "mining-success",
        "duration": 2.5,
        "is_free": True
    },
    "93": {
        "id": "mining-success",
        "duration": 2.5,
        "is_free": True
    },
    "mine fail": {
        "id": "mining-fail",
        "duration": 2.5,
        "is_free": True
    },
    "94": {
        "id": "mining-fail",
        "duration": 2.5,
        "is_free": True
    },
    "fishing pull": {
        "id": "fishing-pull",
        "duration": 1,
        "is_free": True
    },
    "95": {
        "id": "fishing-pull",
        "duration": 1,
        "is_free": True
    },
    "ignition boost": {
        "id": "hcc-jetpack",
        "duration": 30,
        "is_free": True
    },
    "96": {
        "id": "hcc-jetpack",
        "duration": 30,
        "is_free": True
    },
    "star": {
        "id": "emote-stargazer",
        "duration": 8,
        "is_free": True
    },
    "97": {
        "id": "emote-stargazer",
        "duration": 8,
        "is_free": True
    },

}
# Roles class definition
class Roles:
    def __init__(self):
        self.valid_roles = ['Vip']  # Define valid roles
         # Load teleport locations when the bot starts

    def assign_role(self, username: str, role: str) -> str:
        # Logic to assign the role to the user
        # This is a placeholder; implement your actual role assignment logic here
        return f"Role '{role}' assigned to @{username}."

    def list_roles(self) -> str:
        return f"Available roles: {', '.join(self.valid_roles)}"

# Define authorized users


# Define fun facts
# Define rizz (flirt) lines
rizz_lines = [
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "Do you have a map? I keep getting lost in your eyes.",
    "Is your name Google? Because you have everything I'm searching for.",
    "If you were a vegetable, you'd be a cute-cumber!",
    "Do you believe in love at first sight, or should I walk by again?",
    "Are you a parking ticket? Because you've got FINE written all over you.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "Do you have a sunburn, or are you always this hot?",
    "Do you have a twin? Then you must be the most beautiful girl in the world!",
    "Do you have a name, or can I call you mine?"
]

# List of roasts
roasts = [
    "You're like a software update. Whenever I see you, I think, 'Not now.'",
    "I'd explain it to you, but I left my English-to-Dingbat dictionary at home.",
    "You're proof that even evolution makes mistakes.",
    "If I had a dollar for every time I saw someone as clueless as you, I'd have a dollar.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "I'd call you a tool, but that implies you're actually useful.",
    "You're the reason God created the middle finger.",
    "You're like a candle in the wind... useless.",
    "I'd agree with you, but then we'd both be wrong.",
    "You're as useless as the 'ueue' in 'queue'."
]

# Initialize a dictionary to store teleportation points
Guru = {'Shinigami_souls'}

# Dictionary to store outfit codes
Moderator = ["Shinigami_souls","_.POpo"]


class MyBot(BaseBot):
    user_roles = {}  # Dictionary to keep track of user roles
    message_queue = deque()  # Queue to hold messages
    emote_queue = deque()    # Queue to hold emotes
    message_rate_limit = 10  # Messages per minute
    emote_rate_limit = 5    # Emotes per minute
    last_message_time = datetime.now()
    last_emote_time = datetime.now()
    user_data = {}

    def __init__(self, room_id: str, token: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = room_id
        self.token = token
        self.bot_name = ""
        self.session_metadata = None
        self.looping_users = {}
        self.looping_tasks = {}
        self.looping_emotes = {}  # Store looping emotes for users
        self.roles = Roles()  # Initialize the Roles class
        self.room_owner = ["Shinigami_souls", "unive2", "_.POpo"]
        self.authorized_users = Moderator  # Use the global AUTHORIZED_USERS
        self.fun_fact_task = None  # To hold the fun fact task
        self.message_time = None  # Unlimited message time
        self.get_emote_duration = 30  # Default emote duration in seconds
        self.send_welcome_message = False  # Flag to control sending welcome messages
        self.looping_emote_task = None  # To keep track of the looping task
        self.load_user_roles()  # Load user roles when the bot starts
        self.user_data = {}
        self.load_user_data()
        self.room_name = "🇮🇳 INDIAN 🚩™️"
        self.user_last_visit = {}  # Dictionary to store user last visit times
        self.on_user_join_task = None  # Task to handle user join events
        self.last_message_time = datetime.now()  # Track the last time a message was sent
        self.mute_duration = timedelta()  # Track mute duration
        self.room_invite_link = "https://high.rs/room?id=6771048903b4ddc599e5a8dd&invite_id=67754f307b80e1381616a15b"
        self.user_profile_data_file = 'user_profile_data.json'
        self.user_profiles = {}
        self.user_profiles = self.load_user_profiles()
        self.positions_folder = Path("teleport_positions")
        self.positions_folder.mkdir(exist_ok=True)
        self.frozen_users = {}  # Dictionary to store frozen users
        self.frozen_users_ids = {}  # Dictionary to store frozen users IDs
        self.Moderator = self.load_moderators()  # Load moderators when the bot starts

    def load_moderators(self):
        """Load moderators from mod.json."""
        if os.path.exists('mod.json'):
            with open('mod.json', 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []  # Return an empty list if the file is corrupt
        return []  # Return an empty list if the file doesn't exist

    def save_moderators(self):
        """Save moderators to mod.json."""
        with open('mod.json', 'w') as f:
            json.dump(Moderator, f)

    def load_user_data(self):
        """Loads user data from user_data.json."""
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as f:
                try:
                    self.user_data = json.load(f)
                except json.JSONDecodeError:
                    self.user_data = {}  # Handle empty or corrupt file
        else:
            self.user_data = {}

    def save_user_data(self):
        """Saves user data to user_data.json."""
        with open('user_data.json', 'w') as f:
            json.dump(self.user_data, f)
        logger.info("User data saved")

    def load_user_roles(self):
        """Load user roles from a JSON file."""
        try:
            with open('user_roles.json', 'r') as f:
                self.user_roles = json.load(f)
        except FileNotFoundError:
            self.user_roles = {}  # Initialize to empty if file doesn't exist
        except json.JSONDecodeError:
            self.user_roles = {}  # Initialize to empty if JSON is invalid

    def save_user_roles(self):
        """Save user roles to a JSON file."""
        with open('user_roles.json', 'w') as f:
            json.dump(self.user_roles, f)

    def load_user_logs(self):
        """Loads user logs from user_logs.json."""
        if os.path.exists('user_logs.json'):
            with open('user_logs.json', 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}  # Handle empty or corrupt file
        return {}

    def save_user_logs(self, user_logs):
        """Saves user logs to user_logs.json."""
        with open('user_logs.json', 'w') as f:
            json.dump(user_logs, f)

    def load_user_profiles(self):
        """Loads user profiles from user_profile_data.json."""
        if os.path.exists(self.user_profile_data_file):
            with open(self.user_profile_data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}  # Handle empty or corrupt file
        return {}

    def save_user_profiles(self):
        """Saves user profiles to user_profile_data.json."""
        with open(self.user_profile_data_file, 'w') as f:
            json.dump(self.user_profiles, f)
    
    @staticmethod
    def load_conversations(file_path="conversations.json"):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save_conversations(conversations, file_path="conversations.json"):
        with open(file_path, "w") as f:
            json.dump(conversations, f)

    @staticmethod
    def load_UserEmote_ids(file_path="UserEmotes.json"):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save_UserEmote_ids(UserEmote_ids, file_path="UserEmotes.json"):
        with open(file_path, "w") as f:
            json.dump(UserEmote_ids, f)

    def save_position(self, position_name, position, restricted=False):
        file_path = self.positions_folder / f"{position_name}.json"
        with open(file_path, 'w') as f:
            json.dump({
                "x": position.x,
                "y": position.y,
                "z": position.z,
                "facing": position.facing,
                "restricted": restricted
            }, f)

    def load_position(self, position_name):
        file_path = self.positions_folder / f"{position_name}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                return Position(
                    data.get("x", 0),
                    data.get("y", 0),
                    data.get("z", 0),
                    facing=data.get("facing", 'FrontRight')
                ), data.get("restricted", False)
        return None, None

    def delete_position(self, position_name):
        file_path = self.positions_folder / f"{position_name}.json"
        if file_path.exists():
            os.remove(file_path)
            return True
        return False
        

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        self.session_metadata = session_metadata
        logger.info(f"{self.bot_name} is running!")
        self.print_session_metadata(session_metadata)
        asyncio.create_task(self.start_welcome_loop())
        asyncio.create_task(self.monitor_frozen_users())
        await self.highrise.walk_to(Position(16.5,0.0,14.5))
        await asyncio.sleep(10)
        asyncio.create_task(self.start_bot_emote_loop())
        await asyncio.sleep(10)
        self.load_user_data() # Load user data on bot start




    def print_session_metadata(self, session_metadata: SessionMetadata) -> None:
        logger.debug("Session Metadata structure:")
        for attr in dir(session_metadata):
            if not attr.startswith("_"):
                value = getattr(session_metadata, attr)
                logger.debug(f"{attr}: {value}")

    async def on_user_join(self, user: User, position: Position) -> None:
        try:
            user_id = user.id
            if user_id not in self.user_data:
                self.user_data[user_id] = {"join_count": 0, "total_time": 0, "last_join": None}
                self.user_last_visit[user.username] = datetime.now(timezone.utc).timestamp()

            self.user_data[user_id]["join_count"] += 1
            self.user_data[user_id]["last_join"] = datetime.now(timezone.utc).timestamp()

            join_count = self.user_data[user_id]["join_count"]

            # List of messages to send when a moderator joins
            # Start of Selection
            moderator_messages = [
                f"𝘽𝙤𝙤𝙢 @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝗵𝗮𝘀 𝗮𝗿𝗿𝗶𝘃𝗲𝗱! 𝗟𝗲𝘁 𝘁𝗵𝗲 𝗳𝘂𝗻 𝗯𝗲𝗴𝗶𝗻🎉!",
                f"𝙇𝙤𝙤𝙠 𝙬𝙤'𝙨 𝙝𝙚𝙧𝙚! @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙝𝙖𝙨 𝙟𝙤𝙞𝙣𝙚𝙙 𝙪𝙨! 𝙇𝙚𝙩'𝙨 𝙩𝙝𝙚 𝙛𝙪𝙣 𝙗𝙚𝙜𝙞𝙣𝙨 😼!",
                f"@{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙞𝙨 𝙞𝙣 𝙩𝙝𝙚 𝙝𝙤𝙪𝙨𝙚! 𝙏𝙞𝙢𝙚 𝙛𝙤𝙧 𝙨𝙤𝙢𝙚 𝙛𝙪𝙣🥳!",
                f"𝘼𝙩𝙩𝙚𝙣𝙩𝙞𝙤𝙣 𝙚𝙫𝙚𝙧𝙮𝙤𝙣𝙚! @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙞𝙨 𝙣𝙤𝙬 𝙞𝙣 𝙩𝙝𝙚 𝙧𝙤𝙤𝙢🤫!",
                f"𝙏𝙃𝙀 𝙍𝙊𝙊𝙈 𝙄𝙎 𝙎𝙃𝘼𝙆𝙄𝙉𝙂! @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙄𝙎 𝙄𝙉 𝙏𝙃𝙀 𝙃𝙊𝙐𝙎𝙀🌪️!",
                f"𝙏𝙃𝙀 𝙋𝙊𝙒𝙀𝙍𝙁𝙐𝙇 @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙃𝘼𝙎 𝘼𝙍𝙍𝙄𝙑𝙀𝘿! 🚀".replace("𝙇", "𝙡"),
                f"𝙏𝙃𝙀 𝙍𝙊𝙊𝙈 𝙄𝙎 𝙊𝙑𝙀𝙍𝙋𝙊𝙒𝙀𝙍𝙀𝘿! @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙄𝙎 𝙄𝙉 𝙏𝙃𝙀 𝙃𝙊𝙐𝙎𝙀🔥!",
                f"𝙏𝙃𝙀 𝙎𝙐𝙋𝙀𝙍𝙄𝙊𝙍 @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙃𝘼𝙎 𝘼𝙍𝙍𝙄𝙑𝙀𝘿! 👑",
                f"𝙏𝙃𝙀 𝙍𝙊𝙊𝙈 𝙄𝙎 𝙎𝙃𝘼𝙆𝙄𝙉𝙂! @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙄𝙎 𝙄𝙉 𝙏𝙃𝙀 𝙃𝙊𝙐𝙎𝙀🌪️!",
                f"👑 𝙏𝙃𝙀 𝙇𝙀𝘿𝙀𝙍 𝙃𝘼𝙎 𝙀𝙉𝙏𝙀𝙍𝙀𝘿! @{𝙪𝙨𝙚𝙧.𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚} 𝙄𝙎 𝙄𝙉 𝙏𝙃𝙀 𝙃𝙊𝙐𝙎𝙀👑!",
            ]

            # Check if the user is a moderator
            if user.username in self.Moderator:
                message = random.choice(moderator_messages)  # Select a random message
                await self.highrise.chat(message)  # Send the message to the chat
            # Welcome message to the user
            message = f"Welcome to {self.room_name}! This is your {join_count} visit!"
            if user.username not in self.Moderator:
                for _ in range(10):
                    await self.highrise.react("heart", user_id)
            # Check if the user is a moderator
            if user.username in self.Moderator:
                # Send the user a wink
                for _ in range(10):
                    await self.highrise.react("wink", user_id)
            self.save_user_data()
            # Check if the user is a VIP
            if user.username in self.user_roles:
                # Send the user a random react
                for _ in range(10):
                    react = random.choice(["heart", "wink", "clap", "wave"])
                    await self.highrise.react(react, user_id)
            await self.highrise.send_whisper(user_id, message)
            self.save_user_data()
        except Exception as e:
            logger.exception(f"Error in on_user_join: {str(e)}")


    async def on_user_leave(self, user: User) -> None:
        try:
            user_id = user.id
            if user_id in self.user_data and self.user_data[user_id]["last_join"] is not None:
                join_time = self.user_data[user_id]["last_join"]
                leave_time = datetime.now(timezone.utc).timestamp()
                time_spent = leave_time - join_time
                self.user_data[user_id]["total_time"] += time_spent
                self.user_data[user_id]["last_join"] = None
                self.save_user_data()
        except Exception as e:
            logger.exception(f"Error in on_user_leave: {str(e)}")




    async def on_chat(self, user: User, message: str) -> None:

        user_id = user.id  # Assuming user.id gives you the user ID
        UserEmote_ids = self.load_UserEmote_ids()

        if user.id not in UserEmote_ids:
            await self.highrise.send_whisper(user.id, f"You need to send 'hello' to add your profile before using any commands @{user.username}.")
            return

        # Check for single emote command
        if message.isdigit():  # Check if the message is a number
            emote_key = message  # Use the message directly as the key
            if emote_key in emote_list:  # Check if the key exists in emote_list
                emote_id = emote_list[emote_key]["id"]  # Get the emote ID
                await self.highrise.send_emote(emote_id, user.id)  # Send the emote
                return
        elif message in emote_list:  # Check if the message is an emote name
            emote_id = emote_list[message]["id"]  # Get the emote ID
            await self.highrise.send_emote(emote_id, user.id)  # Send the emote
            return
        else:
            # Check for emote names with spaces
            for emote_name in emote_list.keys():
                if message.lower() == emote_name.lower():  # Case-insensitive comparison
                    emote_id = emote_list[emote_name]["id"]  # Get the emote ID
                    await self.highrise.send_emote(emote_id, user.id)  # Send the emote
                    return
                
        if message.lower().startswith("-create tele "):
            if user.username not in self.Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                return
            parts = message.split()
            position_name = parts[2]
            restricted = True  # Set to True or False based on your logic
            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                    if room_user.id == user.id:
                        current_position = pos 
                        self.save_position(position_name, current_position, restricted=restricted)
                        await self.highrise.send_whisper(user.id, f"Position '{position_name}' saved for teleport.")
                        break
            else:
                await self.highrise.send_whisper(user.id, "Unable to save your current position.")
        elif message.lower().startswith("-remove tele "):
            if user.username not in self.Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                return
            position_name = message[13:].strip()  
            if self.delete_position(position_name):
                await self.highrise.send_whisper(user.id, f"Position '{position_name}' removed.")
            else:
                await self.highrise.send_whisper(user.id, f"Position '{position_name}' not found.")
        elif message.lower() in [f.stem.lower() for f in self.positions_folder.glob("*.json")]:
            position_name = message.lower()
            saved_position, restricted = self.load_position(position_name)
            if restricted:
                if user.username not in self.Moderator and user.username not in self.user_roles:
                        await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                        return
                if saved_position:
                    await self.highrise.teleport(user.id, saved_position)
                    await self.highrise.send_whisper(user.id, f"Teleported to '{position_name}'.")
                else:
                    await self.highrise.send_whisper(user.id, f"Position '{position_name}' does not exist.")

        elif message.lower().startswith("-mod"):
            await self.give_mod(user, message)

         


        if message.lower().startswith("-changefit"):
                    await self.highrise.set_outfit(outfit=[
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='body-flesh',
                                                            account_bound=False,
                                                            active_palette=0
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='eye-n_basic2018zanyeyes',
                                                            account_bound=False,
                                                            active_palette=7
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='eyebrow-n_10',
                                                            account_bound=False,
                                                            active_palette=1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='nose-n_01',
                                                            account_bound=False,
                                                            active_palette=0
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='pants-n_room12019rippedpantsblack',
                                                            account_bound=False,
                                                            active_palette=-1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='watch-n_room32019blackwatch',
                                                            account_bound=False,
                                                            active_palette=-1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='shirt-n_room22109denimjacket',
                                                            account_bound=False,
                                                            active_palette=0
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='shoes-n_room12019sneakersblack',
                                                            account_bound=False,
                                                            active_palette=-1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='hair_back-n_malenew09',
                                                            account_bound=False,
                                                            active_palette=1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='hair_front-n_malenew09',
                                                            account_bound=False,
                                                            active_palette=1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='mouth-basic2018lollipop',
                                                            account_bound=False,
                                                            active_palette=-1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='glasses-n_registrationavatars2023billieglasses',
                                                            account_bound=False,
                                                            active_palette=-1
                                                        ),
                                                        Item(
                                                            type='clothing',
                                                            amount=1,
                                                            id='freckle-n_basic2018freckle22',
                                                            account_bound=False,
                                                            active_palette=1
                                                        ),
                                                        ])

        if message.lstrip().startswith('-tele'):
            if user.username not in self.Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                return

            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]
            usernames = [user.username.lower() for user in users]

            parts = message[1:].split()
            args = parts[1:]

            if len(args) < 2:
                await self.highrise.send_whisper(user.id, "Usage: -tele @username <position_name>")
                return
            elif args[0][0] != "@":
                await self.highrise.send_whisper(user.id, "Incorrect format. Please use '@username'.")
                return
            elif args[0][1:].lower() not in usernames:
                await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
                return

            position_name = " ".join(args[1:])
            
            # Determine the destination based on the position name
            if position_name.lower() == 'floor 1':
                dest = Position(18.5, 0.0, 9.0)
                restricted = False  # Set to False for predefined floors
            elif position_name.lower() == 'floor 2':
                dest = Position(15.5, 6.0, 6.5)
                restricted = False  # Set to False for predefined floors
            elif position_name.lower() == 'floor 3':
                dest = Position(15.5, 12.0, 6.0)
                restricted = False  # Set to False for predefined floors
            else:
                # Load the position based on the name
                saved_position, restricted = self.load_position(position_name)  # Assuming you have a method to load positions

                if saved_position:
                    dest = saved_position
                else:
                    await self.highrise.send_whisper(user.id, f"Position '{position_name}' does not exist.")
                    return

            user_id = next(
                (u.id for u in users if u.username.lower() == args[0][1:].lower()),
                None)
            if not user_id:
                await self.highrise.send_whisper(user.id, f"User {args[0][1:]} unavailable.")
                return

            # Check if the position is restricted
            if restricted and user.username not in Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to teleport to this position.")
                return

            await self.highrise.teleport(user_id, dest)  # Teleport the user to the destination
            await self.highrise.send_whisper(user.id, f"Teleported {args[0][1:]} to '{position_name}'.")
    
                
        if message.lower().startswith("-stuck"):
            await self.freeze_user(user, message)
        
        elif message.lower().startswith("-leave"):
            await self.unfreeze_user(user, message)

        if message.lower().startswith("-host"):  # Changed from ! to -
            await self.get_host_coordinates(user)

        elif message.lower().startswith("-heartall"):
            await self.send_heart_reaction(user)

        elif message.lower().startswith("-heart"):
            await self.send_heart_reaction_to_user(user, message)

        elif message.lower().startswith("-winkall"):
            await self.send_wink_reaction(user)

        elif message == "-floor 1":
            await self.highrise.teleport(user.id, Position(18.5, 0.0, 9.0))

        elif message == "-floor 2":
            await self.highrise.teleport(user.id, Position(15.5, 6.0, 6.5))

        elif message == "-floor 3":
            await self.highrise.teleport(user.id, Position(15.5, 12.0, 6.0))

        # Check for summon command
        elif message.lower().startswith("-summon"):
            await self.summon_user(user, message)

        # Check for goto command
        elif message.lower().startswith("-goto"):
            await self.goto_user(user, message)



        # Check for come command
        elif message.lower().startswith("-come"):
            await self.come(user)



        # Check for loop emote command
        elif message.lower().startswith("-loop"):
            await self.loop_emote(user, message)
        



        # Start sending fun facts command for authorized users


        # Rizz command
        elif message.lower().startswith("-rizz"):
            await self.send_rizz(user)

        # Flirt command
        elif message.lower().startswith("-flirt"):
            await self.send_flirt(user)

        

        # Love percentage command
        elif message.lower().startswith("-love percentage"):
            await self.send_love_percentage(user)

        # Hate percentage command
        elif message.lower().startswith("-hate percentage"):
            await self.send_hate_percentage(user)

        # Emote command
        elif message.lower().startswith("-send"):
            await self.perform_emote(user, message)





        # Check for roast command
        elif message.lower().startswith("-roast"):
            await self.roast_user(user, message)




        # Check for give role command
        elif message.lower().startswith("-give"):
            await self.give_role(user, message)



        # Check for the roles command
        elif message.lower() == "-Vip":
            await self.show_roles(user)

        elif message.lower().endswith(" all") and message.startswith("-"):
            emote_name_or_number = message[1:-4].strip()  # Extract the emote name or number (removing " all")
            emote_id = None

            # Check if the emote_name_or_number is a number
            if emote_name_or_number.isdigit():
                emote_key = emote_name_or_number  # Use the numeric string directly as the key
                if emote_key in emote_list:  # Check if the key exists in emote_list
                    emote_id = emote_list[emote_key]["id"]  # Get the emote ID
                else:
                    await self.highrise.send_whisper(user.id, "Emote number out of range.")
                    return
            else:
                # Find the emote ID based on name
                for emote_name, emote_data in emote_list.items():
                    if emote_name.lower() == emote_name_or_number.lower():
                        emote_id = emote_data["id"]
                        break

            if emote_id:
                # Check if the user has permission (e.g., is a moderator)
                if user.username not in self.Moderator:  # Adjust this check based on your role management
                    await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                    return

                # Get all users in the room
                room_users = await self.highrise.get_room_users()
                for room_user, _ in room_users.content:
                    await self.highrise.send_emote(emote_id, room_user.id)  # Send the emote to each user
                await self.highrise.send_whisper(user.id, f"Sent '{emote_name_or_number}' to all users.")
            else:
                await self.highrise.send_whisper(user.id, "Emote not found.")
            return  # Exit after processing the command


        if message.startswith("-kick"):
            # Check if the user is authorized to use the kick command
            if user.username not in self.Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                return

            # Separate message into parts
            parts = message.split()

            # Check if message is valid "kick @username"
            if len(parts) != 2:
                await self.highrise.send_whisper(user.id, "Invalid kick command format. Use: kick @username")
                return

            # Extract username from the message
            username = parts[1][1:] if parts[1].startswith("@") else parts[1]

            # Check if user is in the room
            room_users = (await self.highrise.get_room_users()).content
            user_id = None  # Initialize user_id to None
            for room_user, pos in room_users:
                if room_user.username.lower() == username.lower():
                    user_id = room_user.id
                    break

            if user_id is None:  # Check if user_id was found
                await self.highrise.send_whisper(user.id, "User not found, please specify a valid user.")
                return

            # Kick user
            try:
                await self.highrise.moderate_room(user_id, "kick")
                # Send message to chat
                await self.highrise.send_whisper(user.id, f"@{username} has been kicked from the room.")
            except Exception as e:
                await self.highrise.send_whisper(user.id, f"Error kicking user: {str(e)}")

        elif message.lower() == "-inviteall":
            if user.username not in self.Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                return
            await self.highrise.send_whisper(user.id, "Inviting all users to the room...")
            room_id = "6771048903b4ddc599e5a8dd"
            conversations = self.load_conversations()
            for conversation_id in conversations.keys():
                await asyncio.sleep(1)
                await self.highrise.send_message(conversation_id, f"Don't you want to come hang with me? Let's have a good time together. Come join {self.room_invite_link} and have a good time with us 😎")
                await self.highrise.send_message(conversation_id, content="", message_type="invite", room_id=room_id)
            await self.highrise.send_whisper(user.id, "Invited all users to the room.")
            return
        if message.lower().startswith("-emotelist"):
                    loop_list1 = [
                        'Emote list:',
                    '1. Model', '2. Dont Start Now', '3. Russian Dance', '4. Teleport', 
                    '5. Curtsy', '6. Lets Go Shopping', '7. Greedy', '8. Flex', '9. Sing Along',
                    '10. Pennys Dance', ]
                    loop_list1 = '\n'.join(loop_list1)
                    loop_list2 = [
                    '11. Bow', '12. Snowball Fight', '13. Confused', '14. Charging',
                    '15. Floating', '16. Frog Hop', '17. Enthused', '18. Grave Dance', '19. Lambi Pose',
                    '20. Sword Fight',
                      ]
                    loop_list2 = '\n'.join(loop_list2)
                    loop_list3 = ['21. Do the Worm', '22. Viral Groove', '23. Shuffle Dance', '24. Cursing',
                    '25. Raise the Roof', '26. Emote Cute', '27. Telekinesis', '28. Energy Ball', '29. Maniac',
                    '30. Snow Angel', 
                     ]
                    loop_list3 = '\n'.join(loop_list3)
                    loop_list4 = ['31. Sweating', '32. Kpop Dance', '33. Flirty Wave', '34. Cutey',
                    '35. Casual Dance', '36. Pose 1', '37. Pose 3', '38. Pose 5', '39. Pose 7',
                    '40. Pose 8',
                      ]
                    loop_list4 = '\n'.join(loop_list4)
                    loop_list5 = ['41. Gagging', '42. Savage Dance', '43. Say So Dance', 
                    '44. Fashion', '45. Gravity', '46. UwU', '47. Wrong',
                    '48. Sleigh', '49. Hyped', '50. Zombie',
                      ]
                    loop_list5 = '\n'.join(loop_list5)
                    loop_list6 = ['51. Punk', '52. Shy',
                    '53. Icecream', '54. Timejump', '55. Touch', '56. Air Guitar', '57. Kawaii',
                    '58. Scritchy', '59. Celebration', '60. Surprise',]
                    loop_list6 = '\n'.join(loop_list6)
                    loop_list7 = ['61. Bashful', '62. Creepy Cute',
                    '63. Pose 10', '64. Repose', '65. Boxer', '66. Creepy Puppet', '67. Penguin',
                    '68. Yes', '69. Tired', '70. Sad',]
                    loop_list7 = '\n'.join(loop_list7)
                    loop_list8 = ['71. Kiss', '72. Tummy Ache',
                    '73. Jinglebell', '74. Nervous', '75. Toilet', '76. Astronaut',
                    '77. Anime Dance', '78. Ice Skating', '79. Head Blowup',
                    '80. Ditzy Pose',]
                    loop_list8 = '\n'.join(loop_list8)
                    loop_list9 = ['81. Gift', '82. Push It', '83. Launch',
                    '84. Salute', '85. Cute Salute', '86. Fairy Twirl', '87. Fairy Float',
                    '88. Smooch', '89. Fishing Pull', '90. Fishing Cast',]
                    loop_list9 = '\n'.join(loop_list9)
                    loop_list10 = ['91. Fishing',
                    '92. Mining', '93. Mine Success', '94. Mine Fail', '95. Fishing Pull',
                    '96. Ignition Boost']
                    loop_list10 = '\n'.join(loop_list10)
                    await self.highrise.send_whisper(user.id, loop_list1)
                    await self.highrise.send_whisper(user.id, loop_list2)
                    await self.highrise.send_whisper(user.id, loop_list3)
                    await self.highrise.send_whisper(user.id, loop_list4)
                    await self.highrise.send_whisper(user.id, loop_list5)
                    await self.highrise.send_whisper(user.id, loop_list6)
                    await self.highrise.send_whisper(user.id, loop_list7)
                    await self.highrise.send_whisper(user.id, loop_list8)
                    await self.highrise.send_whisper(user.id, loop_list9)
                    await self.highrise.send_whisper(user.id, loop_list10)

        if message.lower().startswith("-tipall"):
            if user.username not in self.Moderator:
                await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
                return
            parts = message.split(" ")
            if len(parts) != 2:
                await self.highrise.send_message(user.id, "Invalid command")
                return
            # Checks if the amount is valid
            try:
                amount = int(parts[1])
            except:
                await self.highrise.chat("Invalid amount")
                return
            # Checks if the bot has the amount
            bot_wallet = await self.highrise.get_wallet()
            bot_amount = bot_wallet.content[0].amount
            if bot_amount < amount:
                await self.highrise.chat("Not enough funds")
                return
            # Get all users in the room
            room_users = await self.highrise.get_room_users()
            # Check if the bot has enough funds to tip all users the specified amount
            total_tip_amount = amount * len(room_users.content)
            if bot_amount < total_tip_amount:
                await self.highrise.chat("Not enough funds to tip everyone")
                return
            # Tip each user in the room the specified amount
            for room_user, pos in room_users.content:
                bars_dictionary = {
                    10000: "gold_bar_10k",
                    5000: "gold_bar_5000",
                    1000: "gold_bar_1k",
                    500: "gold_bar_500",
                    100: "gold_bar_100",
                    50: "gold_bar_50",
                    10: "gold_bar_10",
                    5: "gold_bar_5",
                    1: "gold_bar_1"
                }
                fees_dictionary = {
                    10000: 1000,
                    5000: 500,
                    1000: 100,
                    500: 50,
                    100: 10,
                    50: 5,
                    10: 1,
                    5: 1,
                    1: 1
                }
                # Convert the amount to a string of bars and calculate the fee
                tip = []
                remaining_amount = amount
                total = 0  # Initialize total here
                for bar in bars_dictionary:
                    if remaining_amount >= bar:
                        bar_amount = remaining_amount // bar
                        remaining_amount = remaining_amount % bar
                        for i in range(bar_amount):
                            tip.append(bars_dictionary[bar])
                            total += bar + fees_dictionary[bar]  # Accumulate total here
                if total > bot_amount:
                    await self.highrise.chat("Not enough funds")
                    return
                for bar in tip:
                    await self.highrise.tip_user(room_user.id, bar)
        elif message.startswith("-ban"):
            if user.username in self.Moderator:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: -ban @username")
                    return

                mention = parts[1]
                username_to_ban = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_ban.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_ban.lower())
                    user_id_to_ban = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_ban, "ban", 3600)  # Ban for 1 hour
                    await self.highrise.chat(f"Banned {mention} for 1 hour.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

        elif message.startswith("-mute"):
            if user.username in self.Moderator:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: -mute @username")
                    return

            mention = parts[1]
            username_to_mute = mention.lstrip('@')  # Remove the '@' symbol from the mention
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]  # Extract the User objects
            user_ids = [user.id for user in users]  # Extract the user IDs

            if username_to_mute.lower() in [user.username.lower() for user in users]:
                user_index = [user.username.lower() for user in users].index(username_to_mute.lower())
                user_id_to_mute = user_ids[user_index]
                await self.highrise.moderate_room(user_id_to_mute, "mute",3600)  # Mute for 1 hour
                await self.highrise.chat(f"Muted {mention} for 1 hour.")
            else:
                await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")


        elif message.startswith("-unmute"):
            if user.username in self.Moderator:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: -unmute @username")
                    return

            mention = parts[1]
            username_to_mute = mention.lstrip('@')  # Remove the '@' symbol from the mention
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]  # Extract the User objects
            user_ids = [user.id for user in users]  # Extract the user IDs

            if username_to_mute.lower() in [user.username.lower() for user in users]:
                user_index = [user.username.lower() for user in users].index(username_to_mute.lower())
                user_id_to_mute = user_ids[user_index]
                await self.highrise.moderate_room(user_id_to_mute, "mute",1)  # Mute for 1 hour
                await self.highrise.chat(f"{mention} Unmuted.")
            else:
                await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")

        elif message.startswith("-wallet"):
            if user.username in Moderator:
                wallet = await self.highrise.get_wallet()
                for currency in wallet.content:
                    if currency.type == 'gold':
                        gold = currency.amount
                        await self.highrise.send_whisper(user.id, f"I have {gold}g in my wallet.")
                        return
                await self.highrise.send_whisper(user.id, "No gold in wallet.")



    async def come(self, user: User) -> None:
        # Check if the user is authorized
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id,

                f"You are not authorized to use this command, @{user.username}."
            )
            return

        # Get the user's current position
        response = await self.highrise.get_room_users()
        your_pos = None
        for content in response.content:
            if content[0].id == user.id:
                your_pos = content[1]  # Assuming content[1] is the user's position
                break

        if not your_pos:
            await self.highrise.send_whisper(user.id,
                "Invalid command, please specify a valid username.")
            return

        await self.highrise.send_whisper(user.id, "AA rha hu bhai")
        await self.highrise.walk_to(your_pos)

    async def summon_user(self, user: User, message: str) -> None:
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id,
                f"You are not authorized to use this command, @{user.username}."
            )
            return
        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -summon <@username>")
            return

        target_username = parts[1][1:]  # Remove the '@' from the username

        # Get the current position of the summoner
        summoner_position = await self.get_user_position(user)

        if not summoner_position:
            await self.highrise.send_whisper(user.id, "Could not retrieve your coordinates.")
            return

        # Find the target user in the room
        room_users = await self.highrise.get_room_users()
        target_user = None
        for room_user, position in room_users.content:
            if room_user.username.lower() == target_username.lower():
                target_user = room_user
                break

        if target_user:
            try:
                await self.highrise.teleport(target_user.id, summoner_position)
                await self.highrise.send_whisper(user.id, f"{target_username} has been summoned to your location.")
            except Exception as e:
                print("Error during summoning:", e)
                await self.highrise.send_whisper(user.id, "An error occurred while trying to summon the user.")
        else:
            await self.highrise.send_whisper(user.id, f"User @{target_username} not found in the room.")

    async def goto_user(self, user: User, message: str) -> None:
        """Teleport the summoner to the specified user's location."""
        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -goto <@username>")
            return

        target_username = parts[1][1:]  # Remove the '@' from the username

        # Find the target user in the room
        room_users = await self.highrise.get_room_users()
        target_user = None
        for room_user, position in room_users.content:
            if room_user.username.lower() == target_username.lower():
                target_user = room_user
                break

        if target_user:
            try:
                target_position = await self.get_user_position(target_user)
                await self.highrise.teleport(user.id, target_position)
                await self.highrise.send_whisper(user.id, f"You have been teleported to @{target_username}'s location.")
            except Exception as e:
                print("Error during goto:", e)
                await self.highrise.send_whisper(user.id, "An error occurred while trying to go to the user.")
        else:
            await self.highrise.send_whisper(user.id, f"User @{target_username} not found in the room.")

    async def get_user_position(self, user: User) -> Position:
        """Get the current position of a user."""
        room_users = await self.highrise.get_room_users()
        for room_user, position in room_users.content:
            if room_user.id == user.id:
                return position  # Return the Position object
        return None  # Return None if the user is not found

    async def loop_emote(self, user: User, message: str) -> None:
        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -loop <emote name> or -loop stop")
            return

        emote_name = " ".join(parts[1:])

        # If the user wants to stop the loop
        if emote_name.lower() == "stop":
            await self.stop_loop(user)  # Call the stop loop method
            return

        # Find the emote info based on the name
        emote_info = emote_list.get(emote_name)

        if emote_info is None:
            await self.highrise.send_whisper(user.id, f"Emote '{emote_name}' not found.")
            return

        emote_id = emote_info["id"]
        duration = emote_info["duration"]

        # If the user is already looping an emote, cancel the existing task
        if user.id in self.looping_tasks:
            await self.stop_loop(user)  # Call the stop loop method

        # Create a new task for the new emote loop
        async def emote_loop():
            await self.highrise.send_whisper(user.id, f"Now looping {emote_name}.")  # Inform the user
            while user.id in self.looping_tasks:
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                    await asyncio.sleep(duration)  # Use the duration from the emote info
                except Exception as e:
                    print(f"Error sending emote: {e}")
                    break

        self.looping_tasks[user.id] = asyncio.create_task(emote_loop())


    async def stop_loop(self, user: User) -> None:
            """Stops the looping task for the user."""
            if user.id not in self.looping_tasks:
                await self.highrise.send_whisper(user.id,
                    f"You are not currently looping any emotes, @{user.username}.")
                return

            print(f"Stopping loop for user: {user.username}")  # Debugging line
            self.looping_tasks[user.id].cancel()
            del self.looping_tasks[user.id]
            await self.highrise.send_whisper(user.id, "Stopping the loop.")

    async def send_rizz(self: BaseBot, user: User) -> None:
        rizz = random.choice(rizz_lines)
        await self.highrise.chat(f"@{user.username}, {rizz}")

    async def send_flirt(self: BaseBot, user: User) -> None:
        flirt_message = random.choice(rizz_lines)
        await self.highrise.chat(f"@{user.username}, {flirt_message}")


    async def send_love_percentage(self: BaseBot, user: User) -> None:
        love_percentage = random.randint(0, 100)
        await self.highrise.chat(
            f"@{user.username}, your love percentage is {love_percentage}%!")

    async def perform_emote(self, user: User, message: str) -> None:
        """Performs an emote on a specified user."""
        # Check if the user is authorized
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id,
                f"You can't use this command, @{user.username}."
            )
            return

        parts = message.split(" ")
        if len(parts) < 3:
            await self.highrise.send_whisper(user.id, "Usage: -send <emote_name> <@username>")
            return

        emote_name = parts[1]
        target_username = parts[2][1:] if parts[2].startswith("@") else parts[
            2]  # Remove '@' if present

        # Find the emote ID from the updated emote list
        emote_info = emote_list.get(emote_name.lower())  # Use the updated method to get emote ID

        if emote_info is None:
            await self.highrise.send_whisper(user.id, f"Emote '{emote_name}' not found.")
            return

        emote_id = emote_info["id"]  # Get the emote ID from the emote info

        # Get the target user's ID
        room_users = (await self.highrise.get_room_users()).content
        target_user_id = None
        for room_user, _ in room_users:
            if room_user.username.lower() == target_username.lower():
                target_user_id = room_user.id
                break

        if target_user_id is None:
            await self.highrise.send_whisper(user.id,
                f"User @{target_username} not found in the room.")
            return

        # Send the emote to the target user
        try:
            await self.highrise.send_emote(emote_id, target_user_id)
            await self.highrise.send_whisper(user.id,
                f"@{user.username} performed '{emote_name}' on @{target_username}!"
            )
        except Exception as e:
            await self.highrise.send_whisper(user.id,
                f"Failed to send emote to @{target_username}: {str(e)}")
            return



    async def roast_user(self, user: User, message: str) -> None:
        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -roast <@username>")
            return

        target_username = parts[1][1:] if parts[1].startswith("@") else parts[1]

        # Get the list of users in the room
        room_users = (await self.highrise.get_room_users()).content
        target_user_id = None

        # Find the target user's ID
        for room_user, _ in room_users:
            if room_user.username.lower() == target_username.lower():
                target_user_id = room_user.id
                break

        if target_user_id is None:
            await self.highrise.send_whisper(user.id,
                f"User @{target_username} not found in the room.")
            return

        # Send a random roast to the target user
        roast_message = random.choice(roasts)
        await self.highrise.chat(f"@{target_username}, {roast_message}")


    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        try:
            response = await self.highrise.get_messages(conversation_id)
            logger.info(f"Received messages: {response}")
            UserEmote_ids = self.load_UserEmote_ids()

            if user_id not in UserEmote_ids:
                UserEmote_ids[user_id] = True 
                self.save_UserEmote_ids(UserEmote_ids) 

            conversations = self.load_conversations()

            if conversation_id not in conversations:
                conversations[conversation_id] = True
                self.save_conversations(conversations) 

            await self.highrise.send_message(conversation_id, "Your profile has been added successfully!!")

        except Exception as e:
            logging.error(f"An error occurred in on_message: {e}")



        if isinstance(response, GetMessagesRequest.GetMessagesResponse):
            if user_id not in self.user_profiles:
                # Get the content of the latest message
                message = response.messages[0].content
                logger.info(f"Received message from {user_id}: {message}")

            if message.lower().startswith("-emotelist"):
                loop_list1 = [
                        'Emote list:',
                    '1. Model', '2. Dont Start Now', '3. Russian Dance', '4. Teleport', 
                    '5. Curtsy', '6. Lets Go Shopping', '7. Greedy', '8. Flex', '9. Sing Along',
                    '10. Pennys Dance', '11. Bow', '12. Snowball Fight', '13. Confused', '14. Charging',
                    '15. Floating', '16. Frog Hop', '17. Enthused', '18. Grave Dance', '19. Lambi Pose',
                    '20. Sword Fight', ]
                loop_list1 = '\n'.join(loop_list1)
                loop_list2 = [
                    '21. Do the Worm', '22. Viral Groove', '23. Shuffle Dance', '24. Cursing',
                    '25. Raise the Roof', '26. Emote Cute', '27. Telekinesis', '28. Energy Ball', '29. Maniac',
                    '30. Snow Angel', '31. Sweating', '32. Kpop Dance', '33. Flirty Wave', '34. Cutey',
                    '35. Casual Dance', '36. Pose 1', '37. Pose 3', '38. Pose 5', '39. Pose 7',
                    '40. Pose 8',  ]
                loop_list2 = '\n'.join(loop_list2)
                loop_list3 = [
                    '41. Gagging', '42. Savage Dance', '43. Say So Dance', 
                    '44. Fashion', '45. Gravity', '46. UwU', '47. Wrong',
                    '48. Sleigh', '49. Hyped', '50. Zombie', '51. Punk', '52. Shy',
                    '53. Icecream', '54. Timejump', '55. Touch', '56. Air Guitar', '57. Kawaii',
                    '58. Scritchy', '59. Celebration', '60. Surprise',]
                loop_list3 = '\n'.join(loop_list3)
                loop_list4 = [
                    '61. Bashful', '62. Creepy Cute',
                    '63. Pose 10', '64. Repose', '65. Boxer', '66. Creepy Puppet', '67. Penguin',
                    '68. Yes', '69. Tired', '70. Sad', '71. Kiss', '72. Tummy Ache',
                    '73. Jinglebell', '74. Nervous', '75. Toilet', '76. Astronaut',
                    '77. Anime Dance', '78. Ice Skating', '79. Head Blowup',
                    '80. Ditzy Pose', ]
                loop_list4 = '\n'.join(loop_list4)
                loop_list5 = [
                     '81. Gift', '82. Push It', '83. Launch',
                    '84. Salute', '85. Cute Salute', '86. Fairy Twirl', '87. Fairy Float',
                    '88. Smooch', '89. Fishing Pull', '90. Fishing Cast', '91. Fishing',
                    '92. Mining', '93. Mine Success', '94. Mine Fail', '95. Fishing Pull',
                    '96. Ignition Boost',]
                loop_list5 = '\n'.join(loop_list5)
                await self.highrise.send_message(conversation_id, loop_list1)
                await self.highrise.send_message(conversation_id, loop_list2)
                await self.highrise.send_message(conversation_id, loop_list3)
                await self.highrise.send_message(conversation_id, loop_list4)
                await self.highrise.send_message(conversation_id, loop_list5)



    async def start_bot_emote_loop(self) -> None:
        while True:
            emote_name = random.choice(list(emote_list.keys()))  # Assuming emote_list is a dictionary
            emote_info = emote_list[emote_name]
            emote_id = emote_info["id"]
            await self.highrise.send_emote(emote_id)
            await asyncio.sleep(emote_info["duration"])  # Use the duration from the emote info



    async def on_whisper(self, user: User, message: str) -> None:
        await self.highrise.send_whisper(user.id, message)
        if message.lower().startswith("hello"):
            await self.highrise.send_whisper(user.id,f"Hello, <@{user.username}>!")
        if message.lower().startswith("-help"):
            await self.highrise.send_whisper(user.id,"Here are the commands you can use: -host, -summon, -goto, -username, etc.")






    async def start_welcome_loop(self) -> None:
        """Starts a loop that sends a welcome message to the room."""
        while True:
            await self.highrise.chat(f"Welcome to {self.room_name} \nPlease PM 'hello' to me for making your profile\nPM '-emotelist' to get the Emote list")
            await asyncio.sleep(2600)  # Sleep for 15 seconds


    async def show_roles(self, user: User) -> None:
        """Show the roles of users to the authorized user."""
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id, "You are not authorized to view roles.")
            return

        # Prepare the roles message
        roles_message = "User Roles:\n"
        for username, role in self.user_roles.items():
            roles_message += f"@{username}: {role}\n"

        # Send the roles message to the authorized user
        await self.highrise.send_whisper(user.id, roles_message)
    async def get_host_coordinates(self, user: User) -> None:
        if user.username not in self.room_owner:
            await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
            return
        # Get the user's current position
        response = await self.highrise.get_room_users()
        user_position = None

        for content in response.content:
            if content[0].id == user.id:
                user_position = content[1]  # Assuming content[1] is the user's position
                break

        if user_position is None:
            await self.highrise.send_whisper(user.id, "Could not retrieve your position.")
            return

        logger.info(f"User Position: {user_position}")

        await self.highrise.send_whisper(user.id, f"Your Position: {user_position}")

    async def promote_user(self, user: User, message: str) -> None:
        if message.startswith("-promote"):
            if user.username not in self.Moderator:
                await self.highrise.chat("You do not have permission to use this command.")
                return

            parts = message.split()
            if len(parts) != 3:
                await self.highrise.chat("Invalid promote command format. Use: promote @username role")
                return

            _, username, role = parts
            username = username[1:] if username.startswith("@") else username

            if role.lower() not in ["moderator", "designer","host"]:
                await self.highrise.chat("Invalid role, please specify a valid role.")
                return

            await self.change_user_role("promote", username, role)

    async def demote_user(self, user: User, message: str) -> None:
        if message.startswith("-demote"):
            if user.username not in self.Moderator:
                await self.highrise.chat("You do not have permission to use this command.")
                return

            parts = message.split()
            if len(parts) != 3:
                await self.highrise.chat("Invalid demote command format. Use: demote @username role")
                return

            _, username, role = parts
            username = username[1:] if username.startswith("@") else username

            if role.lower() not in ["moderator", "designer"]:
                await self.highrise.chat("Invalid role, please specify a valid role.")
                return

            await self.change_user_role("demote", username, role)
    async def give_role(self, user: User, message: str) -> None:
        """Assigns a role to a user."""
        parts = message.split(" ")
        if len(parts) < 3:
            await self.highrise.chat("Usage: -give <role> <@username>")
            return

        role = parts[1].lower()
        target_username = parts[2][1:] if parts[2].startswith("@") else parts[2]

        # Validate the role
        if role not in self.roles.valid_roles:
            await self.highrise.chat(f"Invalid role '{role}'. Available roles: {', '.join(self.roles.valid_roles)}.")
            return

        # Assign the role using the Roles class
        result = self.roles.assign_role(target_username, role)
        self.user_roles[target_username] = role  # Save the assigned role
        await self.highrise.chat(result)

        # Save user roles to file
        self.save_user_roles()  # Save roles after assignment

    async def remove_role(self, user: User, message: str) -> None:
        """Removes a role from a user."""
        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -remove <@username>")
            return

        target_username = parts[1][1:] if parts[1].startswith("@") else parts[1]

        # Check if the user is authorized to remove roles
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
            return

        # Remove the role from the user
        if target_username in self.user_roles:
            del self.user_roles[target_username]
            self.save_user_roles()  # Save changes to the user roles file
            await self.highrise.send_whisper(user.id, f"Role removed from @{target_username}.")
        else:
            await self.highrise.send_whisper(user.id, f"User @{target_username} does not have a role.")

    async def send_heart_reaction(self, user: User) -> None:
        """Sends a heart reaction to all users in the room if the user has the required role."""
        # Check if the user has a role
        if user.username not in self.Moderator and user.username not in self.user_roles:
            await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
            return

        # Get the list of users in the room
        room_users = await self.highrise.get_room_users()

        # Send heart reaction to each user
        for room_user, _ in room_users.content:
            try:
                await self.highrise.react("heart", room_user.id)  # Sending heart reaction
            except Exception as e:
                print(f"Failed to send heart reaction to {room_user.username}: {str(e)}")

        await self.highrise.send_whisper(user.id, "Sent heart reactions to all users!")

    async def send_heart_reaction_to_user(self, user: User, message: str) -> None:
        if user.username not in self.Moderator and user.username not in self.user_roles:
            await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
            return
        """Sends a specified number of heart reactions to a specific user."""
        parts = message.split(" ")
        if len(parts) < 3:
            await self.highrise.send_whisper(user.id, "Usage: -heart <@username> <number of hearts>")
            return

        target_username = parts[1][1:] if parts[1].startswith("@") else parts[1]  # Remove '@' if present
        try:
            number_of_hearts = int(parts[2])  # Convert the number of hearts to an integer
        except ValueError:
            await self.highrise.send_whisper(user.id, "Please provide a valid number of hearts (max 100).")
            return

        # Limit the number of hearts to 100
        if number_of_hearts > 500:
            number_of_hearts = 500

        # Find the target user in the room
        room_users = await self.highrise.get_room_users()
        target_user_id = None
        for room_user, _ in room_users.content:
            if room_user.username.lower() == target_username.lower():
                target_user_id = room_user.id
                break

        if target_user_id is None:
            await self.highrise.send_whisper(user.id, f"User @{target_username} not found in the room.")
            return

        # Send the specified number of heart reactions
        for _ in range(number_of_hearts):
            try:
                await self.highrise.react("heart", target_user_id)  # Sending heart reaction
            except Exception as e:
                await self.highrise.send_whisper(user.id, f"Failed to send heart reaction: {str(e)}")
                return

        await self.highrise.send_whisper(user.id, f"Sent {number_of_hearts} hearts to @{target_username}!")
    async def send_wink_reaction(self, user: User) -> None:
        """Sends a wink reaction to all users in the room if the user has the required role."""
        # Check if the user has a role
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id, "You are not authorized to use this command.")
            return

        # Get the list of users in the room
        room_users = await self.highrise.get_room_users()

        # Send heart reaction to each user
        for room_user, _ in room_users.content:
            try:
                await self.highrise.react("wink", room_user.id)  # Sending wink reaction
            except Exception as e:
                print(f"Failed to send wink reaction to {room_user.username}: {str(e)}")

        await self.highrise.send_whisper(user.id, "Sent wink reactions to all users!")
        
    async def freeze_user(self, user: User, message: str) -> None:
        """Freezes a user at their current position."""
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
            return

        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -stuck @username")
            return

        target_username = parts[1][1:]  # Remove '@' from the username

        # Find the target user in the room
        room_users = await self.highrise.get_room_users()
        target_user = None
        target_position = None  # Initialize target_position

        for room_user, position in room_users.content:
            if room_user.username.lower() == target_username.lower():
                target_user = room_user
                target_position = position  # Get the position from the room_users
                break

        if target_user:
                # Store the user's current position using their ID
                self.frozen_users[target_user.id] = {
                    "username": target_user.username,
                    "position": target_position  # Ensure this is a Position object
                }
                await self.highrise.send_whisper(user.id, f"User @{target_username} has been frozen at their current position.")
        else:
            await self.highrise.send_whisper(user.id, f"User @{target_username} not found in the room.")


    async def monitor_frozen_users(self):
        """Monitor frozen users and teleport them back if they move."""
        while True:
            await asyncio.sleep(1)  # Check every second
            for user_id, user_data in list(self.frozen_users.items()):
                current_position = await self.user_position(user_id)
                original_position = user_data["position"]  # This should be a Position object

                # Check if the current position is different from the original position
                if (current_position.x != original_position.x or 
                    current_position.y != original_position.y or 
                    current_position.z != original_position.z):  # Include z-coordinate
                    await self.highrise.teleport(user_id, original_position)  # Teleport back to original position

    async def user_position(self, user_id: str) -> Position:
        """Get the current position of a user by their ID."""
        room_users = await self.highrise.get_room_users()
        for room_user, position in room_users.content:
            if room_user.id == user_id:
                return position  # Return the Position object
        return None  # Return None if the user is not found
    
    async def unfreeze_user(self, user: User, message: str) -> None:
        """Unfreezes a user, allowing them to move freely."""
        if user.username not in self.Moderator:
            await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
            return

        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -leave @username")
            return

        target_username = parts[1][1:]  # Remove '@' from the username

        # Check if the user is frozen
        target_user_id = None
        for user_id, data in self.frozen_users.items():
            if data["username"].lower() == target_username.lower():
                target_user_id = user_id
                break

        if target_user_id and target_user_id in self.frozen_users:
            del self.frozen_users[target_user_id]  # Remove the user from the frozen_users dictionary
            await self.highrise.send_whisper(user.id, f"User @{target_username} has been unfrozen.")
        else:
            await self.highrise.send_whisper(user.id, f"User @{target_username} is not frozen or not found.")
    async def give_mod(self, user: User, message: str) -> None:
        """Gives moderator role to a specified user, only if the command is issued by the room owner."""
        if user.username not in self.room_owner:
            await self.highrise.send_whisper(user.id, "You do not have permission to use this command.")
            return

        parts = message.split(" ")
        if len(parts) < 2:
            await self.highrise.send_whisper(user.id, "Usage: -mod @username")
            return

        target_username = parts[1][1:]  # Remove the '@' from the username

        # Find the target user in the room
        room_users = await self.highrise.get_room_users()
        target_user = None
        for room_user, _ in room_users.content:
            if room_user.username.lower() == target_username.lower():
                target_user = room_user
                break

        if target_user:
            # Debugging output
            print(f"Attempting to add {target_user.username} as a moderator.")

            # Add the target user to the Moderator list
            if target_user.username not in self.Moderator:
                self.Moderator.append(target_user.username)
                self.save_moderators()  # Save the updated moderator list
                await self.highrise.send_whisper(user.id, f"{target_username} has been given moderator privileges.")
            else:
                await self.highrise.send_whisper(user.id, f"{target_username} is already a moderator.")
        else:
            await self.highrise.send_whisper(user.id, f"User @{target_username} not found in the room.")

    async def run(self):
        bot_definition = __main__.BotDefinition(self, self.room_id, self.token)
        await __main__.main([bot_definition])


if __name__ == "__main__":
    room_id = "6771048903b4ddc599e5a8dd"  # Replace with your room ID
    token = "9b87d2fa3947148c45583fd5812401aca8f3a05028fc657d59bfee41396779a3"  # Replace with your API token
    asyncio.run(MyBot(room_id, token).run())

        