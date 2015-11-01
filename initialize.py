#!/usr/bin/python                                                
import sys, os                                                   
                                                                 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))            
print "BASE_DIR : %s" % BASE_DIR                                 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hexactf.settings") 

from django.conf import settings                                 
from gameboard.models import Entries, SolverListModel, Categories
from django.contrib.auth.models import User

print "[+] Add Category..."
try:
	print "[+] Add Forensic Category"
	c = Categories(title="Forensic", color="black")
	c.save()
	print "[+] Success"
except:
	print "[!] Fail!"
try:
	print "[+] Add System Category"
	c = Categories(title="System", color="red")
	c.save()
	print "[+] Success"
except:
	print "[!] Fail!"
try:
	print "[+] Add Web Category"
	c = Categories(title="Web", color="blue")
	c.save()
	print "[+] Success"
except:
	print "[!] Fail!"

try:
	print "[+] Add Reversing Category"
	c = Categories(title="Reversing", color="teal")
	c.save()
	print "[+] Success"
except:
	print "[!] Fail!"

try:
	print "[+] Add Misc Category"
	c = Categories(title="Misc", color="purple")
	c.save()
	print "[+] Success"
except:
	print "[!] Fail!"

try:
        print "[+] Add Crypto Category"
        c = Categories(title="Crypto", color="yellow")
        c.save()
        print "[+] Success"
except:
        print "[!] Fail!"

