import wx,  urllib2, YahooParser
from numpy import array,append, shape
import matplotlib, os
# We want matplotlib to use a wxPython backend
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib import pyplot as plt
from enthought.traits.api import Any, Instance
from enthought.traits.ui.wx.editor import Editor
from enthought.traits.ui.basic_editor_factory import BasicEditorFactory
from enthought.traits.api import HasTraits, Str, CInt, Enum, Button
from enthought.traits.ui.api import View, Item



class _MPLFigureEditor(Editor):
    scrollable  = True
    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()
    def update_editor(self):
        pass
    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # The panel lets us add additional controls.
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        # matplotlib commands to create a canvas
        mpl_control = FigureCanvas(panel, -1, self.value)
        sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
        toolbar = NavigationToolbar2Wx(mpl_control)
        sizer.Add(toolbar, 0, wx.EXPAND)
        self.value.canvas.SetMinSize((10,10))
        return panel

class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor

#The box for the query
#Click 'query' to search
class ImageLookup(HasTraits):
    query = Str
    lookup_url = Str
    lookup = Button()
    view = View('query', Item('lookup', show_label=False),)
    def _lookup_fired(self):
        #trigger websearch
        self.lookup_url = self.query

#Lists what url we are grabbing the image from
class UrlBox(HasTraits):
    url = Str
    view = View(Item('url', style='readonly', show_label=False))
    def showurl(self, value):
        self.url = value

#Buttons for altering the picture
#flip image, move 1/3 of image , double pixels
class AlterPicture(HasTraits):
    Flip = Button()
    MovePixels = Button()
    DoublePixels = Button()
    view = View(Item('Flip', show_label=False), Item('MovePixels', show_label=False), Item('DoublePixels', show_label=False))
    flip = CInt
    move = CInt
    double = CInt
    def _Flip_fired(self):
        self.flip+=1
    def _MovePixels_fired(self):
        self.move+=1
    def _DoublePixels_fired(self):
        self.double+=1

#Image show-er (not shower)
#Refreshes the canvas after each search, alter
#Loads up stock solar panel image
class ImageShower(HasTraits):
    url = Str
    figure = Instance(Figure, ())
    axes = None
    image_file = None
    im = None
    view = View(Item('figure', editor=MPLFigureEditor(),
                            show_label=False),
                    width=400,
                    height=300,
                    resizable=True)
    def __init__(self):
        super(ImageShower, self).__init__()
        self.axes = self.figure.add_subplot(111)
        img = plt.imread("image.jpg")
        self.image_file = img[::-1]
        self.im = self.axes.imshow(img[::-1])

#uses the yahoo search GET api
#tries to open pages from the resultset, stops at the first available one
    def loadimage(self, query=None):
        yahoo = YahooParser.LookupImage(query)
        urls = yahoo.lookUp()
        for item in urls['ResultSet']['Result']:
            if 'Url' in item:
                try:
                    raw = urllib2.urlopen(item['Url']).read() 
                    self.url =item['Url']
                    name = self.url.split('/')[-1]
                    fpath = os.path.join(os.path.abspath('.'), 'images',self.url.split('/')[-1])
                    file = open(fpath,"w")
                    file.write(raw)
                    file.close()
                    img = plt.imread(fpath)[::-1]
                    self.image_file = array(img)
                    self.im.set_data(img)
                    self.figure.canvas.draw()
                    break
                except IndexError:  pass
    
    def image_distort_1(self):
        """
        Flip image upside down
        """
        im_array= self.image_file
        distorted_im_array = im_array[::-1]
        self.im.set_data(distorted_im_array)
        self.image_file = distorted_im_array
        self.figure.canvas.draw()
    
    def image_distort_2(self, value):
        """
        Move bottom third of rows to the top
        """
        im_array = self.image_file
        distorted_im_array = append(im_array[shape(im_array)[0]/3:], 
            im_array[:shape(im_array)[0]/3], 0)
        self.im.set_data(distorted_im_array)
        self.image_file = distorted_im_array
        self.figure.canvas.draw()
    
    def image_distort_3(self, value):
        """
        # Multiply each pixel value by 2
        """
        im_array = self.image_file
        distorted_im_array = array(im_array*int(2))
        self.image_file = distorted_im_array
        self.im.set_data(distorted_im_array )
        self.figure.canvas.draw()

class Container(HasTraits):
    shower = Instance(ImageShower)
    page_url = Instance(UrlBox)
    lookup = Instance(ImageLookup)
    alter = Instance(AlterPicture)
    view = View(Item('lookup',style = 'custom',show_label=True,),Item('page_url',style = 'custom',show_label=True,), Item('shower',style = 'custom', show_label = False,), Item('alter',style = 'custom', show_label = False,),width = 800, height = 600, resizable = True)

if __name__ == "__main__":
    # Create a window to demo the editor
    img = ImageLookup()
    urlbox = UrlBox()
    shower = ImageShower()
    alter = AlterPicture()
#Refresh canvas after we look up an image
    img.on_trait_change(shower.loadimage, name='lookup_url') 
#Refresh canvas after altering an image
    alter.on_trait_change(shower.image_distort_1, name='flip')
    alter.on_trait_change(shower.image_distort_2, name='move')
    alter.on_trait_change(shower.image_distort_3, name='double')
#Change url box after looking something up
    shower.on_trait_change(urlbox.showurl, name='url')
   
    container = Container(lookup = img,page_url=urlbox, shower = shower, alter = alter)
    container.configure_traits()
