
#This py can ananlyse the sdlxliff files, and collect TUs info in List like:
#[
#['SourceFilepath','Segment ID','Source', 'Source Language Code(like,en-US)','Target','Target Language Code(like,zh-CN)','Status', {id dics}, 'Origin', 'original-from', 'Match Rate', 'Locked'],
#[....],
#[....],
#.
#.
#.
#[....]
#]

#By Bill, Fanzhixin

import re
def gtagreplace(sdlxliffstr):
    tagre=re.compile('<tag id="([^><]*?)">(.*?)</tag>',re.S)
    tags=tagre.findall(sdlxliffstr)
    #print(tags)
    subtags=[]
    suptags=[]
    for tag in tags:
        if 'Superscript' in tag[1]:
            suptags.append(tag[0])
        if 'Subscript' in tag[1]:
            subtags.append(tag[0])
    for tag in suptags:
        sdlxliffstr = re.sub('<g id="'+tag+'"[^><]*?>([^><]*?)</g>','<SUP>\\1</SUP>',sdlxliffstr)
    for tag in subtags:
        sdlxliffstr = re.sub('<g id="'+tag+'"[^><]*?>([^><]*?)</g>','<SUB>\\1</SUB>',sdlxliffstr)
    sdlxliffstr = re.sub('<g [^<>]*?>', '', sdlxliffstr)  # 删除 <g> 标签和其属性
    sdlxliffstr = sdlxliffstr.replace('</g>','')  # 删除 </g> 标签
    return sdlxliffstr

def GetTUsInfosSDLXLIFF(sdlxliffpath):
    #get all TUs's info
    tuinfolist=[]
    #load sdlxliff
    f= open(sdlxliffpath, 'r',encoding='utf-8') 
    sdlxliffstr=f.read()
    f.close()
    sdlxliffstr=gtagreplace(sdlxliffstr)
    #define x tag re
    #xre=re.compile('<x [^<>]*?>',re.S)
    # remove all x tag
    #sdlxliffstr=re.sub(xre,' ',sdlxliffstr)
    #define trackchange re
    sdldelre=re.compile('<mrk mtype="x-sdl-deleted" ([^<>]*?)>(.*?)</mrk>',re.S)
    sdladdre=re.compile('<mrk mtype="x-sdl-added" ([^<>]*?)>(.*?)</mrk>',re.S)
    #difine comment change re
    sdlcommre=re.compile('<mrk mtype="x-sdl-comment" ([^<>]*?)>(.*?)</mrk>',re.S)
    sdllocationre=re.compile('<mrk mtype="x-sdl-location" [^<>]*?>',re.S)
    #remove x-sdl-location mrk
    sdlxliffstr=re.sub(sdllocationre,'',sdlxliffstr)
    #convert trachange mrk to xsdl elements
    
    sdlxliffstr=re.sub(sdldelre,'<xsdldeleted \\1>\\2</xsdldeleted>',sdlxliffstr)
    sdlxliffstr=re.sub(sdladdre,'<xsdladded \\1>\\2</xsdladded>',sdlxliffstr)
    #convert comment mrk to xsdl emements
    commentmatches=sdlcommre.findall(sdlxliffstr)
    while(len(commentmatches)>0):
        sdlxliffstr=re.sub(sdlcommre,'<xsdlcomment \\1>\\2</xsdlcomment>',sdlxliffstr)
        commentmatches=sdlcommre.findall(sdlxliffstr)
    #default rex file 
    filere=re.compile('<file [^><]*?original="([^><]*?)"[^><]*?>(.*?)</file>',re.S)
    #default rex Source lanuage
    Sourcelangre=re.compile('source-language="([^<>]*?)"',re.S)
    #default rex target lanuage
    targetlangre=re.compile('target-language="([^<>]*?)"',re.S)
    # default rex TUs
    transunitre=re.compile('<trans-unit [^<>]*?>.*?</trans-unit>',re.S)
    # default rex source segments
    source_segs4match=re.compile('<seg-source>(.*?)</seg-source>',re.S)
    # default rex target segments
    target4match=re.compile('<target>(.*?)</target>',re.S)
    # default rex mrk segment
    mrk4match=re.compile('<mrk mtype="seg" mid="([^<>]*?)">(.*?)</mrk>',re.S)
    #default rex emtymrk segment
    mrkem4match=re.compile('(<mrk mtype="seg" [^<>]*?)/>',re.S)
    #replace empty mrk from <mrk/> to <mrk></mrk>
    sdlxliffstr=re.sub(mrkem4match,r'\1></mrk>',sdlxliffstr)
    #default rex group
    groupre=re.compile('<group>.*?</group>',re.S)
    #default rex structure
    cxtre=re.compile('<sdl:cxt [^<>]*?id="([^<>]*?)"',re.S)
    #default rex structure def-cxts
    cxtdefre=re.compile('<cxt-def ([^<>]*?)>',re.S)
    sdlcxtdefre=re.compile('<sdl:cxt-def ([^<>]*?)>',re.S)
    # get all cxts
    #get target lanuage
    sourcelanmatchs=Sourcelangre.findall(sdlxliffstr)
    if len(sourcelanmatchs)>0:
        sourcelan=sourcelanmatchs[0]
    else:
        sourcelan=''
    #get target lanuage
    targetlanmatchs=targetlangre.findall(sdlxliffstr)
    if len(targetlanmatchs)>0:
        targetlan=targetlanmatchs[0]
    else:
        targetlan=''
    #get File path in sdlxliff
    filestrs=filere.findall(sdlxliffstr)
    for filestr in filestrs:
    #get groups
        oringalpath=filestr[0]
        cxttags=cxtdefre.findall(filestr[1])
        if len(cxttags)==0:
            cxttags=sdlcxtdefre.findall(filestr[1])
        cxtdefdic={}
        #print(cxttags)
        #print(sdlxliffpath)
        #print(filestr)
        for cxttag in cxttags:
            pros=cxttag.split('" ')
            cxtcontdic={}
            for pro in pros:
                pro=pro.replace('"','')
                ppair=pro.split('=')
                #print(ppair)
                if ppair[0]=='id':
                    cxtid=ppair[1]
                else:
                    #print(sdlxliffpath)
                    #print(ppair)
                    if len(ppair)>1:
                        cxtcontdic[ppair[0]]=ppair[1]
            cxtdefdic[cxtid]=cxtcontdic
        #print(cxtdefdic)
        groups=groupre.findall(filestr[1])
        for group in groups:
            #get cxtidd
            cxtidd=cxtre.findall(group)[0]
            
            # get TUs list
            transunits=transunitre.findall(group)
            for transunit in transunits:
                source_segs=source_segs4match.findall(transunit)
                #get source segments list
                target_segs=target4match.findall(transunit)
                #get target segments list
                for source_seg in source_segs:
                    #loop source segments
                    smrks=mrk4match.findall(source_seg)
                    #get mrks in source segment return Tuples list
                    #print(smrks)
                    if len(smrks)>0:
                        #if more than one mrk
                        for smrk in smrks:
                            #loop TUs
                            idid=smrk[0]
                            #idid is mrk id
                            tuinfo=[]
                            tuinfo.append(oringalpath)
                            #add orginal file path
                            tuinfo.append(idid)
                            #add the segment id
                            tuinfo.append(smrk[1])
                            #add source mrk segment to tuinfo
                            tuinfo.append(sourcelan)
                            #add source language code
                            
                            mrkid4match=re.compile('<mrk mtype="seg" mid="'+idid+'">(.*?)</mrk>',re.S)
                            #define rex mrk with id
                            segdefmatch=re.compile('<sdl:seg id="'+idid+'"([^<>]*?)>',re.S)
                            #define rex splited mrk with id
                            segsplitsdefmatch=re.compile('<sdl:seg id="'+idid.replace('_x0020_',' ')+'"([^<>]*?)>',re.S)
                            #define rex sdl:seg properties with id
                            confmatch=re.compile('conf="([^<>]*?)"')
                            #define rex status
                            originmatch=re.compile('origin="([^<>]*?)"')
                            #define rex translation from
                            originsystemmatch=re.compile('origin-system="([^<>]*?)"')
                            #define rex translation system from 
                            percentmatch=re.compile('percent="([^<>]*?)"')
                            #define rex matchrate
                            lockedmatch=re.compile('locked="([^<>]*?)"')
                            #define rex locked status
                            
                            if len(target_segs)>0:
                                targetmrks=mrkid4match.findall(target_segs[0])
                                if len(targetmrks)>0:
                                    tuinfo.append(targetmrks[0])
                            else:
                                tuinfo.append('')
                            #add target language
                            tuinfo.append(targetlan)
                            #if found target mrk according idid, add to tuinfo list,if not found add the '' to target mrk
                            
                            segdefs=segdefmatch.findall(transunit)
                            #get segment status according idid
                            # if have status, add to tuinof, or not add ""
                            if len(segdefs)>0:
                                confv=confmatch.findall(segdefs[0])
                                if len(confv)>0:
                                    tuinfo.append(confv[0])
                                else:
                                    tuinfo.append('')
                                # if have origin, add to tuinof, or not add ""
                                # add structrue info
                                #print(sdlxliffpath)
                                #print(cxtidd)
                                #print(cxtdefdic)
                                if cxtidd not in cxtdefdic:
                                    
                                    tuinfo.append(list(cxtdefdic)[-1])
                                else:
                                    tuinfo.append(cxtdefdic[cxtidd])
                                originv=originmatch.findall(segdefs[0])
                                if len(originv)>0:
                                    tuinfo.append(originv[0])
                                else:
                                    tuinfo.append('New')
                                # if have origin system, add to tuinof, or not add ""
                                originsystemv=originsystemmatch.findall(segdefs[0])
                                if len(originsystemv)>0:
                                    tuinfo.append(originsystemv[0])
                                else:
                                    tuinfo.append('')
                                    # if have matchrate, add to tuinof, or not add ""
                                percentv=percentmatch.findall(segdefs[0])
                                if len(percentv)>0:
                                    tuinfo.append(percentv[0])
                                else:
                                    tuinfo.append('')
                                    # if have locked, add to tuinof, or not add ""
                                lockedfv=lockedmatch.findall(segdefs[0])
                                if len(lockedfv)>0:
                                    tuinfo.append(lockedfv[0])
                                else:
                                    tuinfo.append('')
                                #add tuifo list to tuinfolist
                                tuinfolist.append(tuinfo)
                            if '_x0020_' in idid:
                                segdefs=segsplitsdefmatch.findall(transunit)
                                #get splited segment status according idid
                                # if have status, add to tuinof, or not add ""
                                if len(segdefs)>0:
                                    confv=confmatch.findall(segdefs[0])
                                    if len(confv)>0:
                                        tuinfo.append(confv[0])
                                    else:
                                        tuinfo.append('')
                                    # if have origin, add to tuinof, or not add ""
                                    if cxtidd not in cxtdefdic:
                                    
                                        tuinfo.append(list(cxtdefdic)[-1])
                                    else:
                                        tuinfo.append(cxtdefdic[cxtidd])
                                    originv=originmatch.findall(segdefs[0])
                                    if len(originv)>0:
                                        tuinfo.append(originv[0])
                                    else:
                                        tuinfo.append('')
                                    # if have origin system, add to tuinof, or not add ""
                                    originsystemv=originsystemmatch.findall(segdefs[0])
                                    if len(originsystemv)>0:
                                        tuinfo.append(originsystemv[0])
                                    else:
                                        tuinfo.append('')
                                        # if have matchrate, add to tuinof, or not add ""
                                    percentv=percentmatch.findall(segdefs[0])
                                    if len(percentv)>0:
                                        tuinfo.append(percentv[0])
                                    else:
                                        tuinfo.append('')
                                        # if have locked, add to tuinof, or not add ""
                                    lockedfv=lockedmatch.findall(segdefs[0])
                                    if len(lockedfv)>0:
                                        tuinfo.append(lockedfv[0])
                                    else:
                                        tuinfo.append('')
                                    #add tuifo list to tuinfolist
                                    tuinfolist.append(tuinfo)
                    

    return(tuinfolist)   
if __name__ == '__main__':
    
    #sublpulist=['GetTUsInfosSDLXLIFF.py','ConvertSDLXLIFFtoXLSX.py','subfolder\IFxResourcesDG.resx']
    #print(gitpull(gitlocal,'2023-02-09',sublpulist,'updateReport.csv'))
    #print(Amendsplit(r'c:\RA\FT_Optix\UI\20230314\ToAlign\ide_translations_ftoptixstudio.fr.ts.sdlxliff_pre - Copy - Copy - Copy.back.sdlxliff',False))
    print(GetTUsInfosSDLXLIFF(r'd:\PS\KMF\Work\KMF\QA\低错样例\tocheck\错误文件 19_【3-2-rs原料药】s2-生产-en_QH_WY.docx.sdlxliff'))
