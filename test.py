import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import telepot
import time
import tkinter as tk
from PIL import Image, ImageTk

model = load_model('C:/Users/adity/Downloads/Wild_Animal_Detection_and_Alert_System-main/Wild_Animal_Detection_and_Alert_System-main/keras_model.h5')

class_labels = ['HUMAN', 'TIGER', 'LION', 'CHEETAH', 'HYENA', 'DONKEY', 'GOAT', 'DEER', 'HOUSE', 'ELEPHANT', 'FOX', 'LEOPARD', 'RHINOCEROS', 'SNAKE', 'WOLF', 'CAT', 'CHIMPANZEE', 'COW', 'DOG', 'DUCK', 'MONKEY', 'ZEBRA']

bot_token = "6666638666:AAFqDSJM5Hnw-YoAhIG0WiFr69btxtFk3Yc"
chat_id = "1035950237"  
bot = telepot.Bot(bot_token)
last_detection_time = time.time()

def predict_animal(frame):
    global last_detection_time  # Declare it as a global variable
    img = cv2.resize(frame, (224, 224))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    prediction = model.predict(img_tensor)
    class_index = np.argmax(prediction[0])
    class_label = class_labels[class_index]
    if class_label in ['TIGER', 'LION', 'CHEETAH', 'HYENA', 'ELEPHANT', 'FOX', 'LEOPARD', 'RHINOCEROS', 'SNAKE', 'WOLF'] and time.time() - last_detection_time >= 5:
        cv2.imwrite('captured_image.jpg', frame)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open('captured_image.jpg', 'rb') as photo:
            bot.sendPhoto(chat_id, photo, caption=f'''🚨 ALERT: {class_label} Detected 🚨
                        📅 Timestamp: {current_time} 🕒
                        Take immediate precautions for your safety:
                        1️⃣ Stay calm and alert.
                        2️⃣ Follow official instructions.
                        3️⃣ Take necessary precautions.
                        4️⃣ Stay informed from reliable sources.
                        5️⃣ Help others while maintaining distance.
                        Cooperate with authorities and stay safe! 
                        We will provide further updates as soon as possible.Stay safe and stay vigilant!''')
        last_detection_time = time.time()
    return class_label

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Use the default webcam
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_capture = tk.Button(window, text="Capture", width=10, command=self.capture_frame)
        self.btn_capture.pack(padx=10, pady=10)

        self.after_id = None
        self.update()
        self.window.mainloop()

    def capture_frame(self):
        ret, frame = self.vid.read()
        if ret:
            predict_animal(frame)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.after_id = self.window.after(10, self.update)

    def __del__(self):
        if self.after_id:
            self.window.after_cancel(self.after_id)
        if self.vid.isOpened():
            self.vid.release()

# Create a Tkinter window and pass it to the WebcamApp class
root = tk.Tk()
app = WebcamApp(root, "Wild Animal Detection App")
