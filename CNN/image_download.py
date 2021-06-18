from google_images_download import google_images_download   #importing the library
import sys

if __name__ == '__main__':
    #keyword = sys.argv[1]
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": "" + "dog" + "", "limit": 50, "print_urls": True}
    #arguments = {"keywords":"dog","limit":5000,"print_urls":True,"chromedriver":"chromedriver.exe"}
    paths = response.download(arguments)