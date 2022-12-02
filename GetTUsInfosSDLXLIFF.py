
#GetTUsInfosSDLXLIFF get TUs info Source, Target, Status, matchrate, Locked, origin to list[[],[]...] 
#By Bill, Fanzhixin

import re

def GetTUsInfosSDLXLIFF(sdlxliffpath):
    #get all TUs's info
    tuinfolist=[]
    #load sdlxliff
    f= open(sdlxliffpath, 'r',encoding='utf-8') 
    sdlxliffstr=f.read()
    f.close()
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
    # get all cxts
    cxttags=cxtdefre.findall(sdlxliffstr)
    cxtdefdic={}
    for cxttag in cxttags:
        pros=cxttag.split('" ')
        cxtcontdic={}
        for pro in pros:
            pro=pro.replace('"','')
            ppair=pro.split('=')
            if ppair[0]=='id':
                cxtid=ppair[1]
            else:
                cxtcontdic[ppair[0]]=ppair[1]
        cxtdefdic[cxtid]=cxtcontdic
            
    #get groups
    groups=groupre.findall(sdlxliffstr)
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
                        tuinfo=[]
                        tuinfo.append(smrk[1])
                        #add source mrk segment to tuinfo
                        idid=smrk[0]
                        #idid is mrk id
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
