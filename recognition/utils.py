import cv2
import numpy as np


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def draw_bounding_boxes(image, v_boxes, v_labels, v_scores):

    for i in range(len(v_boxes)):
        box = v_boxes[i]
        y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
        width, height = x2 - x1, y2 - y1
        label = "%s (%.3f)" % (v_labels[i], v_scores[i])
        region = np.array([[x1 - 3,        y1],
                           [x1-3,        y1 - height-26],
                           [x1+width+13, y1-height-26],
                           [x1+width+13, y1]], dtype='int32')
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 5)
        cv2.fillPoly(image,[region], (255, 0, 0))
        cv2.putText(image,
                    label,
                    (x1+13, y1-13),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1e-3 * image.shape[0],
                    (0,0,0),
                    2)
    return image
