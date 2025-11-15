# streamlit_app.py
# Fichier unifié pour le déploiement sur Streamlit Cloud

import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# --- 1. LOGIQUE DU BACKEND (main.py) ---

# --- MODÉLISATION DES DONNÉES ---
class Answer(BaseModel):
    id: str
    text: str
    scoring: Dict[str, Dict[str, float]] = Field(default_factory=dict)

class Question(BaseModel):
    id: str
    section: str
    text: str
    input_type: str
    answers: List[Answer] = Field(default_factory=list)
    rows: List[Dict[str, str]] = []
    conditional_config: Dict[str, Any] = {}

class Questionnaire(BaseModel):
    title: str
    introduction: str
    questions: List[Question]

# --- BASE DE DONNÉES DES QUESTIONS ---
questionnaire_db = Questionnaire(
    title="Diagnostic Melania",
    introduction="""
    Parle-nous de ta peau comme à une amie bienveillante. 
    Ce diagnostic confidentiel va t'aider à comprendre ta peau, à comprendre ses besoins réels 
    et à recevoir une routine personnalisée pour en prendre soin.
    """,
    questions=[
        Question(id="q1", section="SECTION 1 : QUI ES-TU ?", text="Comment t'appelles-tu ?", input_type="text_input", answers=[]),
        Question(id="q2", section="SECTION 1 : QUI ES-TU ?", text="Tu es :", input_type="radio", answers=[Answer(id="q2_a1", text="Une femme", scoring={"generalites": {"sexe": 10}}), Answer(id="q2_a2", text="Un homme", scoring={"generalites": {"sexe": 5}})]),
        Question(id="q3", section="SECTION 1 : QUI ES-TU ?", text="Tu as :", input_type="radio", answers=[Answer(id="q3_a1", text="Moins de 20 ans", scoring={"facteurs_primaires": {"tranche_age": 2.5}, "problematique": {"production_se": 10}}), Answer(id="q3_a2", text="Entre 20 - 29 ans", scoring={"facteurs_primaires": {"tranche_age": 5}, "problematique": {"production_se": 7.5}}), Answer(id="q3_a3", text="Entre 30 - 39 ans", scoring={"facteurs_primaires": {"tranche_age": 7.5}, "problematique": {"production_se": 5}}), Answer(id="q3_a4", text="Entre 40 - 49 ans", scoring={"facteurs_primaires": {"tranche_age": 10}, "problematique": {"production_se": 2.5}}), Answer(id="q3_a5", text="Plus de 50 ans", scoring={"facteurs_primaires": {"tranche_age": 10}, "problematique": {"production_se": 0}})]),
        Question(id="q4", section="SECTION 1 : QUI ES-TU ?", text="Tu habites où ?", input_type="text_input", answers=[]),
        Question(id="q5", section="SECTION 1 : QUI ES-TU ?", text="Comment décrirais-tu ta couleur de peau naturelle (Avant toute dépigmentation ou éclaircissement) ?", input_type="skin_tone_selector", answers=[Answer(id="q5_unknown", text="Je ne reconnais plus ma couleur naturelle", scoring={})]),
        Question(id="q6", section="SECTION 2 : TES BESOINS & OBJECTIFS", text="Qu'est ce que tu aimerais le plus pour ta peau ?", input_type="radio_with_other", answers=[Answer(id="q6_a1", text="La réparer (peau abîmée, tâches, boutons, dépigmentation, sécheresse)", scoring={"user_preferences": {"objectif_declare": 10}}), Answer(id="q6_a2", text="L'entretenir (peau mixte, grasse, terne, sensible, irrégulière)", scoring={"user_preferences": {"objectif_declare": 5}}), Answer(id="q6_a3", text="La sublimer (éclat sain, uniformité, prévention anti-âge)", scoring={"user_preferences": {"objectif_declare": 2.5}}), Answer(id="q6_other", text="Autre", scoring={})]),
        Question(id="q7", section="SECTION 3 : TES HABITUDES & TON ENVIRONNEMENT", text="A quelle fréquence te nettoies-tu ?", input_type="grid_choice", answers=[Answer(id="q7_c1", text="Le matin et le soir", scoring={"facteurs_secondaires": {"frequence_nettoyage": 2}}), Answer(id="q7_c2", text="Seulement le matin ou en soirée", scoring={}), Answer(id="q7_c3", text="Seulement le soir", scoring={}), Answer(id="q7_c4", text="Plus de deux fois par jour", scoring={}), Answer(id="q7_c5", text="Ça dépend des jours", scoring={})], rows=[{"id": "visage", "text": "Le visage"}, {"id": "corps", "text": "Le corps"}]),
        Question(id="q8", section="SECTION 3 : TES HABITUDES & TON ENVIRONNEMENT", text="Utilises-tu des produits fait maison ?", input_type="radio_with_conditional_text", answers=[Answer(id="q8_a1", text="Oui", scoring={"facteurs_secondaires": {"type_produits": 10}}), Answer(id="q8_a2", text="Non", scoring={"facteurs_secondaires": {"type_produits": 0}}), Answer(id="q8_a3", text="Parfois", scoring={"facteurs_secondaires": {"type_produits": 5}})], conditional_config={"trigger_answers": ["q8_a1", "q8_a3"], "prompt_text": "Précise nous lesquels :"}),
        Question(id="q9", section="SECTION 3 : TES HABITUDES & TON ENVIRONNEMENT", text="Utilises-tu souvent des gants, brosses ou éponges sur ton visage ?", input_type="radio", answers=[Answer(id="q9_a1", text="Oui", scoring={"facteurs_secondaires": {"usage_gants": 10}}), Answer(id="q9_a2", text="Non", scoring={"facteurs_secondaires": {"usage_gants": 0}}), Answer(id="q9_a3", text="Parfois", scoring={"facteurs_secondaires": {"usage_gants": 5}})]),
        Question(id="q10", section="SECTION 3 : TES HABITUDES & TON ENVIRONNEMENT", text="Es-tu régulièrement exposé(e) à des facteurs qui peuvent agresser la peau (chaleur, poussière, stress, pollution, etc.) ?", input_type="radio", answers=[Answer(id="q10_a1", text="Oui, très souvent", scoring={"facteurs_secondaires": {"facteurs_externes": 10}}), Answer(id="q10_a2", text="Parfois", scoring={"facteurs_secondaires": {"facteurs_externes": 7.5}}), Answer(id="q10_a3", text="Rarement", scoring={"facteurs_secondaires": {"facteurs_externes": 5}}), Answer(id="q10_a4", text="Presque jamais", scoring={"facteurs_secondaires": {"facteurs_externes": 2.5}})]),
        Question(id="q11", section="SECTION 3 : TES HABITUDES & TON ENVIRONNEMENT", text="Dans ton quotidien, tu es :", input_type="radio", answers=[Answer(id="q11_a1", text="Le plus souvent en extérieur", scoring={"facteurs_secondaires": {"facteurs_externes_environnement": 10}}), Answer(id="q11_a2", text="Le plus souvent en intérieur, sans climatisation", scoring={"facteurs_secondaires": {"facteurs_externes_environnement": 5}}), Answer(id="q11_a3", text="Le plus souvent en intérieur climatisé", scoring={"facteurs_secondaires": {"facteurs_externes_environnement": 2.5}}), Answer(id="q11_a4", text="Un peu de tout ça, ça dépend des jours", scoring={"facteurs_secondaires": {"facteurs_externes_environnement": 7.5}})]),
        Question(id="q12", section="SECTION 4 : L'HISTORIQUE COSMÉTIQUE", text="As-tu déjà utilisé des produits éclaircissants ou dépigmentants ?", input_type="radio", answers=[Answer(id="q12_a1", text="Oui, en ce moment même", scoring={"facteurs_primaires": {"historique_cosmetique": 10}}), Answer(id="q12_a2", text="Oui, il y a moins de 3 mois", scoring={"facteurs_primaires": {"historique_cosmetique": 7.5}}), Answer(id="q12_a3", text="Oui, il y a plus de 3 mois", scoring={"facteurs_primaires": {"historique_cosmetique": 5}})]),
        Question(id="q13", section="SECTION 4 : L'HISTORIQUE COSMÉTIQUE", text="T'arrive t-il d'utiliser du fond de teint ?", input_type="radio", answers=[Answer(id="q13_a1", text="Oui, tous les jours", scoring={"facteurs_secondaires": {"usage_fond_teint": 10}}), Answer(id="q13_a2", text="Oui, de temps en temps", scoring={"facteurs_secondaires": {"usage_fond_teint": 7.5}}), Answer(id="q13_a3", text="Occasionnellement pour certaines sorties", scoring={"facteurs_secondaires": {"usage_fond_teint": 5}}), Answer(id="q13_a4", text="Non, ou alors vraiment très rarement", scoring={"facteurs_secondaires": {"usage_fond_teint": 0}})]),
        Question(id="q14", section="SECTION 4 : L'HISTORIQUE COSMÉTIQUE", text="T'arrive t-il de faire des soins en institut de beauté ?", input_type="radio", answers=[Answer(id="q14_a1", text="Oui, environ une fois par mois", scoring={"facteurs_secondaires": {"frequence_soins": 0}}), Answer(id="q14_a2", text="Oui, moins d'une fois par trimestre", scoring={"facteurs_secondaires": {"frequence_soins": 5}}), Answer(id="q14_a3", text="Non, ou alors vraiment très rarement", scoring={"facteurs_secondaires": {"frequence_soins": 10}}), Answer(id="q14_a4", text="Non, je me fais mes soins moi-même à la maison", scoring={"facteurs_secondaires": {"frequence_soins": 2.5}})]),
        Question(id="q15", section="SECTION 4 : L'HISTORIQUE COSMÉTIQUE", text="As-tu déjà eu des réactions fortes à un produit ? (Démangeaisons, brûlures, boutons, tâches)", input_type="radio", answers=[Answer(id="q15_a1", text="Oui", scoring={"facteurs_primaires": {"sensibilite": 10}}), Answer(id="q15_a2", text="Non", scoring={"facteurs_primaires": {"sensibilite": 0}})]),
        Question(id="q16", section="SECTION 4 : L'HISTORIQUE COSMÉTIQUE", text="As-tu déjà remarqué un éclaircissement ou un blanchiment après usage d'un produit ?", input_type="radio", answers=[Answer(id="q16_a1", text="Oui", scoring={}), Answer(id="q16_a2", text="Non", scoring={}), Answer(id="q16_a3", text="Je n'en suis pas sûr(e)", scoring={})]),
        Question(id="q17", section="SECTION 4 : L'HISTORIQUE COSMÉTIQUE", text="As-tu déjà été sous traitement médical récent ? (Pilule, antibiotiques, corticoïdes, etc)", input_type="radio", answers=[Answer(id="q17_a1", text="Oui", scoring={}), Answer(id="q17_a2", text="Non", scoring={})]),
        Question(id="q18", section="SECTION 5 : TON HYGIÈNE DE VIE", text="Entre les mille et une choses à faire, parviens-tu à dormir au moins 7h par nuit ?", input_type="radio", answers=[Answer(id="q18_a1", text="Oui, toujours", scoring={"facteurs_secondaires": {"sommeil": 0}}), Answer(id="q18_a2", text="Oui, quelques fois", scoring={"facteurs_secondaires": {"sommeil": 5}}), Answer(id="q18_a3", text="Non, ou alors vraiment très rarement", scoring={"facteurs_secondaires": {"sommeil": 10}})]),
        Question(id="q19", section="SECTION 5 : TON HYGIÈNE DE VIE", text="Dans le tourbillon de la journée, penses-tu à boire au moins 1,5L d'eau ?", input_type="radio", answers=[Answer(id="q19_a1", text="Oui, toujours", scoring={"facteurs_secondaires": {"hydratation_interne": 0}}), Answer(id="q19_a2", text="Oui, quelques fois", scoring={"facteurs_secondaires": {"hydratation_interne": 5}}), Answer(id="q19_a3", text="Non, ou alors vraiment très rarement", scoring={"facteurs_secondaires": {"hydratation_interne": 10}})]),
        Question(id="q20", section="SECTION 5 : TON HYGIÈNE DE VIE", text="Ton alimentation est plutôt :", input_type="radio", answers=[Answer(id="q20_a1", text="Riche en légumes, fruits, eau", scoring={"facteurs_secondaires": {"alimentation": 0}}), Answer(id="q20_a2", text="Riche en gras, sucre, sel", scoring={"facteurs_secondaires": {"alimentation": 10}}), Answer(id="q20_a3", text="Un peu des deux", scoring={"facteurs_secondaires": {"alimentation": 5}})]),
        Question(id="q21", section="SECTION 5 : TON HYGIÈNE DE VIE", text="Es-tu souvent stressé(e) ou anxieux(se) ?", input_type="radio", answers=[Answer(id="q21_a1", text="Oui très souvent", scoring={"facteurs_secondaires": {"exposition_stress": 7.5}}), Answer(id="q21_a2", text="Oui quelque fois", scoring={"facteurs_secondaires": {"exposition_stress": 5}}), Answer(id="q21_a3", text="Rarement", scoring={"facteurs_secondaires": {"exposition_stress": 2.5}})]),
        Question(id="q22", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="Au réveil, ton visage :", input_type="radio", answers=[Answer(id="q22_a1", text="Brille partout", scoring={"caracteristiques_principales": {"nature_peau": 7.5}}), Answer(id="q22_a2", text="Brille sur le front/nez", scoring={"caracteristiques_principales": {"nature_peau": 5}}), Answer(id="q22_a3", text="Est sec, ça tire même", scoring={"caracteristiques_principales": {"nature_peau": 10}}), Answer(id="q22_a4", text="Est normal", scoring={"caracteristiques_principales": {"nature_peau": 2.5}})]),
        Question(id="q23", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="De manière générale, les pores sur le visage sont :", input_type="radio", answers=[Answer(id="q23_a1", text="Très visibles et dilatés", scoring={"caracteristiques_principales": {"type_pores": 10}}), Answer(id="q23_a2", text="Visibles mais pas trop", scoring={"caracteristiques_principales": {"type_pores": 5}}), Answer(id="q23_a3", text="Presque invisibles", scoring={"caracteristiques_principales": {"type_pores": 0}})]),
        Question(id="q24", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="Après le lavage du visage, la peau :", input_type="radio", answers=[Answer(id="q24_a1", text="Devient sèche avec des tiraillements", scoring={"caracteristiques_principales": {"hydratation_cutanee": 10}}), Answer(id="q24_a2", text="Blanchit et reste blanche tant que tu ne te oins", scoring={"caracteristiques_principales": {"hydratation_cutanee": 2.5}}), Answer(id="q24_a3", text="Blanchit et le reste par endroit même lorsque je me suis ointe", scoring={"caracteristiques_principales": {"hydratation_cutanee": 7.5}}), Answer(id="q24_a4", text="Blanchit et recommence à briller après", scoring={"caracteristiques_principales": {"hydratation_cutanee": 2.5}}), Answer(id="q24_a5", text="Présente des zones brillantes et d'autres qui tiraillent", scoring={"caracteristiques_principales": {"hydratation_cutanee": 5}}), Answer(id="q24_a6", text="Semble normale, confortable", scoring={"caracteristiques_principales": {"hydratation_cutanee": 0}})]),
        Question(id="q25", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="Après l'application des soins, ressens-tu l'un de ces effets ?", input_type="checkbox", answers=[Answer(id="q25_a1", text="- picotements légers", scoring={"facteurs_primaires": {"barriere_cutanee": 7.5}, "barriere_cutanee": {"sensibilite_elevee": 5}}), Answer(id="q25_a2", text="- brûlures ou échauffement", scoring={"facteurs_primaires": {"barriere_cutanee": 10}, "barriere_cutanee": {"sensibilite_tres_elevee": 7.5}}), Answer(id="q25_a3", text="- démangeaisons", scoring={"facteurs_primaires": {"barriere_cutanee": 5}, "barriere_cutanee": {"sensibilite_elevee": 5}}), Answer(id="q25_a4", text="- aucune réaction, ma peau est confortable", scoring={"facteurs_primaires": {"barriere_cutanee": 0}, "barriere_cutanee": {"sensibilite_normal": 2.5}})]),
        Question(id="q26", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="As-tu des zones plus foncées que d'autres ?", input_type="radio", answers=[Answer(id="q26_a1", text="Oui", scoring={}), Answer(id="q26_a2", text="Non", scoring={}), Answer(id="q26_a3", text="Je ne sais pas", scoring={})]),
        Question(id="q27", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="As-tu des boutons douloureux ou kystiques ?", input_type="radio", answers=[Answer(id="q27_a1", text="Oui", scoring={"facteurs_primaires": {"type_acnee": 10}}), Answer(id="q27_a2", text="Non", scoring={"facteurs_primaires": {"type_acnee": 0}})]),
        Question(id="q28", section="SECTION 6 : ÉTAT ACTIF DE TA PEAU", text="As-tu des tâches brunes anciennes ?", input_type="radio", answers=[Answer(id="q28_a1", text="Oui", scoring={"facteurs_primaires": {"pigmentation": 10}}), Answer(id="q28_a2", text="Non", scoring={"facteurs_primaires": {"pigmentation": 0}})]),
        Question(id="q29", section="SECTION 7 : LES DÉTAILS CIBLE", text="Où se trouvent principalement les vergetures ?", input_type="checkbox", answers=[Answer(id="q29_a1", text="Cuisses / Jambes", scoring={"caracteristiques_specifiques": {"presence_vergetures": 10}}), Answer(id="q29_a2", text="Bras", scoring={"caracteristiques_specifiques": {"presence_vergetures": 10}}), Answer(id="q29_a3", text="Ventre", scoring={"caracteristiques_specifiques": {"presence_vergetures": 10}}), Answer(id="q29_a4", text="Seins", scoring={"caracteristiques_specifiques": {"presence_vergetures": 10}}), Answer(id="q29_a5", text="Autres", scoring={})]),
        Question(id="q30", section="SECTION 7 : LES DÉTAILS CIBLE", text="As-tu des allergies connues ?", input_type="radio_with_conditional_text", answers=[Answer(id="q30_a1", text="Oui", scoring={"caracteristiques_specifiques": {"presence_allergie": 10}}), Answer(id="q30_a2", text="Non", scoring={"caracteristiques_specifiques": {"presence_allergie": 0}})], conditional_config={"trigger_answers": ["q30_a1"], "prompt_text": "Lesquelles ?"}),
        Question(id="q31", section="SECTION 7 : LES DÉTAILS CIBLE", text="Souhaites-tu que ton diagnostic te recommande une routine complète ou juste des points essentiels ?", input_type="radio", answers=[Answer(id="q31_a1", text="Une routine complète", scoring={"generalites": {"type_routine": 10}}), Answer(id="q31_a2", text="Des points essentiels", scoring={"generalites": {"type_routine": 5}}), Answer(id="q31_a3", text="J'hésite", scoring={"generalites": {"type_routine": 2.5}})])
    ]
)

# --- FONCTION DE CALCUL DU DIAGNOSTIC ---
def produce_diagnostic(user_answers: Dict[str, str]):
    diagnostic_profile = {}
    answer_map = {
        ans.id: ans
        for q in questionnaire_db.questions
        for ans in q.answers
    }

    for key, answer_id in user_answers.items():
        if key.endswith(("_text", "_slider", "_conditional_text")):
            continue
        if answer_id in answer_map:
            answer_obj = answer_map[answer_id]
            for typologie, categories in answer_obj.scoring.items():
                if typologie not in diagnostic_profile:
                    diagnostic_profile[typologie] = {}
                for categorie, score in categories.items():
                    diagnostic_profile[typologie][categorie] = diagnostic_profile[typologie].get(categorie, 0) + score
    return {"diagnostic_profile": diagnostic_profile}


# --- 2. INTERFACE DE L'APP (app.py) ---

# --- CONFIGURATION DE LA PAGE ET STYLE ---
st.set_page_config(
    page_title="Diagnostic de Peau - Melania",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    st.markdown("""
    <style>
        /* --- CORRECTION CSS V2 --- */

        /* Style général */
        .stApp { background-color: #F0F2F6; }

        /* En-tête */
        .header { background-color: #FFFFFF; padding: 2rem; border-radius: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .header h1 { color: #333; }
        .header p { color: #555; font-size: 1.1rem; }

        /* Conteneur de section */
        .section-container { background-color: #FFFFFF; padding: 2rem 2.5rem; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); margin-bottom: 2rem; }
        .section-container h2 { color: #D97D54; border-bottom: 2px solid #F0F2F6; padding-bottom: 0.5rem; margin-bottom: 1.5rem; font-size: 1.5rem; }

        /* --- CORRECTIONS DE VISIBILITÉ ET DE STYLE --- */

        /* Cible le texte des questions (passé en markdown) et le met en gras */
        .st-emotion-cache-1y4p8pa > p > strong {
            font-weight: 700 !important; /* Gras */
            color: #31333F !important; /* Texte sombre */
        }

        /* Cible le texte des options de réponse (radio, checkbox) */
        .st-emotion-cache-6qob1r, .st-emotion-cache-1y4p8pa {
            color: #31333F !important; /* Texte sombre */
        }
        
        /* Cible le texte des champs de saisie (text_input) */
        .stTextInput label {
            font-weight: 700 !important; /* Gras */
            color: #31333F !important; /* Texte sombre */
        }

        /* --- FIN DES CORRECTIONS --- */

        /* Bouton principal */
        .stButton>button { width: 100%; height: 3rem; font-size: 1.2rem; font-weight: bold; background-color: #D97D54; color: white; border: none; border-radius: 5px; }
        .stButton>button:hover { background-color: #C76B43; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACE UTILISATEUR ---
load_css()

st.markdown(f"""
<div class="header">
    <h1>{questionnaire_db.title}</h1>
    <p>{questionnaire_db.introduction}</p>
</div>
""", unsafe_allow_html=True)

user_answers = {}
sections = {}
for q in questionnaire_db.questions:
    if q.section not in sections:
        sections[q.section] = []
    sections[q.section].append(q)

# Dans streamlit_app.py, remplace la boucle d'affichage des questions

for section_title, questions_in_section in sections.items():
    with st.container():
        st.markdown(f'<div class="section-container"><h2>{section_title}</h2>', unsafe_allow_html=True)
        for i, q in enumerate(questions_in_section):
            with st.container():
                q_id = q.id
                q_type = q.input_type
                q_text = q.text
                q_answers = q.answers

                if q_type == 'text_input':
                    # On utilise directement le label ici car le CSS le met en gras
                    user_answers[q_id] = st.text_input(q_text, key=q_id, placeholder="Votre réponse...")
                
                elif q_type == 'radio':
                    st.markdown(f"**{q_text}**")
                    answer_options = [ans.text for ans in q_answers]
                    answer_text_to_id = {ans.text: ans.id for ans in q_answers}
                    selected_option = st.radio(" ", options=answer_options, key=q_id, horizontal=True, label_visibility="collapsed")
                    if selected_option:
                        user_answers[q_id] = answer_text_to_id[selected_option]
                
                elif q_type == 'grid_choice':
                    st.markdown(f"**{q_text}**")
                    q_rows = q.rows
                    if not q_rows or not q_answers:
                        st.warning("Erreur de configuration pour cette question.")
                    else:
                        col_answer_map = {ans.text: ans.id for ans in q_answers}
                        col_options = [ans.text for ans in q_answers]
                        for row in q_rows:
                            row_id = row.get('id')
                            row_text = row.get('text')
                            if not row_id or not row_text: continue
                            # On utilise le label de st.radio pour les lignes de la grille
                            selected_option = st.radio(label=f"*{row_text}*", options=col_options, key=f"{q_id}_{row_id}", horizontal=True)
                            if selected_option:
                                user_answers[f"{q_id}_{row_id}"] = col_answer_map[selected_option]
                
                elif q_type == 'checkbox':
                    st.markdown(f"**{q_text}**")
                    for answer in q_answers:
                        ans_id = answer.id
                        ans_text = answer.text
                        if st.checkbox(ans_text, key=ans_id):
                            user_answers[ans_id] = ans_id
                
                elif q_type == 'radio_with_other':
                    st.markdown(f"**{q_text}**")
                    other_option_text = "Autre"
                    regular_options = [ans.text for ans in q_answers if ans.text != other_option_text]
                    all_display_options = regular_options + [other_option_text]
                    answer_text_to_id = {ans.text: ans.id for ans in q_answers}
                    selected_option = st.radio(" ", options=all_display_options, key=q_id, label_visibility="collapsed")
                    if selected_option:
                        user_answers[q_id] = answer_text_to_id[selected_option]
                        if selected_option == other_option_text:
                            other_text = st.text_input("Veuillez préciser :", key=f"{q_id}_other_text")
                            if other_text:
                                user_answers[f"{q_id}_other_text"] = other_text
                
                elif q_type == 'radio_with_conditional_text':
                    st.markdown(f"**{q_text}**")
                    answer_options = [ans.text for ans in q_answers]
                    answer_text_to_id = {ans.text: ans.id for ans in q_answers}
                    selected_option_text = st.radio(" ", options=answer_options, key=q_id, horizontal=True, label_visibility="collapsed")
                    if selected_option_text:
                        selected_id = answer_text_to_id[selected_option_text]
                        user_answers[q_id] = selected_id
                        q_config = q.conditional_config
                        if selected_id in q_config.get('trigger_answers', []):
                            prompt = q_config.get('prompt_text', "Veuillez préciser :")
                            conditional_text = st.text_input(prompt, key=f"{q_id}_conditional")
                            if conditional_text:
                                user_answers[f"{q_id}_conditional_text"] = conditional_text
                
                elif q_type == 'skin_tone_selector':
                    st.markdown(f"**{q_text}**")
                    st.info("Ta couleur naturelle n'est pas un teint, c'est ton niveau réel de mélanine...")
                    st.markdown("**Comment décrirais-tu ton teint ?**")
                    skin_tone_value = st.slider(" ", 1, 10, key=f"{q_id}_slider", label_visibility="collapsed")
                    user_answers[f"{q_id}_slider"] = str(skin_tone_value)
                    if q_answers:
                        unknown_answer = q_answers[0]
                        is_unknown = st.checkbox(unknown_answer.text, key=q_id)
                        if is_unknown:
                            user_answers[q_id] = unknown_answer.id

            if i < len(questions_in_section) - 1:
                st.markdown("<hr style='margin: 1.5rem 0; border-color: #F0F2F6;'>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Utiliser deux colonnes pour centrer le bouton
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Produire mon diagnostic", type="primary", use_container_width=True):
        with st.spinner("Analyse de vos réponses..."):
            # Appel direct de la fonction de calcul (plus besoin de l'API)
            diagnostic_result = produce_diagnostic(user_answers)

        if diagnostic_result:
            # Stocker le résultat dans l'état de la session pour le conserver
            st.session_state['diagnostic_result'] = diagnostic_result
            # Force un rechargement de la page pour afficher le résultat en bas
            st.rerun()

# Afficher le résultat s'il est présent dans l'état de la session
if 'diagnostic_result' in st.session_state:
    with st.container():
        st.markdown('<div class="section-container"><h2>Résultat de votre Diagnostic (Profil de score)</h2>', unsafe_allow_html=True)
        st.success("Votre profil a été généré avec succès !")
        
        # Afficher le JSON du profil de score
        st.json(st.session_state['diagnostic_result']['diagnostic_profile'])
        
        st.info("Ce profil technique sera utilisé pour générer un diagnostic textuel personnalisé dans la prochaine version.")
        st.markdown('</div>', unsafe_allow_html=True)
