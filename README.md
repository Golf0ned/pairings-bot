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

### Configure Blasts
```
/configureblasts <school> <channel-id>
```

Sets the school to filter pairings by and the channel that blasts should be sent to.

`school` should be identical to the name as displayed on Tabroom.

`channel-id` refers to the developer ID of the channel blasts should be sent to. With developer mode on in Discord, you can copy the channel ID by right clicking the channel and selecting the bottom selection.

### Configure Tournament
```
/configuretournament <tournament-id> <event-id>
```

Sets the tournament to blast pairings from and the event pairings will be pulled from.

Both `tournament-id` and `event-id` can be found in the URL of the entries in the event on Tabroom.

(Insert screenshot here)

### Pairings
```
/pairings <optional team-code>
```

Post the pairings from the most recent round for a specific team/partnership.

If `team-code` is left blank, posts the pairings from the most recent round for all teams/parnerships.

The team code refers to just the initials of the team code (i.e. excluding school).

(Insert screenshot here)

### Start Blasts
```
/startblasts
```

Starts tournament blasts. Checks every 5 seconds.

### Stop Blasts
```
/stopblasts
```

Stops tournament blasts.

## Getting Started
Will be up ASAP!

(still wip, soz :/)
