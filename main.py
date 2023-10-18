from flask import Flask, request, render_template
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        if file:
            image = Image.open(file)
            output_image = remove(image)

            # Change the background (You'll need to customize this part)
            # For example, let's save the image with a transparent background
            output_image = output_image.convert("RGBA")

            # Save the resulting image
            output_buffer = io.BytesIO()
            output_image.save(output_buffer, format="PNG")
            output_bytes = output_buffer.getvalue()

            return render_template("result.html", result_image=output_bytes)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
