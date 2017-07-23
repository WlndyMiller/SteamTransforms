# SteamTransforms
A set of local transforms for Maltego to graph Steam user profiles.

## Usage
### Entities
#### Steam Account
##### Properties
+ `URL` Steam profile URL
+ `Short title` Current Alias
+ `Title` Unique identifier of user from URL
+ `Image` Current profile picture
### Transforms
#### To Steam Account
Runs on: `maltego.Alias`, `maltego.Person`

Searchs the Steam Community for profiles with the input entity name. Adds `WindyMiller.SteamAccount` entities for each found.

![](http://i.imgur.com/Q2c7uVy.png)

#### To Person
Runs on: `WindyMiller.SteamAccount`

Gets the users 'real' name if profile is public.
![](http://i.imgur.com/YkwBq8R.png)
#### To Location
Runs on: `WindyMiller.SteamAccount`

Gets the users location if profile is public.
![](http://i.imgur.com/N2nshkF.png)
#### To Friends List
Runs on: `WindyMiller.SteamAccount`

Gets the users friends list if profile is public. Shuffles the list before returning to Maltego so running multiple times against the same entity can get additional results in Maltego CE.

![](http://i.imgur.com/PMtf5YI.png)

#### To Alias
Runs on: `WindyMiller.SteamAccount`

Steam keeps a record of the past 10 aliases used. This will get that list and is avaiable with any profile (public or private)

![](http://i.imgur.com/ZJpX28N.png)

#### 
## Installation

Create the directory `/opt/maltego` if it does not already exist.
```bash
mkdir /opt/maltego
cd /opt/maltego`
```

Either (A) clone the repository and download Steam.mtz or (B) download the release tar.gz.

### (A) Clone
```bash
git clone https://github.com/WlndyMiller/SteamTransforms
wget https://github.com/WlndyMiller/SteamTransforms/releases/download/v0.1/Steam.mtz
```

### (B) Release
```
wget https://github.com/WlndyMiller/SteamTransforms/releases/download/v0.1/SteamTransforms0.1.tar.gz
tar -xvzf SteamTransforms.tar.gz
```

### Configure Maltego
In Maltego navigate to `Import | Export` on the ribbon
Select `Import Config` and select `Steam.mtz`

Select to import all Entities and Local Transforms and click Finish.
