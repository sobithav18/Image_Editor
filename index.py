# Install necessary packages
# pip3 install flask opencv-python
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

# Configure upload directory and accepted file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

# Initialize Flask app with configuration
app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to validate file extensions
def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to handle image processing based on the chosen operation
def process_image(filename, operation):
    print(f"Performing {operation} on file: {filename}")
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(img_path)
    
    match operation:
        case "gray":
            processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            output_filename = f"static/{filename}"
            cv2.imwrite(output_filename, processed_img)
            return output_filename
        case "convert_webp":
            output_filename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(output_filename, img)
            return output_filename
        case "convert_jpg":
            output_filename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(output_filename, img)
            return output_filename
        case "convert_png":
            output_filename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(output_filename, img)
            return output_filename
    return None

# Route for homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route for the 'About' page
@app.route("/about")
def about():
    return render_template("about.html")

# Route for image editing/processing
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        # Retrieve the selected operation from the form
        operation = request.form.get("operation")
        
        # Check if a file is uploaded
        if 'file' not in request.files:
            flash('No file uploaded')
            return "Error: No file uploaded"
        
        file = request.files['file']
        
        # Handle cases where no file is selected
        if file.filename == '':
            flash('No file selected')
            return "Error: No file selected"
        
        # Process the uploaded file if it is of an allowed type
        if file and is_file_allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processed_file_path = process_image(filename, operation)
            flash(f"Image processing complete. View your result <a href='/{processed_file_path}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")

# Run the app on port 5001 in debug mode
if __name__ == "__main__":
    app.run(debug=True, port=5001)
