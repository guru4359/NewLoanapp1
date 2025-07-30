from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "demo_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BANK_CONFIG_FILE = "config/banks.json"

def load_banks():
    with open(BANK_CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

BANKS = load_banks()

@app.route("/")
def index():
    return render_template("index.html", banks=BANKS)

@app.route("/loan/<bank_id>", methods=["GET", "POST"])
def loan(bank_id):
    bank = BANKS.get(bank_id)
    if not bank:
        return "Bank not found", 404

    if request.method == "POST":
        data = request.form.to_dict()
        file = request.files.get("kyc_doc")
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            data["uploaded_file"] = filename

        session["form_data"] = data
        return redirect(url_for("preview", bank_id=bank_id))

    return render_template("loan_form.html", bank=bank)

@app.route("/preview/<bank_id>", methods=["GET", "POST"])
def preview(bank_id):
    data = session.get("form_data", {})
    bank = BANKS.get(bank_id)

    if request.method == "POST":
        # In real use case: store to DB, send SMS/email, etc.
        return render_template("success.html", bank=bank, data=data)

    return render_template("preview.html", bank=bank, data=data)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    global BANKS

    if request.method == "POST":
        new_config = request.get_json()
        with open(BANK_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)
        BANKS = new_config
        return jsonify({"message": "Configuration saved successfully"})

    return render_template("admin.html", banks=BANKS)

if __name__ == "__main__":
    app.run(debug=True)
    
   
