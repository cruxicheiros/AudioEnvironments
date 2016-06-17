import os
import sys
from random import randint
from openal.audio import SoundSink, SoundSource, SoundListener
from openal.loaders import load_wav_file
import getch

def load_sound(fname):
	dirname = os.path.dirname(__file__)
	fname = os.path.join(dirname, fname)
	data = load_wav_file(fname)
	return data
	
def place_sound(pos, wav, loop_bool):
	source = SoundSource(position = pos)
	source.queue(wav)
	source.looping = loop_bool
	return source
	
def move_source_random(source, x_lower, x_higher, y_lower, y_higher, z_lower, z_higher):
	source.position = [randint(x_lower, x_higher), randint(y_lower, y_higher), randint(z_lower, z_higher)]
	return source.position
	
def orient_listener(currently_facing, delta):
	directions = [(0, 0, 1, 0, 1, 0), 
	(1, 0, 1, 0, 1, 0), 
	(1, 0, 0, 0, 1, 0), 
	(1, 0, -1, 0, 1, 0), 
	(0, 0, -1, 0, 1, 0), 
	(-1, 0, -1, 0, 1, 0), 
	(-1, 0, 0, 0, 1, 0), 
	(-1, 0, 1, 0, 1, 0)]
	
	for i in directions:
		if i == currently_facing:
			i_index = directions.index(i)
			
			if delta:
				if i_index == len(directions) - 1:
					return directions[0]
				else:
					return directions[i_index + 1]
			else:
				if i == 0:
					return directions[len(directions) - 1]
				else:
					return directions[i_index - 1]
				
	
def mainloop():
	listener = SoundListener()
	listener.orientation = (0, 0, -1, 0, 1, 0)
	
	sink = SoundSink()
	sink.activate()
	
	rain = place_sound([0, -7, -1], load_sound("rfrog.wav"), True)
	sink.play(rain)
	
	birds = place_sound([5, 5, 5], load_sound("chirps1.wav"), True)
	sink.play(birds)
	
	creek = place_sound([-7, -7, 7], load_sound("creek.wav"), True)
	sink.play(creek)
	
	while 1 == 1:
		birds.position = move_source_random(birds, -8, 8, 0, 7, -10, 10)
		char = ord(getch.getch())
		
		if char == 97:
			listener.orientation = orient_listener(listener.orientation, False)

		if char == 100:
			listener.orientation = orient_listener(listener.orientation, True)
			
		if char == 112:
			break
		
		sink.update()

	
if __name__ == "__main__":
    sys.exit(mainloop())