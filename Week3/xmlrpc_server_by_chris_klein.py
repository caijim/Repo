import SimpleXMLRPCServer
import sys
from scipy import *
from matplotlib import pyplot 

class Some_Class_We_Want_Remotely_Accessible:
    def image_distort_1(self, im_list):
        """
        Multiply each pixel value by 0.5
        """
        # Multiply each pixel value by 0.5
        im_array = array(im_list)
        distorted_im_array = im_array*0.5
        pyplot.imshow(distorted_im_array[::-1])
        pyplot.savefig("server_distorted.png")
        distorted_im_list = distorted_im_array.tolist()
        return distorted_im_list
    
    def image_distort_2(self, im_list):
        """
        Move bottom third of rows to the top
        """
        im_array = array(im_list)
        distorted_im_array = append(im_array[shape(im_array)[0]/3:], 
            im_array[:shape(im_array)[0]/3], 0)
        pyplot.imshow(distorted_im_array[::-1])
        pyplot.savefig("server_distorted.png")
        distorted_im_list = distorted_im_array.tolist()
        return distorted_im_list
    
    def image_distort_3(self, im_list):
        """
        Subsample the image by 2 and then repeat it out in a 2x2 new image 
        called the "add_image". Then add this to the original image.
        """
        im_array = array(im_list)
        sub_im = im_array[::2, ::2]
        sub_im2 = append(sub_im, sub_im, 0)
        add_array = append(sub_im2, sub_im2, 1)
        distorted_im_array = im_array + add_array
        pyplot.imshow(distorted_im_array[::-1])
        pyplot.savefig("server_distorted.png")
        distorted_im_list = distorted_im_array.tolist()
        return distorted_im_list

host = ""
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 5020
server = SimpleXMLRPCServer.SimpleXMLRPCServer((host, port), allow_none=True)
server.register_instance(Some_Class_We_Want_Remotely_Accessible())
server.register_multicall_functions()
server.register_introspection_functions()
print "XMLRPC Server is starting at:", host, port
server.serve_forever()