from discord.ext.commands import command
from discord.ext.commands import  Cog
from discord import Role
from ..db import db
from discord.utils import get



class welcome(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command(name="role")
    async def give_role_to_someone(self, ctx, member, role: Role = None):
        if role == None:
            for role in ctx.author.roles:
                if role.name == "Newbie":
                    await ctx.author.remove_roles(ctx.guild.get_role(775674479598370846))
            role = get(ctx.guild.roles, name=f"{member}")
            await self.bot.log_message(f"**{ctx.author.name}** gave himself/herself a role **{role}** ")
            await ctx.author.add_roles(role)

        else:
            if ctx.author.guild_permissions.administrator:
                user = ctx.guild.get_member(self.member_id_maker(member))

                await self.bot.log_message(f"**{ctx.author.name}** gave role **{role}** to **{ctx.author.name}**")
                await user.add_roles(role)

            else:
                user = ctx.guild.get_member(self.member_id_maker(member))

                await self.bot.log_message(f"**{ctx.author.name}** tried to give **{user.name}** role **{role}** without permission!")
                await ctx.channel.send("You don't have permissions to do that! Try **!role <ROLE>**")


    def member_id_maker(self, member):
        for i in ['<', '>', '!', '@']:
            member = member.replace(i, '')

        # Строчка кода от Миши
        # member = str(member[3:-1])

        return int(member)


    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO students(UserID) VALUES (?)",
                   member.id)

        await self.bot.log_message(f"**{member.name}** has joined the server")
        await member.add_roles(member.guild.get_role(775674479598370846))


    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM students WHERE UserID = ?", member.id)

        await self.bot.log_message(f"**{member.name}** has left the server")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")


def setup(bot):
    bot.add_cog(welcome(bot))