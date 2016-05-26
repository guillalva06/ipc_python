import numpy as np
import cv2


def find_marker(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	c = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		return cv2.minAreaRect(c)
	return c


def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

def estimate_distance(camera):
	image = cv2.imread('images/distance/calibration.jpg')
	marker = find_marker(image)
	focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
	cont = 0
	list_distances = list()
	while cont < 10:
		(grabbed, frame) = camera.read()
		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		cont = cont + 1
		if not grabbed:
			break
		marker = find_marker(frame)
		if marker is not None:
			list_distances.append(distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0]))
	list_distances.sort()
	return list_distances[4]
	# cleanup the camera and close any open windows

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the known distance from the camera to the object, which
# in this case is 30 cm
KNOWN_DISTANCE = 30.0

# initialize the known object width, which in this case, the tennis
# ball is 6 cm
KNOWN_WIDTH = 6.0

