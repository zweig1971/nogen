#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 14:35:10 2014

@author: zweig
"""

import sys
import getopt

from datetime import datetime

PFAD_HostConf = "/common/usr/dhcp/hosts.conf"
PFAD_NagiosOb = "/etc/nagios/objects/"
PFAD_CpHost   = "myhosts.conf"

detec_sw ="nwt"
detec_pex="pexaria"
detec_scu="scu"
detec_expl="exploder"
detec_vme="vme"

detec_hd_end="PHYSICAL HOSTS"
detec_co ="#"

fileCfg_begin="nodes_"
fileCfg_end=".cfg"

host_struct=["define host {", "use", "host_name", "address", "}"]



# hilfe anzeigen
def help_txt():
    print "usage: nogen [argument] [filename]"
    print "Nodes generator (nogen) generate from the host.conf file a cfg file for nagios"
    print "The standart file name is"+PFAD_NagiosOb+"nodes_xxx.cfg." 
    print "The file must be exist."
    print "arguments are :"
    print "-n  --nwt   create wr-switches nagos file"
    print "-p  --pex   create pexarias nagios file"
    print "-s  --scu   create scu nagios file"
    print "-e  --expl  create exploder nagios file"  
    print "-v  --vme   create vme nagios file"



# durchsucht das host file nach der gesuchten nomenklatur duch und gibt
# die ip zurueck
def extract(detec, PFAD_file):
    sw_found=[]    
    # -- datei öffnen
    try:
        datei = open(PFAD_file, "r")
    except Exception:
        sys.exit ("Cant open host file")

    for line in datei:
        if line.strip(): #leere zeilen entfernen
            if not (line.startswith(detec_co)):     #kommentarzeilen entfernen
                line=line.split(",")                #zeile auftrennen
                name=line[3]                        #an 3ter stelle sollte namen der unit stehen
                if name.rfind(detec_co):            #wenn kommentar vorhanden -> abschneiden    
                    name=name.split(detec_co)[0]
                
                if detec in name:                   #name = gesuchter name
                    sw_found.append(name.rstrip()+";"+line[2].rstrip())        #ip in liste speichen
    return sw_found


# generiert eine aus der ip/name eine structur 
def makehost(unitlist, name_use):
    hostlist=[]
    for line in unitlist:
        name, ip=line.split(";")
        hostlist.append(host_struct[0])
        hostlist.append("\t"+host_struct[1]+"\t\t"+name_use)
        hostlist.append("\t"+host_struct[2]+"\t"+name)
        hostlist.append("\t"+host_struct[3]+"\t\t"+ip)
        hostlist.append("\t"+host_struct[4]+"\n")
    return(hostlist)


# liest ein altes node_xxx.cfg ein und liest header aus
def extract_header(PFAD_file):
    header=[]

    # -- datei öffnen
    try:
        datei = open(PFAD_file, "r")
    except Exception:
        print "Error: Cant open "+PFAD_file
        sys.exit ()
    
    for line in datei:
        if detec_hd_end in line:
            header.append(line.rstrip())
            break
        else:
            header.append(line.rstrip())
  
    datei.close()
    return header        

# ergebnis sichern
def write_file(hostlist, filename):        


    try:
        datei=open(filename,"w")
    except Exception:
        sys.exit ("Cant write result file")
    
    for line in hostlist:
        datei.write(str(line)+"\n")
        
    datei.close()

#--------------
# -------------------------- main ------------------------------   
#--------------

FileOutName = "None"
myhostlist=[]
todo ="-h"

# arguments einlesen
try:
    myopts, args = getopt.getopt(sys.argv[1:],"hnpsev",["help","nwt","pex","scu","expl","vme","firm-mon","net-mon","wr-mon","all","xxx"])
except getopt.GetoptError, err:
    print str(err)
    help_txt()   
    sys.exit(2)

for o, arg in myopts:

    if o in ("-h","--help"):
        help_txt()   
        sys.exit(2)
    elif o in ("-n","--nwt"):
        todo=detec_sw
        FileOutName=args
    elif o in ("-p","--pex"):
        todo=detec_pex
        FileOutName=args
    elif o in ("-s","--scu"):
        todo=detec_scu
        FileOutName=args
    elif o in ("-e","--expl"):
        todo=detec_expl
        FileOutName=args
    elif o in ("-v","--vme"):
        todo=detec_vme
        FileOutName=args
    else: 
        help_txt()



if todo == "-h":
        help_txt()
        sys.exit(2)

#file name generieren
try:
    filename=FileOutName[0]
except:
    filename = fileCfg_begin+todo+fileCfg_end
    filename=PFAD_NagiosOb+filename

# host file durchsuchen & informationen extrahieren
unitlist=extract(todo, PFAD_HostConf)

# host liste generieren
host_list=makehost(unitlist, todo)

# header der vorhandenen datei einlesen
header= extract_header(filename)

# datum & uhrzeit
header.append("### Generated on "+str(datetime.now())+"\n")

# ergebnisse zusammenfuehren
for line in header:
    myhostlist.append(line)
    
for line in host_list:
    myhostlist.append(line)

# file speichern
write_file(myhostlist, filename)

  
    
    