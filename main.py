from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
from simple_facerec import SimpleFacerec

# Variables
cam = FALSE
scan = FALSE
snapshot = FALSE
unknown = TRUE

root = Tk()
root.title("Face Recognition Application")

# size and place adjustments of the application window
root.geometry("%dx%d+%d+%d" % (1200, 700, 70, 30))


# CANVAS
# Upper part of the window
header = Frame(root, width=1200, height=150, bg="#F1F7F8")
header.grid(columnspan=4, rowspan=2, row=0)

# Middle part of the window
middle = Frame(root, width=1200, height=450, bg="#C0D0D8")
middle.grid(columnspan=4, rowspan=3, row=2)

cam_d = Frame(root, width=560, height=420, bg="#9FB3BC")
cam_d.grid(columnspan=2, rowspan=3, row=2, column=0)

cam_w = Frame(root, width=560, height=420, bg="#9FB3BC")
cam_w.grid(columnspan=2, rowspan=3, row=2, column=0)

# Lower part of the window
footer = Frame(root, width=1200, height=100, bg="#405863")
footer.grid(columnspan=4, rowspan=1, row=5)


# INSTRUCTIONS
# Instruction for camera
instruction = Label(root, text="Please open the camera", font=("Montserrat", 20), bg="#F1F7F8", fg="#30424B")
instruction.grid(row=0, column=0, columnspan=2)

# Footnote for user to understand when to save their name & face
instruction2 = Label(root, text="Note: Please register if the name tag is   'unknown'", font=("Montserrat", 10), bg="#405863", fg="#F1F7F8")
instruction2.grid(row=5, column=0, sticky=W, padx=30)

# User name display
text3 = StringVar()
instruction3 = Label(root, textvariable=text3, font=("Montserrat", 20), bg="#F1F7F8", fg="#30424B")
text3.set("[ your name will be displayed here ]")
instruction3.grid(row=1, column=2, columnspan=2)

# Instruction for entering name
instruction4 = Label(root, text="Please write your name", font=("Montserrat", 20), bg="#C0D0D8", fg="#30424B")
instruction4.grid(row=3, column=2, sticky=N, columnspan=2)

# Empty string for possible warnings
text5 = StringVar()
instruction5 = Label(root, textvariable=text5, font=("Montserrat", 10), bg="#C0D0D8", fg="#30424B")
text5.set("")
instruction5.grid(row=4, column=2, columnspan=2)


# BUTTONS
# Camera Button
button_text = StringVar()
cam_btn = Button(root, textvariable=button_text, command=lambda: open_cam(), font=("Montserrat", 12, "bold"), bg="#4F6D7A", fg="#F1F7F8", height=1, width=15, disabledforeground="#9FB3BC")
button_text.set("Open Camera")
cam_btn.grid(row=1, column=0, columnspan=2)

# Exit Button
exit_text = StringVar()
exit_btn = Button(root, textvariable=exit_text, command=root.destroy, font=("Montserrat", 10, "bold"), bg="#F1F7F8", fg="#30424B", height=1, width=10)
exit_text.set("Exit")
exit_btn.grid(row=5, column=3, sticky=E, padx=30)

# Unused buttons
''' # Login Button
login_text = StringVar()
login_btn = Button(root, textvariable=login_text, font=("Montserrat", 12, "bold"), bg="#4F6D7A", fg="#F1F7F8", height=1, width=12)
login_text.set("Login")
login_btn.grid(row=2, column=3, sticky=W)

# Register Button
register_text = StringVar()
register_btn = Button(root, textvariable=register_text, font=("Montserrat", 12, "bold"), bg="#4F6D7A", fg="#F1F7F8", height=1, width=12)
register_text.set("Register")
register_btn.grid(row=2, column=2, sticky=E)
'''

# Save Button
# When clicked it snapshots the frame and saves to file 'images' - saves your 'face' for future recognition -
save_text = StringVar()
save_btn = Button(root, textvariable=save_text, command=lambda : snapshot_on(), font=("Montserrat", 14, "bold"), bg="#4F6D7A", fg="#F1F7F8", height=1, width=10)
save_text.set("Save")
save_btn.grid(row=3, column=2, rowspan=2, columnspan=2)

# Scan On Button
# When clicked it activates the face recognition feature - see if you are in the system or not -
scan_on_text = StringVar()
scan_on_btn = Button(root, textvariable=scan_on_text, command=lambda : scan_on(), font=("Montserrat", 14, "bold"), bg="#4F6D7A", fg="#F1F7F8", height=1, width=10)
scan_on_text.set("Scan On")
scan_on_btn.grid(row=2, column=2, sticky=E, padx=10)

# Scan off Button
# When clicked it deactivates the face recognition feature - if not in the system save your face by clicking 'save' -
scan_off_text = StringVar()
scan_off_btn = Button(root, textvariable=scan_off_text, command=lambda : scan_off(), font=("Montserrat", 14, "bold"), bg="#4F6D7A", fg="#F1F7F8", height=1, width=10)
scan_off_text.set("Scan Off")
scan_off_btn.grid(row=2, column=3, sticky=W, padx=10)

# Input Box
# The entry box for user to enter the preferred name for the photo which is going to be saved as your name & face
input_box = Entry(root, width=25, font=("Montserrat", 16), justify="center")
input_box.grid(row=3, column=2, columnspan=2)


# method for opening the camera
# in this the method there are; snapshot, scan and scan off  features
# every action needs to be done when the camera is open !
def open_cam():
   global cam
   cam = TRUE
   camera_w = Label(cam_w)
   camera_w.grid(row=2, column=0)

   # Testing (unused code segment)
   '''
   face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   '''

   cap = cv2.VideoCapture(0)

   text5.set("Please first check whether you are in the system or not by clicking 'Scan On'")

   # displaying the frames of the cpatured video
   def show_frames():
      global unknown    # to indicate whether the user is in the system or not (unknown)

      if snapshot == TRUE:     # If the user clicks the save button (snapshot = TRUE)
         if unknown == TRUE:     # If the user is unknown after scanning (unknown = TRUE) then user can save their name & face
            click(cap)
         elif unknown == FALSE:     # If not, a warning message will appear
            text5.set("You are already in system, cannot save again :(")

      cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)

      if scan == TRUE:     # If the user clicks the scan button (scan = TRUE) (the scan features activates)

         # Testing (unused code segment)
         '''faces = face_cascade.detectMultiScale(cv2image, 1.1, 4)
         for (x, y, w, h) in faces:
            cv2.rectangle(cv2image, (x, y), (x + w, y + h), (255, 0, 127), 2)
         '''

         sfr = SimpleFacerec()
         sfr.load_encoding_images("images/")

         face_locations, face_names = sfr.detect_known_faces(cv2image)

         for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(cv2image, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 127), 2)
            cv2.rectangle(cv2image, (x1, y1), (x2, y2), (255, 0, 127), 2)


         if face_names != ['Unknown']:
            unknown = FALSE
            text5.set("Face Detected! Hello {}".format(face_names))
         if face_names == ['Unknown']:
            unknown = TRUE
            text5.set("You are not in the system")

         text3.set(face_names)

      img = Image.fromarray(cv2image)
      img = img.resize((530, 390), Image.Resampling.LANCZOS)
      # image flip (mirrow view)
      img = Image.fromarray(np.fliplr(img))
      imgtk = ImageTk.PhotoImage(image=img)

      camera_w.imgtk = imgtk
      camera_w.configure(image=imgtk)
      camera_w.after(20, show_frames)

   button_text.set("Camera Opened")

   show_frames()

   cam_btn["state"] = "disabled"
#end of method open_cam()

# when clicked on the Scan On button -> scan = TRUE (we can go inside the if scan == TRUE: statement which activates the face recognition feature)
# gives warning message if camera is not opened
def scan_on():
   global scan
   if cam == TRUE:
      scan = TRUE
   elif cam == FALSE:
      text5.set("Please first open the camera ^^")
#end of method scan_on()

# when clicked on the Scan Off button -> scan = FALSE (we cannot go inside the if scan == TRUE: statement so the face recognition feature deactivates)
# gives warning message if camera and scan features are not on
def scan_off():
   global scan
   if cam == TRUE:
      if scan == TRUE:
         scan = FALSE
      elif scan == FALSE:
         text5.set("Scan feature is already off.")
   else:
      text5.set("Please first open the camera ^^")
#end of method scan_off()

# when clicked on the Save button -> snapshot = TRUE (we can go inside the if snapshot == TRUE: statement which activates the click(cap) method to save the photo)
# gives warning message if camera is not opened
def snapshot_on():
   global snapshot
   if cam == TRUE:
      snapshot = TRUE
   else:
      text5.set("Please first open the camera and check whether you are in the system or not")
# end of method snapshot_on()

# method for saving the desired photo to the images file in the project
# saves as name.jpg & name cannot be empty, if so gives a warning message
# make snapshot = FALSE after saving photo & empty the entry box for new input
def click(cap):
   global snapshot

   input = input_box.get()
   ret, frame = cap.read()

   if input != "":
      img_name = "{}.jpg".format(input)
      path = (r"C:\Users\IPEK\PycharmProjects\pythonProject3\images")
      cv2.imwrite(os.path.join(path, img_name), np.fliplr(frame))
      text5.set("{} is saved!".format(img_name))
   else:
      text5.set("cannot save T^T please write your name!")

   snapshot = FALSE
   input_box.delete(0, END)
# end of method click(cap)


root.mainloop()