#!/usr/bin/env python3
from  ctypes import *


def crash():

#   i = ctypes.c_char('a')
   i = c_char(b'a')
#   j = ctypes.pointer(i)
   j = pointer(i)
   c = 0

   while True:
      j[c] = b'a'
      c += 1
   j
   return

crash()
  
   
