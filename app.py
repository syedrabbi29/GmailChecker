from flask import Flask, request, jsonify, render_template
import imaplib
import os

# Pydroid এবং অনলাইন হোস্টিং দুই জায়গাতেই পাথ ঠিক রাখার জন্য অটো-ডিটেকশন
current_dir = os.path.dirname(os.path.abspath(__file__))
if "temp_iiec_codefile" in current_dir or not os.path.exists(os.path.join(current_dir, 'index.html')):
    # যদি Pydroid এর টেম্প ফোল্ডারে রান হয়, তবে মোবাইল স্টোরেজের পাথ নেবে
    base_path = '/storage/emulated/0/GmailChecker'
else:
    # গিটহাব বা সার্ভারে রান হলে কারেন্ট ফোল্ডার নেবে
    base_path = current_dir

app = Flask(__name__, 
            template_folder=base_path, 
            static_folder=base_path, 
            static_url_path='')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def check_gmail():
    data = request.get_json()
    email = data.get('email')
    app_password = data.get('app_password', '')
    
    # পাসওয়ার্ডের মাঝখানের স্পেসগুলো রিমুভ করা
    clean_password = app_password.replace(" ", "")
    
    try:
        # জিমেইলের IMAP সার্ভারে লগইন টেস্ট
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, clean_password)
        mail.logout()
        return jsonify({"status": "success", "message": "✓ জিমেইলটি অ্যাক্টিভ এবং অ্যাপ পাসওয়ার্ডটি সঠিক!"})
    except imaplib.IMAP4.error:
        return jsonify({"status": "error", "message": "✗ ভেরিফিকেশন ব্যর্থ! জিমেইল নিষ্ক্রিয় অথবা অ্যাপ পাসওয়ার্ডটি ভুল।"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
