# icd9_lookup_stub.py

"""
Stub lookup table for ICD-9 codes to condition descriptions.
Used for enriching FHIR JSON bundles with readable diagnoses.
"""

ICD9_LOOKUP = {
    "1120": "Candidiasis of mouth",
    "1122": "Candidiasis of skin and nails",
    "1179": "Other and unspecified mycoses",
    "25002": "Diabetes mellitus without mention of complication, type II or unspecified type, uncontrolled",
    "25080": "Diabetes with other specified manifestations, type II or unspecified type, not stated as uncontrolled",
    "2720": "Pure hypercholesterolemia",
    "2721": "Pure hyperglyceridemia",
    "4010": "Malignant essential hypertension",
    "4011": "Benign essential hypertension",
    "41401": "Coronary atherosclerosis of native coronary artery",
    "4280": "Congestive heart failure, unspecified",
    "496": "Chronic airway obstruction, not elsewhere classified",
    "53081": "Esophageal reflux",
    "5849": "Acute kidney failure, unspecified",
    "585": "Chronic kidney disease, unspecified",
    "5853": "Chronic kidney disease, Stage III (moderate)",
    "5854": "Chronic kidney disease, Stage IV (severe)",
    "5855": "Chronic kidney disease, Stage V",
    "5856": "End stage renal disease",
    "5990": "Urinary tract infection, site not specified",
    "7802": "Syncope and collapse",
    "78650": "Chest pain, unspecified",
    "78659": "Chest pain, other",
    "V5861": "Long-term (current) use of anticoagulants",
    "V5867": "Long-term (current) use of insulin",
    "V103": "Personal history of malignant neoplasm of breast",
    "V1254": "Personal history of transient ischemic attack (TIA), and cerebral infarction without residual deficits",
    "V1582": "History of tobacco use",
    "V4501": "Cardiac pacemaker in situ",
    "V5865": "Long-term (current) use of steroids",
    # Add more mappings as needed...
}