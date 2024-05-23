from flask import Flask, render_template, request
import tempfile

from calorie_counter import get_calories_from_image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]

    if image.filename == "":
        return {
            "error": "No image uploaded",
        }, 400

    temp_file = tempfile.NamedTemporaryFile()
    image.save(temp_file.name)

    calories = get_calories_from_image(temp_file.name)
    temp_file.close()

    return {
        "calories": calories,
    }

if __name__ == "__main__":
    app.run(debug=True)
