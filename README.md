# BDPlayLister

BDPlayLister is a helper script for Kodi that enables automatic selection of the used
Blu-ray playlist when playing back Blu-rays in directories.

It works by presenting itself as and external player that actually calls Kodi
back through JSON RPC and instructs it to play back the correct playlist.

## Usage
The script has currently two checks for which playlist to use.
* Place .srt subtitle file next to a playlist file in YOUR_MOVIE/BDMV/PLAYLIST
   * For example when you want to play 00800.mpls playlist, place SRT-subtitle in YOUR_MOVIE/BDMV/PLAYLIST/00800.eng.srt
      * .eng language specification is optional.
* Place playlist.txt file in the Blu-ray BDMV root (same directory as index.bdmv file)
   * Write playlist number inside the playlist.txt file. For example "00800" without the quotes.

## Requirements
* Python 2.7+
* python-xbmc library https://github.com/jcsaaddupuy/python-xbmc

## Configuration
* Kodi needs to have the JSON RPC interface enabled. Set System - Services - Web server - "Allow remote control via HTTP" as enabled.
   * Script uses port 8080
   * Authentication is not supported at this time.
* Copy bdplaylister.bat and bdplaylister.py to a directory
* Modify or replace your existing Kodi userdata/playercorefactory.xml with the provided one.
   * Necessary portions are the <players> section and the <filename> rule for ".*index.bdmv"
   * Change the players - players - "filename" path to point to your bdplaylister.bat
* Modify bdplaylister.bat so that the path to bdplaylister.py is correct.

## Troubleshooting
* Kodi can crash if the stopping of initial playback and starting the playlist playback are timed incorrectly.
   * bdplaylister.py has 0,1 second timeouts (time.sleep) before it calls back to Kodi to stop and start playback again.
   * Increase these timeouts if Kodi freezes when starting Blu-ray playback.
   * If you disable the console hiding from Kodi config and the .bat for debugging, you need to increase the timeouts to few seconds.

## Why external player hack and not a Kodi add-on?
Kodi add-on system doesn't allow us to react before it either opens the prompt for user to select a playlist, or continues by using the longest playlist in the Blu-ray.

Add-ons only receive events when the playback has already started, so add-on would need to stop the current playback and then continue playback of the selected playlist.

This playback stopping and restarting can be problematic especially if Kodi is also set to change the display refresh rate on playback. Stopping the playback while the player might still be initializing can cause Kodi to crash.
Especially the DSPlayer branch with madVR renderer doesn't like untimely interruptions to playback initialization.

Our external player does not care if the playback stops abruptly, since it doesn't really play anything which allows us to quickly instruct Kodi to play the specific playlist instead of the whole Blu-ray.
This also results in much less UI flickering compared to add-on method.