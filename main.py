from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
        <h2 style='text-align:center; margin-top : 50px ;'>
            ✅ Patient Management System — Flask App Running Successfully!
        </h2>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
