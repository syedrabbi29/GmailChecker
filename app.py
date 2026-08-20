import imaplib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def verify_gmail(email, app_password):
    # পাসওয়ার্ডের মাঝের স্পেসগুলো রিমুভ করা
    clean_password = app_password.replace(" ", "")
    try:
        # Gmail IMAP সার্ভারে কানেক্ট ও লগইন চেষ্টা
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, clean_password)
        mail.logout()
        return True
    except Exception:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check-credentials", methods=["POST"])
def check_credentials():
    data = request.get_json()
    email = data.get("email", "").strip()
    app_password = data.get("password", "").strip()

    if not email or not app_password:
        return jsonify({"success": False, "message": "Email এবং App Password উভয়ই প্রয়োজন!"}), 400

    is_valid = verify_gmail(email, app_password)
    
    if is_valid:
        return jsonify({"success": True, "message": "Success! জিমেইল এবং অ্যাপ পাসওয়ার্ড সঠিক আছে।"})
    else:
        return jsonify({"success": False, "message": "নায়! জিমেইল অথবা অ্যাপ পাসওয়ার্ড ভুল।"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
