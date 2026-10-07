from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///symptomwise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

CONDITIONS = {
    "Common Cold": {
        "description": "नाक और गले का आमतौर पर हल्का वायरल संक्रमण।",
        "symptoms": ["runny nose", "sneezing", "sore throat", "cough", "congestion"],
        "precautions": ["Rest and drink fluids.", "Wash hands regularly.", "Consider saline spray for nasal congestion."],
        "when_to_seek_help": "Seek medical advice for breathing difficulty, chest pain, dehydration, or symptoms that worsen or persist.",
        "image": "https://images.unsplash.com/photo-1584515933487-779824d29309?auto=format&fit=crop&w=1000&q=85",
        "color": "#6c7cff"
    },
    "Influenza": {
        "description": "एक संक्रामक श्वसन बीमारी, जिसमें बुखार, बदन दर्द और थकान हो सकती है।",
        "symptoms": ["fever", "body aches", "chills", "cough", "fatigue", "headache"],
        "precautions": ["Rest and maintain hydration.", "Stay home while feverish.", "Ask a clinician promptly if you are at higher risk."],
        "when_to_seek_help": "Urgent care is important for difficulty breathing, persistent chest pain, confusion, or severe dehydration.",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1000&q=85",
        "color": "#9b6cff"
    },
    "Asthma": {
        "description": "लंबे समय तक रहने वाली स्थिति, जिसमें साँस की नलियों में सूजन और सिकुड़न हो सकती है।",
        "symptoms": ["wheezing", "shortness of breath", "chest tightness", "cough"],
        "precautions": ["Follow your prescribed asthma action plan.", "Avoid known triggers where possible.", "Keep prescribed reliever medication accessible."],
        "when_to_seek_help": "Severe breathlessness or symptoms not relieved by your prescribed rescue plan are an emergency.",
        "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1000&q=85",
        "color": "#20b8a6"
    },
    "Type 2 Diabetes": {
        "description": "ऐसी स्थिति जिसमें शरीर रक्त में मौजूद ग्लूकोज़ का सही उपयोग नहीं कर पाता।",
        "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow healing"],
        "precautions": ["Follow your clinician's monitoring and treatment plan.", "Choose balanced meals and regular activity.", "Do not change medication without medical advice."],
        "when_to_seek_help": "Seek urgent help for confusion, fainting, vomiting with severe weakness, or very high/low glucose symptoms.",
        "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=1000&q=85",
        "color": "#f0a44b"
    },
    "Hypertension": {
        "description": "रक्तचाप का लगातार सामान्य से अधिक रहना; कई बार कोई स्पष्ट लक्षण नहीं होते।",
        "symptoms": ["headache", "dizziness", "blurred vision"],
        "precautions": ["Measure blood pressure correctly and keep a log.", "Take prescribed medicines as directed.", "Discuss salt intake, exercise, and alcohol with a clinician."],
        "when_to_seek_help": "Very high blood pressure with chest pain, breathlessness, weakness, or vision/speech changes needs emergency care.",
        "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1000&q=85",
        "color": "#ed6a8b"
    },
    "Pneumonia": {
        "description": "ऐसा संक्रमण जो एक या दोनों फेफड़ों की वायु थैलियों में सूजन पैदा करता है।",
        "symptoms": ["fever", "cough", "shortness of breath", "chest pain", "fatigue"],
        "precautions": ["Rest and drink fluids if able.", "Follow medical treatment instructions.", "Avoid smoking and second-hand smoke."],
        "when_to_seek_help": "Prompt medical evaluation is important, especially for breathlessness, blue lips, confusion, or worsening chest pain.",
        "image": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?auto=format&fit=crop&w=1000&q=85",
        "color": "#4c9be8"
    },
    "Gastroenteritis": {
        "description": "पेट और आँतों की सूजन, जिसमें अक्सर उल्टी या दस्त हो सकते हैं।",
        "symptoms": ["diarrhea", "vomiting", "nausea", "stomach cramps", "fever"],
        "precautions": ["Take frequent small sips of fluid; oral rehydration solution may help.", "Wash hands carefully.", "Eat gentle foods as tolerated."],
        "when_to_seek_help": "Seek help for blood in stool/vomit, severe pain, fainting, or signs of dehydration.",
        "image": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?auto=format&fit=crop&w=1000&q=85",
        "color": "#23b99a"
    },
    "Anemia": {
        "description": "स्वस्थ लाल रक्त कोशिकाओं या हीमोग्लोबिन का सामान्य से कम स्तर।",
        "symptoms": ["fatigue", "weakness", "dizziness", "shortness of breath", "pale skin"],
        "precautions": ["Ask about blood tests to identify the cause.", "Discuss iron-rich foods and supplements with a clinician.", "Do not self-start high-dose supplements without advice."],
        "when_to_seek_help": "Seek prompt care for fainting, chest pain, severe breathlessness, or rapidly worsening weakness.",
        "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1000&q=85",
        "color": "#e77d69"
    },
    "GERD": {
        "description": "पाचन संबंधी स्थिति जिसमें पेट का अम्ल या सामग्री वापस भोजन नली की ओर आ सकती है।",
        "symptoms": ["heartburn", "acid reflux", "sour taste", "chest discomfort", "cough"],
        "precautions": ["Try smaller meals and avoid personal trigger foods.", "Avoid lying down for 2–3 hours after meals.", "Ask a clinician about frequent or persistent symptoms."],
        "when_to_seek_help": "New or severe chest pain needs emergency assessment, particularly with sweating or breathlessness.",
        "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=1000&q=85",
        "color": "#e5a64d"
    },
    "Migraine": {
        "description": "तंत्रिका तंत्र से जुड़ी स्थिति, जिसमें बार-बार सिरदर्द और अन्य लक्षण हो सकते हैं।",
        "symptoms": ["headache", "nausea", "light sensitivity", "sound sensitivity", "visual changes"],
        "precautions": ["Rest in a quiet, dark room if helpful.", "Track possible triggers and headache patterns.", "Discuss recurring attacks and treatment options with a clinician."],
        "when_to_seek_help": "A sudden worst-ever headache, new weakness, confusion, fainting, or new vision/speech problems is an emergency.",
        "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1000&q=85",
        "color": "#8e7af5"
    }
}

SYMPTOMS = sorted({s for item in CONDITIONS.values() for s in item["symptoms"]})

SYMPTOM_HI = {
    "runny nose": "नाक बहना", "sneezing": "छींक आना", "sore throat": "गले में खराश",
    "cough": "खाँसी", "congestion": "नाक बंद होना", "fever": "बुखार",
    "body aches": "शरीर में दर्द", "chills": "ठंड लगना", "fatigue": "थकान",
    "headache": "सिरदर्द", "wheezing": "साँस लेते समय सीटी जैसी आवाज़",
    "shortness of breath": "साँस फूलना", "chest tightness": "सीने में जकड़न",
    "increased thirst": "ज़्यादा प्यास लगना", "frequent urination": "बार-बार पेशाब आना",
    "blurred vision": "धुंधला दिखना", "slow healing": "घाव भरने में देर",
    "dizziness": "चक्कर आना", "chest pain": "सीने में दर्द", "diarrhea": "दस्त",
    "vomiting": "उल्टी", "nausea": "जी मिचलाना", "stomach cramps": "पेट में ऐंठन",
    "weakness": "कमज़ोरी", "pale skin": "त्वचा का पीला/फीका दिखना",
    "heartburn": "सीने में जलन", "acid reflux": "एसिड का गले तक आना",
    "sour taste": "मुँह में खट्टा स्वाद", "light sensitivity": "रोशनी से परेशानी",
    "sound sensitivity": "आवाज़ से परेशानी", "visual changes": "दृष्टि में बदलाव"
}
CONDITION_HI = {
    "Common Cold": {"name": "सामान्य सर्दी", "category": "साँस संबंधी"},
    "Influenza": {"name": "इन्फ्लुएंज़ा (फ्लू)", "category": "वायरल संक्रमण"},
    "Asthma": {"name": "अस्थमा (दमा)", "category": "साँस संबंधी"},
    "Type 2 Diabetes": {"name": "टाइप 2 डायबिटीज़", "category": "मेटाबॉलिक स्वास्थ्य"},
    "Hypertension": {"name": "उच्च रक्तचाप", "category": "हृदय स्वास्थ्य"},
    "Pneumonia": {"name": "निमोनिया", "category": "फेफड़ों का स्वास्थ्य"},
    "Gastroenteritis": {"name": "गैस्ट्रोएंटेराइटिस", "category": "पाचन स्वास्थ्य"},
    "Anemia": {"name": "एनीमिया (खून की कमी)", "category": "रक्त स्वास्थ्य"},
    "GERD": {"name": "एसिड रिफ्लक्स (GERD)", "category": "पाचन स्वास्थ्य"},
    "Migraine": {"name": "माइग्रेन", "category": "न्यूरोलॉजी"}
}


class SymptomCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def calculate_matches(selected):
    results = []
    for name, info in CONDITIONS.items():
        matches = [s for s in selected if s in info["symptoms"]]
        if matches:
            score = round(100 * len(matches) / max(1, len(info["symptoms"])))
            results.append({
                "name": name, "description": info["description"], "symptoms": info["symptoms"],
                "matches": matches, "score": score, "color": info["color"], "image": info["image"]
            })
    return sorted(results, key=lambda x: (len(x["matches"]), x["score"]), reverse=True)

@app.route("/")
def index():
    return render_template("index.html", symptoms=SYMPTOMS, symptom_hi=SYMPTOM_HI, condition_hi=CONDITION_HI, condition_count=len(CONDITIONS))

@app.route("/results", methods=["POST"])
def results():
    selected = request.form.getlist("symptoms")
    if not selected:
        return render_template("index.html", symptoms=SYMPTOMS, symptom_hi=SYMPTOM_HI, condition_hi=CONDITION_HI, condition_count=len(CONDITIONS),
                               error="Choose at least one symptom to see an educational symptom overlap summary.")
    selected = [s for s in selected if s in SYMPTOMS]
    db.session.add(SymptomCheck(symptoms=", ".join(selected)))
    db.session.commit()
    matches = calculate_matches(selected)
    chart_data = [{"label": CONDITION_HI.get(m["name"], {}).get("name", m["name"]), "score": m["score"], "color": m["color"]} for m in matches[:6]]
    return render_template("results.html", selected=selected, matches=matches, chart_data=chart_data, symptom_hi=SYMPTOM_HI, condition_hi=CONDITION_HI)

@app.route("/condition/<path:name>")
def condition(name):
    info = CONDITIONS.get(name)
    if not info:
        return render_template("404.html"), 404
    return render_template("condition.html", name=name, info=info, condition_hi=CONDITION_HI, symptom_hi=SYMPTOM_HI)

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
