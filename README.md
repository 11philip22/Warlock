![alt text](https://i.imgur.com/pqer0qT.png)

At the moment Warlock a ncat multiplexer using tmux.

TODO:
- [ ] get rid of the time.sleep
- [x] get rid of empty tmux tab created by 
`os.system("tmux -S {0}/tmux new -s netcat -d".format(locatie))`

- [ ] check if there is a tmux session running named netcat 
instead of checking if the tmux socket exists 
`if not os.path.exists("{0}/tmux".format(locatie)):`
- [ ] close threads propper
- [ ] delete unused sockets
- [ ] better arguments 
- [ ] close tmux propper
