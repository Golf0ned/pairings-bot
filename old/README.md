<div align="center">
<pre>
 ███████████             ███             ███                             
░░███░░░░░███           ░░░             ░░░                              
 ░███    ░███  ██████   ████  ████████  ████  ████████    ███████  █████ 
 ░██████████  ░░░░░███ ░░███ ░░███░░███░░███ ░░███░░███  ███░░███ ███░░  
 ░███░░░░░░    ███████  ░███  ░███ ░░░  ░███  ░███ ░███ ░███ ░███░░█████ 
 ░███         ███░░███  ░███  ░███      ░███  ░███ ░███ ░███ ░███ ░░░░███
 █████       ░░████████ █████ █████     █████ ████ █████░░███████ ██████ 
░░░░░         ░░░░░░░░ ░░░░░ ░░░░░     ░░░░░ ░░░░ ░░░░░  ░░░░░███░░░░░░  
             ███████████            █████                ███ ░███        
            ░░███░░░░░███          ░░███                ░░██████         
             ░███    ░███  ██████  ███████               ░░░░░░          
             ░██████████  ███░░███░░░███░                                
             ░███░░░░░███░███ ░███  ░███                                 
             ░███    ░███░███ ░███  ░███ ███                             
             ███████████ ░░██████   ░░█████                              
            ░░░░░░░░░░░   ░░░░░░     ░░░░░                               

---------------------------------------------------------------------------
discord bot to post tabroom pairings
</pre>
</div>

Ever forget to check tabroom and end up late to a round because it didn't send a notification? Tired of constantly refreshing Tabroom the minute pairings are supposed to be released and straining your fingers?

Enter PairingsBot---a Discord bot that blasts Tabroom pairings to your server. Stress less about pairings, and more about the round ahead of you.

<!-- <details>

<summary>Table of Contents</summary>

pfft you thought i had time to implement this. will do once i write more stuff sorry

</details> -->

## Features & Commands

### Help
```
/help
```

Displays all commands.

<img width="497" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/a9cdd2c3-0032-41ad-90cf-5f54eb74eba5">


### Configure Blasts
```
/configureblasts <school> <channel>
```

Sets the school to filter pairings by and the channel that blasts should be sent to.

<img width="416" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/d873d396-3c0b-42e5-93fb-d1bc213d8205">

`school`: school name, as displayed on Tabroom.

`channel`: Discord channel blasts will be sent to.


### Configure Tournament
```
/configuretournament <tournament-id> <event-id>
```

Sets the tournament and event pairings will be pulled from.

<img width="319" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/5b692f5b-b6d0-470c-a514-96faf5a42628">

`tournament-id`: Tabroom's tournament id, as shown below.

`event-id`: Tabroom's event id in the URL, as shown below.

<img width="800" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/fec2fba6-8463-4a9a-89b0-a05d7190fd85">


### Display Config
```
/displayconfig
```

Displays all configured settings. If a specific section isn't configured, tells which section isn't configured.

<img width="290" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/3d19d76c-4029-44d0-8c08-0e49bc3f1a25">


### Start Blasts
```
/startblasts
```

Starts tournament blasts. Checks every 8 seconds.

<img width="271" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/47364abc-4f71-4fa4-ada4-ea497f8975f7">

A blast contains all teams of the configured school and their sides, opponents, judge(s), and room.

<img width="316" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/3789ccbe-d577-4cb1-9740-988b4c844535">

### Stop Blasts
```
/stopblasts
```

Stops tournament blasts.

<img width="240" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/649d76d1-c920-4d53-aab1-b310e42b64bc">


### Pairings
```
/pairings <optional team-code>
```

Post the pairings from the most recent round for for a specific team/partnership.

`team-code`: initials of the team code, as shown in screenshot (optional)

If `team-code` is left empty, posts pairings for all teams/partnerships under the configured school.

<img width="305" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/0a907ad0-205e-4b97-9b7a-63296c3060be">

Refer to [`/startblasts`](https://github.com/Golf0ned/pairings-bot#start-blasts) for more info on blasts.


## Getting Started/Setup

I'm not looking for this bot to get formal Discord verification. If enough people use it and I get an angry email from Palmer, I'll rewrite it to be public.

For those who are interested in using this bot for their own teams, download the most recent package on the repo, update the `.env` file, and host through whichever service you fancy.

I personally used Railway via GitHub repo. Here's a template link (note the referral code---feel free to remove): https://railway.app/template/JabnMS?referralCode=gV3U7a

[UPDATE 1/5/24] I had trouble installing the dependencies for discord.py on Python 3.12. You should use Python 3.11...for the time being[sic]. The template is updated to reflect this.
