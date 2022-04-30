#!/usr/bin/env python
# coding:UTF-8
"""LSBSteg.py

Usage:
  LSBSteg.py encode -t <type> -i <input> -o <output> -s <secret>
  LSBSteg.py decode -t <type> -i <input> -o <output>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -t, --type=<type>         Type of secret to hide [ image | text | binary ]
  -s,--secret=<secret>      File or text to hide (-f "secret message" or -f secret.bin)
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
"""

import cv2
import docopt
import numpy as np


class SteganographyException(Exception):
    pass


class LSBSteg():
    def __init__(self, im):
        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height
        
        self.maskONEValues = [1,2,4,8,16,32,64,128]
        #Mask used to put one ex:1->00000001, 2->00000010 .. associated with OR bitwise
        # self.maskONE = self.maskONEValues.pop(0) #Will be used to do bitwise operations
        
        self.maskZEROValues = [254,253,251,247,239,223,191,127]
        #Mak used to put zero ex:254->11111110, 253->11111101 .. associated with AND bitwise
        # self.maskZERO = self.maskZEROValues.pop(0)
        
        self.curwidth = 0  # Current width position
        self.curheight = 0 # Current height position
        self.curchan = 0   # Current channel position

        self.counter = 0 # counter used for determining 1337

    def put_binary_value(self, bits): #Put the bits in the image with 1337
        for c in bits:
            val = list(self.image[self.curheight,self.curwidth]) #Get the pixel value as a list
            if self.counter % 4 == 0: # lsb = 1
                if int(c) == 1:
                    val[self.curchan] = int(val[self.curchan]) | self.maskONEValues[0] #OR with maskONE
                else:
                    val[self.curchan] = int(val[self.curchan]) & self.maskZEROValues[0] #AND with maskZERO
            elif self.counter % 4 == 1 or self.counter % 4 == 2: # lsb = 3
                if int(c) == 1:
                    val[self.curchan] = int(val[self.curchan]) | self.maskONEValues[2] #OR with maskONE
                else:
                    val[self.curchan] = int(val[self.curchan]) & self.maskZEROValues[2] #AND with maskZERO
            else: # lsb = 7
                if int(c) == 1:
                    val[self.curchan] = int(val[self.curchan]) | self.maskONEValues[6] #OR with maskONE
                else:
                    val[self.curchan] = int(val[self.curchan]) & self.maskZEROValues[6] #AND with maskZERO
                
            self.image[self.curheight,self.curwidth] = tuple(val)
            self.next_slot() #Move "cursor" to the next space
        
    def next_slot(self):#Move to the next slot were information can be taken or put
        self.counter += 1
        if self.curchan == self.nbchannels-1: #Next Space is the following channel
            self.curchan = 0
            if self.curwidth == self.width-1: #Or the first channel of the next pixel of the same line
                self.curwidth = 0
                if self.curheight == self.height-1:#Or the first channel of the first pixel of the next line
                    raise SteganographyException("No available slot remaining (image filled)")
                else:
                    self.curheight +=1
            else:
                self.curwidth +=1
        else:
            self.curchan +=1

    def read_bit(self): #Read a single bit int the image with 1337
        val = self.image[self.curheight,self.curwidth][self.curchan]
        if self.counter % 4 == 0: # lsb = 1
            val = int(val) & self.maskONEValues[0]
        elif self.counter % 4 == 1 or self.counter % 4 == 2: # lsb = 3
            val = int(val) & self.maskONEValues[2]
        else: # lsb = 7
            val = int(val) & self.maskONEValues[6]
        
        self.next_slot()
        if val > 0:
            return "1"
        else:
            return "0"
    
    def read_byte(self):
        return self.read_bits(8)
    
    def read_bits(self, nb): #Read the given number of bits
        bits = ""
        for i in range(nb):
            bits += self.read_bit()
        return bits

    def byteValue(self, val):
        return self.binary_value(val, 8)
        
    def binary_value(self, val, bitsize): #Return the binary value of an int as a byte
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganographyException("binary value larger than the expected size")
        while len(binval) < bitsize:
            binval = "0"+binval
        return binval

    def encode_text(self, txt):
        l = len(txt)
        binl = self.binary_value(l, 16) #Length coded on 2 bytes so the text size can be up to 65536 bytes long
        self.put_binary_value(binl) #Put text length coded on 4 bytes
        for char in txt: #And put all the chars
            c = ord(char)
            self.put_binary_value(self.byteValue(c))
        return self.image
       
    def decode_text(self):
        ls = self.read_bits(16) #Read the text size in bytes
        l = int(ls,2)
        i = 0
        unhideTxt = ""
        while i < l: #Read all bytes of the text
            tmp = self.read_byte() #So one byte
            i += 1
            unhideTxt += chr(int(tmp,2)) #Every chars concatenated to str
        return unhideTxt

    def encode_image(self, imtohide):
        height, width, nbchannels = imtohide.shape
        if self.width*self.height*self.nbchannels < width*height*nbchannels:
            raise SteganographyException("Carrier image not big enough to hold all the datas to steganography")
        binw = self.binary_value(width, 16) #Width coded on to byte so width up to 65536
        binh = self.binary_value(height, 16)
        binc = self.binary_value(nbchannels, 2) # need 2 bits for channel number
        self.put_binary_value(binw) #Put width
        self.put_binary_value(binh) #Put height
        self.put_binary_value(binc) #Put channels
        for h in range(height): #Iterate the hole image to put every pixel values
            for w in range(width):
                for chan in range(nbchannels):
                    val = imtohide[h,w][chan]
                    self.put_binary_value(self.byteValue(int(val)))
        return self.image

    def decode_image(self):
        width = int(self.read_bits(16),2) #Read 16bits and convert it in int
        height = int(self.read_bits(16),2)
        nbchannels = int(self.read_bits(2), 2)
        unhideimg = np.zeros((height,width,3), np.uint8) #Create an image in which we will put all the pixels read
        for h in range(height):
            for w in range(width):
                for chan in range(nbchannels):
                    val = list(unhideimg[h,w])
                    val[chan] = int(self.read_byte(),2) #Read the value
                    unhideimg[h,w] = tuple(val)
        return unhideimg
    
    def encode_binary(self, data):
        l = len(data)
        if self.width*self.height*self.nbchannels < l+64:
            raise SteganographyException("Carrier image not big enough to hold all the datas to steganography")
        self.put_binary_value(self.binary_value(l, 64))
        for byte in data:
            byte = byte if isinstance(byte, int) else ord(byte) # Compat py2/py3
            self.put_binary_value(self.byteValue(byte))
        return self.image

    def decode_binary(self):
        l = int(self.read_bits(64), 2)
        output = b""
        for i in range(l):
            output += bytearray([int(self.read_byte(),2)])
        return output


def main():
    args = docopt.docopt(__doc__, version="0.2")
    type = args["--type"]
    in_f = args["--in"]
    out_f = args["--out"]
    in_img = cv2.imread(in_f)
    in_img = cv2.cvtColor(in_img, cv2.COLOR_BGR2RGB)
    steg = LSBSteg(in_img)
    lossy_formats = ["jpeg", "jpg"]

    if args['encode']:
        #Handling lossy format
        out_name, out_ext = out_f.split(".")
        if out_ext in lossy_formats:
            out_f = out_name + ".png"
            print("Output file changed to ", out_f)

        if type == "binary":
            data = open(args["--secret"], "rb").read()
            res = steg.encode_binary(data)
            cv2.imwrite(out_f, res)
        elif type == "image":
            secret_img = cv2.imread(args["--secret"])
            secret_img = cv2.cvtColor(secret_img, cv2.COLOR_BGR2RGB)
            new_im = steg.encode_image(secret_img)
            new_im = cv2.cvtColor(new_im, cv2.COLOR_BGR2RGB)
            cv2.imwrite(out_f, new_im)
        elif type == "text":
            img_encoded = steg.encode_text(args["--secret"])
            cv2.imwrite(out_f, img_encoded)
        else:
            print("Incorrect type. Choose either 'image', 'binary', or 'text'")
            exit()

    elif args["decode"]:
        if type == "binary":
            raw = steg.decode_binary()
            with open(out_f, "wb") as f:
                f.write(raw)
        elif type == "image":
            orig_im = steg.decode_image()
            orig_im = cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGB)
            cv2.imwrite(out_f, orig_im)
        elif type == "text":
            with open(out_f, "w") as f:
                f.write(steg.decode_text())
        else:
            print("Incorrect type. Choose either 'image', 'binary', or 'text'")
            exit()


if __name__=="__main__":
    main()