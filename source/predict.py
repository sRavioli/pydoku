thresh = 128  # define a threshold, 128 is the middle of black and white in grey scale
# threshold the image
gray = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]

# Find contours
cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    x, y, w, h = cv2.boundingRect(c)

    if x < 3 or y < 3 or h < 3 or w < 3:
        # Note the number is always placed in the center
        # Since image is 28x28
        # the number will be in the center thus x >3 and y>3
        # Additionally any of the external lines of the sudoku will not be thicker than 3
        continue
    ROI = gray[y : y + h, x : x + w]
    # increasing the size of the number allws for better interpreation,
    # try adjusting the number and you will see the differnce
    ROI = scale_and_centre(ROI, 120)

    tmp_sudoku[i][j] = predict(ROI)


def predict(img):
    image = img.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)[1]
    image = cv2.resize(image, (28, 28))
    # display_image(image)
    image = image.astype("float32")
    image = image.reshape(1, 28, 28, 1)
    image /= 255

    # plt.imshow(image.reshape(28, 28), cmap='Greys')
    # plt.show()
    model = load_model("cnn.hdf5")
    pred = model.predict(image.reshape(1, 28, 28, 1), batch_size=1)
    # return pred.argmax()
