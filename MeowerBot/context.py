from datetime import datetime

import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Bot import Bot

import weakref
import requests
from .types.api.chats import ChatGroup
from .types.api.user import User as RawUser

class PartialChat:
    def __init__(self, id, bot: "Bot"):
        self.id = id
        self.bot: "Bot" = bot

    async def send_msg(self, message) -> Post:
        return await Post(self.bot, self.bot.api.send_post(self.id, message).to_dict(), self)

    async def fetch(self):
        return Chat(await self.bot.api.get_chat(self.id))

class Chat(PartialChat):
    def __init__(self, data: ChatGroup, bot):
        super().__init__(data._id, bot)

        self.created     = data.created
        self.deleted     = data.deleted
        self.last_active = data.last_active
        self.members     = data.members
        
        self.owner       = data.owner
        self.type        = data.type
        self.nickname    = data.nickname

class PartialUser:
    def __init__(self, username, bot: "Bot"):
        self.username = username
        self.bot = bot

    async def fetch(self):
        return User(self.username, RawUser.from_json(await self.bot.api._get_user(username, "")))

class User(PartialUser):
    def __init__(self, username, bot, data: RawUser):
        super().__init__(username, bot)

        self.data: RawUser = data

        self.banned = self.data.banned
        self.created = self.data.created
        self.flags = self.data.flags
        self.last_seen = self.data.last_seen
        self.data.lower_username =  self.data.lower_username
        self.lvl = self.data.lvl
        self.name = self.data.name
        self.permissions = self.data.permissions
        self.pfp_data = self.data.pfp_data
        self.quote = self.data.quote
        self.id = self.data.uuid
        

class Post:
    def __init__(self, bot, _raw, chat):
        self.bot = bot
        self._raw = _raw
        self.user: User = User(bot, self._raw["u"])

        self.chat: PartialChat = PartialChat(chat, bot)
        self.data = self._raw["p"]
        self._id = self._raw["post_id"]
        self.type = self._raw["type"]
        self.date = datetime.fromtimestamp(self._raw["t"]["e"])

    def __str__(self):
        return str(self.data)
    
    async def reply(self, message):
        self.chat.send_msg(f"@{self.user.name} [{self.id}]")


class Context:
    def __init__(self, post, bot):
        self.message = Post(bot, post)
        self.user = self.message.user
        self.bot = bot

    async def send_msg(self, msg):
        self.message.chat.send_msg(msg)

    async def reply(self, msg):
        await self.message.reply(msg)

