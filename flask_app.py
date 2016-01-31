# On this example we are going to show how to send a file
# to the browser for the user to "Download" it, instead
# of just outputing text.
# To ilustrate this, the default route will print a CSV file
# while the download route will open a "Save as..." dialog
# Browse the /download route to see it in action

from flask import Flask, render_template, send_file, url_for
import mdd_downloader
import time
import os
# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'some_secret'
data_folder = 'data'


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/ajax/loading')
# def ajax_index():
#     # time.sleep(5)
#     return render_template('loading.html')
# # This route will prompt a file download with the csv lines

@app.route('/mdd', methods=['GET', 'POST'])
def mdd():
    # ajax_index()
    mdd_downloader.MeteorologicalDataDownloader().main()
    time.sleep(5)
    return render_template('mdd.html')


@app.route("/downloads")
def download():
    import shutil
    shutil.make_archive('uploads/data', 'zip', './data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    else:
        shutil.rmtree(data_folder)
        os.makedirs(data_folder)
    url_for('index')
    return send_file('uploads/data.zip',
                     mimetype='text/zip',
                     attachment_filename='data.zip',
                     as_attachment=True)

# @app.route('/download')
# def download():
#     csvList = open('uploads/data.csv')
#     csvList = '\n'.join(','.join(row) for row in csvList)
#     response = make_response(open(csvList).readlines())
#     # This is the key: Set the right header for the response
#     # to be downloaded, instead of just printed on the browser
#     response.headers["Content-Disposition"] = "attachment; filename=data.csv"
#     return response

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )