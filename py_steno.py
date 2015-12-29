# PROGRAM:   py_steno.py
# AUTHOR:    Rick Elwood
#
# PURPOSE:   py_steno is a Steganography application that will encode()
#            text into the binary data of a PNG image. It accomplishes
#            this by modifying the least significant bits (LSB) in the
#            RGB channels.
#
# NOTES:     Uses the Python Imaging Library - PIL 3.0


from PIL import Image


def tobits(msg):
    """
    :param msg: string to be converted into bits
    :return: Generator that creates a stream of bits
    """
    bits = []
    for i in range(len(msg)):
        uchar = ord(msg[i])
        for j in range(0, 8):
            yield uchar & 1
            uchar = uchar >> 1
    while True:
        yield 0


def encode(msg, image):
    """
    :param msg: String to be encoded.
    :param image: Image object to be embedded with the message
    :return: Image object with message embedded
    """
    bit_count = 0
    byte_val = 0
    msg_bits = tobits(msg)
    for row in range(image.height):
        for col in range(image.width):
            pix = list(image.getpixel((col, row)))
            print(pix)
            for i in range(0, 3):
                if bit_count == 8:
                    bit_count = 0
                    if byte_val == 0:
                        return image
                    else:
                        byte_val = 0
                if next(msg_bits):
                    pix[i] = pix[i] | 1
                    byte_val += (2 ** bit_count)
                else:
                    pix[i] = pix[i] & 0b11111110
                bit_count += 1
            new_img.putpixel((col, row), (pix[0], pix[1], pix[2]))
    return image


def decode(image):
    """
    :param image: Image object to be decoded
    :return: The encoded message as a String
    """
    num = 0
    bytes = 0
    dec_msg = ''
    for row in range(image.height):
        for col in range(image.width):
            pix = list(image.getpixel((col, row)))
            print(pix)
            for i in range(0, 3):
                bit = pix[i] & 0b00000001
                if bytes == 7:
                    if num == 0:
                        return dec_msg
                    else:
                        dec_msg += chr(num)
                        num = 0
                        bytes = 0
                else:
                    num += bit * (2 ** bytes)
                    bytes += 1
    return dec_msg


# Open image to test functions
old_img = Image.open('sloth.PNG')
new_img = old_img.copy()
old_img.close()

# encode secret msg into LSB, decode and recover the message
msg = 'This is a secret message.'
new_image = encode(msg, new_img)
new_img.save('sloth_new.PNG')
dec_msg = decode(new_image)
print(dec_msg)

# close
new_img.close()
