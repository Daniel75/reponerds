Longe Ripper is an easy to use tool for ripping DVD and BluRay with one
click within Kodi. Lounge Ripper is a program addon and require some additional
tools.

Pre-Requisites:

By default, Longe Ripper utilizes MakeMKV <http://www.makemkv.com/> and
HandBrake <https://handbrake.fr/> to do the actual ripping and encoding of DVDs
and BluRays, so these must be installed prior to it working.

MakeMKV:

MakeMKV is the software responsible for ripping and decrypting the video.
It is proprietary software, and costs $50 for a license, but is free to
use while it is in beta. During the beta, you can get the current license from
<http://www.makemkv.com/forum2/viewtopic.php?f=5&t=1053> which needs to be
updated every 60 days. You can also show your support and purchase a full
license (which will not change through versions or updates) for the software
on their website <http://makemkv.com/buy/>.

Installation - Ubuntu:

sudo add-apt-repository ppa:heyarje/makemkv-beta
sudo apt-get update
sudo apt-get install makemkv-bin makemkv-oss

or load a shellscript from <https://github.com/b-jesch/buildMakeMKV> that do the
installation, automatic update and key management for you.

Installation - Windows/Mac:

http://www.makemkv.com/download/

Open the MakeMKV GUI and enter the key from the above-mentioned forum post, or
your purchased license.

HandBrake:

HandBrake transcodes the files output by MakeMKV and compresses them to their
final format. HandBrake is free and open-source software.

Installation - Ubuntu (Do not use the version in the Ubuntu repos):

sudo add-apt-repository ppa:stebbins/handbrake-releases
sudo apt-get update
sudo apt-get install handbrake-cli

Installation - Windows/Mac:

https://handbrake.fr/downloads2.php

After installation of makemkv and handbrake you are now able to use the addon.
Enter the correct system settings and create at least one profile. Be aware that
the content of the temp folder will be deleted after successfully operations
so don't use your movie folder or other important folders as temp! The content
within will be deleted!

For a list of additional parameters take a look at <https://trac.handbrake.fr/wiki/CLIGuide>