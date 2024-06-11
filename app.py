from flask import Flask, request, jsonify, render_template
import requests
import json
from elasticsearch import Elasticsearch

app = Flask(__name__)

def them_ban_ghi(record):
    # add a new record to elastic
    es = Elasticsearch("http://localhost:9200"); 
    response = es.index(index="songs_index", body=record)
    print(response.get('result'))

    # add a new record to elastic
    es = Elasticsearch("http://localhost:9200") 
    response = es.index(index="songs_index", body=record)
    print(response.get('result'))

def find_all(text):
    #find songs that has artist, song name, lyrics similar to text
    es = Elasticsearch("http://localhost:9200")  
    query1 = {
        "query": {
            "multi_match": {
                "query": text,
                "fields": ["song_name", "artist", "lyrics"],
                "fuzziness": "AUTO"  
            }
        }
    }
    query2 = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"song_name": text}},
                    {"match": {"artist": text}},
                    {"match": {"lyrics": text}}
                ]
            }
        }
    }
    # call elastic api in python
    response = es.search(index="songs_index", body=query2)
    hits = response['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])
    json_string = json.dumps(results, indent=4,ensure_ascii=False)
    return(json_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # client wanna add a new song record to the service. they provide song name, artist and the song's audio file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # check if file type is valid and forward to viet asr api
    if file and allowed_file(file.filename):
        try:
            # Forward the file to another API
            files = {'file': (file.filename, file.stream, 'audio/mpeg')}
            #files = {'file': (file.filename, file.stream, file.mimetype)}
            response = requests.post('http://localhost:5001/transcribe', files=files)
            if response.status_code == 200:
                data={}
                data["artist"] = request.form.get('artist')
                data["song_name"] = request.form.get('song_name')
                data["lyrics"]=response.text.encode().decode('unicode_escape')
                print("response text: "+data["lyrics"])
                them_ban_ghi(data)
                return jsonify(data), 200
            else:
                return jsonify({'error': 'Failed to forward the file'}), response.status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    # if file type not in mp3,wav. return a err
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/process_text', methods=['POST'])
def process_text():
    # client wanna search for songs that has artist, songs_name or lyrics similar to the provided text
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    #get the text provided by client
    text = data['text']
    # Thực hiện tim kiem dua tren du lieu dau vao
    result = find_all(text)
    return result, 200

def allowed_file(filename): # check if uploaded file's extension is accepted
    ALLOWED_EXTENSIONS = {'mp3', 'wav'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
