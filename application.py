# from flask import Flask
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import time
# from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
app = Flask(__name__)
@app.route('/',methods=['GET'])
@cross_origin() # its purpose is to be available to different countries
def index():
    return render_template("index.html")
@app.route('/results',methods=['POST','GET'])
@cross_origin() # its purpose is to be available to different countries
def result():
    if request.method == 'POST':
        try:
            searchString = request.form['content']
            print(searchString)
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            yt = searchString
            driver.get(yt)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(5)  # Add a sleep time to wait for more videos to load

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # box = soup.findAll('div', {'class': 'ytd-rich-grid-media'})
            box = soup.findAll('div',id = 'contents')


            # Print the number of videos found
            print(f"Found {len(box)} videos")

            driver.quit()
            urls = []
            thumbnails = []
            for i in range(len(box)):
                try:
                    if("https://www.youtube.com"+box[i].a["href"] not in urls):
                        p =box[i].a["href"]
                        q = p[9:]
                        thumbnails.append("http://img.youtube.com/vi/"+q+"/hqdefault.jpg")
                        urls.append("https://www.youtube.com"+box[i].a["href"])
                except Exception as e:
                    pass
            vid_titles =[]
            for i in range(len(box)):
                try:
                    if(box[i].findAll('a',id="video-title-link")[0].text not in vid_titles):
                        vid_titles.append(box[i].findAll('a',id="video-title-link")[0].text)
                except Exception as e:
                    pass
            views=[]
            for i in range(0,len(box)):
                try:
                    if(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[0].text not in views):
                        views.append(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[0].text)
                except Exception as e:
                    pass
            time = []
            for i in range(0,len(box),3):
                try:
                    # if(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[1].text not in time):
                    time.append(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[1].text)
                except Exception as e:
                    pass
            url5 = urls[0:6]
            thumb5 = thumbnails[0:6]
            title5 = vid_titles[0:6]
            view5 = views[0:6]
            time5 = time[0:6]
            final = []
            for i in range(6):
                mydict = {"Video Urls": url5[i], "Thumbnail Urls": thumb5[i], "Title": title5[i], "Views": view5[i],
                          "Upload time": time5[i]}
                final.append(mydict)
            # client = pymongo.MongoClient("mongodb+srv://breakratr:breakratr@cluster0.ln0bt5m.mongodb.net/?retryWrites=true&w=majority")
            # db = client['review_scrap']
            # review_col = db['review_scrap_data']
            # review_col.insert_many(mydict)
            return render_template('results.html', videos=final[0:len(final)])
                
                
        except  Exception as e:
            return e
if __name__ == '__main__':
    app.run(debug=True)
