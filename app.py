from flask import Flask , render_template, request, jsonify ,send_file,abort
import os
import Stopify
import shutil
app = Flask(__name__)

@app.route('/',methods=['GET'])
def serve_html():
    return render_template('index.html')


@app.route('/downloadZip',methods=['POST','GET'])
def downloadZip():
     if request.method == 'GET':
          return render_template('index.html')
     elif request.method == 'POST':
        user_input = request.form.get('playlist')
       
        Stopify.getTrackIDs(user_input)


        filepath = os.path.dirname(os.path.abspath(__file__))+"\\output.zip"
        if os.path.exists(filepath):
                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name='example.zip',
                    mimetype='application/zip'
                )
        else:
        # If the file does not exist, return a 404 Not Found error
            return abort(404)

        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
