from urllib2 import URLError
import os, json, urllib2
from flask import Flask, render_template, request, flash
from forms import ChannelForm
import string
 
 # Create Flask instance using current shell name (this allows running on both your computer and on a server)
app = Flask(__name__)
app.secret_key = "secret_key"
YOUR_API_KEY = "AIzaSyCvmUuH7_MNaGQG5Sxbb6jhyVTa_5aLCA8"
# .route Decorator function creates the actual URL structure of the site - see example below for adding additional pages

@app.route('/', methods=['GET','POST'])
def CostlyBanana():
    form = ChannelForm(request.form)
    data = ""
    data2= ""
    thumbnail_data = []
    title_data = []
    id_data = []

    channelsDetails = []

    if request.method == 'POST':
        #get channel, channel url
        channelname = form.channelname.data
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q={channelname}&type=channel&key={api_key}".format(channelname=channelname,api_key=YOUR_API_KEY)
        try:
            data = json.load(urllib2.urlopen(url))
            try:
                channel = []
                channel.append(data['items'][0]['snippet']['thumbnails']['default']['url'])
                channel.append(data['items'][0]['snippet']['title'])
                channel.append(data['items'][0]['snippet']['channelId'])
                search_url = "https://www.googleapis.com/youtube/v3/subscriptions?key=AIzaSyCvmUuH7_MNaGQG5Sxbb6jhyVTa_5aLCA8&part=snippet&channelId={channelid}&key={api_key}".format(channelid=id_data,api_key=YOUR_API_KEY)
                data = json.load(urllib2.urlopen(url))
                channelsDetails.append(channel)
                count = 0
                while count < data['pageInfo']['totalResults']:
                    results = 0
                    while results < data['pageInfo']['resultsPerPage'] and results + count < data['pageInfo']['totalResults']:
                        channelsDetails.append([data['items'][results]['snippet']['thumbnails']['default']['url'], data['items'][results]['snippet']['title'], data['items'][results]['snippet']['channelId']])
                        count += 1
                        results += 1
                    try:
                        search_url = "https://www.googleapis.com/youtube/v3/subscriptions?key=AIzaSyCvmUuH7_MNaGQG5Sxbb6jhyVTa_5aLCA8&part=snippet&channelId={channelid}&nextPageToken={next_page_token}&key={api_key}".format(channelid=id_data[count], next_page_token=data['pageInfo']['nextPageToken'], api_key=YOUR_API_KEY)
                    except:
                        break
            except:
                pass
        except:
            flash("No channel with videos found!")
    return render_template('home.html', data=channelsDetails, form=form)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
