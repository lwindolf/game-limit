# game-limit
Auto-kill script to enforce application usage time

Usage
-----

First install the script. For example

    cp game-limit.py /usr/local/bin
    chmod a+x /usr/local/bin/game-limit.py

And hook it into a user account, e.g. in ~/.xinitrc

    nohup /usr/local/bin/game-limit.py

Upon next login the script should work.
