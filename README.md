# Commander Keen in the Mystery of Isis IIa

<img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/level1-demo.gif" height=400> |

Source code (& associated files) dump of Commander Keen: The Mystery Of Isis IIa. This is the most recent incarnation of this fan game, which was released in 2012. It is built entirely in Python/PyGame. This repo mainly serves as a historical archive, and won't be actively maintained.

## Engine feature list

This is a full featured side-scroller written in PyGame, and has a number of interesting features:

* classic 2D sidescroller with angled (45 and 60 degree) ground
* all classic mechanics (jump, pogo, ledge grabbing, look up/down) + some new ones (swimming)
* HUD
* multiple weapons and collectable items
* locked door & key system
* editable levels (via Tiled map editor)
* parallaxing background
* 2x background & 2x foreground tile layers
* particle system
* animated tiles
* translucent background & foreground tiles
* weather effects (night, clouds, rain, snow)

## Dependencies

### Python 3

In `/src-python3` there is a modified version of the original source code, which appears to run using:

* `python==3.7.4`
* `pygame==2.0.3`

With a few changes:

* resources read directly from `/data` directory (no encrypted zip file)
* custom fonts are not enabled (couldn't load TTF files properly)
* custom maps won't work (couldn't port UI code)
* debug keys enabled by default:
  * `s` - show statistics (use `c` to cycle colour)
  * `h` - display solid/hidden areas
  * `j` - jump cheat
  * `k` - get all keys
  * `l` - more lives
  * `i` - get all weapons (1-6 are the main weapons, then 7-8 are the secret weapons)

### Python 2 (original)

The original dependency list (to run the game from source via `/src`) is not known, but this is a guide:

* `python==2.6.5`
* `pygame==1.9.1`
* `czipfile`
* `py2exe` (for producing a .EXE file)


## Repo structure

* `/v1.1a` - the latest compiled executable (for Windows) of the game. Note the `data/keendata.is2` file is an encrypted `.zip` file. You can extract files from here using the password `314ThEmYsTeRyOfIsIsIiAsCbCtIg314` and therefore "mod" the game (change graphics, edit the levels, etc) by putting them back into the zip archive with the same password.
* `/design` - some early design docs (story) and sketches. There is a whole host more original files to be found, but mostly these are already organised and included in the various game assets.
* `/resources` - most of the game assets (graphics, sounds, fonts) from `keendata.is2`, but extracted and unencrypted.
* `/screenshots` - a screenshot of every level.
* `/src` - the actual original Python source code. If you were to attempt to get this running, you should copy these files `/v1.1a` since that contains the appropriate structure to read the datafiles.
* `/src-python3` - modified code to run on recent Python (3+) and Pygame (2+) verrsions. To get this running, copy the `/v1.1a/data` folder across and unzip the `keendaata.is2` using above instructions so all the files are in `/data`. Then `python isis.py`

## Screenshots

<img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/design/level1.png" height=400>

| <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl1.png" width=320px height=200px> | <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl2.png" width=320px height=200px> | <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl3.png" width=320px height=200px> |
| --- | --- | --- |
| <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl4.png" width=320px height=200px> | <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl5.png" width=320px height=200px> | <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl6.png" width=320px height=200px> |
| <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl7.png" width=320px height=200px> | <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl8.png" width=320px height=200px> | <img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/screenshots/lvl9.png" width=320px height=200px> |

<img src="https://github.com/isonian314/commander-keen-isis-iia-1.1/blob/main/resources/maps/level9-dungeon-full.png">

All level maps can be found in the [resources/maps](https://github.com/isonian314/commander-keen-isis-iia-1.1/tree/main/resources/maps) directory.
## Links and further reading/watching

* [KeenWiki entry](https://keenwiki.shikadi.net/wiki/The_Mystery_of_Isis_II)
* YouTube:
  * [Early demos](https://www.youtube.com/channel/UCnbeUDjpoOFq9Fq7n0xFSwA)
  * [Soundtrack](https://www.youtube.com/playlist?list=PLYUlMHifBHYh4BUC22Qqgi501DxtAiZms)
  * [Full playthroughs](https://www.youtube.com/watch?v=LZZb_Oy38jw&list=PLwraIWFfRcQ9mtlsCNaEohsRIDCNkUxnl)
 
## Credits

Various people have worked on this project over time, who are mostly well documented in various places (web, wiki, pckf, and in-game).
