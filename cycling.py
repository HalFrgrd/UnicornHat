import time

#The following was needed from trouble importing unicornhat.py
import ws2812, atexit

def clean_shutdown():
  '''
  Registered at exit to ensure ws2812 cleans up after itself
  and all pixels are turned off.
  '''
  off()
  ws2812.terminate(0)

_rotation = 0

atexit.register(clean_shutdown)

ws2812.init(64)

map = [
  [7 ,6 ,5 ,4 ,3 ,2 ,1 ,0 ],
  [8 ,9 ,10,11,12,13,14,15],
  [23,22,21,20,19,18,17,16],
  [24,25,26,27,28,29,30,31],
  [39,38,37,36,35,34,33,32],
  [40,41,42,43,44,45,46,47],
  [55,54,53,52,51,50,49,48],
  [56,57,58,59,60,61,62,63]
]

def clear():
  '''
  Clear the buffer
  '''
  for x in range(64):
    ws2812.setPixelColor(x,0,0,0)

def off():
  '''
  Clear the buffer and immediately update UnicornHat to
  turn off all pixels.
  '''
  clear()
  show()
 
def get_index_from_xy(x, y):
  '''
  Convert an x, y value to an index on the display
  '''
  if x > 7 or x < 0:
    raise ValueError('X position must be between 0 and 7')
    return
  if y > 7 or y < 0:
    raise ValueError('Y position must be between 0 and 7')
    return

  y = 7-y

  if _rotation == 90:
    x,y = y,7-x
  if _rotation == 180:
    x,y = 7-x,7-y
  if _rotation == 270:
    x,y = 7-y,x

  return map[x][y]

def set_pixel(x, y, r, g, b):
  '''
  Set a single pixel to RGB colour
  '''
  index = get_index_from_xy(x, y)
  if index != None:
    ws2812.setPixelColor(index, r, g, b)

def show():
  '''
  Update UnicornHat with the contents
  of the display buffer
  '''
  ws2812.show()


# Creating the first 8 columns of the virtual screen (only the arrow)
# Pivot on the first element of the elements to get screen.
orange, black = [235, 200, 29],[0, 0, 0]
virtualscreen = [[black, black, black, black, black, black, black, black], [black, black, black, orange, orange, black, black, black], [black, black, orange, orange, orange, orange, black, black], [black, orange, orange, orange, orange, orange, orange, black], [orange, orange, orange, orange, orange, orange, orange, orange], [orange, orange, orange, black, black, orange, orange, orange], [orange, orange, black, black, black, black, orange, orange], [orange, black, black, black, black, black, black, orange]]

#The following was made redundant because of modifications to the next part of the script.
## Setting pixels using the virtual screen.
## for x in range(8):
##	for y in range(8):
##		set_pixel(x,y,virtualscreen[x][y][0],virtualscreen[x][y][1],virtualscreen[x][y][2])
## 		show()

for a in range(100): #the range/8 for the number of loops (range: how many times it will shift one pixel to the left)
	
	#Displaying the visible part of the screen.
	for x in range(0,8):
		for y in range(0,8):
			r,g,b = virtualscreen[x][y]
			set_pixel(x,y,r,g,b)
		show()
	time.sleep(0.05)

	# adding the first column to the back of the virtual screen
	# and removing the first column. pop removes and returns the element at index.
	virtualscreen.append(virtualscreen.pop(0))