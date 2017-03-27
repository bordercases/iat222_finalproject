import xml.etree.ElementTree as ET
from PIL import Image
from itertools import product

__PIXEL_DIM__ = 15
__IMAGE__ = "../static/McFogg.png"
__DOM__ = "newMcfogg.xml"

with open(__DOM__, "w") as newmMcfoggDom:
    newmMcfoggDom.write("<div class='top'></div>")


class McFogg:
    # memeMap is a tuple for location and source for image
    memeMap = []

    def __init__(self, imgSrc):
        # take image and convert it to color array
        # populate active array with null values equivalent to being inactive
        self.image = Image.open(imgSrc)
        # self.image = self.image.resize((int(self.image.width/__PIXEL_DIM__), int(self.image.height/__PIXEL_DIM__)))
        # pixel array
        pixelArray = self.image.load()
        self.pixelColors = [pixelArray[x, y] for x, y in product(range(0, self.image.width, 15), range(0, self.image.height, 15))]

        # generate color array
        self.color = list(self.image.getdata())

        # generate filled array
        # keeps record of which pixels are hidden and which are not
        self.filled = [False] * (self.image.width + self.image.height)

        # tree root element (returns element)
        self.tree = ET.parse(__DOM__)
        self.root = self.tree.getroot()


    def getRoot(self):
        return self.root

    def getCols(self):
        """
        XPath Query: * (I'm currently assuming it's one level deep only)
        """
        return self.root.findall('*')

    def getRows(self):
        """
        XPath Query: *//
        """
        return self.root.findall('*//')

    def getDomAsString(self):
        return ET.tostring(self.root, "unicode")

    def check(self):
        assert(len(self.filled) == self.image.height + self.image.width)
        assert(len(self.color) == len(self.filled))
        activePixels = filter(self.filled)
        assert(len(memeMap) == filter(self.filled))

    def isPixelHue(self, activeValue):
        return not self.isTransparent(activeValue)

    def isPixelTransparent(self, activeValue):
        return activeValue == 0,0,0,0

    def isElementHidden(self, divElement):
        pass

    def gridifyImage(self):

        # geometry of grid
        """
        To avoid hardcoding I'm going to be parameterizing many of the dimensions used for the color, filled, and memeMap arrays here, but
        as the concrete case is the McFogg, I'll be using our current image as an example of the mechanics.

        Our image is currently 1005 x 1005 dot pixels. This image is thus square. However, each pixel of the image *relative to itself* is
        in fact 15 x 15 dots. This parameter, which must be set as a constant in the codebase (as it is not detectable without using machinery that we do not have), acts as the measurement for each pixel of the image in terms of dots.

        We then end up with a situation where we can now detect each pixel in consecution if we iterate over the array in a 15x15 fashion. (Can we assert this as true?). And finally we can determine the size of a div which may be used to redraw and overlap the image.

        The acid test here will be as follows:
        * If we can draw McFogg entirely with HTML elements, taken off of an original root image, we win.
        * Then, if we can redraw random parts of McFogg, we win.
        * If we can replace McFogg parts with images, we win.
        * If we can replace McFogg with images and color overlays, we win.

        Pray to the gods that this is performant.
        """

        # we need to set up columns, pixels are forced down to corresponding row
        # only way to get the effect I'm looking for in the DOM is nesting. so we are going to establish columns as one large structure, with consecutive rows inside of it.

        # semantics choices
        # use divs almost exclusively
        # use tables
        # use lists with decked out css
        # we'll go with divs
        # * column div: has length of image and width of pixel
        # * row div: has length of pixel and width of pixel
        # * content is a link and an image. for now ignore.

        # column element for xml tree
        """
        col = ET.Element.SubElement(root, "div", {"width": __PIXEL_DIM__, "length": image.height})
        """

        # row element for xml tree
        """
        row = ET.Element.SubElement(myCol, "div", {"width": __PIXEL_DIM__, "length": __PIXEL_DIM__})
        """

        i = 0
        for c in range(0, self.image.height, __PIXEL_DIM__):
            style = 'width:'+str(__PIXEL_DIM__)+"px"+';'+'height: '+str(self.image.height)+"px"+';'+'float:'+'left'+';'+'z-index:-1'+';'
            newCol = ET.Element("div", {"class": "col", "style": style})
            newCol.text = " "
            self.tree.getroot().append(newCol)

            for r in range(0, self.image.width, __PIXEL_DIM__):

                # we should be able to replicate the pixelated image like this, but enlarged
                # return html elements with the data all matched up to what it ought to be
                    # Color set -> div background
                    # Link set  -> a href
                    # Image source set -> img src
                # Coordinates
                    # Row -> div styles/class?
                    # Column -> div styles/class?

                # TODO: "Check-if-filled" system
                rgba = self.colorEncode(self.pixelColors[i])
                data = { "background-color": rgba, "link":"", "image":"", "visibility": "visible"}

                style = 'width:'+str(__PIXEL_DIM__)+"px"+';'+'height: '+str(__PIXEL_DIM__)+"px"+';'+'background-color:'+data["background-color"]+';'+'visibility:'+data["visibility"]+';'+'float:'+'down'+';'

                newRow = ET.SubElement(newCol, "div", {"class": "row", "style": style})
                newRow.text = " "
                newLink = ET.SubElement(newRow, "a", {"href": data["link"]})
                newImg = ET.SubElement(newLink, "img", {"src": data["image"]})

                i += 1

        print("iteration count", i)
        # columns are essentially invisible, they must be filled up with rows
        # TODO: does this upset the counting? not if we just handle rows directly? figure this out
          # in the end it's only row elements that get colors, not columns.
          # we skip over the parts of the flattened list that involve columns
          # columns occur every image.width times, starting from 0.

    def colorEncode(self, cP):
        # destruct color pixel from 'color' var into components
        r, g, b, a = cP[0], cP[1], cP[2], cP[3]
        # this is the format css likes for colors with alpha channels
        return "rgba("+str(r)+","+str(g)+","+str(b)+","+str(a)+")"

    def insertImage(self, imgLink, pixelCoords):
        pass

mf = McFogg(__IMAGE__)
mf.gridifyImage()
#print(mf.getDomAsString())
file = open("mcfogg.html", "w")
file.write("<html>"+mf.getDomAsString()+"</html>")
file.close()
#print(mf.pixelColors)
print(len(mf.color), len(mf.pixelColors))
print(len(mf.color) / len(mf.pixelColors), ((1005**2) / (15**2)))
