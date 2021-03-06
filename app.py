from cProfile import label
import tkinter as tk
from tkinter import W, filedialog, Text
import os
import cv2
from sklearn import utils
from Image_Similarity import CompareHistogram as ch
from Image_Similarity import CompareFeatures as cf
from Image_Similarity import Image_Diff as id
import numpy as np
from PIL import ImageTk, Image
import time
from sklearn import metrics

(
#root = tk.Tk()
#apps = []
#canvas = tk.Canvas(root, height=500, width=500, bg="#263D42")
#canvas.pack()  # attach canvas
#frame = tk.Frame(root, bg="white")
#frame.pack()
#frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
#
#
#def compareImages(frame=frame):
#    time_t = 0
#    test_input_path = []
#    for i in range(178):
#        frame_th = ''
#        frame_num = time_t + i
#        if frame_num < 10:
#            frame_th = '00' + str(frame_num)
#        elif frame_num < 100:
#            frame_th = '0' + str(frame_num)
#        else:
#            frame_th = str(frame_num)
#        test_input_path.append("./datasets/testing/frames/01/" + frame_th + ".jpg")
#
#    pred_input_path = []
#    for i in range(174):
#        frame_th = ''
#        frame_num = time_t + i
#        if frame_num < 10:
#            frame_th = '00' + str(frame_num)
#        elif frame_num < 100:
#            frame_th = '0' + str(frame_num)
#        else:
#            frame_th = str(frame_num)
#        pred_input_path.append("./datasets/predicted/pred/frames/0" + frame_th + ".jpg")
#
#    test_input_imgs = []
#    for i in range(178):
#        img = cv.imread(test_input_path[i])
#        test_input_imgs.append(img)
#
#   pred_input_imgs = []
#   for i in range(174):
#        img = cv.imread(pred_input_path[i])
#        pred_input_imgs.append(img)
#    #t_minus_one_frames = input_imgs[:4]
#    #tensor_imgs = torch.tensor(t_minus_one_frames)
#
#    # load frame score
#    frame_scores = np.load("./datasets/predicted/anomaly_score.npy")
#
#    test_img = test_input_imgs[1]
#    for i in range(174):
#        # load the two input images
#        imageA = test_input_imgs[i+4]  # test frame
#        imageB = pred_input_imgs[i]  # pred frame
#
#        #imageA = cv.imread(args["first"])  # test frame
#        #imageB = cv.imread(args["second"])  # pred frame
#
#        # load mode of program
#        mode = int(2)
#
#        # resize image
#        w1, h1, c1 = imageA.shape
#        w2, h2, c2 = imageB.shape
#
#        if w1 != 256:
#            imageA = cv.resize(imageA, (256, 256))
#        if w2 != 256:
#            imageB = cv.resize(imageB, (256, 256))
#
#        # Show images
#        #cv.imshow("Test frame", cv .resize(imageA, None, fx=1, fy=1))
#        #cv.imshow("Pred frame", cv.resize(imageB, None, fx=1, fy=1))
#
#        # Run compare modules
#        if mode == 0:
#            ch.compareHistogram(imageA, imageB)
#        elif mode == 1:
#            cf.compareSIFT(imageA, imageB)
#        elif mode == 2:
#            compared_img_A, compared_img_B = id.image_differences_return(imageA, imageB, frame_scores[i])
#        # Create an object of tkinter ImageTk
#        imgA = ImageTk.PhotoImage(Image.fromarray(compared_img_A))
#        imgB = ImageTk.PhotoImage(Image.fromarray(compared_img_B))
#        # Create a Label Widget to display the text or Image
#        label = tk.Label(frame, image=imgA)
#        label.pack()
##
##def addApp(): 
#    # delete attached apps before attach the new app
#    for widget in frame.winfo_children():
#        widget.destroy()  # destroy everthing
#        
#    filename = filedialog.askopenfilename(initialdir="/", title="Select File", 
#                                       filetypes=(("executables", "*.exe"), ("all files", "*.*")))
#    apps.append(filename)
#    print(filename)
#    for app in apps:
#        label = tk.Label(frame, text=app, bg="gray")
#        label.pack()
##
##def runApps():
#    for app in apps:
#        os.startfile(app)
##
##openFile = tk.Button(root, text="Load File", padx=10, pady=5, 
#                    fg="white", bg="#253D42", command=addApp)
##
##runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, 
#                    fg="white", bg="#253D42", command=runApps)
##
##compareImages_app = tk.Button(root, text="Compare Images on Ped2", padx=10, pady=5, 
#                    fg="white", bg="#253D42", command=compareImages())
##
##
### Attach function on canvas
##compareImages_app.pack()
##runApps.pack()
##openFile.pack()
##
##root.mainloop()
)

def get_dataset_frames():
    time_t = 0
    test_input_path = []
    for i in range(178):
        frame_th = ''
        frame_num = time_t + i
        if frame_num < 10:
            frame_th = '00' + str(frame_num)
        elif frame_num < 100:
            frame_th = '0' + str(frame_num)
        else:
            frame_th = str(frame_num)
        test_input_path.append("./datasets/testing/frames/01/" + frame_th + ".jpg")

    pred_input_path = []
    for i in range(174):
        frame_th = ''
        frame_num = time_t + i
        if frame_num < 10:
            frame_th = '00' + str(frame_num)
        elif frame_num < 100:
            frame_th = '0' + str(frame_num)
        else:
            frame_th = str(frame_num)
        pred_input_path.append("./datasets/predicted/pred/frames/0" + frame_th + ".jpg")

    test_input_imgs = []
    for i in range(178):
        img = cv2.imread(test_input_path[i])
        test_input_imgs.append(img)

    pred_input_imgs = []
    for i in range(174):
        img = cv2.imread(pred_input_path[i])
        pred_input_imgs.append(img)

    return test_input_imgs, pred_input_imgs

def optimalThreshold(anomal_scores, labels):
    y_true = 1 - labels[0, :1962]
    y_true  = np.squeeze(y_true)
    y_score = np.squeeze(anomal_scores[:1962])
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_score)
    frame_auc = metrics.roc_auc_score(y_true, y_score)
    print("AUC: {}".format(frame_auc))
    # calculate the g-mean for each threshold
    gmeans = np.sqrt(tpr * (1-fpr))
    # locate the index of the largest g-mean
    ix = np.argmax(gmeans)
    print('Best Threshold=%f, G-Mean=%.3f' % (threshold[ix], gmeans[ix]))
    # plot the roc curve for the model
    #pyplot.plot([0,1], [0,1], linestyle='--', label='No Skill')
    #pyplot.plot(fpr, tpr, marker='.', label='Logistic')
    #pyplot.scatter(fpr[ix], tpr[ix],  marker='o', color='black', label='Best')
    ## axis labels
    #pyplot.xlabel('False Positive Rate')
    #pyplot.ylabel('True Positive Rate')
    #pyplot.legend()
    # show the plot
    #pyplot.show()
    #return threshold[ix]
    #anomaly_score_total_list, np.expand_dims(1-labels_list, 0)
    #print()
    return threshold[ix]

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        if self.video_source == 0:
            self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        else:
            self.canvas = tk.Canvas(window, width = 650, height = 300)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.ImgDiff = id.Image_Difference()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.iter_frame = 0

        #if video_source == 0:   
        #    self.update()
        #else:
        self.static_update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        ## Get a frame from the video source
        #ret, frame = self.vid.get_frame()
#
        #if ret:
        #    # convert opencv narray image to PIL image
        #    self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
        #    # attach image on canvas
        #    self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
#
        #self.window.after(self.delay, self.update)
        pass

    def static_update(self):
        # Get a frame from the video source
        test_frame, predicted_frame, anomaly_score = self.vid.get_static_frame(self.iter_frame)

        test_img, pred_img = self.ImgDiff.image_differences(test_frame, predicted_frame, anomaly_score, self.vid.opt_threshold)
        #cv.waitKey(0)
        #cv2.imshow("Test frame compared", cv2.resize(test_frame, None, fx=1, fy=1))
        #cv2.imwrite("Result_Original.png", imageA)
        #cv2.imshow("Pred frame compared", cv2.resize(predicted_frame, None, fx=1, fy=1))
        #cv2.waitKey(5)

        # Closes all the frames
        
        # convert opencv narray image to PIL image
        self.photo_test = ImageTk.PhotoImage(image = Image.fromarray(test_img))
        # attach image on canvas
        self.canvas.create_image(0, 0, image = self.photo_test, anchor = tk.NW)
        # convert opencv narray image to PIL image
        self.photo_pred = ImageTk.PhotoImage(image = Image.fromarray(pred_img))
        # attach image on canvas
        self.canvas.create_image(300, 0, image = self.photo_pred, anchor = tk.NW)

        self.window.after(self.delay, self.static_update)

        if self.iter_frame == 170:
            self.iter_frame = 0
        else:
            self.iter_frame+=1

class VideoCapture:
    def __init__(self, video_source=0):
        self.video_source = video_source
        # Open the video source, # capture video by webcam by default 
        if video_source == 0:
            self.vid = cv2.VideoCapture(video_source)  
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", video_source)
                    
            # Get video source width and height
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        else:
            # load test and predicted frames
            test_frames, predicted_framese = get_dataset_frames()
            self.vid = [test_frames, predicted_framese]
            # load frame
            self.frame_scores = np.load("./datasets/predicted/anomaly_score.npy")
            labels = np.load('./data/frame_labels_'+'ped2'+'.npy')
            self.opt_threshold = optimalThreshold(self.frame_scores, labels)


    def get_frame(self):
        #if self.vid.isOpened():
        #    ret, frame = self.vid.read()
        #    if ret:
        #        # Return a boolean success flag and the current frame converted to BGR
        #        return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #    else:
        #        return (ret, None)
        #else:
        #    return (ret, None)
        pass
#
    def get_static_frame(self, iter_frame):
        # load the two input images
        i = iter_frame
        list_imageA = self.vid[0]  # test frame
        imageA = list_imageA[i+4]
        list_imageB = self.vid[1]
        imageB = list_imageB[i]    # pred frame

        # resize image
        w1, h1, c1 = imageA.shape
        w2, h2, c2 = imageB.shape
        if w1 != 256:
            imageA = cv2.resize(imageA, (256, 256))
        if w2 != 256:
            imageB = cv2.resize(imageB, (256, 256))

        anomaly_score = self.frame_scores[i]
        return imageA, imageB, anomaly_score

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.video_source == 0:
            if self.vid.isOpened():
                self.vid.release()
        else:
            pass

# Create a window and pass it to the Application object
App(tk.Tk(), "Tkinter and OpenCV", video_source=1)
cv2.destroyAllWindows()