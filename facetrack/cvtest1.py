import cv

cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture  = cv.CaptureFromCAM(camera_index)

def repeat():
	global capture
	global camera_index
	frame = cv.QueryFrame(capture)
	cv.ShowImage("w1", frame)
	c = cv.WaitKey(10)
	if(c=="n"):
		camera_index += 1
		capture = cv.CaptureFromCAM(camera_index)
		if not capture:
			camera_index = 0
			capture = cv.CaptureFromCAM(camera_index)
			
while True:
	repeat()
	
