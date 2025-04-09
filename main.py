import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



# 🔒 รายชื่อ channel ที่จะ "ล็อก" ไม่ให้พิมพ์ (ใส่เป็นชื่อหรือ ID ก็ได้)
locked_channels = ["ล็อกแชท", "secret-channel"]  # หรือใส่เป็น ["123456789012345678"]

@bot.event
async def on_ready():
    print(f'บอท {bot.user} พร้อมใช้งานแล้ว!')

# ✅ ระบบล็อกแชท (ลบข้อความทันที)
@bot.event
async def on_message(message):
    if message.channel.name in locked_channels and not message.author.bot:
        await message.delete()
        print(f"ลบข้อความจาก {message.author} ในห้อง {message.channel.name}")
        return
    await bot.process_commands(message)

# 🧹 ลบข้อความหลายข้อความ
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount > 100:
        await ctx.send("ลบได้สูงสุด 100 ข้อความต่อครั้งนะ")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 คือลบคำสั่ง !clear ด้วย
    await ctx.send(f"🧹 ลบ {len(deleted)-1} ข้อความแล้ว", delete_after=3)

# ✅ คำสั่งเพิ่ม/ลบห้องจากลิสต์ล็อก
@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx):
    channel = ctx.channel.name
    if channel in locked_channels:
        await ctx.send("ห้องนี้ถูกล็อกอยู่แล้ว 🔒")
    else:
        locked_channels.append(channel)
        await ctx.send("ล็อกห้องนี้เรียบร้อยแล้ว 🔒")

@bot.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):
    channel = ctx.channel.name
    if channel in locked_channels:
        locked_channels.remove(channel)
        await ctx.send("ปลดล็อกห้องนี้เรียบร้อยแล้ว 🔓")
    else:
        await ctx.send("ห้องนี้ยังไม่ได้ถูกล็อกนะ")
server_on()  # เรียกใช้ฟังก์ชัน server_on() เพื่อเริ่มเซิร์ฟเวอร์ Flask
bot.run(os.getenv('TOKEN'))  # ใช้ Token จาก environment variable
