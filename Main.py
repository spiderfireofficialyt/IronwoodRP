import discord
from discord.ext import commands
import time

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

active_sessions = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ---------------- SESSION START ----------------
@bot.command(name="sessionstart")
async def sessionstart(ctx):
    role_id = 1515898985204944966

    if not any(role.id == role_id for role in ctx.author.roles):
        await ctx.send("❌ No permission.")
        return

    start_time = int(time.time())

    embed = discord.Embed(
        title="📊 Session Information",
        color=discord.Color.green()
    )

    embed.add_field(name="Server Name", value="Ironwood State Roleplay", inline=False)
    embed.add_field(name="Server Owner", value="spider_spaz25", inline=False)
    embed.add_field(name="Code", value="ISRPNew", inline=False)
    embed.add_field(name="Session Started", value=f"<t:{start_time}:R>", inline=False)
    embed.add_field(name="Session Started By", value=ctx.author.mention, inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1518798605417451601/1518806629729173644/2.png")

    msg = await ctx.send(
        content="<@&1515899006922920107> <@&1515898975763562579> @here",
        embed=embed
    )

    await msg.add_reaction("👍")

# ---------------- VOTING ----------------
@bot.command(name="sessionvote")
async def sessionvote(ctx):
    role_id = 1515898985204944966

    if not any(role.id == role_id for role in ctx.author.roles):
        await ctx.send("❌ No permission.")
        return

    start_time = int(time.time())

    embed = discord.Embed(
        title="📊 Session Vote Started",
        description=(
            "Hello, Ironwood members. A fellow staff member has started a vote.\n\n"
            "**Please vote 👍 to start a session.**\n"
            "We are requiring **7 votes**."
        ),
        color=discord.Color.green()
    )

    embed.add_field(name="Votes", value="0 / 7", inline=False)
    embed.add_field(name="Session Started", value=f"<t:{start_time}:R>", inline=False)
    embed.add_field(name="Started By", value=ctx.author.mention, inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1518798605417451601/1518806629729173644/2.png")

    msg = await ctx.send(
        content="<@&1515899006922920107> <@&1515898975763562579> @here",
        embed=embed
    )

    await msg.add_reaction("👍")

    active_sessions[msg.id] = {
        "votes": set(),
        "required": 7,
        "start_time": start_time,
        "starter": ctx.author.id
    }

# ---------------- SESSION SHUTDOWN ----------------
@bot.command(name="sessionshutdown")
async def sessionshutdown(ctx):
    role_id = 1515898985204944966

    if not any(role.id == role_id for role in ctx.author.roles):
        await ctx.send("❌ No permission.")
        return

    end_time = int(time.time())

    embed = discord.Embed(
        title="🚨 Session Shutdown",
        description=(
            "**The current session has been shut down.**\n\n"
            "Thank you to everyone who attended."
        ),
        color=discord.Color.red()
    )

    embed.add_field(name="Session Ended By", value=ctx.author.mention, inline=False)
    embed.add_field(name="Time", value=f"<t:{end_time}:R>", inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1518798605417451601/1518806629729173644/2.png")

    await ctx.send(embed=embed)
    import discord
from discord import app_commands
from discord.ext import commands

ALLOWED_ROLE_ID = 1515898934650994729
LOG_CHANNEL_ID = 1515899244404543672

BANNER_URL = "https://cdn.discordapp.com/attachments/1518798605417451601/1518806626772193301/6.png"

class Promotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_permission(self, interaction: discord.Interaction) -> bool:
        return any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)

    @app_commands.command(name="promote", description="Promote a member to a new rank")
    @app_commands.describe(
        member="Member to promote",
        new_rank="New role to assign",
        reason="Reason for promotion"
    )
    async def promote(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        new_rank: discord.Role,
        reason: str
    ):

        if not self.has_permission(interaction):
            return await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True
            )

        await member.add_roles(new_rank, reason=f"Promoted by {interaction.user} | {reason}")

        embed = discord.Embed(
            title="Promotion Notice",
            color=discord.Color.green(),
            description=(
                f"**Member:** {member.mention}\n"
                f"**New Rank:** {new_rank.mention}\n"
                f"**Reason:** {reason}\n"
                f"**Promoted by:** {interaction.user.mention}"
            )
        )
        embed.set_image(url=BANNER_URL)

        # DM user
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            pass

        # Log channel
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        # Public channel response
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Promotion(bot))
    import discord
from discord import app_commands
from discord.ext import commands

ALLOWED_ROLE_ID = 1515898934650994729
LOG_CHANNEL_ID = 1515899245738328155

BANNER_URL = "https://cdn.discordapp.com/attachments/1518798605417451601/1518806619440418816/7.png"

import discord
from discord import app_commands
from discord.ext import commands

ALLOWED_ROLE_ID = 1515898934650994729
LOG_CHANNEL_ID = 1515899245738328155

BANNER_URL = "https://cdn.discordapp.com/attachments/1518798605417451601/1518806619440418816/7.png"

class InfractionSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cases = {}
        self.case_counter = 0

    def has_permission(self, interaction: discord.Interaction) -> bool:
        return any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)

    # ---------------- INFRACTION ----------------
    @app_commands.command(name="infraction", description="Issue an infraction (creates a case)")
    async def infraction(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        severity: str,
        reason: str
    ):

        if not self.has_permission(interaction):
            return await interaction.response.send_message(
                "No permission.",
                ephemeral=True
            )

        self.case_counter += 1
        case_id = f"CASE #{self.case_counter}"

        self.cases[case_id] = {
            "member_id": member.id,
            "moderator_id": interaction.user.id,
            "severity": severity,
            "reason": reason,
            "revoked": False
        }

        embed = discord.Embed(
            title=f"Infraction Logged | {case_id}",
            color=discord.Color.red(),
            description=(
                f"**Member:** {member.mention}\n"
                f"**Severity:** {severity}\n"
                f"**Reason:** {reason}\n"
                f"**Issued by:** {interaction.user.mention}"
            )
        )
        embed.set_image(url=BANNER_URL)

        # DM user
        try:
            dm_embed = discord.Embed(
                title="Infraction Received",
                color=discord.Color.red(),
                description=(
                    f"**Server:** {interaction.guild.name}\n"
                    f"**Case:** {case_id}\n"
                    f"**Severity:** {severity}\n"
                    f"**Reason:** {reason}"
                )
            )
            dm_embed.set_image(url=BANNER_URL)

            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass

        # Log channel
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        # Public response (MENTION USER)
        await interaction.response.send_message(
            f"⚠️ {member.mention} has received **{case_id}** | {severity}\nReason: {reason}"
        )

    # ---------------- REVOKE ----------------
    @app_commands.command(name="revoke", description="Revoke an infraction case")
    async def revoke(
        self,
        interaction: discord.Interaction,
        case_id: str,
        reason: str
    ):

        if not self.has_permission(interaction):
            return await interaction.response.send_message(
                "No permission.",
                ephemeral=True
            )

        case = self.cases.get(case_id)

        if not case:
            return await interaction.response.send_message(
                "Case not found.",
                ephemeral=True
            )

        if case["revoked"]:
            return await interaction.response.send_message(
                "This case is already revoked.",
                ephemeral=True
            )

        case["revoked"] = True

        member = interaction.guild.get_member(case["member_id"])

        embed = discord.Embed(
            title=f"Case Revoked | {case_id}",
            color=discord.Color.green(),
            description=(
                f"**Member:** {member.mention if member else case['member_id']}\n"
                f"**Original Reason:** {case['reason']}\n"
                f"**Revoke Reason:** {reason}\n"
                f"**Revoked by:** {interaction.user.mention}"
            )
        )
        embed.set_image(url=BANNER_URL)

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

        await interaction.response.send_message(
            f"✅ {case_id} has been revoked.\nReason: {reason}"
        )

async def setup(bot):
    await bot.add_cog(InfractionSystem(bot))

import discord
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.hybrid_command(
        name="afk",
        description="Set yourself as AFK."
    )
    async def afk(self, ctx, *, reason: str = "AFK"):
        self.afk_users[ctx.author.id] = reason

        embed = discord.Embed(
            title="💤 AFK Enabled",
            description=f"{ctx.author.mention} is now AFK.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Remove AFK status
        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]

            embed = discord.Embed(
                title="👋 Welcome Back!",
                description=f"{message.author.mention}, your AFK status has been removed.",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)

        # Notify if an AFK user is mentioned
        for member in message.mentions:
            if member.id in self.afk_users:
                embed = discord.Embed(
                    title="💤 User is AFK",
                    description=f"{member.mention} is currently AFK.",
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="Reason",
                    value=self.afk_users[member.id],
                    inline=False
                )
                await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AFK(bot))
    import discord
from discord import app_commands

FEEDBACK_CHANNEL_ID = 1515899324645511239

@bot.tree.command(
    name="feedback",
    description="Submit feedback for Ironwood State Roleplay."
)
@app_commands.describe(
    feedback="Tell us what you think about Ironwood."
)
async def feedback(interaction: discord.Interaction, feedback: str):
    channel = bot.get_channel(FEEDBACK_CHANNEL_ID)

    if channel is None:
        await interaction.response.send_message(
            "❌ The feedback channel could not be found.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📝 Ironwood Server Feedback",
        description=feedback,
        color=discord.Color.dark_blue()
    )

    embed.add_field(
        name="Submitted By",
        value=f"{interaction.user.mention}\n{interaction.user} (`{interaction.user.id}`)",
        inline=False
    )

    embed.add_field(
        name="Submitted At",
        value=f"<t:{int(interaction.created_at.timestamp())}:F>",
        inline=False
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(
        text="Ironwood State Roleplay • Community Feedback"
    )

    await channel.send(embed=embed)

    await interaction.response.send_message(
        "✅ Thank you! Your feedback has been submitted to the Ironwood management team.",
        ephemeral=True
    )
    import discord
from discord.ext import commands
from discord import app_commands

STAFF_ROLE_ID = 1515898975763562579
REQUEST_CHANNEL_ID = 1515899264159580232


class StaffRequestView(discord.ui.View):
    def __init__(self, requester_id: int):
        super().__init__(timeout=None)
        self.requester_id = requester_id

    @discord.ui.button(label="Respond", style=discord.ButtonStyle.green, emoji="📩")
    async def respond(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        # Only staff can respond
        if STAFF_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(
                "❌ Only staff members can use this button.",
                ephemeral=True
            )
            return

        # Disable the button
        button.disabled = True

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            f"<@{self.requester_id}> **{interaction.user.mention}** is now responding to your staff request.",
            allowed_mentions=discord.AllowedMentions(users=True)
        )


@bot.tree.command(
    name="staffrequest",
    description="Request assistance from the Ironwood staff team."
)
@app_commands.describe(
    reason="Why do you need a staff member?"
)
async def staffrequest(interaction: discord.Interaction, reason: str):

    channel = bot.get_channel(REQUEST_CHANNEL_ID)

    if channel is None:
        await interaction.response.send_message(
            "❌ Staff request channel not found.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📨 New Staff Request",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="Requested By",
        value=f"{interaction.user.mention}\n{interaction.user}",
        inline=False
    )

    embed.add_field(
        name="Reason",
        value=reason,
        inline=False
    )

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="Ironwood State Roleplay • Staff Request")

    await channel.send(
        content=f"<@&{STAFF_ROLE_ID}>",
        embed=embed,
        view=StaffRequestView(interaction.user.id),
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

    await interaction.response.send_message(
        "✅ Your staff request has been sent.",
        ephemeral=True
    )
    import discord
from discord.ext import tasks
import random
from datetime import time
import pytz

GENERAL_CHANNEL_ID = 1515899208446644285

quotes = [
    "💪 Discipline beats motivation when motivation fades.",
    "🚓 Stay ready so you never have to get ready.",
    "🎯 Focus on progress, not perfection.",
    "🔥 Pressure creates diamonds—stay steady under it.",
    "⭐ Consistency is what turns effort into results.",
    "🚔 Respect is earned through action, not words.",
    "⚡ Small steps daily lead to big results.",
    "🛡️ Control your mindset, control your outcome.",
    "🚀 Work in silence, let success make the noise.",
    "🌄 Every shift is a chance to improve.",
    "📈 Growth starts where comfort ends.",
    "💙 Stay calm under pressure, stay sharp under stress.",
    "🏆 Winners train, losers complain.",
    "🎖️ Your reputation is built one decision at a time.",
    "🚨 Stay alert. Stay alive. Stay sharp.",
    "🔥 Hard work never skips the grind.",
    "🌟 You don’t rise to the occasion—you fall to your training.",
    "🚓 Patrol with purpose, not boredom.",
    "⚡ Be the standard, not the exception.",
    "🎯 Precision comes from practice.",
    "🛡️ Leadership is action, not authority.",
    "🚔 Discipline is doing it even when you don’t feel like it.",
    "🌄 Every mistake is a lesson if you learn from it.",
    "💪 Strength is built in silence.",
    "🚀 Keep going when others quit.",
    "⭐ Your effort today builds your rank tomorrow.",
    "🔥 Stay hungry, stay humble.",
    "📊 Improvement is better than excuses.",
    "🚓 Serve with pride, protect with honor.",
    "🎖️ Respect the badge by respecting the work.",
    "⚡ Train your mind like you train your body.",
    "🛡️ Calm minds make sharp officers.",
    "🚨 Awareness is your greatest tool.",
    "🌟 Don’t wish for it—work for it.",
    "💙 Integrity is what you do when no one watches.",
    "🏆 Earn it daily.",
    "🚔 Responsibility is the price of authority.",
    "🔥 Push past limits, then create new ones.",
    "🚀 Hard days build strong officers.",
    "🎯 Stay locked in.",
    "⭐ Excellence is a habit, not an act.",
    "📈 Improve or repeat.",
    "🛡️ Control your reaction, control the situation.",
    "🚓 Duty first, everything else second.",
    "⚡ Make every second count.",
    "🌄 One shift can change everything.",
    "💪 You are stronger than yesterday.",
    "🔥 Don’t stop when you’re tired—stop when you’re done.",
    "🚨 Awareness prevents mistakes.",
    "🎖️ Respect the chain of command.",
    "🚔 Stay professional at all times.",
    "🌟 Lead yourself before you lead others.",
    "📊 Progress is built, not given.",
    "🛡️ Your mindset defines your performance.",
    "🚀 Keep improving even when no one notices.",
    "⭐ Discipline creates freedom.",
    "💙 Stay composed under pressure.",
    "🎯 Aim for consistency.",
    "🔥 Growth requires discomfort.",
    "🚓 Every call matters.",
    "⚡ Stay sharp, stay prepared.",
    "🛡️ Honor the uniform.",
    "🚔 Control the situation, don’t become it.",
    "🌄 Every shift is training.",
    "💪 Push harder than yesterday.",
    "🔥 Results follow effort.",
    "🚀 Build habits that build you.",
    "⭐ Earn respect, don’t demand it.",
    "📈 Keep leveling up.",
    "🛡️ Think before you act.",
    "🚓 Stay disciplined in chaos.",
    "⚡ Focus wins fights.",
    "🎯 Precision over speed.",
    "💙 Stay loyal to the mission.",
    "🏆 Excellence is expected.",
    "🚔 Never cut corners.",
    "🔥 Outwork your old self.",
    "🌟 Improvement is endless.",
    "🚀 Small discipline = big results.",
    "🛡️ Stay alert, stay safe.",
    "🚓 Control emotions, control outcomes.",
    "⚡ Be reliable under pressure.",
    "🎯 Stay mission-focused.",
    "💪 Strength comes from repetition.",
    "🔥 No excuses, only effort.",
    "🚨 Stay aware of everything.",
    "⭐ Be the officer others rely on.",
    "📈 Growth is daily.",
    "🛡️ Stay calm, act smart.",
    "🚔 Every decision matters.",
    "🌄 Keep moving forward.",
    "💙 Serve with purpose.",
    "🏆 Train like it matters—because it does.",
    "🚀 Never settle.",
    "🔥 Earn your place every day.",
    "🎖️ Respect is built, not given.",
    "⚡ Stay consistent.",
    "🎯 Master your basics.",
    "💪 Push limits safely.",
    "🚓 Stay professional always.",
    "🌟 Be better than yesterday."
]

@tasks.loop(time=time(hour=9, minute=0, tzinfo=pytz.timezone("America/Edmonton")))
async def daily_motivation():
    channel = bot.get_channel(GENERAL_CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="🌟 Ironwood Daily Motivation",
            description=random.choice(quotes),
            color=discord.Color.gold()
        )
        embed.set_footer(text="Ironwood State Roleplay • Stay disciplined")
        await channel.send(embed=embed)

@daily_motivation.before_loop
async def before_daily_motivation():
    await bot.wait_until_ready()

daily_motivation.start()
import discord
from discord import app_commands
import time

@bot.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    start_time = time.time()

    await interaction.response.send_message("🏓 Pinging...")

    end_time = time.time()
    api_latency = round(bot.latency * 1000)
    response_time = round((end_time - start_time) * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Bot Latency",
        value=f"{api_latency}ms",
        inline=True
    )

    embed.add_field(
        name="Response Time",
        value=f"{response_time}ms",
        inline=True
    )

    await interaction.edit_original_response(content=None, embed=embed)
    import discord
import time
from discord.ext import commands

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    start_time = time.time()

    msg = await ctx.send("🏓 Pinging...")

    end_time = time.time()
    api_latency = round(bot.latency * 1000)
    response_time = round((end_time - start_time) * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Bot Latency",
        value=f"{api_latency}ms",
        inline=True
    )

    embed.add_field(
        name="Response Time",
        value=f"{response_time}ms",
        inline=True
    )

    await msg.edit(content=None, embed=embed)
    import discord
from discord import app_commands

RP_LOG_CHANNEL = 1515899259579400213
STAFF_ROLE_ID = 1515898975763562579


@bot.tree.command(
    name="roleplayrequest",
    description="Submit a roleplay request for Ironwood."
)
@app_commands.describe(
    roblox_user="Roblox Username",
    roleplay_type="Type of roleplay (DOT, LEO, Fire, Civ, etc.)",
    location="Location (required for DOT)"
)
async def roleplayrequest(
    interaction: discord.Interaction,
    roblox_user: str,
    roleplay_type: str,
    location: str = None
):

    roleplay_type = roleplay_type.upper()

    if roleplay_type == "DOT" and not location:
        return await interaction.response.send_message(
            "❌ DOT roleplays require a location.",
            ephemeral=True
        )

    embed = discord.Embed(
        title="📋 Ironwood Permission Log",
        color=discord.Color.blue()
    )

    embed.add_field(name="👤 Discord User", value=interaction.user.mention, inline=False)
    embed.add_field(name="🎮 Roblox Username", value=roblox_user, inline=False)
    embed.add_field(name="🚨 Roleplay Type", value=roleplay_type, inline=False)
    embed.add_field(name="📍 Location", value=location or "N/A", inline=False)

    embed.set_footer(text="Ironwood State Roleplay • RP System")

    channel = bot.get_channel(RP_LOG_CHANNEL)

    if channel:
        await channel.send(

            embed=embed,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

    await interaction.response.send_message(
        "✅ Your roleplay request has been submitted.",
        ephemeral=True
    )

    import discord
from discord import app_commands
import time

# ---------------- CONFIG ----------------
STAFF_ROLE_ID = 1515898985204944966
PING_ROLE_ID = 1515899006922920107
PING_ROLE_2 = 1515898975763562579

active_sessions = {}

# ---------------- PERMISSION CHECK ----------------
def has_role(interaction: discord.Interaction):
    return any(role.id == STAFF_ROLE_ID for role in interaction.user.roles)


# ---------------- SESSION START ----------------
@bot.tree.command(name="sessionstart", description="Start a server session.")
async def sessionstart(interaction: discord.Interaction):

    if not has_role(interaction):
        return await interaction.response.send_message("❌ No permission.", ephemeral=True)

    start_time = int(time.time())

    embed = discord.Embed(
        title="📊 Session Information",
        color=discord.Color.green()
    )

    embed.add_field(name="Server Name", value="Ironwood State Roleplay", inline=False)
    embed.add_field(name="Server Owner", value="spider_spaz25", inline=False)
    embed.add_field(name="Code", value="ISRPNew", inline=False)
    embed.add_field(name="Session Started", value=f"<t:{start_time}:R>", inline=False)
    embed.add_field(name="Session Started By", value=interaction.user.mention, inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1518798605417451601/1518806629729173644/2.png")

    await interaction.response.send_message(
        content=f"<@&{PING_ROLE_ID}> <@&{PING_ROLE_2}>",
        embed=embed
    )


# ---------------- SESSION VOTE ----------------
@bot.tree.command(name="sessionvote", description="Start a session vote.")
async def sessionvote(interaction: discord.Interaction):

    if not has_role(interaction):
        return await interaction.response.send_message("❌ No permission.", ephemeral=True)

    start_time = int(time.time())

    embed = discord.Embed(
        title="📊 Session Vote Started",
        description="React 👍 to vote for session start. 7 votes required.",
        color=discord.Color.green()
    )

    embed.add_field(name="Votes", value="0 / 7", inline=False)
    embed.add_field(name="Started", value=f"<t:{start_time}:R>", inline=False)
    embed.add_field(name="Started By", value=interaction.user.mention, inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1518798605417451601/1518806629729173644/2.png")

    msg = await interaction.response.send_message(
        content=f"<@&{PING_ROLE_ID}> <@&{PING_ROLE_2}>",
        embed=embed
    )

    # store vote system
    active_sessions[interaction.id] = {
        "votes": set(),
        "required": 7,
        "starter": interaction.user.id
    }


# ---------------- SESSION SHUTDOWN ----------------
@bot.tree.command(name="sessionshutdown", description="End the current session.")
async def sessionshutdown(interaction: discord.Interaction):

    if not has_role(interaction):
        return await interaction.response.send_message("❌ No permission.", ephemeral=True)

    end_time = int(time.time())

    embed = discord.Embed(
        title="🚨 Session Shutdown",
        description="The current session has been shut down.",
        color=discord.Color.red()
    )

    embed.add_field(name="Ended By", value=interaction.user.mention, inline=False)
    embed.add_field(name="Time", value=f"<t:{end_time}:R>", inline=False)

    embed.set_image(url="https://cdn.discordapp.com/attachments/1518798605417451601/1518806629729173644/2.png")

    await interaction.response.send_message(embed=embed)

bot.run("MTUyMzM4MzEyNDkyMTI4Njc2Nw.GQjvwY.TcTNO1figVcz8ezQo9GM56ZIixzP-oAljmhOPI")