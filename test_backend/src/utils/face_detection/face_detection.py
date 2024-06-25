import cv2 


def face_detction(img_path):
    ret,_img = cv2.imread(img_path)
    print("_img:",_img)
    print("ret:",ret)
    
if __name__ == "__main__":
    print(face_detction(img_path="static/images/1_Spark_streaming_presentation.jpg"))