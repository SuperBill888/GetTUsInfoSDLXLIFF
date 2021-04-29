
#GetTUsInfosSDLXLIFF get TUs info Source, Target, Status, matchrate, Locked, origin to list[[],[]...] 
#By Bill, Fanzhixin

import re

def GetTUsInfosSDLXLIFF(sdlxliffpath):
    tuinfolist=[]
    f= open(sdlxliffpath, 'r',encoding='utf-8') 
    sdlxliffstr=f.read()
    f.close()
    transunitre=re.compile('<trans-unit [^<>]*?>.*?</trans-unit>',re.S)
    source_segs4match=re.compile('<seg-source>(.*?)</seg-source>',re.S)
    target4match=re.compile('<target>(.*?)</target>',re.S)
    mrk4match=re.compile('<mrk mtype="seg" mid="([^<>]*?)">(.*?)</mrk>',re.S)

    #tagmkre=re.compile('<[^<>]*?>')
    transunits=transunitre.findall(sdlxliffstr)
    
    for transunit in transunits:
        tuinfo=[]
        #print(transunit)
        source_segs=source_segs4match.findall(transunit)
        target_segs=target4match.findall(transunit)
        for source_seg in source_segs:
            smrks=mrk4match.findall(source_seg)
            #print(smrks)
            if len(smrks)>0:
                tuinfo.append(smrks[0][1])
                idid=smrks[0][0]
                mrkid4match=re.compile('<mrk mtype="seg" mid="'+idid+'">(.*?)</mrk>',re.S)
                segdefmatch=re.compile('<sdl:seg id="'+idid+'"([^<>]*?)>',re.S)
                confmatch=re.compile('conf="([^<>]*?)"')
                originmatch=re.compile('origin="([^<>]*?)"')
                originsystemmatch=re.compile('origin-system="([^<>]*?)"')
                percentmatch=re.compile('percent="([^<>]*?)"')
                lockedmatch=re.compile('locked="([^<>]*?)"')

                if len(target_segs)>0:
                    targetmrks=mrkid4match.findall(target_segs[0])
                    if len(targetmrks)>0:
                        tuinfo.append(targetmrks[0])
                else:
                    tuinfo.append('')
                segdefs=segdefmatch.findall(transunit)

                confv=confmatch.findall(segdefs[0])
                if len(confv)>0:
                    tuinfo.append(confv[0])
                else:
                    tuinfo.append('')
                originv=originmatch.findall(segdefs[0])
                if len(originv)>0:
                    tuinfo.append(originv[0])
                else:
                    tuinfo.append('')
                originsystemv=originsystemmatch.findall(segdefs[0])
                if len(originsystemv)>0:
                    tuinfo.append(originsystemv[0])
                else:
                    tuinfo.append('')
                percentv=percentmatch.findall(segdefs[0])
                if len(percentv)>0:
                    tuinfo.append(percentv[0])
                else:
                    tuinfo.append('')
                lockedfv=lockedmatch.findall(segdefs[0])
                if len(lockedfv)>0:
                    tuinfo.append(lockedfv[0])
                else:
                    tuinfo.append('')
                tuinfolist.append(tuinfo)

    return(tuinfolist)   
