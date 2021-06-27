import math
import re, vectorMath
from tkinter import *
import processing

# print(vectorMath.inner_product([2, -3], [1, 4]))
# print(vectorMath.length_vector([1, 4]))

# print(vectorMath.angle_between_two_vector([2, 3, 5], [0, 0, 2]))
# print(vectorMath.angle_between_two_vector([3, 7, 1], [0, 0, 2]))
# print(math.sin(90))


processing.build_vec_mod()


def search():
    t = input1.get()
    # fi = open("corpus/{}.txt".format(t), "r")
    # c = fi.read()
    # resu = Text()
    # resu.insert()
    # fi.close()
    # resu.pack()
    output1.delete(0, END)
    output1.insert(0, t)
    print(t)


root = Tk()
root.title("IR")
root.minsize(600, 300)
lable1 = Label(root, text="inter your query", font=("Arial Bold", 20))
lable1.pack()

input1 = Entry(root, width=75)
input1.pack()

B = Button(root, text="search", font=("Arial Bold", 10), command=search)
B.pack()

output1 = Entry(root, width=50)
output1.pack()

root.mainloop()
