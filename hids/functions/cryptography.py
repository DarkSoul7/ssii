import os, struct, binascii
from Crypto.Cipher import AES
from Crypto import Random


key = binascii.hexlify(b'Integritychecker')


def encrypt_file(infile, out_filename, chunksize=64 * 1024):
    global key

    iv = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, iv)
    file_size = len(infile)
    cont = 0

    with open(out_filename, 'wb') as outfile:
        outfile.write(struct.pack('<Q', file_size))
        outfile.write(iv)

        while True:
            chunk = infile[chunksize*cont:chunksize*(cont+1)]

            chunk = bytes(chunk, encoding='utf-8')

            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)

            outfile.write(encryptor.encrypt(chunk))
            cont += 1


def decrypt_file(in_filename, chunksize=24*1024):
    global key
    outfile = ''

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break

            outfile += decryptor.decrypt(chunk).decode(encoding='utf-8').strip()

    return outfile
