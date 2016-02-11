
import os, os.path
import json
import requests

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

jsonfile="SRUdump_GvN_PRB01_07022016.json"
with open(jsonfile) as data_file:
    data = json.load(data_file)

current_dir = os.path.dirname(os.path.realpath(__file__))
outputdir=os.path.join(current_dir, "output")
os.chdir(outputdir)

#bestaande html-files in die dir weggooien voordat er nieuwe naar toe geschreven worden
folder = outputdir
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)


for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcx:recordIdentifier")#PRB01:175094691
    ppn=ppn_long.split(":")[1]#175094691

    title=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:title")
    date=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:created")
    objectholder=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:recordRights") #in welke collectie zit het boek?

    thumbnail=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:thumbnail")
    thumb_url=thumbnail['content']        #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X&role=thumbnail
    thumb_baseurl=thumb_url.split("&")[0] #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X

    contributorlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:contributor")
    auteurlist=[]
    auteurstring=""
    drukkerlist=[]
    drukkerstring=""
    uitgeverlist=[]
    uitgeverstring=""
    if str(contributorlist) != "None":
        if isinstance(contributorlist, dict): # contributorlist = dict
            if contributorlist['dcx:role'] == "uitgever":
                uitgeverstring=str(contributorlist['content'])
            elif contributorlist['dcx:role'] == "drukker":
                drukkerstring=str(contributorlist['content'])
            elif contributorlist['dcx:role'] == "auteur":
                auteurstring=str(contributorlist['content'])
            else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")

        else: # contributorlist = list of dicts
            for dic in contributorlist:
                if dic['dcx:role'] == "uitgever":
                    uitgeverlist.append(dic['content'])
                elif dic['dcx:role'] == "drukker":
                    drukkerlist.append(dic['content'])
                elif dic['dcx:role'] == "auteur":
                    auteurlist.append(dic['content'])
                else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")
            uitgeverstring='; '.join(map(str, uitgeverlist))
            drukkerstring='; '.join(map(str, drukkerlist))
            auteurstring='; '.join(map(str, auteurlist))
            #print(str(auteurstring))

    taglist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:subject")
    tagstring = ""
    #taglist can either be a string or a list[] of strings
    #http://www.decalage.info/en/python/print_list
    if str(taglist) != "None":
        if isinstance(taglist, str): #taglist is een string
            tagstring=str(taglist)
        else: #taglist is een list[] of strings
            tagstring=', '.join(map(str, taglist))

    alternativelist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:alternative")
    alternativestring = ""
    if str(alternativelist) != "None":
        if isinstance(alternativelist, str):
            alternativestring=str(alternativelist)
        else:
            alternativestring=' '.join(map(str, alternativelist))

    descriptionlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:description")
    descriptionstring = ""
    if str(descriptionlist) != "None":
        if isinstance(descriptionlist, str):
            descriptionstring=str(descriptionlist)
        else:
            descriptionstring=' '.join(map(str, descriptionlist))

    annotationlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:annotation")
    annotationstring = ""
    if str(annotationlist) != "None":
        if isinstance(annotationlist, str):
            annotationstring=str(annotationlist)
        else:
            annotationstring='<li>'.join(map(str, annotationlist))

    identifier=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:identifier")
    GvNwebsiteURL=[]
    dci_list=[d['content'] for d in identifier]
    for item in dci_list:
        if str(item).startswith("http"):
            GvNwebsiteURL.append(item)

    ispartoflist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:isPartOf")
    thisParentID=""
    for dic in ispartoflist:
        if dic['xsi:type'] == "parent":
            thisParentID=str(dic['content'])

    thumbnail=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:thumbnail")
    thumb_url=thumbnail['content']


    # a = GvNwebsiteURL[0].split("PRB01:")[1]
    # b = thumb_baseurl.split("PRB01:")[1]
    # if a != b:
    #     print("DIFFERENT!!")
    #     print(a)
    #     print(b+"\n -------")

    HTMLoutputfile = open(ppn+".html", "w")
    HTMLoutputfile.write("<!DOCTYPE html><html><head><title>Beelden voor GVN:PRB01 -- PPN=" +ppn+"</title><meta http-equiv='content-type' content='text/html;charset=utf-8'/></head><body>")
    HTMLoutputfile.write("<style type='text/css'></style>")
    HTMLoutputfile.write("<a href='../index.html'><< Terug naar overzichtspagina</a></style>")
    HTMLoutputfile.write("<h1>Collectie GVN:PRB01 -- PPN= "+ppn+"</h1>")
    HTMLoutputfile.write("<img src='"+thumb_url+"' align='left' vspace='0' hspace='10'/>")
    HTMLoutputfile.write("<h2>"+str(title)+"</h2>")

    if alternativestring:
        HTMLoutputfile.write("<b>Alternatieve titel(s):</b> "+alternativestring+"<br/><br/>")

    HTMLoutputfile.write("<b>Jaar van uitgave:</b> "+str(date)+"<br/><br/>")

    if auteurstring:
        HTMLoutputfile.write("<b>Auteur(s):</b> "+auteurstring+"<br/>")
    if uitgeverstring:
        HTMLoutputfile.write("<b>Plaats/naam uitgever:</b> "+uitgeverstring+"<br/>")
    if drukkerstring:
        HTMLoutputfile.write("<b>Plaats/naam drukker:</b> "+drukkerstring+"<br/>")

    if descriptionstring:
        HTMLoutputfile.write("<br/><b>Beschrijving:</b> "+descriptionstring+"<br/><br/>")
    if annotationstring:
        HTMLoutputfile.write("<b>Annotatie(s):</b><ul><li> "+annotationstring+"</ul>")
    if tagstring:
        HTMLoutputfile.write("<b>Tags:</b> "+tagstring+"<br/><br/>")

    HTMLoutputfile.write("Dit boek is onderdeel van de collectie van de "+str(objectholder)+"</br/><br/>")
    HTMLoutputfile.write("Boek op het GvN: <a href='"+GvNwebsiteURL[0]+"'>"+GvNwebsiteURL[0]+"</a><br/>")
    HTMLoutputfile.write("Beschrijving boek in de KB-catalogus: <a href='http://opc4.kb.nl/PPN?PPN="+ppn+"'>http://opc4.kb.nl/PPN?PPN="+ppn+"</a><br/><br/>")

    rowwidth=5
    maximages=100
    numberofimages =0
    for i in range(0,int(maximages/rowwidth)+1):
        for j in range(1,rowwidth+1):
            #r = requests.head(thumb_url+"&count="+str(rowwidth*i+j)+"&role=page")
            #if int(r.status_code) == 200:
            HTMLoutputfile.write("<img src='"+thumb_url+"&count="+str(rowwidth*i+j)+"&role=page'><a href='"+thumb_baseurl+"&role=page&count=" + str(rowwidth*i+j) + "&role=image&size=large'>Image"+str(j+rowwidth*i)+"</a>")
            numberofimages=numberofimages+1
    HTMLoutputfile.write("<br/><br/>")
    HTMLoutputfile.write("Aantal beelden = "+  str(numberofimages) +"<br/><br/>")

    #find related books based on same parentID
    if thisParentID:
        boekstring="<ol>"
        teller=0
        for boek in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):
            ispartoflist2=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek],"dcterms:isPartOf")
            #print(ispartoflist2)
            parentID=""
            for dic2 in ispartoflist2:
                if dic2['xsi:type'] == "parent":
                    parentID=str(dic2['content'])
            if parentID == thisParentID:
                ppn_lang = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek], "dcx:recordIdentifier")#PRB01:175094691
                ppn2=ppn_lang.split(":")[1]#175094691
                title2=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek], "dc:title")
                thumbnail2=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek],"dcx:thumbnail")
                thumb_url2=thumbnail2['content']
                boekstring = boekstring + "<li><img src='"+thumb_url2+"' width='50' align='center'>&nbsp;&nbsp;<a href='"+ppn2+".html'>"+title2+"</a><br/><br/></li>"
                teller=teller+1
        HTMLoutputfile.write("<b>Alle "+str(teller)+" boeken in de serie "+thisParentID+":</b>"+boekstring+"</ol>")

    HTMLoutputfile.write("</body></html>")
    HTMLoutputfile.close()



# XMLoutputfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
# XMLoutputfile.write("<records>\n")
# #path = os.path.join(images_base_path,images_dir)
# for infile in glob.glob(os.path.join(current_dir, '*.jpg')):
#     picname=infile.lstrip(current_dir)
#     #XMLoutputfile.write("current file is: " + picname)
#     XMLoutputfile.write("   <record>\n")
#     #---Begin variables
#     XMLoutputfile.write("       <accessionnumber>http://opc4.kb.nl/PPN?PPN="+ accessionnumber +"</accessionnumber>\n")
#     XMLoutputfile.write("       <author>"+ author + "</author>\n")
#     XMLoutputfile.write("       <editor>{{Information field|name=Editor|value="+editor+"}}</editor>\n")
#     XMLoutputfile.write("       <printer>{{Information field|name=Printer|value="+printer+"}}</printer>\n")
#     XMLoutputfile.write("       <publisher>{{Information field|name=Publisher|value="+publisher+"}}</publisher>\n")
#     XMLoutputfile.write("       <date>" + date + "</date>\n")
#     XMLoutputfile.write("       <description>Page " + picname.rstrip(".jpg") + " from ''" + title + "'', "  + description +"</description>\n")
#     XMLoutputfile.write("       <dimensions>" + dimensions + "</dimensions>\n")
#     XMLoutputfile.write("       <Institution>" + institution + "</Institution>\n")
#     XMLoutputfile.write("       <medium>"+ medium +"</medium>\n")
#     XMLoutputfile.write("       <notes>" + notes + "</notes>\n")
#     XMLoutputfile.write("       <permission>"+permission+"</permission>\n")
#     XMLoutputfile.write("       <placeofcreation>"+placeofcreation+"</placeofcreation>\n")
#     XMLoutputfile.write("       <source>"+source+"</source>\n")
#     XMLoutputfile.write("       <title>Page " + picname.rstrip(".jpg") + " from ''"+ title +"''</title>\n")
#     XMLoutputfile.write("       <wikidata>" + wikidata + "</wikidata>\n")
#     XMLoutputfile.write("       <GWToolsettitle>"+ title + " (KB) - Page " + picname.rstrip(".jpg") + "</GWToolsettitle>\n")
#     XMLoutputfile.write("       <URLtothemediafile>"+images_base_url+picname+"</URLtothemediafile>\n")
#     #---End variables
#     XMLoutputfile.write("   </record>\n")
# XMLoutputfile.write("</records>\n")

