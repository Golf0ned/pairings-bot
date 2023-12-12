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

Tired of constantly refreshing Tabroom the minute pairings are supposed to be released?

Enter PairingsBot---a Discord bot that blasts Tabroom pairings to your server.

<!-- <details>

<summary>Table of Contents</summary>

pfft you thought i had time to implement this. will do once i write more stuff sorry

</details> -->

## Features & Commands

### Help
```
/help
```

Self-explanatory. Displays all commands.

<img width="484" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/cd08d0fd-7ab5-4200-93a4-8b71775e23e0">

### Configure Blasts
```
/configureblasts <school> <channel>
```

Sets the school to filter pairings by and the channel that blasts should be sent to.

<img width="381" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/6a2f41c2-2eaa-4eff-bba9-47c54eb7492b">

`school` should be identical to the school name as displayed on Tabroom.

`channel` is the channel blasts will be sent to.

### Configure Tournament
```
/configuretournament <tournament-id> <event-id>
```

Sets the tournament to blast pairings from and the event pairings will be pulled from.

<img width="296" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/39eed070-c273-43e4-871d-26c48cbde0da">

Both `tournament-id` and `event-id` can be found in the URL of the entries in the event on Tabroom.

<img width="923" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/8e89f6b1-882c-4025-9fe6-f31ae3727524">

### Display Config
```
/displayconfig
```

Displays all configured settings. If a specific section isn't configured, tells which section isn't configured.

(Insert screenshot here)

### Pairings
```
/pairings <optional team-code>
```

Post the pairings from the most recent round for a specific team/partnership.

If `team-code` is left blank, posts the pairings from the most recent round for all teams/parnerships.

Refer to [`/startblasts`](https://github.com/Golf0ned/pairings-bot#start-blasts) for more info on blasts.

The team code refers to just the initials of the team code (i.e. excluding school).

(Insert screenshots here)

### Start Blasts
```
/startblasts
```

Starts tournament blasts. Checks every 8 seconds.

<img width="271" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/47364abc-4f71-4fa4-ada4-ea497f8975f7">

A blast contains teams' sides, opponents, judges, and room.

(Insert screenshot here)

### Stop Blasts
```
/stopblasts
```

Stops tournament blasts.

<img width="240" alt="image" src="https://github.com/Golf0ned/pairings-bot/assets/60253050/649d76d1-c920-4d53-aab1-b310e42b64bc">

## Getting Started/Setup

This bot was not written for public use. As such, it most likely won't get formal Discord verification. If enough people use it and I get an angry email from Palmer, I'll rewrite it to be public.

For those who are interested in using this bot for their own teams, download the most recent package on the repo, update the `.env` file, and host through whichever service you fancy.

I personally used Railway via GitHub repo. Here's a template link (note the referral code---feel free to remove): https://railway.app/template/JabnMS?referralCode=gV3U7a
