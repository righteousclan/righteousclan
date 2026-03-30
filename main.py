import discord
from discord.ext import commands
import json
import fastapi
import asyncio
import os

BOT_TOKEN = os.getenv(BOT_TOKEN)

app = FastAPI()

@app.get("/")
async def root():
    return
    
@app.on_event("startup")
async def start_bot():
    asyncio.create_task(bot.start(BOT_TOKEN))

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="!")

lb = []
def load_lb():
    global lb
    try:
        with open("lb.json", "r") as f:
            content = f.read()
            if not content:
                return                            
            lb = json.loads(content)
    except FileNotFoundError:
         return
                  
def save_lb():
    with open("lb.json", "w") as f:
        f.write(json.dumps(lb))
        
@bot.event
async def on_ready():
    print("Logged in")
    await bot.tree.sync()
    print("Synced commands") 
    load_lb()
    print("Loaded leaderboard")
    
@bot.tree.command(name="leaderboard", description="View the comp leaderboard")
async def leaderboard(interaction: discord.Interaction):
   await interaction.response.defer()
   emojis = {
              1: "🥇",
              2:"🥈",
              3:"🥉",
              4:"4️⃣",
              5: "5️⃣" ,
              6: "6️⃣",
              7: "7️⃣",
              8: "8️⃣",
              9: "9️⃣",
              10: "🔟"
          }
          
   embed = discord.Embed(
	                    title="Comp Leaderboard 🏆",
	                    color=discord.Colour.yellow()
                    )
                    
   if not lb:
       for r in range(1, 11):
           embed.add_field(name=emojis[r], value="Unclaimed")                      
                    
   for position, player in enumerate(lb):
       embed.add_field(name=emojis[position+1], value=f"**{player}**")

   if len(lb) < 10:
       unclaimed = 10 - len(lb)
       for r in range(len(lb) + 1, 11):
           embed.add_field(name=emojis[r], value="Unclaimed")
   
   await interaction.followup.send(embed=embed)

    
@bot.tree.command(name="add", description="Add a player to the leaderboard")         
@commands.has_permissions(manage_guild=True)
async def add(interaction: discord.Interaction, player_ign: str):
    await interaction.response.defer(ephemeral=True)
    if len(lb) == 10:
        await interaction.followup.send("The leaderboard is already full, can't add more players.", ephemeral=True)
        return
    lb.append(player_ign)
    save_lb()
    await interaction.followup.send(f"Successfully added {player_ign} to the first unclaimed position!")
    
@bot.tree.command(name="remove", description="Remove a player from the leaderboard")         
@commands.has_permissions(manage_guild=True)
async def remove(interaction: discord.Interaction, player_ign: str):
    await interaction.response.defer(ephemeral=True)
    if not player_ign.strip() in lb:
        await interaction.followup.send(f"{player_ign.strip()} doesn't exist in the leaderboard", ephemeral=True) 
        return
    lb.remove(player_ign.strip())
    save_lb()
    await interaction.followup.send(f"Successfully removed {player_ign.strip()} from the leaderboard!")
    
    
@bot.tree.command(name="swap", description="Swap a player's postion in the leaderboard")         
@commands.has_permissions(manage_guild=True)
async def swap(interaction: discord.Interaction, player_ign: str, position: int):
    await interaction.response.defer(ephemeral=True)
    
    if position > 10:
        await interaction.followup.send(f"Position {position} doesn't exist. The leaderboard has only 10 slots", ephemeral=True)
        return
     
    if len(lb) < position:
        await interaction.followup.send(f"Cannot swap with an unclaimed position ({position}). Use /add to add someone to the first unclaimed position.", ephemeral=True)
        return 
        
    if not player_ign.strip() in lb:
        await interaction.followup.send(f"{player_ign.strip()} doesn't exist in the leaderboard", ephemeral=True)
        return
        
    player_to_swap = lb.index(player_ign.strip())
    swap_with = position - 1
    
    lb[player_to_swap], lb[swap_with] = lb[swap_with], lb[player_to_swap]
    save_lb()
    
    await interaction.followup.send("Successfully swapped positions!", ephemeral=True)

@bot.tree.command(name="replace", description="Replace a player in the leaderboard")    
@commands.has_permissions(manage_guild=True)
async def replace(interaction: discord.Interaction, player_ign: str, new_player_ign: str):
     await interaction.response.defer(ephemeral=True)
     if not player_ign.strip() in lb:
        await interaction.followup.send(f"{player_ign.strip()} doesn't exist in the leaderboard", ephemeral=True)
        return
        
     player_to_replace = lb.index(player_ign.strip())
     lb[player_to_replace] = new_player_ign
     save_lb()
     await interaction.followup.send(f"Successfully replaced {player_ign} with {new_player_ign}", ephemeral=True)
    
@bot.tree.command(name="result", description="Post a comp match result")
@commands.has_permissions(manage_guild=True)
async def pr(interaction: discord.Interaction, player1: str, player2: str, score: str):
    try:
        player1_score, player2_score = tuple(score.split("-"))
        player1_score, player2_score = int(player1_score), int(player2_score) 
    except Exception:
        await interaction.followup.send("Score must be like this: 2-3, 4-1", ephemeral=True)
        return
        
    channel = await bot.fetch_channel(1488144108550750389)
    desc = f"""
     **Total matches**: {player1_score+player2_score}
**{player1}** score: {player1_score} ({round((player1_score/player1_score+player2_score)*100)}%)
**{player2}** score: {player2_score} ({round((player2_score/player1_score+player2_score)*100)}%)
       
**Winner 🏆**: **{player1 if player1_score > player2_score else player2}** (by +{player1_score - player2_score if player1_score > player2_score else player2_score - player1_score})
     """
    draw_desc = f"""
     **Total matches**: {player1_score+player2_score}
**{player1}** score: {player1_score} (50%)
**{player2}** score: {player2_score} (50%)
       
**Winner 🏆**: None
     """
  
    embed = discord.Embed(
                      title="Comp Fight Result",
                      description=draw_desc if player1_score == player2_score else desc,
                      color=discord.Colour.gold()
                      ) 
    await channel.send(embed=embed)
    await interaction.followup.send("Succesfully posted results in <#1488144108550750389>")
             
             
bot.run(BOT_TOKEN)
    
    

        
              
	
