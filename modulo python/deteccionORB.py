import cv2
import math

def deteccion(fot, obj):
    
    grises = cv2.cvtColor(fot,cv2.COLOR_BGR2GRAY)
    grises2 = cv2.cvtColor(obj,cv2.COLOR_BGR2GRAY)
    hist2 = cv2.calcHist([grises2],[0],None,[256],[0,256])
    encontrado = False	
    a=0
    for ss in hist2:
        a=a+1 
	if max(hist2)==ss:
	   break	
    _,thresh = cv2.threshold(grises,a-10,a+40,cv2.THRESH_BINARY)
    thresh = cv2.erode (thresh,cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)),iterations = 4)
    thresh = cv2.dilate (thresh,cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)),iterations = 2)
    thresh = cv2.GaussianBlur(thresh, (5,5), 0)
    contours,hierarchy = cv2.findContours(thresh, 1, 2)[-2:]
    punto=(-1,-1,-1)
    puntoseval=[]
    area=0
    if len(contours)<500 and len(contours)>0:		
	for ocu in contours:
            ocurrencias = cv2.moments(ocu)
            if ocurrencias['m00']>20000 and ocurrencias['m00']<100000:
                posx = int(ocurrencias['m10']/ocurrencias['m00'])
                posy = int(ocurrencias['m01']/ocurrencias['m00'])
		area=int(math.sqrt(ocurrencias['m00']))
		if(area<fot.shape[0] and area<fot.shape[1]):
		     puntoseval.append((int(posx),int(posy), area))
                cv2.circle (fot,(posx,posy),int(math.sqrt(ocurrencias['m00'])),(255,20,147), 2)
	for pun in puntoseval:
            grises = cv2.GaussianBlur(grises, (5,5), 0)
            grises2 = cv2.GaussianBlur(grises2, (5,5), 0)
	    orb = cv2.ORB_create()
	    #orb = cv2.ORB()
	    xx1=pun[0]-pun[2]*3/4
            yy1=pun[1]-pun[2]*3/4
            xx2=pun[0]+pun[2]*3/4
            yy2=pun[1]+pun[2]*3/4
	    lims=grises.shape
	    
	    if(xx1>0 and yy1>0 and xx2>0 and yy2>0 and xx2>(xx1+10) and yy2>(yy1+10) and xx2<lims[1], yy2<lims[0]):	
		grisesseg=grises[yy1:yy2,xx1:xx2]
		cv2.rectangle(fot,(xx1,yy1),(xx2,yy2),(0,255,100),2)
		puntosORB = orb.detect(grisesseg,None)
		puntosORB,descriptoresORB = orb.compute(grisesseg,puntosORB)
		puntosORB2 = orb.detect(grises2,None)
		puntosORB2,descriptoresORB2 = orb.compute(grises2,puntosORB2)
		seleccionador=cv2.BFMatcher()
		ocurrencias = seleccionador.knnMatch(descriptoresORB,descriptoresORB2, k=2)
		for sel1, sel2 in ocurrencias:
		    if sel1.distance < sel2.distance*0.75:
	 		img1_idx = sel1.queryIdx
			punto=(pun[0], pun[1],pun[2])
			encontrado=True

	    if(encontrado):
		break
    return punto
