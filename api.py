from flask import Flask, request, jsonify, render_template
import os
import librosa
from infer import VietASR

app = Flask(__name__)

config = 'configs/quartznet12x1_vi.yaml'
encoder_checkpoint = 'models/acoustic_model/vietnamese/JasperEncoder-STEP-289936.pt'
decoder_checkpoint = 'models/acoustic_model/vietnamese/JasperDecoderForCTC-STEP-289936.pt'
lm_path = 'models/language_model/3-gram-lm.binary'

vietasr = VietASR(
    config_file=config,
    encoder_checkpoint=encoder_checkpoint,
    decoder_checkpoint=decoder_checkpoint,
    lm_path=lm_path,
    beam_width=50
)

# Đường dẫn thư mục để lưu trữ file audio
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/transcribe', methods=['POST'])
def transcribe_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # check if file type is valid and save it to local
    if file :
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        audio_signal, _ = librosa.load(file_path, sr=16000)
        data = vietasr.transcribe(audio_signal)
        print(data)
        return jsonify(data), 200
        #response = jsonify(data)
        #response.headers['Content-Type'] = 'application/json; charset=utf-8'
        #return response, 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)