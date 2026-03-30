# Righteous Clan bot
The discord bot for Righteous Clan

## Commands
### Public
`/leaderboard` - sends the comp leaderboard

... yeah only one public command 💀

## Private (mod only)
`/add <player_ign>` - Adds a player to the first unclaimed spot in the leaderboard

`/remove <player_ign>` - Removes a player from the leaderboard and shifts leaderboard positions accordingly 

`/replace <player_ign> <new_player_ign>` - Replaces a player in the leaderboard with a new one in the same position 

`/swap <player_ign> <position>` - Swaps the position of a player with the player in the specified position

`/result <player1> <player2>` - Posts comp fight result in an embed in the `#comp-results` channel with stuff like total matches, each player's wins, win percentage of each player and the winner which is automatically detected from the provided score

## For nerds
The leaderboard is stored in a JSON file (`lb.json`) because a whole ass database would've been unnecessary af

the Fastapi app in the code exists because the bot is deployed as a web service on render where the bot is a asyncio task coz I'm broke to purchase render's background worker (tho other hosts exist that allow bot deployment without requiring a web service but eh who cares, render gets the job done)

took 5 hours to make smh ✌️💔

