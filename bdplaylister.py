import os
import sys
import time
from xbmcjson import XBMC, PLAYER_VIDEO

REQUEST_URL = "http://localhost:8080/jsonrpc"

# Return list of playlist numbers (in string) that have srt file next to them.
def find_srt(bd_path):
    srt_list = []
    if os.path.exists(bd_path) and os.path.isdir(bd_path):
        playlist_dir = os.path.join(bd_path, "PLAYLIST")
        files = os.listdir(playlist_dir)
        for file in files:
            if file.lower().endswith(".srt"):
                playlist = file.lower().split(".")[0]
                if len(playlist) == 5:
                    try:
                        int(playlist)
                        srt_list.append(playlist)
                    except ValueError:
                        print "SRT filename ", playlist, " did not contain a valid playlist number."
                else:
                    print "SRT filename ", playlist, " had invalid length."
    return srt_list

# Check playlist.txt file for preferred playlist.
def check_playlist_txt(bd_path):
    playlist = ""
    pl_path = bd_path + "playlist.txt"
    if os.path.exists(pl_path) and os.path.isfile(pl_path):
        content = ""
        with open(pl_path, "r") as fp:
            content = fp.read()
            content = content.strip()
        if len(content) == 5:
            try:
                int(content)
                playlist = content
            except ValueError:
                print "playlist.txt content '", content, "' was not a number"
        else:
          print "playlist.txt content '", content, "' has invalid length."
    return playlist

def stop_playback(xbmc, player_id):
    #time.sleep(3)
    time.sleep(0.1)
    stop_result = xbmc.Player.Stop({"playerid": player_id})
    #print ""Called stop playback with result:", stop_result
    time.sleep(0.1)
    #time.sleep(3)

def play_bd(bdmv_index_path):
    play_target = ""
    xbmc_play_path = ""
    player_id = None

    xbmc = XBMC(REQUEST_URL)
    result = xbmc.Player.GetActivePlayers().get("result")
    #print "Active Players: ", result
    if result and len(result) > 0:
        player_id = result[0].get("playerid")
        if player_id != None:
            result = xbmc.Player.GetItem({"properties": ["file"], "playerid": player_id}).get("result")
            #print "Got item result: ", result
            if result and len(result) > 0:
                item = result.get("item")
                if item:
                    file = item.get("file")
                    if file:
                        #print "Found file: ", file
                        xbmc_play_path = file
    if not xbmc_play_path:
        print "Did not get currently playing file path from JSON-RPC."

    if bdmv_index_path.endswith("index.bdmv") and xbmc_play_path.endswith("index.bdmv"):
        bdmv_root_path = bdmv_index_path[:-10]
        xbmc_play_root_path = xbmc_play_path[:-10]
        #print "Found Blu-ray in path", bdmv_root_path

        srt_list = find_srt(bdmv_root_path)
        playlist_txt = check_playlist_txt(bdmv_root_path)

        # Playlist path change assumes that the internal path from Kodi uses / as directory separator. Works at least for smb:// sources.
        if playlist_txt:
            #print "Found playlist", playlist_txt, "from playlist.txt"
            play_target = xbmc_play_root_path + "PLAYLIST/" + playlist_txt + ".mpls"
        elif len(srt_list) > 0:
            #print "Found SRTs", srt_list
            play_target = xbmc_play_root_path + "PLAYLIST/" + srt_list[0] + ".mpls"
        else:
            print "Did not find overrides, proceeding with index.bdmv"
            play_target = ""

    pid = player_id if player_id != None else PLAYER_VIDEO
    
    if play_target:
        print "Found play target: ", play_target
        stop_playback(xbmc, pid)
        result = xbmc.Player.Open({"item": {"file": play_target}})
        #print "Commanded playback with result: ", result
    elif xbmc_play_path:
        print "Using bdmv ", xbmc_play_path
        stop_playback(xbmc, pid)
        result = xbmc.Player.GetPlayers({"media": "video"}).get("result")
        #print "Found players: ", result
        if result and len(result) > 0:
            dsplayer_id = dvdplayer_id = None
            for player in result:
                #print "Player: ", player
                if player.get("name") == "DSPlayer":
                    dsplayer_id = player.get("playercoreid")
                elif player.get("name") == "DVDPlayer":
                    dvdplayer_id = player.get("playercoreid")
            if dsplayer_id is not None or dvdplayer_id is not None:
                #print "Got internal player id, continuing"
                pid = dsplayer_id if dsplayer_id is not None else dvdplayer_id
                result = xbmc.Player.Open({"item": {"file": xbmc_play_path}, "options": {"playercoreid": pid}})
                #print "Open returned result", result
            else:
                print "Didn't find an internal player from Kodi JSON-RPC."
    else:
        print "Failed to find Kodi internal Blu-ray path for playback."

if __name__ == "__main__":
    print "BDPlaylister called with args: ", sys.argv
    play_bd(sys.argv[1])
