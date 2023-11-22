from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Conversion en PDF
        pdf_filename = os.path.splitext(filename)[0] + '.pdf'
        pdf_filepath = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

        image = Image.open(filepath)
        pdf_canvas = canvas.Canvas(pdf_filepath, pagesize=image.size)
        pdf_canvas.drawInlineImage(filepath, 0, 0, width=image.width, height=image.height)
        pdf_canvas.save()

        # Redirection vers la page de réussite
        return redirect(url_for('success'))

@app.route('/success')
def success():
    return 'Conversion réussie !'

if __name__ == '__main__':
    app.run(debug=True)
