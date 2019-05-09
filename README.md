At the moment Warlock a ncat multiplexer using tmux.

TODO:
- [] close tmux properly
- [] get rid of the time.sleep
- [] get rid of empty tmux tab created by 
```
subprocess.Popen(["tmux -S {0}/tmux new -s netcat -d".format(locatie)], shell=True)
```
