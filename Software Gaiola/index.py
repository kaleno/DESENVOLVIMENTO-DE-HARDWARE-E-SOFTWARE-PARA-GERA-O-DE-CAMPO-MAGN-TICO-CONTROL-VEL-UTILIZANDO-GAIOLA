#https://www.imagebam.com/view/GA2TLM
import urllib.request
page = urllib.request.urlopen("https://www.imagebam.com/view/GA2TLM")
r = str(page.read())
print(r)

