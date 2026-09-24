"""
Single source of truth for the citizen profile form. Templates loop over
this list to render inputs -- adding a new question means adding one dict
here, not touching HTML/JS in three places.
"""

FIELDS = [
    {"name": "age", "type": "number", "label_key": "qAge"},
    {"name": "gender", "type": "select", "label_key": "qGender", "options": [
        ("male", "male"), ("female", "female"), ("other", "other")]},
    {"name": "occupation", "type": "select", "label_key": "qOccupation", "options": [
        ("farmer", "occFarmer"), ("student", "occStudent"), ("entrepreneur", "occEntrepreneur"),
        ("unorganized", "occUnorganized"), ("salaried", "occSalaried"), ("homemaker", "occHomemaker"),
        ("senior", "occSenior"), ("artisan", "occArtisan"), ("vendor", "occVendor"),
        ("unemployed", "occUnemployed")]},
    {"name": "education", "type": "select", "label_key": "qEducation", "options": [
        ("below10", "eduBelow10"), ("ten12", "edu10"), ("grad", "eduGrad"), ("pg", "eduPG")]},
    {"name": "income", "type": "number", "label_key": "qIncome"},
    {"name": "state", "type": "select", "label_key": "qState", "options": "STATES"},
    {"name": "other_info", "type": "text", "label_key": "qOtherInfo", "optional": True},
    {"name": "category", "type": "select", "label_key": "qCategory", "options": [
        ("general", "catGen"), ("obc", "catOBC"), ("sc", "catSC"), ("st", "catST"), ("other", "catOther")]},
]
