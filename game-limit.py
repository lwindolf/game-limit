#!/usr/bin/env python

import os, re
import gtk, gobject, pynotify

class CounterApp:
    def __init__(self):
	self.game_running = 0
	self.counter = 60*25

	if not pynotify.init('Basics'):
		sys.stderr.write('Error: Unable to load pynotify\n')
		sys.exit(1)

        gobject.timeout_add(15000, self.process_check_cb)

    def process_check_cb(self):
	blacklist = [
		"/usr/games/sol"
	]

	# Identify game processes from blacklist
	result=0
	pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

	for pid in pids:
	    try:
		name = os.readlink(os.path.join('/proc', pid, 'exe'))
		if name in blacklist:
			result = 1
			# Kill process if timer was run down already
			if self.counter == 0:
			    # FIXME: Do kill info via libnotify
				print "Killing PID %s..." % pid
				pynotify.Notification('Spiel abgebrochen (Spielzeit ueberschritten)!').show()
				os.kill(int(pid), 9)
	    except IOError: # proc has already terminated
		continue
	    except OSError: # Permission denied
	    	continue

	# Do timer management
	if self.counter > 0:
		if result == 0 and self.game_running == 1:
			print "No more game running. Stopping timer..."
			self.game_running = 0
			gobject.source.remove(self.timer)

		if result == 1 and self.game_running == 0:
			print "New game found running. Starting timer..."
			self.game_running = 1
			self.start_timer()

	return True

    def start_timer(self):
        self.timer = gobject.timeout_add(1000, self.countdown_method)
        self.countdown_method()

    def countdown_method(self):
	# FIXME: Do warning via libnotify
	# Do counting
        if self.counter > 0:
	    if self.game_running == 1:
	    	self.counter -= 1

	    if self.counter <= 60:
		modulo = 15
		message = "%ds" % self.counter
	    elif self.counter <= 60*10:
		modulo = 60*2
		message = "%dmin" % (self.counter / 60)
	    else:
		modulo = 60*5
		message = "%dmin" % (self.counter / 60)


	    if self.counter % modulo == 0:
		    pynotify.Notification('Spielzeit: noch ' + message).show()

            return True
        else:
            print "Killing from now on!"
            return False

if __name__ == "__main__":
    app = CounterApp()
    gtk.main()




