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

## Getting Started
Will be up ASAP!

(still wip, soz :/)
