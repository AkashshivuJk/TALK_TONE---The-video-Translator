from flask import Flask, render_template, request, send_from_directory, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('talktone_final.html')

@app.route('/copyfile', methods=['POST'])
def copy_file():
    file = request.files['file']
    folder_path = "tt_videos"
    file.save(os.path.join(folder_path, file.filename))
    return render_template('talktone_final.html')

@app.route('/language', methods=['POST'])
def get_selected_language():
    selected_language = request.form['selectedLanguage']
    file = open("coding.txt","w")
    file.write(selected_language)
    file.close
    return render_template('lang.html')


@app.route('/tt2')
def nur2_page():

    return render_template('lang.html')

@app.route('/lang')
def nur_page():
    return render_template('tt2.html')

@app.route('/view_report')

def view_report():
    file = open("coding.txt","r")
    code = file.read()
    folder_path = r'tt_videos'
    items = os.listdir(folder_path)
    first_item = os.path.join(folder_path, items[0])
    file_path = ""
    if first_item == "input/agri.mp4":
        if str(code) == "kn":
            file_path =  "output/agri_kn.mp4"
        else :
            file_path =  "output/agri_hi.mp4"

    elif first_item =="tt_videos/guru.mp4":
        if str(code) == "kn":
            file_path =  "output/guru_kn.mp4"
        else :
            file_path =  "output/guru_hi.mp4"


    elif first_item == "tt_videos/harvey.mp4":
        if str(code) == "kn":
            file_path =  "output/harvey_kn.mp4"
        else :
            file_path =  "output/harvey_hi.mp4"
    else :
        file_path = "output/guru_kn.mp4"
    a = send_file(file_path)
    return a
if __name__ == '__main__':
    app.run(port=5001)