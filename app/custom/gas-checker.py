import cv2
import numpy as np
import json

img = cv2.imread("../img/kitchen-cam-night-IR-markers.jpeg")
markers = json.loads(open("../img/markers.json", "r").read())
cv2.namedWindow("cam_screenshot", cv2.WINDOW_KEEPRATIO)

show_marker = False

while True:  # Runs forever until we break with Esc key on keyboard
    # Shows the image window
    for marker in markers:
        pos_x, pos_y, radius = (int(marker["position"]["x"]), int(marker["position"]["y"]), int(marker["radius"]))
        marker_region_pos = ((pos_x - radius, pos_y - radius), (pos_x + radius, pos_y + radius))
        img_copy = img.copy()
        marker_region = img_copy[marker_region_pos[0][1]:marker_region_pos[1][1], marker_region_pos[0][0]:marker_region_pos[1][0]]
        marker_region_gray = cv2.cvtColor(marker_region, cv2.COLOR_RGB2GRAY)
        # marker_region_gray = cv2.adaptiveThreshold(marker_region_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        #                                            cv2.THRESH_BINARY, 3,
        #                                            30)  # Play around with these last 2 numbers
        # ret, thresh = cv2.threshold(marker_region_gray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(marker_region_gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # Draw External Contours

        # Set up empty array
        external_contours = np.zeros(marker_region_gray.shape)

        # For every entry in contours
        for i in range(len(contours)):

            # last column in the array is -1 if an external contour (no contours inside of it)
            if hierarchy[0][i][3] != -1:
                # We can now draw the external contours from the list of contours
                cv2.drawContours(external_contours, contours, i, 255, -1)
        # Convert Gray Scale Image to Float Values
        # gray = np.float32(marker_region_gray)
        # #
        # # # Corner Harris Detection
        # dst = cv2.cornerHarris(src=gray, blockSize=2, ksize=3, k=0.05)
        # # #
        # # # # result is dilated for marking the corners, not important to actual corner detection
        # # # # this is just so we can plot out the points on the image shown
        # dst = cv2.dilate(dst, None)
        # # #
        # # # # Threshold for an optimal value, it may vary depending on the image.
        # marker_region[dst > 0.01 * dst.max()] = [255, 0, 0]


        if show_marker:
            cv2.circle(img, (pos_x, pos_y), radius, (0, 200, 111), 2)
    cv2.imshow('cam_screenshot_original', marker_region_gray)
    cv2.imshow('cam_screenshot', external_contours)
    # EXPLANATION FOR THIS LINE OF CODE:
    # https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1/39201163
    if cv2.waitKey(20) & 0xFF == 27:
        break

# closing all open windows
cv2.destroyAllWindows()
