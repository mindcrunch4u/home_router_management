from Crypto.Cipher import AES
import Crypto
import base64

def pkcs7padding(data, block_size=16):
  if type(data) != bytearray and type(data) != bytes:
    raise TypeError("Only support bytearray/bytes !")
  pl = block_size - (len(data) % block_size)
  return data + bytearray([pl for i in range(pl)])

def to_crypto_string(randkey, ivstring, clearpass):
  key = bytes.fromhex(randkey)
  iv  = ivstring.encode('latin-1')
  aes = AES.new(key, AES.MODE_CBC, iv)
  ret = aes.encrypt(pkcs7padding(clearpass.encode()))
  return(bytes(ret).hex())
