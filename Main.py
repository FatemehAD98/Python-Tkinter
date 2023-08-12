import tkinter as tk
from datetime import date
import datetime
import csv
import openpyxl
from datetime import datetime, timedelta
import threading
import time
import re
import winsound
import os
import tkinter as tk
import sounddevice as sd
import wavio
import pythoncom
from tkinter import PhotoImage
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from pydub import AudioSegment
from pydub.playback import play

from PIL import Image, ImageTk,ImageFilter

class MyGUI:

    def __init__(self, root):
        self.root = root
        self.root.geometry("2100x1000")
        self.root.title("ستاره ها")
        # Load the image

        root.config(bg="#FFE1FF")

        self.tk=tk
        self.value_list=[]
        self.cancel = tk.PhotoImage(file="C:/python/close.png").subsample(20)
        self.alarm=tk.PhotoImage(file="C:/python/warning.png").subsample(10)



        self.title_list(":اسم", 1280, 100)
        # self.title_list(":ساعت ورود", 1200, 180)
        self.title_list(":تعداد افراد", 1210, 180)
        self.title_list(":وسیله بازی", 1210, 260)
        self.title_list(":عینک", 1260, 340)
        self.title_list(":کل تایم", 1250, 420)
        self.title_list(":مبلغ قابل پرداخت", 1150, 500)

        self.counter = 0
        self.repetitions = 0
        self.is_recording = False

        self.vlc_process_name = "vlc.exe"  # Adjust this if your VLC process name is different
        self.volume_range = [0.0, 1.0]  # Adjust the volume range if necessary

        #create entry number for تعداد بچه ها
        self.value_number_child = tk.IntVar(value=1)
        self.frame_number_child = tk.Frame()
        self.frame_number_child.place(x=900,y=160)
        # Create the widgets
        self.minus_button = tk.Button(self.frame_number_child, text='-', command=self.decrease_value_number, width=3,
                                      font=('Arial', 14, 'bold'))
        self.minus_button.pack(side=tk.LEFT)

        self.label_game = tk.Label(self.frame_number_child, textvariable=self.value_number_child, width=10, font=('Arial', 14))
        self.label_game.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.plus_button = tk.Button(self.frame_number_child, text='+', command=self.increase_value_number, width=3,
                                     font=('Arial', 14, 'bold'))
        self.plus_button.pack(side=tk.LEFT)




        #create entry number for وسیله بازی
        self.value_game = tk.IntVar(value=0)
        self.frame_game = tk.Frame()
        self.frame_game.place(x=900,y=260)

        # Create the widgets
        self.minus_button = tk.Button(self.frame_game, text='-', command=self.decrease_value_game, width=3,
                                      font=('Arial', 14, 'bold'))
        self.minus_button.pack(side=tk.LEFT)

        self.label_game = tk.Label(self.frame_game, textvariable=self.value_game, width=10, font=('Arial', 14))
        self.label_game.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.plus_button = tk.Button(self.frame_game, text='+', command=self.increase_value_game, width=3,
                                     font=('Arial', 14, 'bold'))
        self.plus_button.pack(side=tk.LEFT)



        # create entry number for عینک
        self.value_glass = tk.IntVar(value=0)
        self.frame_glass = tk.Frame()
        self.frame_glass.place(x=900, y=340)

        # Create the widgets
        self.minus_button = tk.Button(self.frame_glass, text='-', command=self.decrease_value_glass, width=3,
                                      font=('Arial', 14, 'bold'))
        self.minus_button.pack(side=tk.LEFT)

        self.label_glass = tk.Label(self.frame_glass, textvariable=self.value_glass, width=10, font=('Arial', 14))
        self.label_glass.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.plus_button = tk.Button(self.frame_glass, text='+', command=self.increase_value_glass, width=3,
                                     font=('Arial', 14, 'bold'))
        self.plus_button.pack(side=tk.LEFT)


        # create entry number for  کل تایم
        self.time = datetime.strptime("00:00", "%H:%M")  # Set initial time to 00:00
        self.value_total_time = tk.StringVar(value=self.time.strftime("%H:%M"))  # Create a string variable to display the time
        # self.value_total_time= tk.IntVar(value=self.time_string)
        self.frame_total_time = tk.Frame()
        self.frame_total_time.place(x=900, y=420)
        # Create the widgets
        self.minus_button = tk.Button(self.frame_total_time, text='-', command=self.minus_time, width=3,
                                      font=('Arial', 14, 'bold'))
        self.minus_button.pack(side=tk.LEFT)

        self.label_time = tk.Label(self.frame_total_time, textvariable=self.value_total_time, width=10, font=('Arial', 14))
        self.label_time.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.plus_button = tk.Button(self.frame_total_time, text='+', command=self.add_time, width=3,
                                     font=('Arial', 14, 'bold'))
        self.plus_button.pack(side=tk.LEFT)


        # create an entry widget for user input
        my_font = ("Calibri", 15)  # Set the font family and size
        self.nameEntry=self.tk.Entry(self.root, width=25, font=my_font)
        self.nameEntry.place(x=920, y=110)

        # Create the recording button
        record_button = tk.Button(self.root, text="ضبط صدا", command=self.start_recording)
        record_button.place(x=700, y=110)

        # Create a canvas for the scrollable content
        self.canvas = tk.Canvas(self.root, bd=2, relief=tk.SUNKEN, width=350, height=300, bg='White')
        self.canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame inside the canvas for the content
        self.frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0),width=350, window=self.frame, anchor='nw', tags='frame')

        # Create a scrollbar on the left side of the window
        self.scrollbar = tk.Scrollbar(self.root , orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Configure the scrollbar to work with the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.on_canvas_configure)


        self.button("ذخیره و پرداخت")

        self.check_thread = threading.Thread(target=self.check_input_list)
        self.check_thread.start()





    def title_list(self,name, x, y):
        # Create a Label widget
        self.Name = tk.Label(text=name, font=("Calibri", 20 , "bold"))
        # Place the Label widget at my position  on the screen
        self.Name.place(x=x, y=y)

    def button(self,txt):
        # create a button widget
        self.button = tk.Button(text=txt, command=self.entry_save, font=("Calibri", 20))
        # pack the button into the root window
        self.button.place(x=900, y=580)

    def start_recording(self ):
        # Set the recording parameters
        duration = 5  # Recording duration in seconds
        self.sample_rate = 44100  # Sample rate (number of samples per second)
        channels = 2  # Number of audio channels (2 for stereo)

        # Record audio
        self.recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=channels)
        sd.wait()

        return self.recording

    def entry_save(self):
        self.current_date = date.today()
        self.date_string = self.current_date.strftime('%Y-%m-%d')
        if not os.path.exists(self.date_string + ".xlsx"):
           self.excel()

        # Get the value_game from the entry widget and append it to the list
        self.nameVlue = self.nameEntry.get()
        # self.SystemTimeValue = self.enter_time_label.cget("text")
        self.gameValue=self.label_game.cget("text")
        self.glassValue=self.label_glass.cget("text")
        self.ToalTimeValue=self.label_time.cget("text")

        #check empety inputs
        warning = False
        if not self.nameVlue :
            # show an error message or return from the function
            if not warning:
                warning = True
                popup = tk.Toplevel()
                popup.title("هشدار")
                popup.geometry("400x300")
                # Disable main window
                root.attributes("-disabled", True)
                # Disable close button
                popup.protocol("WM_DELETE_WINDOW", lambda: None)
                text = "لطفا همه ی ورودی ها را وارد کنید "
                label = tk.Label(popup, text=text)
                label.pack(padx=10, pady=10)

                def remove():
                    # Enable main window
                    root.attributes("-disabled", False)
                    # Close popup window
                    popup.destroy()
                    # Perform action
                    self.show_warning = False

                continue_button = tk.Button(popup, text="تایید", command=remove)
                continue_button.pack(padx=10, pady=10)

        if warning:
            return

        self.CostValue = self.sum_lbl.cget("text")

        # Check for repetitious names
        show_warning = False
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Frame):
                for label in child.winfo_children():
                    if isinstance(label, tk.Label) and label.cget('text') == "اسم: " + self.nameVlue:
                        if not show_warning:
                            show_warning = True
                            popup = tk.Toplevel()
                            popup.title("هشدار")
                            popup.geometry("400x300")
                            # Disable main window
                            root.attributes("-disabled", True)
                            # Disable close button
                            popup.protocol("WM_DELETE_WINDOW", lambda: None)
                            text = "کودک با این نام در محل بازی وجود دارد .اسم جدید انتخاب کنید "
                            label = tk.Label(popup, text=text)
                            label.pack(padx=10, pady=10)

                            def remove():
                                # Enable main window
                                root.attributes("-disabled", False)
                                # Close popup window
                                popup.destroy()
                                # Perform action
                                self.show_warning = False

                            continue_button = tk.Button(popup, text="تایید", command=remove)
                            continue_button.pack(padx=10, pady=10)

        if show_warning:
            return


        #calculate exite time
        self.current_time = datetime.now().strftime('%H:%M')
        time_format = "%H:%M"
        # Convert clocks to datetime objects

        self.dt_sum=self.exit_time(self.current_time , self.ToalTimeValue)
        self.exitTime=self.dt_sum.strftime("%H:%M")

        self.lst = [self.nameVlue,self.current_time , self.gameValue,
                    self.glassValue ,self.ToalTimeValue, self.CostValue]

        for i in self.lst:
            self.value_list.append(i)
        self.list_of_lists = []
        self.list_of_lists.append(self.lst)

        # EXCEL
        self.current_date = date.today()
        self.date_string = self.current_date.strftime('%Y-%m-%d')
        # Load the existing Excel file
        self.workbook = openpyxl.load_workbook(self.date_string + ".xlsx")
        self.worksheet = self.workbook.active
        # Define the new data you want to add
        for row in self.list_of_lists:
            self.worksheet.append(row)
        self.workbook.save(self.date_string + ".xlsx")

        #VOICE RECORD
        self.add_box_waiting_list(self.nameVlue , self.exitTime)
        # Save the recording to a WAV file
        wavio.write(str(self.counter)+".wav", self.recording, self.sample_rate, sampwidth=2)

        self.value_list.clear()
        self.list_of_lists.clear()
        #reset all inputs
        self.nameEntry.delete(0, 'end')
        self.label_game.config(text="")

        self.value_number_child.set(1)
        self.value_game.set(0)
        self.value_glass.set(0)
        self.value_total_time.set("00:00")
        self.sum_lbl.config(text="0 تومان")



    def exit_time(self, enterTime , totalTime):
        # convert the time strings to datetime objects
        dt1 = datetime.strptime(enterTime, "%H:%M")
        dt2 = datetime.strptime(totalTime, "%H:%M")
        # add the two datetime objects
        dt_sum = dt1 + timedelta(hours=dt2.hour, minutes=dt2.minute)
        return  dt_sum

    def save_time(self):
        if self.check_var.get() == 1:
            self.current_time = datetime.now().strftime('%H:%M')
            self.enter_time_label.config(text=self.current_time)
        x = self.enter_time_label.cget("text")
        return x

    def excel(self):
        # Get current system date
        self.current_date = date.today()
        # Convert date to string in "YYYY-MM-DD" format
        self.date_string = self.current_date.strftime('%Y-%m-%d')
        # Create a new workbook
        self.workbook = openpyxl.Workbook()
        # Select the active worksheet
        self.worksheet = self.workbook.active
        # Write data to cells
        self.worksheet['A1'] = 'اسم'
        self.worksheet['B1'] = 'ساعت ورود'
        self.worksheet['C1'] = 'تعداد وسیله بازی'
        self.worksheet['D1'] = 'عینک'
        self.worksheet['E1'] = 'کل تایم'
        self.worksheet['F1'] = "مبلغ کل"
        # Save the workbook
        self.workbook.save(self.date_string + ".xlsx")




    def add_box_waiting_list(self, name, exit):
        self.counter += 1
        box = tk.Frame(self.frame, bd=2, relief=tk.RIDGE, bg='blue', height=100, width=self.canvas.winfo_width())
        box.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)
        # Create a top toolbar frame
        toolbar = tk.Frame(box, bg='white', height=30)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # Create the first icon label
        icon1 = tk.Label(toolbar, image=self.cancel, state=tk.DISABLED)
        icon1.pack(side=tk.RIGHT, padx=5, pady=2)
        # Create the second icon label
        icon2 = tk.Label(toolbar, image=self.alarm, state=tk.DISABLED)
        icon2.pack(side=tk.LEFT, padx=5, pady=2)
        tk.Label(box, text="اسم: "+ name, width=50, anchor='e', font=("Arial", 15, "bold")).pack()
        # tk.Label(box, text="ساعت ورود: "+ enter, width=50,anchor='e',font=("Arial", 15,"bold")).pack()
        tk.Label(box, text= "ساعت خروج: "+ exit, width=50,anchor='e',font=("Arial", 15,"bold")).pack()
        tk.Label(box, text="شماره: " + str(self.counter), width=50, anchor='e', font=("Arial", 15, "bold")).pack()
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))



    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.frame.configure(width=self.canvas.winfo_width())

    def check_input_list(self):
        while True:
            if len(self.frame.winfo_children()) > 0:
                for child in self.frame.winfo_children():
                    if isinstance(child, tk.Frame):
                        for label in child.winfo_children():
                            current_time_exit = datetime.now().strftime('%H:%M')
                            if isinstance(label, tk.Label) and label.cget('text') == "ساعت خروج: " + current_time_exit:
                                timeExitPattern=self.time_pattern(label.cget("text"))
                                #get third lable in child ( شماره =؟)
                                label_count = 0
                                for child_label in child.winfo_children():
                                    if isinstance(child_label, tk.Label):
                                        label_count += 1
                                        if label_count == 3:
                                            string=child_label.cget('text')
                                            number = ''.join(filter(str.isdigit, string))

                                # Enable icon1 and icon2 labels
                                icon1 = child.winfo_children()[0].winfo_children()[0]
                                icon2 = child.winfo_children()[0].winfo_children()[1]
                                icon1.config(state=tk.NORMAL)
                                icon1.bind("<Button-1>", lambda event: self.handle_click(timeExitPattern))
                                icon2.config(state=tk.NORMAL)
                                icon2.bind("<Button-1>", lambda event: self.stop_alarm())

                                child.configure(bg="red" ,borderwidth=8 )
                                self.play_sound(number)

                                break

            time.sleep(60 - datetime.now().second)  # wait until the next minute starts

    def time_pattern(self,text):
        # Define a regular expression pattern to match the time in "H:M" format
        time_pattern = r"\d{1,2}:\d{2}"
        # Search for the time pattern in the text
        match = re.search(time_pattern, text)
        match_str = match.group()
        return  match_str

    def handle_click(self, exitTime):
        current_time = datetime.now().strftime('%H:%M')
        time_format = "%H:%M"
        # Convert clocks to datetime objects
        datetime1 = datetime.strptime(exitTime, time_format)
        datetime2 = datetime.strptime(current_time, time_format)
        # Calculate difference in minutes
        diff_minutes = int((datetime2 - datetime1).total_seconds() // 60)
        for child in self.frame.winfo_children():
            if isinstance(child, tk.Frame):
                for label in child.winfo_children():
                    if isinstance(label, tk.Label) and label.cget('text') == "ساعت خروج: " + exitTime:
                        self.show_warning(diff_minutes, child)

    def show_warning(self, diff_str, child):
        # Create a popup window
        popup = tk.Toplevel()
        popup.title("هشدار")
        popup.geometry("400x300")
        # Disable main window
        root.attributes("-disabled", True)
        # Disable close button
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
        # Add text label
        costDelay = self.round_to_nearest_5(diff_str)
        strDiff = str(diff_str)
        strCostDelay = str(costDelay)
        text = "کاربر مورد نظر  " + strDiff + "  دقیقه تاخیر دارد.  "
        text2 = "مبلغ قابل پرداخت:  " + strCostDelay
        label = tk.Label(popup, text=text + text2)
        label.pack(padx=10, pady=10)

        # Add buttons
        def continue_action():
            # Enable main window
            root.attributes("-disabled", False)
            # Close popup window
            popup.destroy()
            # Perform action

        continue_button = tk.Button(popup, text="Continue", command=continue_action)
        continue_button.pack(side="left", padx=10, pady=50)

        def remove_action():
            # Enable main window
            root.attributes("-disabled", False)
            # Destroy the child of the frame
            child.destroy()
            self.stop_alarm()
            # Close popup window
            popup.destroy()

        cancel_button = tk.Button(popup, text="حذف", command=remove_action)
        cancel_button.pack(side="right", padx=10, pady=50)

        def tamdid1():
            x=strCostDelay+"15000"
            text2 = "مبلغ قابل پرداخت:  " + x
            label = tk.Label(popup, text=text2)
            label.pack(padx=10, pady=10)
        def tamdid2():
            x=strCostDelay+"25000"
            text2 = "مبلغ قابل پرداخت:  " + x
            label = tk.Label(popup, text=text2)
            label.pack(padx=10, pady=10)
        def tamdid3():
            x=strCostDelay+"15000"
            text2 = "مبلغ قابل پرداخت:  " + x
            label = tk.Label(popup, text=text2)
            label.pack(padx=10, pady=10)

        self.frame_tamdid = tk.Frame(popup)
        self.frame_tamdid.place(x=120, y=160)
        # Create the widgets
        self.minus_button = tk.Button(self.frame_tamdid, text="تمدید1", command=tamdid1, width=4,
                                      font=('Arial', 14 ))
        self.minus_button.pack(side=tk.LEFT)

        self.x = tk.Button(self.frame_tamdid,  text="تمدید2", command=tamdid2, width=4,
                                      font=('Arial', 14))
        self.x.pack(side=tk.LEFT)

        self.plus_button = tk.Button(self.frame_tamdid, text="تمدید3", command=tamdid3, width=4,
                                     font=('Arial', 14))
        self.plus_button.pack(side=tk.LEFT)



    def round_to_nearest_5(self,num):
        remainder = num % 5
        if remainder <= 3:
            x = num - remainder
            cost = (x // 5) * 5000
            return cost
        else:
            y = num + (5 - remainder)
            cost = (y // 5) * 5000
            return cost

    #ALL FUNCTIONS ABOUT VOICES AND CONTROL VLC MUSIC PLAYER
    def decrease_volume(self, volume):
        pythoncom.CoInitialize()  # Initialize the COM library
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            process = session.Process
            if process and process.name():
                process_name = process.name()
                if self.vlc_process_name.lower() in process_name.lower():
                    volume_interface.SetMasterVolume(volume, None)
        pythoncom.CoUninitialize()  # Uninitialize the COM library

    def restore_volume(self):
        pythoncom.CoInitialize()  # Initialize the COM library
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            process = session.Process
            if process and process.name():
                process_name = process.name()
                if self.vlc_process_name.lower() in process_name.lower():
                    volume_interface.SetMasterVolume(1.0, None)
        pythoncom.CoUninitialize()  # Uninitialize the COM library

    def decrease_volume_and_restore(self, voice_duration):
        # Decrease the volume
        self.decrease_volume(0.0001)  # Adjust the desired decreased volume level

        # Wait for the voice to finish playing
        time.sleep(voice_duration)

        # Restore the volume to normal
        self.restore_volume()

    # def play_sound(self , number):
    #
    #     # Code to play the voice
    #     voice_duration = 15  # Adjust the actual duration of the voice in seconds
    #     # Decrease volume in a separate thread
    #     volume_thread = threading.Thread(target=self.decrease_volume_and_restore, args=(voice_duration,))
    #     volume_thread.start()
    #     if self.repetitions >= 2:
    #         return
    #     # Play the sound file and schedule it to play again after 1 second
    #     winsound.PlaySound(number+'.wav', winsound.SND_FILENAME)
    #
    #     self.repetitions += 1
    #     global sound_id
    #     sound_id = root.after(10, self.play_sound , number)
    def play_sound(self, number):
        if self.is_recording:
            # If recording is in progress, wait until it finishes before playing a new sound
            while self.is_recording:
                time.sleep(0.1)

        def play_sound_thread():
            self.is_recording = True
            voice_duration = 15  # Adjust the actual duration of the voice in seconds
            # Decrease volume in a separate thread
            volume_thread = threading.Thread(target=self.decrease_volume_and_restore, args=(voice_duration,))
            volume_thread.start()
            if self.repetitions >= 2:
                self.is_recording = False
                return
            # Play the sound file and schedule it to play again after 1 second
            winsound.PlaySound(str(number) + '.wav', winsound.SND_FILENAME)

            self.repetitions += 1
            sound_id = root.after(10, play_sound_thread)

        # Start playing the sound in a separate thread
        play_thread = threading.Thread(target=play_sound_thread)
        play_thread.start()


    def stop_alarm(self):
        global sound_id
        # Cancel the scheduled sound
        if sound_id is not None:
            root.after_cancel(sound_id)
            sound_id = None

    def decrease_value_game(self):
        self.val= self.value_game.get() - 1
        if self.val>=0:
            self.value_game.set(self.val)
            self.total_time_if()
            # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )
        else:
            self.value_game.set(0)
            self.total_time_if()
            # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )

    def decrease_value_glass(self):
        self.val= self.value_glass.get() - 1
        if self.val>=0:
            self.value_glass.set(self.val)
            self.total_time_if()
            # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )
        else:
            self.value_glass.set(0)
            self.total_time_if()
            # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )


    def decrease_value_number(self):
        self.val= self.value_number_child.get() - 1
        if self.val>1:
            self.value_number_child.set(self.val)
            self.total_time_if()
            # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )
        else:
            self.value_number_child.set(1)
            self.total_time_if()
            # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )



    def increase_value_game(self):
        self.value_game.set(self.value_game.get() + 1)
        self.total_time_if()
        # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )

    def increase_value_glass(self):
        self.value_glass.set(self.value_glass.get() + 1)
        self.total_time_if()
        # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )

    def increase_value_number(self):
        self.value_number_child.set(self.value_number_child.get() + 1)
        self.total_time_if()
        # self.sum_costs((self.value_game.get()*7000),(self.value_glass.get()*25000) )



    def add_time(self):
        self.time += timedelta(minutes=1)  # Increment time by 30 minutes
        # Update the string variable with the new time
        if self.time<=datetime.strptime("03:00", "%H:%M"):
             self.value_total_time.set(self.time.strftime("%H:%M"))
             self.total_time_if()
        else:
            self.time=datetime.strptime("03:00", "%H:%M")
            self.total_time_if()



    def minus_time(self):
        self.time -= timedelta(minutes=30)  # decrement time by 30 minutes
        # Update the string variable with the new time

        if self.time>=datetime.strptime("00:00", "%H:%M"):
             self.value_total_time.set(self.time.strftime("%H:%M"))
             self.total_time_if()
        else:
            self.time=datetime.strptime("00:00", "%H:%M")
            self.total_time_if()

    def total_time_if(self):
        if self.value_total_time.get() == "00:00":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), 0)
        elif self.value_total_time.get() == "00:30":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), (25000*self.value_number_child.get()))
        elif self.value_total_time.get() == "01:00":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), (40000*self.value_number_child.get()))
        elif self.value_total_time.get() == "01:30":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), (65000*self.value_number_child.get()))
        elif self.value_total_time.get() == "02:00":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), (80000*self.value_number_child.get()))
        elif self.value_total_time.get() == "02:30":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), (105000*self.value_number_child.get()))
        elif self.value_total_time.get() == "03:00":
            self.sum_costs((self.value_game.get() * 10000), (self.value_glass.get() * 25000), (120000*self.value_number_child.get()))



    def sum_costs(self, game, glass ,costTime ):
        self.sum=game+glass+costTime
        self.finalSum=self.to_persian_string(self.sum)
        if hasattr(self, 'sum_lbl'):
            self.sum_lbl.destroy()  # Remove the previous label if it exists
        self.sum_lbl = tk.Label(self.root, font=('Arial', 24))
        self.sum_lbl.place(x=950, y=505)
        self.sum_lbl.config(text=self.finalSum)


    def to_persian_string(self, cost):
        # Add commas to separate the currency number from the right
        cost_str=str(cost)
        comma_index = len(cost_str) - 3
        while comma_index > 0:
            cost_str = cost_str[:comma_index] + ',' + cost_str[comma_index:]
            comma_index -= 3
        # Add the "تومان" suffix to the end of the string
        cost_str = cost_str+"تومان"
        return cost_str



root = tk.Tk()
gui = MyGUI(root)
root.mainloop()
