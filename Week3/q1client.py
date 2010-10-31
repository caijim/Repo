import xmlrpclib, sys
import matplotlib.pyplot as plt
from numpy.core.multiarray import array
from numpy.lib.function_base import append
import numpy as np

host, port = "", 5020
server = xmlrpclib.ServerProxy("http://%s:%d" % (host, port))
#available_methods = server.system.listMethods() 
#print "Available methods from server:"
#print server.system.listMethods()
#print server.system.methodHelp('image_distort_1')
#print server.system.methodHelp('image_distort_2')
#print server.system.methodHelp('image_distort_3')

#reading in stock moonlanding image
moon = plt.imread('moonlanding.png')
moon_list = moon.tolist()

trans1 = server.image_distort_1(moon_list)
trans2 =server.image_distort_2(trans1)
final =server.image_distort_3(trans2)


#Multiply pixel values by 2
def reverse_1(input):
    input = array(input)*2
    return input
#Move 1/3 image around twice to end up at original image
def reverse_2(input):
    try:
        input =  server.image_distort_2(server.image_distort_2(input.tolist()))
    except AttributeError:
        input =  server.image_distort_2(server.image_distort_2(input))
    return input

def reverse_3(input, original):
    original= array(original)
#ideally, we would have a recursive function that 
#would calculate four indices based on the top left corner
#and then calculate the rest, but I take the simple route 
    noise = input - original
    smallsquare = noise[:noise.shape[0]/float(2),:noise.shape[1]/float(2)]
    byrow = append(smallsquare, smallsquare, 0)
    bycolumnrow = append(byrow, byrow, 1)
    clean = input-bycolumnrow
    return clean

plt.imshow(reverse_3(reverse_1(reverse_2(final)),moon_list))
plt.gray()
plt.show()

