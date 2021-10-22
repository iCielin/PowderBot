# DuckBot
A Python 3.7 Discord.py bot created for ASA.    
    
## Requirements   
discord.py    
    
## Example bot/config.py    
```py
counting_channel = 1234567890 # Your channel ID
embed_color = 0x000000 # Your color of choice
prefix = "Your prefix"
star_channel = 1234567890 # Your channel ID
star_quota = 2 # The amount of stars needed to get a message onto starboard
token = "Your token"
version = "Version name"

embed_footer_text = "Your choice of embed footer"
```    
    
## Example data_storage.json
```json
{
    "counting": {
        "last-count": {
            "number": 0,
            "member": 0
        },
        "record": 0
    }
}