# SymptomWise — हिंदी UI, डार्क/लाइट मोड

Flask और SQLite पर आधारित शैक्षिक symptom-overlap ऐप। इसमें मोबाइल-फ्रेंडली UI, एनिमेशन, hover effects, चार्ट, हिंदी जानकारी और डार्क/लाइट थीम है।

## चलाने का तरीका

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

ब्राउज़र में `http://127.0.0.1:5000` खोलें।

## फीचर्स
- डार्क और लाइट मोड टॉगल; आपकी पसंद ब्राउज़र में सेव होती है
- हिंदी UI, हिंदी लक्षण, सावधानियाँ और चेतावनी संकेत
- मोबाइल के लिए responsive layout और mobile navigation
- hover transitions, animated cards और scroll reveal
- Chart.js से symptom-overlap bar chart
- SQLite में चुने गए लक्षणों का demo log

## ज़रूरी मेडिकल सूचना
यह केवल शैक्षिक डेमो है, चिकित्सा निदान का विकल्प नहीं। स्कोर लक्षणों की सूची से साधारण मिलान है; यह बीमारी की संभावना नहीं बताता और प्रमाणित चिकित्सा मॉडल नहीं है। इसके आधार पर इलाज शुरू, बंद या न बदलें। गंभीर या तेजी से बिगड़ते लक्षणों पर तुरंत योग्य स्वास्थ्य विशेषज्ञ से संपर्क करें।
