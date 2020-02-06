from tkinter import *
from pynput.mouse import (
	Button as MButton,
	Controller as MController
)
from datetime import datetime, timedelta, time as dtime
from threading import Thread


""" mouse = Controller()


def click():
	# Press and release
	mouse.press(Button.left)
	mouse.release(Button.left)

 """


MOUSE = MController()

START_COUNTER = "00:00:00:00"
FORMAT_TIME = r"%H:%M:%S.%f"

flag_counter_active = False
flag_counter_running = False


def activate_counter():
	global flag_counter_active
	flag_counter_active = True


def terminate_counter():
	global flag_counter_active
	flag_counter_active = False


def reset_counter():
	# Sayacın sonlanmasını bekleme
	while flag_counter_running: pass

	label_counter.configure(text=START_COUNTER)


def on_time_finished():
	MOUSE.click(MButton.left)
	label_counter_title.configure(text="Mause tıklanıldı")

	terminate_counter()
	Thread(target=reset_counter).start()
	# 00:50:00.00


def on_stop_clicked():
	terminate_counter()
	Thread(target=reset_counter).start()

	label_counter_title.configure(text="Durduruldu")

def get_time_remain(time) -> timedelta:
	"""Yerel saat ile verilen time arasındaki farkı bulma

	Arguments:
		time {time} -- Saat bilgisi

	Returns:
		timedelta -- Zaman farkı
	"""
	return time - datetime.strptime(str(datetime.now().time()), FORMAT_TIME)

def is_before(time: dtime) -> bool:
	"""Verilen süre geçildi mi

	Arguments:
		time {dtime} -- Saat bilgisi

	Returns:
		bool -- Geçildiyse evet
	"""
	return get_time_remain(time).days < 0


def update_counter(time):
	global flag_counter_running

	while flag_counter_active:
		flag_counter_running = True

		window.update() # TODO
		time_remain = get_time_remain(time)
		label_counter.configure(text=str(time_remain))

		if time_remain.days < 0:
			on_time_finished()

		flag_counter_running = False

def on_start_clicked():
	# Thread zaten çalışıyorsa tekrar thread oluşturma
	if not flag_counter_active:
		time_string = entry_time.get()
		time = datetime.strptime(time_string, FORMAT_TIME)

		if not is_before(time):
			label_counter_title.configure(text="Kalan süre")

			activate_counter()
			Thread(target=update_counter, args=[time]).start()
		else:
			label_counter_title.configure(text="Verilen vakit eski")


def centerilaze(root: Tk, width: int, height: int):
	# Gets both half the screen width/height and window width/height
	positionRight = int(root.winfo_screenwidth()/2 - width/2)
	positionDown = int(root.winfo_screenheight()/2.5 - height/2)

	# Positions the window in the center of the page.
	root.geometry(f"{width}x{height}+{positionRight}+{positionDown}")
	root.geometry("+{}+{}".format(positionRight, positionDown))

if __name__ == "__main__":

	row = 0

	window = Tk()

	window.title("YClicker")
	window.resizable(False, False)

	centerilaze(window, 360, 180)


	frame_main = Frame(window)
	frame_main.pack()

	label_title = Label(frame_main, text="Tıklanacağı saati giriniz")
	label_title.grid(column=0, row=row, columnspan=2, pady=(10, 0))
	row += 1

	# self.a_button.grid(row=0, column=1, padx=10, pady=10)
	entry_time = Entry(frame_main, width=20, justify="center")
	entry_time.grid(column=0, row=row, columnspan=2, pady=(10,0))
	row += 1

	btn_stop = Button(frame_main, text="Durdur", fg="red", command=on_stop_clicked)
	btn_start = Button(frame_main, text="Başlat", fg="green", command=on_start_clicked)

	btn_stop.grid(column=0, row=row, pady=10)
	btn_start.grid(column=1, row=row, pady=10)
	row += 1

	label_counter_title = Label(
		frame_main, text="Henüz çalışmıyor", font='Helvatica 9 bold', pady=3
	)

	label_counter_title.grid(column=0, row=row, columnspan=2)
	row += 1

	label_counter = Label(frame_main, text=START_COUNTER)
	label_counter.grid(column=0, row=row, columnspan=2)
	row += 1

	window.mainloop()
