import urllib.request
LIST = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
LIST1 = ["4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
for p in LIST1:
    for s in LIST:
        for t in LIST:
            for q in LIST:
                try:
                    page = urllib.request.urlopen('https://www.imagebam.com/view/GA'+p+s+t+q)
                    r = str(page.read())
                    x = r.index('id="gallery-name">')
                    y = r.index('<span class="count">')
                    corte2 = r[y+len('<span class="count">'):]
                    corte1= r[x+len('id="gallery-name">'):]
                    corte = print(corte1.split(sep ="</a>\\n")[0],"\t",corte2.split(sep ="</span>\\n")[0],"\t\t\t\t"+ 'https://www.imagebam.com/view/GA'+p+s+t+q)
                except:
                    continue
#print(r)

