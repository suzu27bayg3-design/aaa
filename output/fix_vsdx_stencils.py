import zipfile, re, sys
src,dst=sys.argv[1],sys.argv[2]
zin=zipfile.ZipFile(src)
zout=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
for info in zin.infolist():
    data=zin.read(info.filename)
    if info.filename=='visio/windows.xml':
        s=data.decode('utf-8')
        n0=len(re.findall(r"<Window [^>]*WindowType='Stencil'",s))
        # self-closing stencil windows
        s=re.sub(r"<Window [^>]*WindowType='Stencil'[^>]*/>","",s)
        # stencil windows with children
        s=re.sub(r"<Window [^>]*WindowType='Stencil'[^>]*>.*?</Window>","",s,flags=re.S)
        print('removed stencil windows:',n0,'remaining:',len(re.findall('WindowType',s)))
        data=s.encode('utf-8')
    zout.writestr(info,data)
zout.close()
