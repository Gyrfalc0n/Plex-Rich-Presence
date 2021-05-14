import time, os
from plexapi.myplex import MyPlexAccount
from pypresence import Presence
from decouple import config

# Python-PLEXapi : https://python-plexapi.readthedocs.io/en/latest/index.html
# PyPresence : https://pypi.org/project/pypresence/

# Get .env file parameters
USERNAME = config('USERNAME')
PASSWORD = config('PASSWORD')
SERVERNAME = config('SERVERNAME')

# Plex server connection
account = MyPlexAccount(USERNAME,PASSWORD)
plex = account.resource(SERVERNAME).connect()

# Refresh delay in seconds
refresh = 15
base_timer = int(time.time())

# Discord RPC connection and parameters
client_id = "842745089696596010"
image = "plex"
large_text = "Plex Media Server"
RPC = Presence(client_id)
RPC.connect()

# update function
def update():
    details = "Idling..."
    timer = int(time.time())
    is_idling = 1
    for item in plex.sessions():
        duration = round(item.duration/1000)
        current_time = round(item.viewOffset/1000)
        stop_time = timer + (duration - current_time)
        time_mn = round((duration - current_time)/60)
        if item.type == "episode":
            details = "Watching " + str(item.grandparentTitle)
            state = str(item.seasonEpisode).upper() + " : " + item.title
        if item.type == "movie":
            details = "Watching a movie"
            state = item.title
        is_idling = 0
    os.system("cls")
    print("\t--------- RPC update ---------")
    print("details = " + details)
    if is_idling == 0:
        print("state = " + state)
        print("end = " + str(time_mn) + "mn (timestamp = " + str(stop_time) + ")")
        RPC.update(state=state,
                details=details,
                large_image=image,
                large_text=large_text,
                end=stop_time)
    else:
        RPC.update(details=details,
                large_image=image,
                large_text=large_text,
                start=base_timer)
while True:
    update()
    time.sleep(refresh)
