import json
import os, os.path
from bs4 import BeautifulSoup

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

outputdirname="output"
current_dir = os.path.dirname(os.path.realpath(__file__))
outputdir=os.path.join(current_dir, outputdirname)

jsonfile="SRUdump_GvN_PRB01_07022016.json"
with open(jsonfile) as data_file:
    data = json.load(data_file)

coll_titel="Prentenboeken van 1810 tot 1950"
coll_home = "http://www.geheugenvannederland.nl/?/nl/collecties/prentenboeken_van_1810_tot_1950"

file="index.html"

HTMLoutputfile = open(file, "w")
HTMLoutputfile.write("<!DOCTYPE html><html><head><title>Titels in GVN:"+coll_titel+"</title><meta http-equiv='content-type' content='text/html;charset=utf-8'/></head><body>")
HTMLoutputfile.write("<style type='text/css'></style>")
HTMLoutputfile.write("<h1>Titels in <a href='"+coll_home+"'>GVN:"+coll_titel+"</a></h1>")
HTMLoutputfile.write("Totaal aantal titels = "+ str(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"]))+"<br/>")
HTMLoutputfile.write("<ol>")

for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcx:recordIdentifier")#PRB01:175094691
    ppn=ppn_long.split(":")[1] #175094691
    titel=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:title")
    titel_kort = titel.split(" / ")[0]
    date=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:created")
    thumbnail=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:thumbnail")
    thumb_url=thumbnail['content']  #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X&role=thumbnail

    HTMLoutputfile.write("<li><img src='"+thumb_url+"' width='50' align='center'/>&nbsp;&nbsp;<a href='"+outputdirname+"/"+ppn+".html'>"+str(titel_kort) +"</a>" + " (" + str(date) + ")<br/><br/></li>")

HTMLoutputfile.write("</ol>")
HTMLoutputfile.write("</body></html>")
HTMLoutputfile.close()

# make html code beautiful // indent and stuff
inputfile = open(file, "r")
soup = BeautifulSoup(inputfile, 'html.parser')
inputfile.close()
outputfile = open(file, "w")
outputfile.write(soup.prettify())
outputfile.close()

