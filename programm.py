import tkinter
from tkinter import filedialog
import cv2
import PIL
import PIL.Image
import PIL.ImageTk
import math
import time
import numpy
from scipy.spatial import Delaunay
import CLSjson
from CLSjson import *

fullscreen = True
class window(tkinter.Frame):
	def __init__(self):
		super().__init__()
		self.morph = morph()
		self.run = True
		self.imgcans = []
		self.highlightedpoint = None
		self.pressed_keys = []
		self.master.bind('<Button-1>', self.click)
		self.starttime = 0
		self.vektor = []
		self.liste_org = []
		self.liste2_org = []
		self.tris = []
		self.firsttime = True
		self.firsttime2 = True
		self.factor = tkinter.DoubleVar()
		self.direction = 1
		# setattr(self.key_events, "starttime", None)
		self.master.bind('<Key>', self.key_events)
		self.master.title("Simple menu")
		self.keydelay = 0.6
		self.draws = []
		self.draw_funcs = [self.draw_points,
					  self.draw_triangles_morph]
		self.master.update()
		self._init_menubar()
		self._init_checkmenu()
		self._init_imgframe()
	def _init_menubar(self):
		self.menubar = tkinter.Menu(self.master)
		self.master.config(menu=self.menubar)
		self.fileMenu = tkinter.Menu(self.menubar)
		self.fileMenu.add_command(label="Exit", command=self.onExit)
		self.fileMenu.add_command(label="Open", command=self.open_img)
		self.fileMenu.add_command(label="Close", command=self.close_img)
		self.menubar.add_cascade(label="File", menu=self.fileMenu)
		
		self.editMenu = tkinter.Menu(self.menubar)
		self.editMenu.add_command(label="Save points", command=self.save_points)
		self.editMenu.add_command(label="Get Saved Points", command=self.get_points)
		self.menubar.add_cascade(label="Edit", menu=self.editMenu)
	def _init_checkmenu(self):
		self.checkmenu = tkinter.Frame(self.master, bg="#252525", width=self.master.winfo_width()/6, height=self.master.winfo_height())
		self.checkmenu.grid_propagate(0)
		self.checkmenu.grid(row=0, column=1)
		self.ckbtn_triangs = tkinter.Checkbutton(self.checkmenu, text="Show Triangulation", onvalue=1)
		self.ckbtn_triangs.switch = 0
		# self.ckbtn_triangs.cget("onvalue")
		self.ckbtn_triangs.config(variable=self.ckbtn_triangs)
		self.ckbtn_triangs.func = self.draw_points
		self.draws.append(self.ckbtn_triangs)
		self.mode = tkinter.Label(self.checkmenu, text="Hi", fg="red")
		self.ckbtn_triangs.grid()

		self.modebtn = tkinter.Button(self.checkmenu, text="fi", command=self.f_i_mode)
		self.modebtn.grid(row=4, column=0)

		self.bar = tkinter.Scale(self.checkmenu, variable=self.factor, resolution=0.05, to=1, orient="horizontal", length=500)
		self.bar.grid(row=51, column=0)

		self.mode.grid(row=50)
	def _init_imgframe(self):
		self.imgframe = tkinter.Frame(self.master, bg="#202020", width=self.master.winfo_width()*5/6, height=self.master.winfo_height())
		self.imgframe.grid(row=0, column=0)
		self.imgframe.grid_propagate(0)
	def update(self):
		self.reset_img()
		self.key_manager()
		for i in self.draw_funcs:
			i()
		self.set_img()
		# self.key_manager()
		self.master.update()
	
	def open_img(self, filename=None):
		imageRoom = tkinter.Canvas(self.imgframe)
		if filename is None:
			imageRoom.filename = filedialog.askopenfilename(parent=self.master, initialdir="./img/", filetypes=(('png files', '*.png'), ('jpg files', '*.jpg')))
		else:
			imageRoom.filename = filename
			print(imageRoom.filename)
		imageRoom.cv_imgorg = cv2.imread(imageRoom.filename)
		imageRoom.cv_img = imageRoom.cv_imgorg
		height, width, selfno_channels = imageRoom.cv_img.shape
		imageRoom.config(width=width, height=height)
		imageRoom.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imageRoom.cv_img))
		imageRoom.create_image(0, 0, image=imageRoom.photo, anchor=tkinter.NW)
		imageRoom.points = [[]]
		imageRoom.grid(row=0, column=len(self.imgcans))
		self.imgcans.append(imageRoom)
		self.master.update()
	def reset_img(self):
		for i in self.imgcans:
			i.cv_img = numpy.copy(i.cv_imgorg)
	def set_img(self):
		for i in self.imgcans:
			i.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(i.cv_img))
			i.create_image(0, 0, image=i.photo, anchor=tkinter.NW)
	def close_img(self):
		pass
	
	def key_events(self, event):
		if self.starttime == None:
			self.starttime = time.time()
			self.pressed_keys.append(event.keycode)
		elif (time.time() - self.starttime) <= self.keydelay:
			if event.keycode in self.pressed_keys:
				pass
			else:
				self.pressed_keys.append(event.keycode)
				self.starttime = time.time()
		else:
			self.starttime = time.time()
			self.pressed_keys = [event.keycode]
	def key_manager(self):
		if (time.time() - self.starttime) <= self.keydelay:
			return
		if 31 in self.pressed_keys and len(self.pressed_keys) == 1:
			self.i_mode()
		if 40 in self.pressed_keys and len(self.pressed_keys) == 1:
			self.d_mode()
		if 43 in self.pressed_keys and len(self.pressed_keys) == 1:
			self.h_mode()
		if 41 and 31 in self.pressed_keys and len(self.pressed_keys) == 2:
			self.f_i_mode()
		if 27 in self.pressed_keys and len(self.pressed_keys) == 1:
			self.r_mode()
		if 9 in self.pressed_keys and len(self.pressed_keys) == 1:
			self.run = False
		if 26 in self.pressed_keys and len(self.pressed_keys) == 1:
			self.e_mode()		
	def bindtc(self, typ, func):
		typ = "<" + typ + ">"
		for i in self.imgcans:
			i.bind(typ, func)
	
	def i_mode(self):
		self.mode["text"] = "insert mode"
		self.bindtc("Button-1", self.set_point)
	def d_mode(self):
		self.mode["text"] = "delete mode"
		self.bindtc("Button-1", self.del_point)
	def h_mode(self):
		self.mode["text"] = "highlight mode"
		self.bindtc("Button-1", self.highlight_point)
	def r_mode(self):
		self.mode["text"] = "set borderpoints"
		self.bindtc("Button-1", self.set_borderpoints)
	def f_i_mode(self):
		self.mode["text"] = "show morphing"
		self.pressed_keys = [41, 31]
		if self.firsttime is True:
			self.draw_funcs.clear()
			self.vektor = numpy.subtract(numpy.array(self.imgcans[1].points[0]), numpy.array(self.imgcans[0].points[0]))
			# morphing.img1 = self.imgcans[0].cv_img
			# morphing.liste1 =  self.imgcans[0].points[0]
			# morphing.vector = self.vektor
			counter = 0
			while counter < 1:
				self.morph.imgs[0].append(self.morph.morph_img(img1=self.imgcans[0].cv_imgorg, liste=self.imgcans[0].points[0], vector=self.vektor, factor=counter))
				self.morph.imgs[1].append(self.morph.morph_img(img1=self.imgcans[1].cv_imgorg, liste=self.imgcans[1].points[0], vector=numpy.multiply(-1, self.vektor), factor=1-counter))
				print(counter)
				counter += 0.05
			self.firsttime = False
			print(len(self.morph.imgs[0]))
		else:
			self.imgcans[0].cv_img = self.morph.imgs[0][int(self.bar.get()*20)-1]
			self.imgcans[1].cv_img = self.morph.imgs[1][int(self.bar.get()*20)-1]
	def e_mode(self):
		if self.firsttime2:
			for i in range(len(self.morph.imgs[0])):
				self.morph.img.append(cv2.addWeighted(self.morph.imgs[1][i], i/len(self.morph.imgs[0]), self.morph.imgs[0][i], 1-i/len(self.morph.imgs[0]), 0.0))
			self.firsttime2 = False
		else:
			self.imgcans[2].cv_img = self.morph.img[int(self.bar.get()*20)-1]

	def set_point(self, event):
		event.widget.points[0].append((event.x, event.y))
	def set_borderpoints(self, event):
		event.widget.points[0].append((event.x, event.y))
		self.imgcans[self.imgcans.index(event.widget) + 1].points[0].append((event.x, event.y))
	def del_point(self, event):
		index = self.imgcans.index(event.widget)
		liste = self.imgcans[index].points
		point = self.get_nearest_point(liste, (event.x, event.y))
		self.imgcans[index].points[point[0][0]].remove(point[1])
	def move_point(self, event):
		if self.highlightedpoint == None:
			print("first have to highlight point")
		else:
			print(self.highlightedpoint)
			self.points[self.highlightedpoint[0]][self.highlightedpoint.index(self.highlightedpoint[1])] = (event.x, event.y)
	def highlight_point(self, event):
		liste = event.widget.points
		nearest_point = self.get_nearest_point(liste, (event.x, event.y))
		index = self.imgcans.index(event.widget)
		self.highlightedpoint = (index, nearest_point)
		self.imgcans[index].cv_img = cv2.drawMarker(self.imgcans[index].cv_img, nearest_point[1], (255, 255, 0))
		self.imgcans[index].photos = (PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.imgcans[index].cv_img)))
		self.imgcans[index].create_image(0, 0, image=self.imgcans[index].photos, anchor=tkinter.NW)
	def save_points(self):
		# name = str(str(self.imgcans[0].filename[51:-4]) + str(self.imgcans[1].filename[51:-4]))
		name = "sebidomwenig"
		mJ.savePunkteVorherNahher(name, "morph", self.imgcans[0].points, self.imgcans[1].points)
	def get_points(self):
		try:
			# name = str(str(self.imgcans[0].filename[6:-4]) + str(self.imgcans[1].filename[6:-4]))
			# print(name)
			name = "sebidomwenig"
			A, B = mJ.getPunkteVorherNahher(name, "morph")
			self.imgcans[0].points = A
			self.imgcans[1].points = B
			pass
		except:
			print("no points available")

	def click(self, event):
		x = event.x_root - self.master.winfo_rootx() 
		y = event.y_root - self.master.winfo_rooty() 
		z = self.master.grid_location(x, y)
	def shiftMove(self, event):
		print("Hi! Nice to meet you! Input your Name!")
		a = input("")
		print("Hi" + a)

	def draw_points(self):
		for i in self.imgcans:
			for x in i.points:
				for z in x:
					cv2.drawMarker(i.cv_img, z, (255, 0, 0))
		if self.highlightedpoint != None:
			self.imgcans[self.highlightedpoint[0]].cv_img = cv2.drawMarker(self.imgcans[self.highlightedpoint[0]].cv_img, self.highlightedpoint[1][1], (255, 255, 0))
			self.imgcans[self.highlightedpoint[0]].photos = (PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.imgcans[self.highlightedpoint[0]].cv_img)))
			self.imgcans[self.highlightedpoint[0]].create_image(0, 0, image=self.imgcans[self.highlightedpoint[0]].photos, anchor=tkinter.NW)
	def draw_triangles(self):
		for i in self.imgcans:
			for x in i.points:
				liste = numpy.array(x)
				if len(x) >= 3:
					tri = Delaunay(liste)
					tris = liste[tri.simplices]
					for z in tris:
						i.cv_img = cv2.line(i.cv_img, tuple(z[0]), tuple(z[1]), (255, 0, 0), 1)
						i.cv_img = cv2.line(i.cv_img, tuple(z[1]), tuple(z[2]), (255, 0, 0), 1)
						i.cv_img = cv2.line(i.cv_img, tuple(z[2]), tuple(z[0]), (255, 0, 0), 1)
						i.photos = (PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(i.cv_img)))
						i.create_image(0, 0, image=i.photos, anchor=tkinter.NW)
	def draw_triangles_morph(self):
		try:
			for x in self.imgcans[0].points:
				liste = numpy.array(x)
				if len(x) >= 3:
					tri = Delaunay(liste)
					tris = liste[tri.simplices]
					for z in tris:
						self.imgcans[0].cv_img = cv2.line(self.imgcans[0].cv_img, tuple(z[0]), tuple(z[1]), (255, 0, 0), 1)
						self.imgcans[0].cv_img = cv2.line(self.imgcans[0].cv_img, tuple(z[1]), tuple(z[2]), (255, 0, 0), 1)
						self.imgcans[0].cv_img = cv2.line(self.imgcans[0].cv_img, tuple(z[2]), tuple(z[0]), (255, 0, 0), 1)
						self.imgcans[0].photos = (PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.imgcans[0].cv_img)))
						self.imgcans[0].create_image(0, 0, image=self.imgcans[0].photos, anchor=tkinter.NW)
			for x in self.imgcans[1].points:
				liste = numpy.array(x)
				if len(x) >= 3:
					tris = liste[tri.simplices]
					for z in tris:
						self.imgcans[1].cv_img = cv2.line(self.imgcans[1].cv_img, tuple(z[0]), tuple(z[1]), (255, 0, 0), 1)
						self.imgcans[1].cv_img = cv2.line(self.imgcans[1].cv_img, tuple(z[1]), tuple(z[2]), (255, 0, 0), 1)
						self.imgcans[1].cv_img = cv2.line(self.imgcans[1].cv_img, tuple(z[2]), tuple(z[0]), (255, 0, 0), 1)
						self.imgcans[1].photos = (PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.imgcans[1].cv_img)))
						self.imgcans[1].create_image(0, 0, image=self.imgcans[0].photos, anchor=tkinter.NW)
			self.tris = tri.simplices
		except:
			pass

	def show_morph(self):
		temp = numpy.add(self.liste_org.copy(), numpy.multiply(self.vektor.copy(), self.factor.get()))
		temp1 = [(int(x[0]), int(x[1])) for x in temp.tolist()]
		self.imgcans[0].points[0] = temp1

	def get_nearest_point(self, liste, pos):
		best_dist = 5000000
		point = (5000, 5000)
		for i in liste:
			for x in i:
				dist = abs(math.sqrt(abs(x[0] - pos[0])**2 + abs(x[1] - pos[1])**2))
				if dist < best_dist:
					index = [liste.index(i), i.index(x)]
					point = x
					best_dist = dist
		return index, point
	def onExit(self):
		self.run = False

	def test(self):
		for i in self.imgcans:
			pass




class morph:
	def __init__(self):
		self.img1 = None
		self.liste1 = None
		self.vector = None
		self.factor = 1
		self.imgs = [[], []]
		self.img = []
	def morph_img(self, img1=None, liste=None, vector=None, factor=None, draw_tris=True):
		if img1 is None:
			img1 = self.img1
		if liste is None:
			liste = self.liste1
		if vector is None:
			vector = self.vector
		if factor is None:
			factor = self.factor
		img2 = 255 * numpy.zeros(img1.shape, dtype = img1.dtype)
		liste1 = numpy.array(liste)
		liste2 = numpy.array(numpy.add(liste1, numpy.multiply(factor, vector)), dtype=int)
		tri = Delaunay(liste1)
		tris = tri.simplices
		tris1 = liste1[tris]
		tris2 = liste2[tris]
		for i in range(len(tris1)):
			r1 = cv2.boundingRect(tris1[i])
			r2 = cv2.boundingRect(tris2[i])
			tris1Cropped = []
			tris2Cropped = []
			for x in range (0, 3):
				tris1Cropped.append(((tris1[i][x][0] - r1[0]),(tris1[i][x][1] - r1[1])))
				tris2Cropped.append(((tris2[i][x][0] - r2[0]),(tris2[i][x][1] - r2[1])))

			img1Cropped = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
			warpMat = cv2.getAffineTransform( numpy.float32(tris1Cropped), numpy.float32(tris2Cropped) )
			img2Cropped = cv2.warpAffine( img1Cropped, warpMat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )
			mask = numpy.zeros((r2[3], r2[2], 3), dtype = numpy.float32)
			cv2.fillConvexPoly(mask, numpy.int32(tris2Cropped), (1.0, 1.0, 1.0), 16, 0)

			img2Cropped = img2Cropped * mask

			img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ((1.0, 1.0, 1.0) - mask)
			img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Cropped

		if draw_tris is True:
			for i in tris:
				img2 = cv2.line(img2, tuple(liste2[i[0]]), tuple(liste2[i[1]]), (255, 0, 0), 1)
				img2 = cv2.line(img2, tuple(liste2[i[1]]), tuple(liste2[i[2]]), (255, 0, 0), 1)
				img2 = cv2.line(img2, tuple(liste2[i[2]]), tuple(liste2[i[0]]), (255, 0, 0), 1)
		return img2









def main():
	root = tkinter.Tk()
	root.geometry("1500x1200")
	if fullscreen == True:
		root.attributes('-fullscreen', True)
		# root.bind('<Escape>',lambda e: root.destroy())
	app = window()
	app.open_img(filename="./img/sebifacharbeit.JPG")
	app.open_img(filename="./img/domfacharbeit.JPG")
	app.open_img(filename="./img/domfacharbeit.JPG")
	app.get_points()
	while app.run == True:
		app.update()
	height, width, layers = app.morph.img[0].shape
	size = (width,height)
	out = cv2.VideoWriter('budterrwenig.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
	for i in range(len(app.morph.img)):
		out.write(app.morph.img[i])
	out.release()
main()