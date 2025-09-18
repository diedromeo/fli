import os
from flask import Flask, render_template_string, request

# The Flask application instance
app = Flask(__name__)

# This is the secret flag, stored on the server in a file.
FLAG_FILE_CONTENT = "ctf7{y0u_f0und_th3_l0c4l_f1l3_1nclu510n}"

# We will simulate a directory structure and a flag file.
def setup_flag_file():
    """
    Simulates the presence of a flag file on the server.
    """
    with open("flag.txt", "w") as f:
        f.write(FLAG_FILE_CONTENT)

# The main page that loads content from a file
@app.route('/')
def index():
    """
    Renders the main page that can include different files based on a URL parameter.
    """
    # The vulnerability is here: The 'file' parameter is not sanitized.
    file_to_load = request.args.get('file', 'index.html')

    # A security-conscious approach would sanitize the input to prevent directory traversal.
    # CRITICAL VULNERABILITY: Directly using user input to open a file.
    if ".." in file_to_load or "/" in file_to_load or "\\" in file_to_load:
        content = "Invalid file path detected."
    else:
        try:
            with open(file_to_load, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            content = "File not found."
    
    # Check if the user is trying to access the flag file.
    if file_to_load == 'flag.txt':
        content = f"""
            <div class="text-center">
                <h2 class="text-2xl font-bold mb-4 text-green-600">Congratulations!</h2>
                <p class="text-gray-600 mb-4">You have successfully found the flag:</p>
                <div class="bg-gray-200 p-4 rounded-md inline-block font-mono text-lg">
                    {FLAG_FILE_CONTENT}
                </div>
                <img src="https://i.pinimg.com/originals/7a/43/dc/7a43dc193276f0abc4b4e729312940e1.gif" class="mt-8 mx-auto rounded-lg shadow-lg max-w-full h-auto" alt="Success GIF">
            </div>
        """
    elif file_to_load == 'index.html':
        content = """
            <h2 class="text-2xl font-bold mb-4">Welcome to Our Company!</h2>
            <p class="text-gray-600">
                We are a cutting-edge technology company dedicated to innovation.
                Feel free to browse our <a href="/?file=about.html" class="text-blue-500 hover:underline">About Us</a> page to learn more.
            </p>
        """
    elif file_to_load == 'about.html':
        content = """
            <h2 class="text-2xl font-bold mb-4">About Us</h2>
            <p class="text-gray-600">
                Founded in 2023, our mission is to provide secure and reliable solutions for the modern world.
            </p>
        """

    return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Company Website</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 min-h-screen">
            <nav class="bg-white shadow-lg">
                <div class="max-w-6xl mx-auto px-4">
                    <div class="flex justify-between items-center py-4">
                        <a href="/" class="text-xl font-bold text-gray-800">CompanyCo.</a>
                        <div>
                            <a href="/?file=index.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-200">Home</a>
                            <a href="/?file=about.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-200">About</a>
                        </div>
                    </div>
                </div>
            </nav>
            <div class="container mx-auto mt-8 p-6 bg-white rounded-lg shadow-md max-w-2xl">
                """ + content + """
            </div>
        </body>
        </html>
    """)

# The Flask application runs here.
if __name__ == '__main__':
    setup_flag_file()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
