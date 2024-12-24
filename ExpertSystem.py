from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def diagnose():
    illnesses = {
        "flu": {'fever', 'cough', 'headache', 'sore_throat', 'body_ache', 'chills', 'fatigue'},
        "common cold": {'cough', 'sneezing', 'runny_nose', 'congestion', 'mild_fever'},
        "COVID-19": {'fever', 'cough', 'loss_of_taste_or_smell', 'shortness_of_breath', 'fatigue', 'body_ache'},
        "strep throat": {'sore_throat', 'fever', 'swollen_lymph_nodes', 'difficulty_swallowing'},
        "allergies": {'sneezing', 'runny_nose', 'itchy_eyes', 'congestion'},
        "pneumonia": {'fever', 'cough', 'shortness_of_breath', 'chest_pain', 'fatigue'},
        "bronchitis": {'cough', 'chest_pain', 'wheezing', 'fatigue', 'sore_throat'},
        "migraine": {'headache', 'nausea', 'sensitivity_to_light', 'sensitivity_to_sound'},
    }

    medicine_recommendations = {
        'fever': 'paracetamol',
        'cough': 'cough syrup (e.g., Benadryl, Robitussin)',
        'headache': 'ibuprofen or acetaminophen',
        'sore_throat': 'lozenges (e.g., Strepsils) or warm salt water gargle',
        'sneezing': 'antihistamines (e.g., loratadine)',
        'runny_nose': 'decongestants (e.g., pseudoephedrine)',
        'loss_of_taste_or_smell': 'vitamin supplements (consult a doctor)',
        'shortness_of_breath': 'consult a doctor immediately',
        'swollen_lymph_nodes': 'anti-inflammatory medication (e.g., ibuprofen)',
        'body_ache': 'pain relievers (e.g., ibuprofen or acetaminophen)',
        'chills': 'warm clothing and paracetamol',
        'fatigue': 'rest and hydration',
        'congestion': 'nasal spray or steam inhalation',
        'itchy_eyes': 'antihistamine eye drops',
        'difficulty_swallowing': 'throat sprays or lozenges',
        'chest_pain': 'consult a doctor immediately',
        'wheezing': 'inhalers (consult a doctor)',
        'nausea': 'anti-nausea medication (e.g., domperidone)',
        'sensitivity_to_light': 'rest in a dark room',
        'sensitivity_to_sound': 'avoid loud noises',
    }

    if request.method == "POST":
        user_input = request.form.get("symptoms")
        user_symptoms = set(map(str.strip, user_input.lower().split(',')))

        scores = {illness: len(user_symptoms & illness_symptoms)
                  for illness, illness_symptoms in illnesses.items()}
        possible_illnesses = {illness: score for illness, score in scores.items() if score >= 1}

        results = []
        for illness, score in sorted(possible_illnesses.items(), key=lambda item: item[1], reverse=True):
            results.append(f"{illness} (matched {score} symptoms)")

        medicines = []
        for symptom in user_symptoms:
            medicine = medicine_recommendations.get(symptom)
            if medicine:
                medicines.append(f"For {symptom}: {medicine}")
            else:
                medicines.append(f"For {symptom}: No specific medicine recommendation available, consult a doctor.")

        return render_template("result.html", results=results, medicines=medicines)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5500)
