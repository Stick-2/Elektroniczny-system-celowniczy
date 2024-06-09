import network
import time
import gc
import usocket as socket
gc.collect()


ssid = 'testAPI'
password = 'abcd'
#def connect_to_wifi(ssid, password):
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

print('Connection successful')
print(ap.ifconfig())
    

#    timeout = 0
    
#    if not wlan.isconnected():  
#        print('Connecting to network...')
#        wlan.connect(ssid, password) 
#
#        while (not wlan.isconnected() and timeout < 5):
#            print(5 - timeout)
##            timeout = timeout +1
#            time.sleep(1)
#            pass  

#    print('Network configuration:', wlan.ifconfig())  


#ssid = 'TP-Link_49F4'
#password = '83337185'

#connect_to_wifi(ssid, password)