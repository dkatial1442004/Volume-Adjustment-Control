import cv2
import time
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm


def calibrate(detector, cap, label):
    print(f"==> Hold {label} and press '{ 'm' if label=='a fist (min)' else 'x' }' to calibrate")
    vals = []
    while True:
        success, img = cap.read()
        if not success:
            continue
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, draw=False)
        if lmList:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            vals.append(math.hypot(x2 - x1, y2 - y1))
            if len(vals) > 30:
                vals.pop(0)
        cv2.putText(img, f"Hold {label}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Calibrating", img)
        key = cv2.waitKey(1) & 0xFF
        if (label == "a fist (min)" and key == ord('m')) or (label == "an open hand (max)" and key == ord('x')):
            break

    cv2.destroyWindow("Calibrating")
    avg = sum(vals) / len(vals) if vals else 0
    print(f">>> Calibrated {label} distance: {avg:.1f}")
    return avg


def main():
    wCam, hCam = 640, 480
    pTime = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    detector = htm.handDetector(detectionCon=0.7)

    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    minVol, maxVol = volume.GetVolumeRange()[:2]  # usually (-65.25, 0.0)

 
    minDist = calibrate(detector, cap, "a fist (min)")
    maxDist = calibrate(detector, cap, "an open hand (max)")
    print(f"Using distance range: [{minDist:.1f}, {maxDist:.1f}]")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, draw=False)

        if lmList:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            length = math.hypot(x2 - x1, y2 - y1)

            # volume percent
            rawVolPer = np.clip(np.interp(length, [minDist, maxDist], [0, 100]), 0, 100)

            # exponential mapping 
            adjustedVolPer = int((rawVolPer / 100) ** 1.8 * 100)

            # volume % to dB range
            vol = np.interp(adjustedVolPer, [0, 100], [minVol, maxVol])
            volBar = np.interp(adjustedVolPer, [0, 100], [400, 150])

            # Set system volume
            volume.SetMasterVolumeLevel(vol, None)

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{adjustedVolPer} %', (40, 450),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime else 0
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Volume Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
