from flask import Flask, request, render_template_string
import easyocr
import os

app = Flask(__name__)
reader = easyocr.Reader(['en'], gpu=False)

HTML_TEMPLATE = '''
<!doctype html>
<html>
  <head>
    <title>Army OCR Demo</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 40px; }
      h2 { color: #003366; }
      form { margin-bottom: 20px; }
      input[type=file] { margin-bottom: 10px; }
      pre { background: #f8f8f8; padding: 10px; border: 1px solid #ddd; }
    </style>
  </head>
  <body>
    <h2>Army OCR Demo</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" required>
      <br>
      <input type="submit" value="Upload & Extract Text">
    </form>
    {% if text %}
      <h3>Extracted Text:</h3>
      <pre>{{ text }}</pre>
    {% endif %}
  </body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def upload_file():
    text = None
    if request.method == "POST":
        f = request.files["file"]
        f.save("temp.jpg")
        results = reader.readtext("temp.jpg")
        text = "\n".join([res[1] for res in results])
        os.remove("temp.jpg")
    return render_template_string(HTML_TEMPLATE, text=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
