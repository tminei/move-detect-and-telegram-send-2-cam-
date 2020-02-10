import cv2
import time
import os
import requests


def sendImage(filename):
    url = "https://api.telegram.org/bot896768722:AAHIFDNb5LvcvEVw_5R4JDCI5DovtpeGWZ4/sendPhoto"
    os.chdir(dir + "/backup")
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id': "-1001249105006"}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)


if __name__ == '__main__':

    cam1state = 1
    cam2state = 0

    dir = os.getcwd()

    if cam1state + cam2state > 0:
        showwindows = 0

        if cam1state:
            cam1 = cv2.VideoCapture("rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=1?.sdp")
            sensindex1 = 0.005
            fgbg1 = cv2.createBackgroundSubtractorMOG2()
            height1 = cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width1 = cam1.get(cv2.CAP_PROP_FRAME_WIDTH)
            smallheigth1 = (int(height1 / 3))
            smallwidth1 = (int(width1 / 3))
            fullsum1 = smallheigth1 * smallwidth1 * 255
            sens1 = int(fullsum1 * sensindex1)
            # print(fullsum1, sens1)
            detect1 = 0

        if cam2state:
            cam2 = cv2.VideoCapture(0)
            sensindex2 = 0.005
            fgbg2 = cv2.createBackgroundSubtractorMOG2()
            height2 = cam2.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width2 = cam2.get(cv2.CAP_PROP_FRAME_WIDTH)
            smallheigth2 = (int(height2 / 3))
            smallwidth2 = (int(width2 / 3))
            fullsum2 = smallheigth2 * smallwidth2 * 255
            sens2 = int(fullsum2 * sensindex2)
            # print(fullsum2, sens2)
            detect2 = 0

        while True:
            if cam1state:
                ret1, frame1fullsize = cam1.read()
                frame1 = cv2.resize(frame1fullsize, (smallwidth1, smallheigth1))
                grayFull1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                grayFull1 = cv2.GaussianBlur(grayFull1, (21, 21), 0)
                fgmask1 = fgbg1.apply(grayFull1)
                thresh1 = cv2.threshold(fgmask1, 200, 255, cv2.THRESH_BINARY)[1]
                thresh1 = cv2.dilate(thresh1, None, iterations=0)
                sum1 = cv2.sumElems(thresh1)
                sumElement1 = round(sum1[0])
                # if sumElement1 > sens1 and showwindows == 2:
                #     cv2.imshow('CAM1full', frame1fullsize)

            if cam2state:
                ret2, frame2fullsize = cam2.read()
                frame2 = cv2.resize(frame2fullsize, (smallwidth2, smallheigth2))
                grayFull2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                grayFull2 = cv2.GaussianBlur(grayFull2, (21, 21), 0)
                fgmask2 = fgbg2.apply(grayFull2)
                thresh2 = cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)[1]
                thresh2 = cv2.dilate(thresh2, None, iterations=0)
                sum2 = cv2.sumElems(thresh2)
                sumElement2 = round(sum2[0])
                # if sumElement2 > sens2 showwindows == 2:
                #     cv2.imshow('CAM2full', frame2fullsize)

            if cam1state:
                if sumElement1 > sens1 and detect1 == 0:
                    detect1 = 1
                    print("CAM1 move detect!")
                    if showwindows == 2:
                        cv2.imshow('CAM1full', frame1fullsize)
                    os.chdir(dir + "/backup")
                    time1str = time.strftime("%Y%m%d-%H%M%S")
                    filename1 = str("d1_c1_" + time1str + ".jpg")
                    cv2.imwrite(filename1, frame1fullsize)
                    sendImage(filename1)

                    if cam2state:
                        time2str = time.strftime("%Y%m%d-%H%M%S")
                        filename2 = str("d1_c2_" + time2str + ".jpg")
                        cv2.imwrite(filename2, frame2fullsize)
                        sendImage(filename2)
                if sumElement1 < sens1 and detect1 == 1:
                    detect1 = 0

            if cam2state:
                if sumElement2 > sens2 and detect2 == 0:
                    detect2 = 1
                    print("CAM2 move detect!")
                    if showwindows == 2:
                        cv2.imshow('CAM2full', frame1fullsize)
                    os.chdir(dir + "/backup")
                    time2str = time.strftime("%Y%m%d-%H%M%S")
                    filename2 = str("d2_c2_" + time2str + ".jpg")
                    cv2.imwrite(filename2, frame2fullsize)
                    sendImage(filename2)

                    if cam1state:
                        time1str = time.strftime("%Y%m%d-%H%M%S")
                        filename1 = str("d2_c1_" + time1str + ".jpg")
                        cv2.imwrite(filename1, frame1fullsize)
                        sendImage(filename1)
                if sumElement2 < sens2 and detect2 == 1:
                    detect2 = 0

            if showwindows == 1:
                if cam2state:
                    cv2.imshow('CAM2', frame2)
                    cv2.imshow('CAM2T', thresh2)

                if cam1state:
                    cv2.imshow('CAM1', frame1)
                    cv2.imshow('CAM1T', thresh1)
    else:
        print("No camera selected")
        exit(0)
