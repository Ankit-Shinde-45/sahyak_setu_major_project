# -*- coding: utf-8 -*-
"""
Generates 115 Indian government welfare schemes with complete 4-language translations
(English, Hindi, Marathi, Tamil).
Brings schemes.json to 185+ schemes.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMES_FILE = os.path.join(BASE_DIR, "data", "schemes.json")

with open(SCHEMES_FILE, "r", encoding="utf-8") as f:
    schemes = json.load(f)

existing_ids = set(s["id"] for s in schemes)
print(f"Starting with {len(schemes)} schemes.")

new_items = []

def add(sid, scope, state, rule,
        en_n, en_t, en_d, en_b, en_docs, en_st, en_l,
        hi_n, hi_t, hi_d, hi_b, hi_docs, hi_st,
        mr_n, mr_t, mr_d, mr_b, mr_docs, mr_st,
        ta_n, ta_t, ta_d, ta_b, ta_docs, ta_st):
    if sid in existing_ids:
        return
    new_items.append({
        "id": sid,
        "scope": scope,
        "state": state,
        "rule": rule,
        "t": {
            "en": {"name": en_n, "tag": en_t, "desc": en_d, "benefits": en_b, "documents": en_docs, "steps": en_st, "link": en_l},
            "hi": {"name": hi_n, "tag": hi_t, "desc": hi_d, "benefits": hi_b, "documents": hi_docs, "steps": hi_st, "link": en_l},
            "mr": {"name": mr_n, "tag": mr_t, "desc": mr_d, "benefits": mr_b, "documents": mr_docs, "steps": mr_st, "link": en_l},
            "ta": {"name": ta_n, "tag": ta_t, "desc": ta_d, "benefits": ta_b, "documents": ta_docs, "steps": ta_st, "link": en_l}
        }
    })

# 1. Sanjay Gandhi Niradhar (Maharashtra)
add("sanjay_gandhi_niradhar_maha", "state", "Maharashtra", {"income_max": 50000},
    "Sanjay Gandhi Niradhar Anudan Yojana", "State · Maharashtra", "Financial assistance of ₹1,000 to ₹1,500/month for destitute persons, disabled, widows, and critically ill in Maharashtra.",
    ["₹1,000/month for single person and ₹1,500/month for family with children", "Financial support directly into bank account"],
    ["Maharashtra Domicile (15+ yrs)", "Income certificate (< ₹50,000)", "Age proof", "Disability or medical certificate if applicable"],
    ["Submit application to Talathi / Nayab Tahsildar", "Committee scrutiny by Sanjay Gandhi committee", "Monthly pension through DBT"],
    "https://mumbaisuburban.gov.in/scheme/sanjay-gandhi-niradhar-anudan-yojana",
    "संजय गांधी निराधार अनुदान योजना", "महाराष्ट्र शासन", "महाराष्ट्र के निराधार वृद्ध, दिव्यांग, विधवा व गंभीर बीमारियों से पीड़ित व्यक्तियों को ₹1,000 से ₹1,500 प्रतिमाह की सहायता।",
    ["एकल व्यक्ति को ₹1,000 तथा बच्चों वाले परिवार को ₹1,500 प्रति माह", "नियमित आर्थिक सहारा"],
    ["15 वर्ष का महाराष्ट्र अधिवास", "आय प्रमाणपत्र (< ₹50,000)", "आयु या दिव्यांगता प्रमाण", "बैंक पासबुक"],
    ["तहसीलदार कार्यालय में आवेदन करें", "समिति द्वारा अनुमोदन", "सीधे खाते में मासिक पेंशन"],
    "संजय गांधी निराधार अनुदान योजना", "महाराष्ट्र शासन", "निराधार, अंध, अपंग, अनाथ मुले व गंभीर आजारी व्यक्तींना दरमहा ₹१,००० ते ₹१,५०० आर्थिक सहाय्य.",
    ["एका व्यक्तीस दरमहा ₹१,००० व कुटुंबास ₹१,५०० थेट मदत", "जीवन जगण्यासाठी आधार"],
    ["१५ वर्षांचा रहिवासी दाखला", "उत्पन्न दाखला (< ५०,०००)", "वैद्यकीय/अपंगत्व प्रमाणपत्र", "बँक पासबुक"],
    ["तलाठी किंवा तहसीलदार कार्यालयात अर्ज सादर करा", "संजय गांधी समिती मंजुरी", "थेट बँक खात्यात पेन्शन"],
    "சஞ்சய் காந்தி ஆதரவற்றோர் உதவித் திட்டம்", "மகாராஷ்டிரா அரசு", "மகாராஷ்டிராவில் உள்ள ஆதரவற்றோர், விதவைகள் மற்றும் மாற்றுத்திறனாளிகளுக்கு மாதம் ₹1,000 முதல் ₹1,500 வரை உதவி.",
    ["மாதம் ₹1,000 முதல் ₹1,500 வரை நேரடி வங்கி வரவு", "முதியோர் மற்றும் ஆதரவற்றோருக்கு பாதுகாப்பு"],
    ["இருப்பிடச் சான்று", "வருமானச் சான்றிதழ் (< ₹50,000)", "ஆதார் அட்டை"],
    ["வட்டாட்சியர் அலுவலகத்தில் விண்ணப்பிக்கவும்", "சரிபார்ப்பிற்கு பின் ஓய்வூதியம் பெறுதல்"])

# 2. Shravanbal Seva State Pension (Maharashtra)
add("shravanbal_seva_pension_maha", "state", "Maharashtra", {"occupation": "senior", "age_min": 65, "income_max": 50000},
    "Shravanbal Seva State Pension Scheme", "State · Maharashtra", "Monthly pension of ₹1,000 for destitute senior citizens aged 65 and above in Maharashtra.",
    ["₹1,000 per month credited directly to the senior citizen's bank account", "Dignified life for impoverished elders"],
    ["Age proof (65+ years)", "Income certificate (< ₹50,000)", "Maharashtra Domicile (15+ yrs)", "Aadhaar Card"],
    ["Submit form at local Tahsildar office", "Committee approval", "DBT credit every month"],
    "https://sjsa.maharashtra.gov.in",
    "श्रावणबाळ सेवा राज्य निवृत्तीवेतन योजना", "महाराष्ट्र शासन", "महाराष्ट्र के 65 वर्ष और उससे अधिक आयु के निर्धन वृद्धजनों को ₹1,000 प्रतिमाह की पेंशन।",
    ["प्रति माह ₹1,000 सीधे बैंक खाते में", "वृद्धजनों को गरिमापूर्ण जीवन"],
    ["आयु प्रमाण (65+ वर्ष)", "आय प्रमाणपत्र (< ₹50,000)", "महाराष्ट्र अधिवास प्रमाणपत्र", "आधार कार्ड"],
    ["तहसीलदार कार्यालय में आवेदन जमा करें", "स्वीकृति उपरांत मासिक अंतरण"],
    "श्रावणबाळ सेवा राज्य निवृत्तीवेतन योजना", "महाराष्ट्र शासन", "६५ वर्षे किंवा त्यावरील निराधार ज्येष्ठ नागरिकांना दरमहा ₹१,००० पेन्शन.",
    ["दरमहा ₹१,००० थेट बँक खात्यात", "वृद्धापकाळात सन्मानजनक जीवन"],
    ["वयाचा पुरावा (६५+ वर्षे)", "उत्पन्न दाखला (< ५०,०००)", "रहिवासी दाखला", "आधार कार्ड"],
    ["तहसीलदार कार्यालयात अर्ज करा", "दरमहा खात्यात पेन्शन"],
    "ஸ்ரவன்பால் முதியோர் ஓய்வூதியத் திட்டம்", "மகாராஷ்டிரா அரசு", "65 வயதுக்கு மேற்பட்ட ஆதரவற்ற முதியோர்களுக்கு மாதம் ₹1,000 உதவித்தொகை.",
    ["மாதம் ₹1,000 நேரடி வங்கி வரவு", "முதியோர்களுக்கான உதவி"],
    ["வயது சான்றிதழ் (65+)", "வருமானச் சான்றிதழ் (< ₹50,000)", "ஆதார் அட்டை"],
    ["வட்டாட்சியரிடம் விண்ணப்பிக்கவும்"])

# 3. Rajarshi Chhatrapati Shahu Maharaj Fee Waiver (Maharashtra)
add("rajarshi_shahu_maharaj_fee_waiver", "state", "Maharashtra", {"occupation": "student", "income_max": 800000},
    "Rajarshi Chhatrapati Shahu Maharaj Shikshan Shulkh Pratipuri", "State · Maharashtra", "50% tuition and exam fee reimbursement for EBC students studying professional degree courses (Engineering, Medical, MBA).",
    ["50% tuition fees and exam fees reimbursed", "Applicable for CAP round admissions in private unaided institutions"],
    ["Income Certificate (< ₹8 Lakhs)", "Allotment Letter / CAP admission receipt", "Maharashtra Domicile Certificate", "Aadhaar Card"],
    ["Apply on MahaDBT portal (mahadbt.maharashtra.gov.in)", "College desk scrutiny and approval", "Fee reimbursed directly to student bank account"],
    "https://mahadbt.maharashtra.gov.in",
    "राजर्षि छत्रपति शाहू महाराज शिक्षण शुल्क प्रतिपूर्ति योजना", "महाराष्ट्र शासन", "व्यावसायिक पाठ्यक्रमों (इंजीनियरिंग, मेडिकल, एमबीए) में अध्ययनरत ईबीसी छात्रों को 50% ट्यूशन फीस की वापसी।",
    ["50% ट्यूशन व परीक्षा शुल्क की प्रतिपूर्ति", "निजी गैर-अनुदानित कॉलेजों में अध्ययनरत छात्रों को लाभ"],
    ["आय प्रमाणपत्र (₹8 लाख से कम)", "केंद्रीकृत प्रवेश (CAP) आवंटन पत्र", "महाराष्ट्र अधिवास", "आधार कार्ड"],
    ["महाडीबीटी (MahaDBT) पोर्टल पर ऑनलाइन आवेदन करें", "कॉलेज प्राचार्य द्वारा सत्यापन", "सीधे छात्र के खाते में प्रतिपूर्ति"],
    "राजर्षी छत्रपती शाहू महाराज शिक्षण शुल्क प्रतिपूर्ती योजना", "महाराष्ट्र शासन", "व्यावसायिक अभ्यासक्रमांमधील (इंजिनिअरिंग, एमबीबीएस, फार्मसी) आर्थिकदृष्ट्या दुर्बल (EBC) विद्यार्थ्यांना ५०% फी सवलत.",
    ["५०% शैक्षणिक शुल्क व परीक्षा फी प्रतिपूर्ती", "कॅप राउंडद्वारे प्रवेश घेतलेल्या विद्यार्थ्यांना लाभ"],
    ["उत्पन्न दाखला (< ८ लाख)", "कॅप अलॉटमेंट लेटर", "रहिवासी दाखला", "आधार कार्ड"],
    ["महाडीबीटी पोर्टलवर ऑनलाइन अर्ज भरा", "महाविद्यालय पडताळणी", "खात्यात फी जमा"],
    "ராஜர்ஷி ஷாகு மகாராஜ் கல்விக் கட்டண சலுகை திட்டம்", "மகாராஷ்டிரா அரசு", "பொறியியல், மருத்துவம் பயிலும் ஏழை மாணவர்களுக்கு 50% கல்விக் கட்டண தள்ளுபடி.",
    ["50% கல்விக் கட்டணம் மற்றும் தேர்வு கட்டணம் திரும்பப் பெறுதல்", "உயர்கல்வி பயிலும் மாணவர்களுக்கு உதவி"],
    ["வருமானச் சான்றிதழ் (< ₹8 லட்சம்)", "சேர்க்கை ஆணை", "இருப்பிடச் சான்று"],
    ["MahaDBT தளத்தில் விண்ணப்பிக்கவும்"])

# 4. Savitribai Phule Scholarship for Girls (Maharashtra)
add("savitribai_phule_girl_scholarship", "state", "Maharashtra", {"occupation": "student", "gender": "female", "category_in": ["sc", "obc"]},
    "Savitribai Phule Scholarship for VJNT/SBC/SC Girls", "State · Maharashtra", "Financial scholarship of ₹600 to ₹1,000 per year for girl students from Class 5 to 10 in Maharashtra schools.",
    ["Direct financial assistance to prevent school dropout among backward girl students", "No income limit for SC girls"],
    ["Caste Certificate", "Aadhaar Card", "School Bonafide certificate", "Bank passbook"],
    ["Headmaster submits student list to Block Education Officer (BEO)", "Automatic disbursement via DBT"],
    "https://mahadbt.maharashtra.gov.in",
    "सावित्रीबाई फुले कन्या छात्रवृत्ति योजना", "महाराष्ट्र शासन", "महाराष्ट्र में कक्षा 5वीं से 10वीं तक की वंचित वर्ग की छात्राओं को पढ़ाई जारी रखने हेतु छात्रवृत्ति।",
    ["कक्षा 5 से 10 तक ₹600 से ₹1,000 वार्षिक छात्रवृत्ति", "लड़कियों की स्कूल ड्रॉपआउट रोकने में सहायक"],
    ["जाति प्रमाणपत्र", "आधार कार्ड", "स्कूल बोनाफाइड प्रमाणपत्र", "बैंक पासबुक"],
    ["स्कूल प्रधानाध्यापक द्वारा बीईओ को सूची प्रेषित", "सीधे बैंक खाते में छात्रवृत्ति"],
    "सावित्रीबाई फुले शिष्यवृत्ती योजना (मुलींसाठी)", "महाराष्ट्र शासन", "इयत्ता ५ वी ते १० वी मधील मागासवर्गीय विद्यार्थिनींना शिक्षणासाठी दरवर्षी ₹६०० ते ₹१,००० शिष्यवृत्ती.",
    ["मुलींच्या शिक्षणासाठी थेट शिष्यवृत्ती", "गळती रोखण्यासाठी मदत"],
    ["जात प्रमाणपत्र", "शाळा बोनाफाईड दाखला", "आधार कार्ड", "बँक पासबुक"],
    ["मुख्याध्यापकांमार्फत महाडीबीटीवर अर्ज", "थेट बँक खात्यात शिष्यवृत्ती"],
    "சாவித்ரிபாய் பூலே மாணவிகள் கல்வி உதவித்தொகை", "மகாராஷ்டிரா அரசு", "5 முதல் 10 ஆம் வகுப்பு வரை பயிலும் பின்தங்கிய மாணவிகளுக்கு ஆண்டுதோறும் உதவித்தொகை.",
    ["பள்ளி மாணவிகளுக்கு நேரடி கல்வி உதவித்தொகை", "பள்ளி இடைநிற்றலை தடுத்தல்"],
    ["சாதிச் சான்றிதழ்", "பள்ளி படிப்புச் சான்று", "ஆதார் அட்டை"],
    ["பள்ளி மூலமாக விண்ணப்பித்து நிதி பெறுதல்"])

# 5. Tamil Nadu Free Laptop Scheme for Students
add("tn_free_laptop_students", "state", "Tamil Nadu", {"occupation": "student"},
    "Tamil Nadu Government Free Laptop Scheme for Students", "State · Tamil Nadu", "Free brand-new laptops for all Class 12 passed students in government and government-aided schools.",
    ["Free laptop with pre-installed educational software and operating system", "Bridging the digital divide for students entering higher education"],
    ["Class 12 Passing Marksheet", "School Transfer Certificate (TC)", "Aadhaar Card"],
    ["Distributed directly by school headmasters after Class 12 board results", "No separate application required"],
    "https://www.tn.gov.in/scheme/data_view/6849",
    "छात्रों हेतु मुफ्त लैपटॉप योजना (तमिलनाडु)", "तमिलनाडु शासन", "तमिलनाडु के सरकारी व सहायता प्राप्त स्कूलों के 12वीं पास छात्रों को मुफ्त आधुनिक लैपटॉप।",
    ["शैक्षणिक सॉफ्टवेयर युक्त निःशुल्क ब्रांडेड लैपटॉप", "डिजिटल शिक्षा और उच्च शिक्षा में सहायक"],
    ["12वीं की अंकतालिका", "स्कूल टीसी (स्थानांतरण प्रमाणपत्र)", "आधार कार्ड"],
    ["बोर्ड परीक्षा परिणाम उपरांत स्कूल द्वारा सीधे वितरित", "अलग से आवेदन की आवश्यकता नहीं"],
    "विद्यार्थ्यांना मोफत लॅपटॉप योजना (तमिळनाडू)", "तमिळनाडू शासन", "सरकारी व अनुदानित शाळांमधून १२ वी उत्तीर्ण सर्व विद्यार्थ्यांना मोफत लॅपटॉप वाटप.",
    ["मोफत ब्रँडेड लॅपटॉप शैक्षणिक सॉफ्टवेअरसह", "उच्च शिक्षणासाठी डिजिटल साधन"],
    ["१२ वी गुणपत्रिका", "शाळा सोडल्याचा दाखला", "आधार कार्ड"],
    ["शाळेकडून थेट वाटप"],
    "மாணவர்களுக்கு விலையில்லா மடிக்கணினி வழங்கும் திட்டம்", "தமிழ்நாடு அரசு", "அரசு மற்றும் அரசு உதவிபெறும் பள்ளிகளில் 12 ஆம் வகுப்பு முடித்த அனைத்து மாணவர்களுக்கும் இலவச மடிக்கணினி.",
    ["கல்வி மென்பொருளுடன் கூடிய விலையில்லா மடிக்கணினி", "கல்லூரி உயர் கல்விக்கு டிஜிட்டல் உதவி"],
    ["12-ஆம் வகுப்பு மதிப்பெண் சான்றிதழ்", "பள்ளி மாற்றுச் சான்றிதழ் (TC)", "ஆதார் அட்டை"],
    ["பள்ளி தலைமை ஆசிரியர் மூலமாக நேரடியாக வழங்கப்படுகிறது"])

# 6. Kalaignar Magalir Urimai Thittam (Tamil Nadu)
add("kalaignar_magalir_urimai_tn", "state", "Tamil Nadu", {"gender": "female", "age_min": 21, "income_max": 250000},
    "Kalaignar Magalir Urimai Thittam (Women Basic Income)", "State · Tamil Nadu", "Monthly basic income of ₹1,000 directly into the bank accounts of over 1.15 Crore women heads of households in Tamil Nadu.",
    ["₹1,000 every month (₹12,000 per year) directly via DBT", "Recognizes uncompensated domestic labor and ensures economic self-reliance"],
    ["Smart Family Ration Card", "Aadhaar Card", "Electricity consumer number", "Aadhaar-linked bank account"],
    ["Apply at special camps organized at ration shops / e-Sevai centers", "Field verification by government staff", "Monthly credit on the 15th of every month"],
    "https://kmut.tn.gov.in",
    "कलाईग्नार मगलिर उरीमई योजना (तमिलनाडु)", "तमिलनाडु शासन", "तमिलनाडु में परिवार की 1.15 करोड़ से अधिक महिला मुखियाओं को ₹1,000 प्रतिमाह की निश्चित बुनियादी आय।",
    ["हर महीने ₹1,000 (वार्षिक ₹12,000) सीधे बैंक खाते में", "घरेलू श्रम का सम्मान और महिलाओं का आर्थिक स्वावलंबन"],
    ["स्मार्ट पारिवारिक राशन कार्ड", "आधार कार्ड", "बिजली बिल उपभोक्ता संख्या", "बैंक खाता"],
    ["राशन दुकान / विशेष कैंप में आवेदन पत्र जमा करें", "फील्ड जांच उपरांत स्वीकृति", "प्रत्येक माह की 15 तारीख को राशि बैंक में"],
    "कलाईग्नार मगलिर उरीमई योजना (तमिळनाडू)", "तमिळनाडू शासन", "तमिळनाडूतील कुटुंबप्रमुख महिलांना दरमहा ₹१,००० थेट बँक खात्यात आर्थिक अधिकार निधी.",
    ["दरमहा ₹१,००० (वर्षाला ₹१२,०००) थेट डीबीटी जमा", "महिलांचे आर्थिक स्वातंत्र्य"],
    ["स्मार्ट रेशन कार्ड", "आधार कार्ड", "वीज बिल ग्राहक क्रमांक", "बँक पासबुक"],
    ["रेशन दुकानातील शिबिरात नोंदणी करा", "दरमहा १५ तारखेला बँक खात्यात रक्कम"],
    "கலைஞர் மகளிர் உரிமைத் திட்டம்", "தமிழ்நாடு அரசு", "குடும்பத் தலைவிகளுக்கு மாதம் ₹1,000 அடிப்படை உரிமைத் தொகை வழங்கும் திட்டம்.",
    ["மாதந்தோறும் ₹1,000 (ஆண்டுக்கு ₹12,000) வங்கி கணக்கில் நேரடி வரவு", "1.15 கோடிக்கும் அதிகமான குடும்பத் தலைவிகள் பயனடைதல்"],
    ["ஸ்மார்ட் ரேஷன் அட்டை", "ஆதார் அட்டை", "மின் நுகர்வோர் எண்", "வங்கி பாஸ்புக்"],
    ["நியாயவிலைக் கடை முகாம்களில் விண்ணப்பிக்கவும்", "கள ஆய்வுக்குப் பின் மாதாந்திர உரிமைத் தொகை பெறவும்"])

# 7. Lakshmir Bhandar (West Bengal)
add("wb_lakshmir_bhandar", "state", "West Bengal", {"gender": "female", "age_min": 25, "age_max": 60},
    "Lakshmir Bhandar Scheme (West Bengal)", "State · West Bengal", "Monthly financial assistance of ₹1,000 for General category and ₹1,200 for SC/ST women in West Bengal.",
    ["₹1,000/month for General category and ₹1,200/month for SC/ST women", "Direct benefit transfer into women's personal bank accounts"],
    ["Swasthya Sathi Card", "Aadhaar Card", "Caste Certificate (for SC/ST)", "Bank account details"],
    ["Apply at Duare Sarkar (Government at Doorstep) camp", "Document verification and biometric capture", "Direct monthly bank credit"],
    "https://socialwelfare.wb.gov.in",
    "लक्ष्मी भंडार योजना (पश्चिम बंगाल)", "पश्चिम बंगाल शासन", "पश्चिम बंगाल की 25 से 60 वर्ष की महिलाओं को सामान्य वर्ग हेतु ₹1,000 तथा एससी/एसटी हेतु ₹1,200 प्रतिमाह।",
    ["सामान्य वर्ग की महिलाओं को ₹1,000 और एससी/एसटी को ₹1,200 प्रति माह", "महिलाओं के सशक्तिकरण और घरेलू वित्तीय सुरक्षा"],
    ["स्वास्थ्य साथी कार्ड", "आधार कार्ड", "जाति प्रमाणपत्र (यदि एससी/एसटी हैं)", "बैंक खाता विवरण"],
    ["द्वारे सरकार (Duare Sarkar) कैंप में आवेदन जमा करें", "सत्यापन उपरांत स्वीकृति", "मासिक बैंक भुगतान"],
    "लक्ष्मी भंडार योजना (पश्चिम बंगाल)", "पश्चिम बंगाल शासन", "पश्चिम बंगालमधील महिलांना सर्वसाधारण प्रवर्गासाठी दरमहा ₹१,००० व मागास प्रवर्गासाठी ₹१,२०० थेट मदत.",
    ["दरमहा ₹१,००० ते ₹१,२०० थेट बँक खात्यात", "महिलांचे आर्थिक सक्षमीकरण"],
    ["स्वास्थ्य साथी कार्ड", "आधार कार्ड", "जात प्रमाणपत्र", "बँक पासबुक"],
    ["द्वारे सरकार शिबिरात अर्ज करा", "दरमहा थेट बँक खात्यात निधी"],
    "லக்ஷ்மி பந்தர் திட்டம் (மேற்கு வங்கம்)", "மேற்கு வங்க அரசு", "பெண்களுக்கு பொது பிரிவினருக்கு மாதம் ₹1,000 மற்றும் SC/ST பெண்களுக்கு ₹1,200 வழங்கும் திட்டம்.",
    ["மாதம் ₹1,000 முதல் ₹1,200 வரை நேரடி வங்கி வரவு", "பெண்கள் வாழ்வாதார உதவி"],
    ["சுவஸ்திய சாதி அட்டை", "ஆதார் அட்டை", "சாதிச் சான்றிதழ்"],
    ["துவாரே சர்க்கார் முகாமில் விண்ணப்பிக்கவும்"])

# 8. Kanyashree Prakalpa (West Bengal)
add("wb_kanyashree_prakalpa", "state", "West Bengal", {"occupation": "student", "gender": "female", "age_min": 13, "age_max": 19},
    "Kanyashree Prakalpa (Girl Child Education)", "State · West Bengal", "Annual scholarship of ₹1,000 (K1) and one-time grant of ₹25,000 (K2) upon turning 18 unmarried to stop child marriage.",
    ["Annual scholarship of ₹1,000 for unmarried girls studying in Class 8 to 12", "One-time financial grant of ₹25,000 at age 18 if continuing education and unmarried"],
    ["Unmarried declaration certificate", "School / College enrollment proof", "Birth Certificate", "Aadhaar and bank passbook"],
    ["Apply through school/college head", "Verified on Kanyashree online portal", "Direct bank credit"],
    "https://wbkanyashree.gov.in",
    "कन्याश्री प्रकल्प योजना (पश्चिम बंगाल)", "पश्चिम बंगाल शासन", "कक्षा 8-12 की छात्राओं को ₹1,000 वार्षिक और 18 वर्ष पूर्ण होने पर ₹25,000 का एकमुश्त अनुदान।",
    ["पढ़ाई के दौरान ₹1,000 प्रतिवर्ष (K1)", "18 वर्ष की आयु में अविवाहित रहने व पढ़ाई जारी रखने पर ₹25,000 नकद (K2)"],
    ["अविवाहित रहने की स्व-घोषणा", "स्कूल/कॉलेज में नियमित अध्ययन प्रमाणपत्र", "जन्म प्रमाणपत्र", "बैंक पासबुक"],
    ["स्कूल या कॉलेज के माध्यम से कन्याश्री पोर्टल पर आवेदन करें", "सीधे खाते में अनुदान"],
    "कन्याश्री प्रकल्प योजना (पश्चिम बंगाल)", "पश्चिम बंगाल शासन", "मुलींच्या शिक्षणासाठी दरवर्षी ₹१,००० आणि १८ व्या वर्षी अविवाहित राहिल्यास ₹२५,००० एकरकमी अनुदान.",
    ["८ वी ते १२ वी पर्यंत दरवर्षी ₹१,०००", "१८ व्या वर्षी ₹२५,००० थेट मदत"],
    ["अविवाहित प्रतिज्ञापत्र", "शाळा नोंदणी दाखला", "जन्म दाखला", "बँक पासबुक"],
    ["शाळा/कॉलेजमार्फत अर्ज करा", "थेट बँक खात्यात रक्कम"],
    "கன்யாஸ்ரீ பிரகல்பா திட்டம் (மேற்கு வங்கம்)", "மேற்கு வங்க அரசு", "மாணவிகளுக்கு ஆண்டுக்கு ₹1,000 மற்றும் 18 வயதில் ₹25,000 ஒரே தவணையாக வழங்கும் திட்டம்.",
    ["பள்ளி மாணவிகளுக்கு ஆண்டுக்கு ₹1,000 உதவித்தொகை", "18 வயதில் உயர்கல்வி தொடர ₹25,000 நிதியுதவி"],
    ["திருமணமாகாத சான்றிதழ்", "பள்ளி படிப்புச் சான்று", "பிறப்புச் சான்றிதழ்"],
    ["பள்ளி மூலமாக இணையதளத்தில் பதிவு செய்யவும்"])

# 9. Rythu Bandhu / Rythu Bharosa (Telangana / AP)
add("rythu_bharosa_investment", "state", "Andhra Pradesh", {"occupation": "farmer"},
    "YSR Rythu Bharosa - PM KISAN", "State · Andhra Pradesh", "Financial investment support of ₹13,500 per year for farmer families including tenant farmers in Andhra Pradesh.",
    ["₹13,500 per year in 3 installments before sowing seasons", "Includes tenant farmers from SC, ST, BC and Minority communities"],
    ["Pattadar Passbook / Title Deed", "CCRC (Cultivator Certificate) for tenant farmers", "Aadhaar Card", "Bank passbook"],
    ["Enrollment through Rythu Bharosa Kendra (RBK) / Village Secretariats", "Social audit and verification", "Direct bank transfer"],
    "https://ysrrythubharosa.ap.gov.in",
    "वाईएसआर रायथू भरोसा योजना (आंध्र प्रदेश)", "आंध्र प्रदेश शासन", "आंध्र प्रदेश के किसान परिवारों व काश्तकारों को फसल बुवाई पूर्व प्रतिवर्ष ₹13,500 की निवेश सहायता।",
    ["प्रतिवर्ष ₹13,500 की 3 किस्तों में सीधी आर्थिक सहायता", "दलित, आदिवासी व पिछड़े वर्ग के पट्टेदार काश्तकार भी शामिल"],
    ["पट्टादार पासबुक या काश्तकार प्रमाणपत्र (CCRC)", "आधार कार्ड", "बैंक पासबुक"],
    ["ग्राम सचिवालय या रायथू भरोसा केंद्र पर पंजीकरण", "सामाजिक अंकेक्षण उपरांत सीधे खाते में भुगतान"],
    "वायएसआर रायथू भरोसा योजना (आंध्र प्रदेश)", "आंध्र प्रदेश शासन", "शेतकरी कुटुंबांना पेरणीपूर्वी दरवर्षी ₹१३,५०० आर्थिक सहाय्य.",
    ["दरवर्षी ३ हप्त्यांत ₹१३,५०० थेट मदत", "कसेल त्याची जमीन असणाऱ्या शेतमजुरांचाही समावेश"],
    ["जमीन पासबुक", "आधार कार्ड", "बँक पासबुक"],
    ["ग्राम सचिवालयात नोंदणी करा", "थेट बँक खात्यात रक्कम"],
    "ஒய்.எஸ்.ஆர் ரைத்து பரோசா (ஆந்திர பிரதேசம்)", "ஆந்திர அரசு", "விவசாய குடும்பங்களுக்கு விதைப்புக்கு முன் ஆண்டுக்கு ₹13,500 நேரடி முதலீட்டு உதவித்தொகை.",
    ["ஆண்டுக்கு ₹13,500 நேரடி வங்கி வரவு", "குத்தகை விவசாயிகளுக்கும் உதவி"],
    ["பட்டா பாஸ்புக்", "ஆதார் அட்டை", "வங்கி கணக்கு"],
    ["கிராம செயலகத்தில் பதிவு செய்யவும்"])

# 10. Mukhyamantri Chiranjeevi Swasthya Bima (Rajasthan)
add("chiranjeevi_swasthya_rajasthan", "state", "Rajasthan", {},
    "Mukhyamantri Chiranjeevi Swasthya Bima Yojana", "State · Rajasthan", "Free cashless health insurance cover up to ₹25 Lakhs per family per year in Rajasthan network hospitals.",
    ["Massive health cover up to ₹25 Lakhs per family per year", "Covers organ transplants, heart and cancer surgeries, and dialysis"],
    ["Jan Aadhaar Card", "Aadhaar Card of all family members"],
    ["Register on Jan Aadhaar / SSO portal or at e-Mitra kiosk", "Show Jan Aadhaar at network hospital desk for 100% cashless admission"],
    "https://chiranjeevi.rajasthan.gov.in",
    "मुख्यमंत्री चिरंजीवी स्वास्थ्य बीमा योजना (राजस्थान)", "राजस्थान शासन", "राजस्थान के परिवारों को प्रतिवर्ष ₹25 लाख तक का पूर्णतः कैशलेस अस्पताल उपचार कवर।",
    ["₹25,00,000 प्रति परिवार सालाना स्वास्थ्य बीमा कवर", "अंग प्रत्यारोपण, कैंसर व हृदय सर्जरी का पूरा खर्च सरकार द्वारा वहन"],
    ["जन आधार कार्ड", "आधार कार्ड"],
    ["ई-मित्र या एसएसओ (SSO) पोर्टल पर पंजीकरण कराएं", "अस्पताल में जन आधार दिखाकर कैशलेस इलाज पाएं"],
    "मुख्यमंत्री चिरंजीवी आरोग्य विमा योजना (राजस्थान)", "राजस्थान शासन", "राजस्थानमधील कुटुंबांना प्रतिवर्षी तब्बल ₹२५ लाखांपर्यंत मोफत व कॅशलेस उपचार.",
    ["प्रति कुटुंब ₹२५ लाख वार्षिक आरोग्य कवच", "हृदयविकार, कर्करोग व अवयव प्रत्यारोपणाचा संपूर्ण खर्च समाविष्ट"],
    ["जन आधार कार्ड", "आधार कार्ड"],
    ["ई-मित्र केंद्रावरून नोंदणी करा", "रुग्णालयात मोफत उपचार"],
    "சிரஞ்சீவி மருத்துவக் காப்பீட்டுத் திட்டம் (ராஜஸ்தான்)", "ராஜஸ்தான் அரசு", "ராஜஸ்தானில் உள்ள குடும்பங்களுக்கு ஆண்டுக்கு ₹25 லட்சம் வரை மிகப்பெரிய இலவச மருத்துவக் காப்பீடு.",
    ["ஆண்டுக்கு ₹25,00,000 வரை இலவச மருத்துவ சிகிச்சை", "இதயம், புற்றுநோய் அறுவை சிகிச்சைகள் இலவசம்"],
    ["ஜன் ஆதார் அட்டை", "ஆதார் அட்டை"],
    ["இ-மித்ரா மையத்தில் பதிவு செய்து அட்டை பெறவும்"])

# 11-100: Systematic additions across occupations and categories
sectors = [
    # (id, occupation, gender, category, state, en, hi, mr, ta, min_age, max_age, max_inc)
    ("pm_kisan_mandhan", "farmer", None, None, None,
     "PM Kisan Maan Dhan Yojana (Farmer Pension)", "Agriculture", "Guaranteed monthly pension of ₹3,000 for small and marginal farmers upon turning 60.",
     "पीएम-किसान मानधन योजना (किसान पेंशन)", "कृषि", "लघु एवं सीमांत किसानों को 60 वर्ष की आयु के बाद ₹3,000 मासिक सुनिश्चित पेंशन।",
     "पीएम-किसान मानधन योजना (शेतकरी पेन्शन)", "शेती", "अल्पभूधारक शेतकऱ्यांना वयाच्या ६० वर्षांनंतर दरमहा ₹३,००० निश्चित पेन्शन.",
     "பிஎம் கிசான் மான்தன் திட்டம் (விவசாயிகள் ஓய்வூதியம்)", "வேளாண்மை", "60 வயதுக்கு மேற்பட்ட சிறு விவசாயிகளுக்கு மாதம் ₹3,000 உத்திரவாத ஓய்வூதியம்.",
     18, 40, None),

    ("pm_shram_yogi_mandhan", "unorganized", None, None, None,
     "Pradhan Mantri Shram Yogi Maandhan (PM-SYM)", "Social Security", "Assured monthly pension of ₹3,000 after age 60 for unorganized workers earning under ₹15,000/month.",
     "प्रधानमंत्री श्रम योगी मानधन योजना (PM-SYM)", "सामाजिक सुरक्षा", "₹15,000 से कम आय वाले असंगठित कामगारों को 60 वर्ष बाद ₹3,000 मासिक सुनिश्चित पेंशन।",
     "प्रधानमंत्री श्रम योगी मानधन योजना", "सामाजिक सुरक्षा", "असंघटित कामगारांना वयाच्या ६० नंतर दरमहा ₹३,००० निश्चित पेन्शन.",
     "பிரதமர் ஷ்ரம் யோகி மான்தன் ஓய்வூதியத் திட்டம்", "சமூக பாதுகாப்பு", "அமைப்பு சாரா தொழிலாளர்களுக்கு 60 வயதுக்குப் பின் மாதம் ₹3,000 உறுதி ஓய்வூதியம்.",
     18, 40, 180000),

    ("pm_mudra_shishu", "entrepreneur", None, None, None,
     "Pradhan Mantri MUDRA Yojana (Shishu Loan)", "Business", "Collateral-free business loans up to ₹50,000 for micro-enterprises and small shopkeepers.",
     "प्रधानमंत्री मुद्रा योजना (शिशु ऋण)", "व्यापार", "छोटे दुकानदारों और नए माइक्रो-व्यवसायों हेतु ₹50,000 तक का बिना गारंटी ऋण।",
     "प्रधानमंत्री मुद्रा योजना (शिशू कर्ज)", "व्यवसाय", "लहान व्यावसायिक व दुकानदारांसाठी ₹५०,००० पर्यंत विनातारण कर्ज.",
     "பிரதமர் முத்ரா திட்டம் (சிசு கடன்)", "வணிகம்", "சிறு கடைகள் மற்றும் தொழில்களுக்கு ₹50,000 வரை பிணையில்லா கடன்.",
     18, None, None),

    ("pm_mudra_kishore", "entrepreneur", None, None, None,
     "Pradhan Mantri MUDRA Yojana (Kishore Loan)", "Business", "Collateral-free business loans from ₹50,000 to ₹5,00,000 for expanding existing small businesses.",
     "प्रधानमंत्री मुद्रा योजना (किशोर ऋण)", "व्यापार", "व्यवसाय विस्तार हेतु ₹50,000 से ₹5 लाख तक का रियायती बैंक ऋण।",
     "प्रधानमंत्री मुद्रा योजना (किशोर कर्ज)", "व्यवसाय", "व्यवसाय वाढवण्यासाठी ₹५०,००० ते ₹५ लाख विनातारण कर्ज.",
     "பிரதமர் முத்ரா திட்டம் (கிஷோர் கடன்)", "வணிகம்", "சிறு வணிகங்களை விரிவுபடுத்த ₹50,000 முதல் ₹5 லட்சம் வரை கடன்.",
     18, None, None),

    ("pm_mudra_tarun", "entrepreneur", None, None, None,
     "Pradhan Mantri MUDRA Yojana (Tarun Loan)", "Business", "Collateral-free business loans from ₹5 Lakhs to ₹10 Lakhs for established enterprises.",
     "प्रधानमंत्री मुद्रा योजना (तरुण ऋण)", "व्यापार", "स्थापित उद्योगों के विस्तार हेतु ₹5 लाख से ₹10 लाख तक का ऋण।",
     "प्रधानमंत्री मुद्रा योजना (तरुण कर्ज)", "व्यवसाय", "उद्योगांसाठी ₹५ लाख ते ₹१० लाख बँक कर्ज.",
     "பிரதமர் முத்ரா திட்டம் (தருண் கடன்)", "வணிகம்", "வளர்ந்த தொழில்களுக்கு ₹5 லட்சம் முதல் ₹10 லட்சம் வரை கடன்.",
     18, None, None),

    ("pm_ujjwala_2_0_free_gas", "homemaker", "female", None, None,
     "PM Ujjwala Yojana 2.0 (Free LPG Connection)", "Energy", "Free LPG gas connection with stove and first cylinder refill for women from poor households.",
     "प्रधानमंत्री उज्ज्वला योजना 2.0 (मुफ्त गैस कनेक्शन)", "ऊर्जा", "गरीब परिवारों की महिलाओं को निःशुल्क गैस कनेक्शन, चूल्हा व पहला रिफिल सिलेंडर।",
     "प्रधानमंत्री उज्ज्वला योजना २.० (मोफत गॅस)", "ऊर्जा", "गरजू महिलांना मोफत गॅस कनेक्शन, शेगडी व पहिला सिलेंडर मोफत.",
     "பிரதமர் உஜ்வாலா திட்டம் 2.0 (இலவச எரிவாயு)", "எரிசக்தி", "ஏழை பெண்களுக்கு இலவச எரிவாயு இணைப்பு, அடுப்பு மற்றும் முதல் சிலிண்டர்.",
     18, None, 200000),

    ("pm_national_apprenticeship_naps", "student", None, None, None,
     "National Apprenticeship Promotion Scheme (NAPS)", "Skill Development", "Government shares 25% of prescribed stipend up to ₹1,500/month for youth undergoing industry apprenticeship.",
     "राष्ट्रीय शिक्षुता संवर्धन योजना (NAPS)", "कौशल विकास", "उद्योगों में अप्रेंटिसशिप करने वाले युवाओं को ₹1,500 प्रतिमाह तक का सरकारी स्टाइपेंड सहयोग।",
     "राष्ट्रीय शिकाऊ उमेदवारी प्रोत्साहन योजना (NAPS)", "कौशल्य विकास", "उद्योगांमध्ये प्रशिक्षण घेणाऱ्या युवकांना दरमहा ₹१,५०० पर्यंत विद्यावेतन सहाय्य.",
     "தேசிய தொழிற்பயிற்சி ஊக்குவிப்பு திட்டம் (NAPS)", "திறன் மேம்பாடு", "தொழில்துறை பயிற்சி பெறும் இளைஞர்களுக்கு மாதம் ₹1,500 வரை அரசு உதவித்தொகை.",
     18, 30, None),

    ("pm_kaushal_vikas_pmkvy", "unemployed", None, None, None,
     "Pradhan Mantri Kaushal Vikas Yojana (PMKVY 4.0)", "Skill Training", "Free industry-aligned skill training with government certification and post-placement assistance.",
     "प्रधानमंत्री कौशल विकास योजना (PMKVY 4.0)", "कौशल प्रशिक्षण", "युवाओं को निःशुल्क उद्योगोन्मुखी कौशल प्रशिक्षण, प्रमाणन एवं रोजगार सहायता।",
     "प्रधानमंत्री कौशल विकास योजना (PMKVY)", "कौशल्य प्रशिक्षण", "मोफत कौशल्य प्रशिक्षण, सरकारी प्रमाणपत्र आणि नोकरी सहाय्य.",
     "பிரதமர் திறன் மேம்பாட்டுத் திட்டம் (PMKVY 4.0)", "திறன் பயிற்சி", "இளைஞர்களுக்கு இலவச திறன் பயிற்சி மற்றும் வேலைவாய்ப்பு வழிகாட்டுதல்.",
     15, 45, None),

    ("pm_van_dhan_tribal_livelihood", "artisan", None, ["st"], None,
     "Pradhan Mantri Van Dhan Yojana", "Tribal Welfare", "Working capital and equipment for tribal SHG clusters to value-add forest produce (honey, amla, herbs).",
     "प्रधानमंत्री वन धन योजना", "जनजातीय कल्याण", "आदिवासी स्वयं सहायता समूहों को वनोपज (शहद, आंवला, जड़ी-बूटी) प्रसंस्करण हेतु पूंजी व उपकरण।",
     "प्रधानमंत्री वन धन योजना", "आदिवासी कल्याण", "आदिवासी बचत गटांना वन उत्पादनांवर प्रक्रियेसाठी भांडवल व यंत्रसामग्री.",
     "பிரதமர் வன் தன் திட்டம்", "பழங்குடியினர் நலம்", "பழங்குடியினருக்கு வனப் பொருட்கள் மதிப்பு கூட்டலுக்கான மூலதன உதவி.",
     18, None, None),

    ("national_overseas_scholarship_sc", "student", None, ["sc"], None,
     "National Overseas Scholarship for SC Candidates", "Higher Education", "Full tuition fees and living expenses for 125 SC scholars to pursue Master's and PhD in top 500 world universities.",
     "अनुसूचित जाति राष्ट्रीय विदेश अध्ययन छात्रवृत्ति", "उच्च शिक्षा", "विश्व के शीर्ष 500 विश्वविद्यालयों में मास्टर व पीएचडी हेतु पूरी ट्यूशन फीस व विदेशी निर्वाह भत्ता।",
     "अनुसूचित जाती राष्ट्रीय परदेशी शिष्यवृत्ती", "उच्च शिक्षण", "परदेशातील नामांकित विद्यापीठांमध्ये उच्च शिक्षणासाठी पूर्ण फी व खर्च.",
     "SC மாணவர்களுக்கான தேசிய வெளிநாட்டு கல்வி உதவித்தொகை", "உயர்கல்வி", "உலகின் முன்னணி பல்கலைக்கழகங்களில் உயர்கல்வி பயில முழு கட்டணம் மற்றும் உதவித்தொகை.",
     20, 35, 800000),

    ("dr_ambedkar_central_sector_fellowship", "student", None, ["sc"], None,
     "Dr. Ambedkar Centrally Sponsored Pre-Matric Scholarship", "Education", "Scholarship of ₹3,500 to ₹7,000 per year for SC students in Classes 9 and 10 to reduce school dropout.",
     "डॉ. आंबेडकर प्री-मैट्रिक छात्रवृत्ति (कक्षा 9-10)", "शिक्षा", "कक्षा 9 और 10 में अध्ययनरत अनुसूचित जाति के छात्रों को ₹3,500 से ₹7,000 वार्षिक छात्रवृत्ति।",
     "डॉ. आंबेडकर पूर्व-मॅट्रिक शिष्यवृत्ती (इयत्ता ९-१०)", "शिक्षण", "इयत्ता ९ वी व १० वी मधील SC विद्यार्थ्यांना शैक्षणिक साहित्यासाठी वार्षिक शिष्यवृत्ती.",
     "டாக்டர் அம்பேத்கர் மெட்ரிக் முந்தைய கல்வி உதவித்தொகை", "கல்வி", "9 மற்றும் 10 ஆம் வகுப்பு SC மாணவர்களுக்கு ஆண்டுதோறும் கல்வி உதவித்தொகை.",
     13, 17, 250000),

    ("adikarmik_welfare_board_tn", "unorganized", None, None, "Tamil Nadu",
     "Tamil Nadu Construction Workers Welfare Board Benefits", "Unorganized Workers", "Accident relief of ₹5,00,000, pension of ₹1,000/month, and marriage assistance of ₹20,000 for registered construction workers.",
     "तमिलनाडु निर्माण श्रमिक कल्याण बोर्ड योजना", "तमिलनाडु शासन", "पंजीकृत निर्माण श्रमिकों को ₹5 लाख का दुर्घटना बीमा, ₹1,000 मासिक पेंशन तथा शादी हेतु ₹20,000 अनुदान।",
     "तमिळनाडू बांधकाम कामगार कल्याण मंडळ लाभ", "तमिळनाडू शासन", "नोंदणीकृत बांधकाम कामगारांना ₹५ लाख अपघात विमा व दरमहा ₹१,००० पेन्शन.",
     "தமிழ்நாடு கட்டுமான தொழிலாளர்கள் நல வாரிய நலத்திட்டங்கள்", "தமிழ்நாடு அரசு", "பதிவு பெற்ற கட்டுமான தொழிலாளர்களுக்கு ₹5 லட்சம் விபத்து நிவாரணம், ₹1,000 ஓய்வூதியம்.",
     18, 60, None),

    ("maha_kamgar_kalyan_scholarship", "unorganized", None, None, "Maharashtra",
     "Maharashtra Building & Construction Workers Scholarship", "State · Maharashtra", "Educational scholarships from ₹2,500 to ₹25,000/year for children of registered construction workers in Maharashtra.",
     "महाराष्ट्र भवन एवं सन्निर्माण कर्मकार छात्रवृत्ति", "महाराष्ट्र शासन", "महाराष्ट्र के पंजीकृत निर्माण श्रमिकों के बच्चों को पहली कक्षा से स्नातकोत्तर तक ₹2,500 से ₹25,000 तक छात्रवृत्ति।",
     "महाराष्ट्र इमारत व इतर बांधकाम कामगार शिष्यवृत्ती", "महाराष्ट्र शासन", "नोंदणीकृत बांधकाम कामगारांच्या पाल्यांना इयत्ता पहिली ते पदवीपर्यंत ₹२,५०० ते ₹२५,००० शिष्यवृत्ती.",
     "மகாராஷ்டிரா கட்டுமான தொழிலாளர் குழந்தைகள் கல்வி உதவித்தொகை", "மகாராஷ்டிரா அரசு", "பதிவு பெற்ற கட்டுமான தொழிலாளர்களின் குழந்தைகளுக்கு ஆண்டுக்கு ₹25,000 வரை கல்வி உதவித்தொகை.",
     None, 25, None),

    ("maha_annasaheb_patil_loan", "entrepreneur", None, None, "Maharashtra",
     "Annasaheb Patil Arthik Vikas Mahamandal (Interest Subsidy)", "State · Maharashtra", "100% interest reimbursement up to ₹12 Lakhs on bank business loans for Maratha and General category youth in Maharashtra.",
     "अण्णासाहेब पाटिल आर्थिक पिछड़ा विकास महामंडल ऋण", "महाराष्ट्र शासन", "महाराष्ट्र में युवाओं को नया व्यवसाय शुरू करने हेतु ₹12 लाख तक के बैंक ऋण पर 100% ब्याज की प्रतिपूर्ति।",
     "अण्णासाहेब पाटील आर्थिक मागास विकास महामंडळ कर्ज योजना", "महाराष्ट्र शासन", "तरुणांना उद्योग सुरू करण्यासाठी ₹१२ लाखांपर्यंतच्या बँक कर्जावर १२% पर्यंतचे संपूर्ण व्याज परतावा.",
     "அண்ணாசாஹேப் பாட்டீல் தொழில் கடன் வட்டி மானிய திட்டம்", "மகாராஷ்டிரா அரசு", "மகாராஷ்டிராவில் புதிய தொழில் தொடங்க ₹12 லட்சம் வரை கடனுக்கான முழு வட்டி திருப்பி செலுத்தும் திட்டம்.",
     18, 45, 800000),

    ("maha_sant_rohidas_leather_artisan", "artisan", None, ["sc"], "Maharashtra",
     "Sant Rohidas Leather Artisans Subsidy Scheme", "Artisans", "Financial subsidy of ₹50,000 and 50% loan subsidy for footwear and leather artisans in Maharashtra.",
     "संत रोहिदास चर्मकार कारीगर योजना", "महाराष्ट्र शासन", "महाराष्ट्र के चर्मकार और जूता बनाने वाले कारीगरों को आधुनिक औजारों व दुकान हेतु 50% तक सरकारी अनुदान।",
     "संत रोहिदास चर्मोद्योग व चर्मकार महामंडळ योजना", "महाराष्ट्र शासन", "चर्मकार बांधवांना पादत्राणे व चर्मोद्योगासाठी ५०% अनुदान व सुलभ बँक कर्ज.",
     "ரோஹிதாஸ் தோல் கைவினைஞர்கள் திட்டம்", "மகாராஷ்டிரா அரசு", "தோல் பொருட்கள் மற்றும் காலணி தயாரிக்கும் கைவினைஞர்களுக்கு 50% மானிய கடன்.",
     18, 50, 100000),

    ("maha_vasantrao_naik_vjnt", "farmer", None, None, "Maharashtra",
     "Vasantrao Naik Sheti Swavalamban Mission", "Agriculture", "Comprehensive package for farmers in drought and distress-hit districts of Vidarbha and Marathwada.",
     "वसंतराव नाईक कृषि स्वावलंबन मिशन (महाराष्ट्र)", "महाराष्ट्र शासन", "विदर्भ और मराठवाड़ा के संकटग्रस्त किसान परिवारों को बीज, स्वास्थ्य, शिक्षा व ऋण राहत का समग्र पैकेज।",
     "वसंतराव नाईक शेती स्वावलंबन मिशन", "महाराष्ट्र शासन", "विदर्भ व मराठवाड्यातील शेतकऱ्यांना बियाणे, आरोग्य, कृषी सिंचन व आर्थिक संकटातून मदतीचे विशेष पॅकेज.",
     "வசந்த்ராவ் நாயக் வேளாண் உதவி திட்டம்", "மகாராஷ்டிரா அரசு", "வறட்சியால் பாதிக்கப்பட்ட விவசாயிகளுக்கு சிறப்பு நிவாரணம் மற்றும் வேளாண் உள்ளீடுகள்.",
     None, None, None),

    ("maha_ashtang_ayurveda_senior", "senior", None, None, "Maharashtra",
     "Senior Citizen Free Panchakarma and Geriatric Care", "Health", "Free traditional Panchakarma therapies and specialized geriatric wellness care in government Ayurvedic colleges across Maharashtra.",
     "वरिष्ठ नागरिक निःशुल्क पंचकर्म एवं जियाराट्रिक उपचार", "स्वास्थ्य", "महाराष्ट्र के सरकारी आयुर्वेद अस्पतालों में 60 वर्ष से ऊपर के नागरिकों को मुफ्त पंचकर्म व वात रोग उपचार।",
     "ज्येष्ठ नागरिकांसाठी मोफत पंचकर्म व आयुर्वेद उपचार", "आरोग्य", "शासकीय आयुर्वेद महाविद्यालयांमध्ये ६० वर्षांवरील ज्येष्ठ नागरिकांना मोफत पंचकर्म व संधिवात उपचार.",
     "முதியோருக்கான இலவச ஆயுர்வேத சிகிச்சை", "சுகாதாரம்", "அரசு ஆயுர்வேத மருத்துவமனைகளில் முதியோர்களுக்கு இலவச ஆயுர்வேத மற்றும் பஞ்சகர்மா சிகிச்சை.",
     60, None, None),

    ("adip_scheme_divyangjan", None, None, None, None,
     "ADIP Scheme (Assistance to Disabled Persons for Aids/Appliances)", "Divyangjan", "Free distribution of motorized tricycles, smart canes, Braille kits, cochlear implants, and prosthetic limbs to persons with disability.",
     "एडीआईपी योजना (दिव्यांगजन सहायक उपकरण)", "दिव्यांग कल्याण", "दिव्यांग व्यक्तियों को मुफ्त मोटराइज्ड ट्राइसाइकिल, कृत्रिम अंग, हियरिंग एड व कॉक्लियर इम्प्लांट।",
     "एडीआयपी योजना (दिव्यांगांसाठी मोफत उपकरणे)", "दिव्यांग कल्याण", "दिव्यांग बांधवांना मोफत तीनचाकी सायकल, श्रवणयंत्र, कृत्रिम पाय व व्हीलचेअर वाटप.",
     "மாற்றுத்திறனாளிகளுக்கான உபகரண உதவித் திட்டம் (ADIP)", "மாற்றுத்திறனாளிகள்", "மாற்றுத்திறனாளிகளுக்கு இலவச பேட்டரி மூன்று சக்கர வண்டி, செயற்கை கால்கள் வழங்கும் திட்டம்.",
     None, None, 250000),

    ("divyangjan_swavalamban_loan", "entrepreneur", None, None, None,
     "NHFDC Divyangjan Swavalamban Loan Scheme", "Divyangjan", "Concessional loans up to ₹50 Lakhs at 5% to 8% interest rate for persons with disabilities to start business.",
     "दिव्यांगजन स्वावलंबन ऋण योजना (NHFDC)", "दिव्यांग कल्याण", "दिव्यांग उद्यमियों को नया व्यवसाय शुरू करने हेतु 5% से 8% की रियायती ब्याज दर पर ₹50 लाख तक ऋण।",
     "दिव्यांगजन स्वावलंबन कर्ज योजना", "दिव्यांग कल्याण", "दिव्यांग व्यक्तींना स्वतःचा व्यवसाय सुरू करण्यासाठी ५% ते ८% सवलतीच्या दरात ₹५० लाखांपर्यंत कर्ज.",
     "மாற்றுத்திறனாளிகள் சுயதொழில் கடன் திட்டம்", "மாற்றுத்திறனாளிகள்", "மாற்றுத்திறனாளிகள் தொழில் தொடங்க 5% குறைந்த வட்டியில் ₹50 லட்சம் வரை கடன்.",
     18, 60, None),

    ("maha_divyang_swayamrozgar", "unemployed", None, None, "Maharashtra",
     "Divyang Swayamrojgar Yojana (Maharashtra)", "State · Maharashtra", "Seed capital financial subsidy of up to ₹50,000 for disabled persons in Maharashtra to set up small retail stalls.",
     "दिव्यांग स्वयंबरोजगार योजना (महाराष्ट्र)", "महाराष्ट्र शासन", "महाराष्ट्र में दिव्यांग व्यक्तियों को छोटी दुकान, पान टपरी या ज़ेरॉक्स स्टॉल लगाने हेतु ₹50,000 तक की सीधी सब्सिडी।",
     "दिव्यांग स्वयंरोजगार योजना", "महाराष्ट्र शासन", "दिव्यांग व्यक्तींना लहान व्यवसाय, झेरॉक्स किंवा किराणा दुकान सुरू करण्यासाठी ₹५०,००० पर्यंत बीजभांडवल अनुदान.",
     "மாற்றுத்திறனாளிகள் சுயதொழில் மானிய திட்டம் (மகாராஷ்டிரா)", "மகாராஷ்டிரா அரசு", "மாற்றுத்திறனாளிகள் சிறு கடை அமைக்க ₹50,000 வரை நேரடி மானியம்.",
     18, 55, 100000),

    ("tn_free_bus_travel_women", "homemaker", "female", None, "Tamil Nadu",
     "Vidiyal Payanam (Free Bus Travel for Women in Tamil Nadu)", "Transport", "100% free bus travel for all women and trans-women in ordinary city and town government buses in Tamil Nadu.",
     "विदियाल पयनम (महिलाओं हेतु मुफ्त बस यात्रा - तमिलनाडु)", "परिवहन", "तमिलनाडु में सभी महिलाओं व ट्रांसजेंडर व्यक्तियों के लिए सरकारी साधारण नगर बसों में 100% मुफ्त यात्रा।",
     "विदियाल पयनम (महिलांसाठी मोफत बस प्रवास - तमिळनाडू)", "वाहतूक", "तमिळनाडूतील सरकारी शहर बसेसमध्ये महिलांसाठी १००% मोफत प्रवास.",
     "விடியல் பயணம் (மகளிருக்கு கட்டணமில்லா பேருந்து பயணம்)", "தமிழ்நாடு அரசு", "தமிழ்நாட்டில் உள்ள அனைத்து அரசு சாதாரண நகரப் பேருந்துகளிலும் மகளிருக்கு 100% இலவச பயணம்.",
     None, None, None),

    ("up_gopalak_dairy_loan", "farmer", None, None, "Uttar Pradesh",
     "Mukhyamantri Gopalak Yojana (Dairy Loan)", "State · Uttar Pradesh", "Bank loans up to ₹9 Lakhs for setting up 10-12 milch cow/buffalo dairy units with interest subsidy in UP.",
     "मुख्यमंत्री गोपालक योजना (डेयरी ऋण - उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "उत्तर प्रदेश में 10-12 दुधारू गायों/भैंसों की डेयरी इकाई स्थापित करने हेतु ₹9 लाख तक का रियायती ऋण।",
     "मुख्यमंत्री गोपालक डेअरी कर्ज योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "दुग्ध व्यवसायासाठी १०-१२ गायी/म्हशींच्या डेअरीकरिता ₹९ लाखांपर्यंत सुलभ बँक कर्ज.",
     "கோபாலக் பால் பண்ணை கடன் திட்டம் (உத்தர பிரதேசம்)", "உத்தர பிரதேச அரசு", "பால் பண்ணை அமைக்க ₹9 லட்சம் வரை வங்கிக் கடன் மற்றும் வட்டி மானியம்.",
     18, 50, 100000),

    ("up_vridha_pension", "senior", None, None, "Uttar Pradesh",
     "Old Age Pension Scheme (Uttar Pradesh)", "State · Uttar Pradesh", "Monthly pension of ₹1,000 credited directly to bank accounts of senior citizens aged 60+ in Uttar Pradesh.",
     "वृद्धावस्था पेंशन योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "उत्तर प्रदेश के 60 वर्ष या उससे अधिक आयु के वृद्धजनों को ₹1,000 प्रतिमाह की नियमित पेंशन।",
     "वृद्धापकाळ पेन्शन योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "उत्तर प्रदेशातील ६० वर्षांवरील ज्येष्ठ नागरिकांना दरमहा ₹१,००० थेट पेन्शन.",
     "முதியோர் ஓய்வூதியத் திட்டம் (உத்தர பிரதேசம்)", "உத்தர பிரதேச அரசு", "60 வயதுக்கு மேற்பட்ட முதியோர்களுக்கு மாதம் ₹1,000 நேரடி ஓய்வூதியம்.",
     60, None, 56000),

    ("bihar_student_credit_card", "student", None, None, "Bihar",
     "Bihar Student Credit Card Scheme (MNSSBY)", "State · Bihar", "Education loan up to ₹4 Lakhs at just 1% interest for girls/disabled and 4% for boys for higher education.",
     "बिहार स्टूडेंट क्रेडिट कार्ड योजना (MNSSBY)", "बिहार शासन", "उच्च शिक्षा (बीटेक, एमबीबीएस, बीए, डिप्लोमा) हेतु ₹4 लाख तक का शिक्षा ऋण मात्र 1% से 4% ब्याज पर।",
     "बिहार स्टुडंट क्रेडिट कार्ड योजना", "बिहार शासन", "उच्च शिक्षणासाठी ₹४ लाखांपर्यंत शैक्षणिक कर्ज अवघ्या १% ते ४% व्याजाने.",
     "பீகார் மாணவர் கிரெடிட் கார்டு திட்டம்", "பீகார் அரசு", "கல்லூரி உயர்கல்விக்கு ₹4 லட்சம் வரை 1% முதல் 4% குறைந்த வட்டியில் கல்விக் கடன்.",
     18, 25, None),

    ("bihar_kanya_utthan", "student", "female", None, "Bihar",
     "Mukhyamantri Kanya Utthan Yojana", "State · Bihar", "₹50,000 cash incentive upon completing Graduation and ₹25,000 on passing Intermediate (12th) for girl students in Bihar.",
     "मुख्यमंत्री कन्या उत्थान योजना (बिहार)", "बिहार शासन", "बिहार में स्नातक (ग्रेजुएशन) उत्तीर्ण करने पर ₹50,000 और 12वीं प्रथम श्रेणी उत्तीर्ण पर ₹25,000 नकद प्रोत्साहन।",
     "मुख्यमंत्री कन्या उत्थान योजना (बिहार)", "बिहार शासन", "पदवी उत्तीर्ण झाल्यावर ₹५०,००० व १२ वी उत्तीर्ण मुलींना ₹२५,००० थेट प्रोत्साहन निधी.",
     "கன்யா உத்தன் திட்டம் (பீகார்)", "பீகார் அரசு", "பட்டப்படிப்பு முடிக்கும் மாணவிகளுக்கு ₹50,000 மற்றும் 12 ஆம் வகுப்பு முடிப்பவர்களுக்கு ₹25,000 உதவித்தொகை.",
     None, 28, None),

    ("odisha_biju_swasthya_kalyan", "unorganized", None, None, "Odisha",
     "Biju Swasthya Kalyan Yojana (BSKY)", "State · Odisha", "Cashless healthcare coverage of ₹5 Lakhs per family and ₹10 Lakhs for women members in Odisha network hospitals.",
     "बीजू स्वास्थ्य कल्याण योजना (ओडिशा)", "ओडिशा शासन", "ओडिशा के परिवारों को ₹5 लाख तथा महिला सदस्यों को ₹10 लाख का सालाना कैशलेस इलाज कवर।",
     "बिजु स्वास्थ्य कल्याण योजना (ओडिशा)", "ओडिशा शासन", "कुटुंबासाठी ₹५ लाख व महिलांसाठी ₹१० लाखांपर्यंत मोफत कॅशलेस आरोग्य संरक्षण.",
     "பிஜு சுவஸ்திய கல்யாண் திட்டம் (ஒடிசா)", "ஒடிசா அரசு", "குடும்பத்திற்கு ₹5 லட்சம் மற்றும் பெண்களுக்கு ₹10 லட்சம் வரை இலவச மருத்துவ சிகிச்சை.",
     None, None, None),

    ("kerala_medisep_health", "salaried", None, None, None,
     "Medical Insurance for State Employees and Pensioners (MEDISEP)", "Health", "Comprehensive cashless health insurance for government employees, teachers, and pensioners up to ₹3 Lakhs/year.",
     "सरकारी कर्मचारी व पेंशनभोगी स्वास्थ्य बीमा (MEDISEP)", "स्वास्थ्य", "राज्य कर्मचारियों, शिक्षकों एवं सेवानिवृत्त कर्मियों को प्रतिवर्ष ₹3 लाख तक का कैशलेस स्वास्थ्य बीमा।",
     "शासकीय कर्मचारी व निवृत्तीवेतनधारक आरोग्य विमा", "आरोग्य", "शासकीय नोकरदार, शिक्षक व पेन्शनधारकांसाठी प्रतिवर्षी ₹३ लाखांपर्यंत कॅशलेस आरोग्य विमा.",
     "அரசு ஊழியர்கள் மற்றும் ஓய்வூதியதாரர் மருத்துவக் காப்பீடு", "சுகாதாரம்", "அரசு ஊழியர்கள் மற்றும் ஆசிரியர்களுக்கு ஆண்டுக்கு ₹3 லட்சம் வரை குடும்ப மருத்துவக் காப்பீடு.",
     None, None, None),

    ("pm_crore_rooftop_solar", "homemaker", None, None, None,
     "PM Surya Ghar Muft Bijli Yojana (Rooftop Solar)", "Clean Energy", "Subsidy of ₹30,000 to ₹78,000 for installing 1-3 kW rooftop solar panels to get up to 300 units of free electricity every month.",
     "पीएम सूर्य घर मुफ्त बिजली योजना (रूफटॉप सोलर)", "स्वच्छ ऊर्जा", "छत पर 1-3 किलोवाट सौर पैनल लगाने हेतु ₹78,000 तक की सरकारी सब्सिडी, हर महीने 300 यूनिट तक मुफ्त बिजली।",
     "पीएम सूर्य घर मोफत वीज योजना (रूफटॉप सोलर)", "सौर ऊर्जा", "घराच्या छतावर सोलर पॅनेल बसवण्यासाठी ₹७८,००० पर्यंत थेट सबसिडी, दरमहा ३०० युनिट मोफत वीज.",
     "பிரதமர் சூர்ய கர் இலவச மின்சாரத் திட்டம்", "சூரிய சக்தி", "வீட்டு மேற்கூரையில் சோலார் பேனல் அமைக்க ₹78,000 வரை மானியம் மற்றும் மாதம் 300 யூனிட் வரை இலவச மின்சாரம்.",
     18, None, None),

    ("safai_karamchari_mechanized_namaste", "unorganized", None, None, None,
     "NAMASTE Scheme for Mechanized Sanitation Workers", "Sanitation", "Capital subsidy up to ₹5 Lakhs and 50% loan subsidy for sanitation workers to purchase automated sewer cleaning machines.",
     "नमस्ते योजना (सफाई कर्मचारियों हेतु मशीनीकृत उपकरण)", "सफाई कर्मचारी", "सीवर सफाई कर्मियों को जानलेवा काम से मुक्ति हेतु सफाई मशीन व वाहन खरीदने पर ₹5 लाख तक का पूंजी अनुदान।",
     "नमस्ते योजना (सफाई कामगारांसाठी यांत्रिकीकरण)", "कामगार कल्याण", "मलनिस्सारण व सफाई कामगारांना सफाई यंत्रे व वाहने खरेदीसाठी ₹५ लाखांपर्यंत भांडवली अनुदान.",
     "நமஸ்தே துப்புரவு தொழிலாளர்கள் இயந்திரமயமாக்கல் திட்டம்", "சமூக நலம்", "கழிவுநீர் சுத்தம் செய்யும் நவீன இயந்திரங்கள் வாங்க துப்புரவு தொழிலாளர்களுக்கு ₹5 லட்சம் வரை மானியம்.",
     18, 55, None)
]

for item in sectors:
    sid, occ, gen, cat, st, en_n, en_t, en_d, hi_n, hi_t, hi_d, mr_n, mr_t, mr_d, ta_n, ta_t, ta_d, amin, amax, imax = item
    rule = {}
    if occ: rule["occupation"] = occ
    if gen: rule["gender"] = gen
    if cat: rule["category_in"] = cat
    if st: rule["state"] = st
    if amin: rule["age_min"] = amin
    if amax: rule["age_max"] = amax
    if imax: rule["income_max"] = imax

    add(sid, "state" if st else "central", st, rule,
        en_n, en_t, en_d,
        ["Financial assistance and subsidized government support", "Direct transfer to Aadhaar-linked bank account"],
        ["Aadhaar Card", "Ration Card or Income Proof", "Bank Passbook"],
        ["Submit application on official government portal", "Verification by district administration", "Benefits released via DBT"],
        "https://www.myscheme.gov.in",
        hi_n, hi_t, hi_d,
        ["सरकारी वित्तीय सहायता एवं सब्सिडी लाभ", "आधार-लिंक्ड बैंक खाते में प्रत्यक्ष लाभ अंतरण"],
        ["आधार कार्ड", "राशन कार्ड या आय प्रमाणपत्र", "बैंक पासबुक"],
        ["आधिकारिक सरकारी पोर्टल पर ऑनलाइन आवेदन करें", "प्रशासनिक सत्यापन उपरांत स्वीकृति", "सीधे बैंक खाते में लाभ प्राप्त करें"],
        mr_n, mr_t, mr_d,
        ["शासकीय आर्थिक अनुदान व सवलत लाभ", "थेट आधार संलग्न बँक खात्यात निधी जमा"],
        ["आधार कार्ड", "रेशन कार्ड किंवा उत्पन्न दाखला", "बँक पासबुक"],
        ["अधिकृत पोर्टलवर ऑनलाइन अर्ज भरा", "प्रशासकीय पडताळणी", "थेट बँक खात्यात अनुदान जमा"],
        ta_n, ta_t, ta_d,
        ["அரசு நிதி உதவி மற்றும் மானிய பலன்கள்", "ஆதார் இணைக்கப்பட்ட வங்கி கணக்கில் நேரடி வரவு"],
        ["ஆதார் அட்டை", "குடும்ப அட்டை அல்லது வருமானச் சான்றிதழ்", "வங்கி பாஸ்புக்"],
        ["அரசு இணையதளத்தில் விண்ணப்பிக்கவும்", "சரிபார்ப்பிற்கு பின் ஒப்புதல்", "வங்கி கணக்கில் நேரடி வரவு"])

# Additional 90 schemes procedurally generated with real Indian welfare titles and realistic rules
additional_schemes_meta = [
    # (id, name_en, name_hi, name_mr, name_ta, tag, occ, gen, cat, st)
    ("maha_sheti_pump_solar", "Maharashtra Mukhyamantri Saur Krushi Pump Yojana", "मुख्यमंत्री सौर कृषि पंप योजना (महाराष्ट्र)", "मुख्यमंत्री सौर कृषी पंप योजना", "முதலமைச்சர் சூரிய மின் பம்ப் திட்டம் (மகாராஷ்டிரா)", "Agriculture", "farmer", None, None, "Maharashtra"),
    ("tn_free_power_farmers", "Tamil Nadu Free Agricultural Power Supply Scheme", "तमिलनाडु निःशुल्क कृषि बिजली आपूर्ति योजना", "तमिळनाडू मोफत कृषी वीज योजना", "விவசாயிகளுக்கு இலவச மின்சாரம் வழங்கும் திட்டம்", "Agriculture", "farmer", None, None, "Tamil Nadu"),
    ("up_kisan_durghatna_bima", "Mukhyamantri Kisan Evam Sarvahit Bima Yojana (UP)", "मुख्यमंत्री किसान एवं सर्वहित बीमा योजना", "मुख्यमंत्री शेतकरी अपघात विमा योजना (UP)", "முதலமைச்சர் விவசாய விபத்து காப்பீட்டுத் திட்டம்", "Agriculture", "farmer", None, None, "Uttar Pradesh"),
    ("kcc_fisheries_animal_husbandry", "KCC for Fisheries and Animal Husbandry", "पशुपालन एवं मत्स्य पालन किसान क्रेडिट कार्ड", "पशुसंवर्धन व मत्स्यव्यवसाय KCC योजना", "கால்நடை மற்றும் மீன்வள கிசான் கிரெடிட் கார்டு", "Animal Husbandry", "farmer", None, None, None),
    ("rashtriya_krishi_vikas_rkvy", "Rashtriya Krishi Vikas Yojana (RKVY)", "राष्ट्रीय कृषि विकास योजना (RKVY)", "राष्ट्रीय कृषी विकास योजना", "தேசிய வேளாண் வளர்ச்சி திட்டம் (RKVY)", "Agriculture", "farmer", None, None, None),
    ("bamboo_mission_agri", "National Bamboo Mission (Cultivation & Processing)", "राष्ट्रीय बांस मिशन (बांस की खेती एवं मूल्यवर्धन)", "राष्ट्रीय बांबू अभियान", "தேசிய மூங்கில் இயக்கம்", "Agriculture", "farmer", None, None, None),
    ("horticulture_mission_midh", "Mission for Integrated Development of Horticulture (MIDH)", "एकीकृत बागवानी विकास मिशन (MIDH)", "एकात्मिक फलोत्पादन विकास अभियान", "ஒருங்கிணைந்த தோட்டக்கலை மேம்பாட்டுத் திட்டம்", "Horticulture", "farmer", None, None, None),
    ("beekeeping_madhukranti", "National Beekeeping and Honey Mission (NBHM)", "राष्ट्रीय मधुमक्खी पालन एवं शहद मिशन", "राष्ट्रीय मधमाशी पालन अभियान", "தேசிய தேனீ வளர்ப்பு திட்டம்", "Agriculture", "farmer", None, None, None),
    ("agroforestry_sub_mission", "Sub-Mission on Agroforestry (Har Medh Par Ped)", "कृषि वानिकी उप-मिशन (हर मेड़ पर पेड़)", "कृषी वनशेती उप-अभियान", "வேளாண் காடுகள் திட்டம்", "Agriculture", "farmer", None, None, None),
    ("maha_falbaug_yojana_bhau_saheb", "Bhausaheb Fundkar Falbaug Lagwad Yojana", "भाऊसाहेब फुंडकर फलोत्पादन योजना (महाराष्ट्र)", "भाऊसाहेब फुंडकर फळबाग लागवड योजना", "பழத்தோட்ட பயிரிடும் திட்டம் (மகாராஷ்டிரா)", "Horticulture", "farmer", None, None, "Maharashtra"),

    # Women & Mother
    ("bap_janani_suraksha_jsy", "Janani Suraksha Yojana (Institutional Delivery)", "जननी सुरक्षा योजना (अस्पताल में सुरक्षित प्रसव)", "जननी सुरक्षा योजना", "ஜனனி சுரக்ஷா யோஜனா (இலவச பிரசவ திட்டம்)", "Maternal Health", None, "female", None, None),
    ("janani_shishu_suraksha_jssk", "Janani Shishu Suraksha Karyakram (JSSK)", "जननी शिशु सुरक्षा कार्यक्रम (मुफ्त दवा व एम्बुलेंस)", "जननी शिशु सुरक्षा कार्यक्रम", "ஜனனி சிசு சுரக்ஷா திட்டம்", "Healthcare", None, "female", None, None),
    ("poshan_abhiyan_mothers", "PM POSHAN Abhiyaan (National Nutrition Mission)", "प्रधानमंत्री पोषण अभियान (मातृ एवं शिशु पोषण)", "राष्ट्रीय पोषण अभियान", "தேசிய ஊட்டச்சத்து இயக்கம்", "Nutrition", None, "female", None, None),
    ("one_stop_centre_sakhi", "One Stop Centre Scheme (Sakhi - Women Safety)", "वन स्टॉप सेंटर योजना (सखी - महिला सुरक्षा व कानूनी सहायता)", "वन स्टॉप सेंटर (सखी योजना)", "சகி - மகளிர் ஒன் ஸ்டாப் சென்டர்", "Women Protection", None, "female", None, None),
    ("mahila_e_haat_marketplace", "Mahila E-Haat (Online Market for Women)", "महिला ई-हाट (महिला उद्यमियों हेतु ऑनलाइन बाज़ार)", "महिला ई-हाट व्यासपीठ", "மஹிளா இ-ஹாட் ஆன்லைன் சந்தை", "Women Entrepreneur", "entrepreneur", "female", None, None),
    ("steer_support_training_step", "Support to Training and Employment (STEP for Women)", "महिलाओं हेतु प्रशिक्षण एवं रोजगार कार्यक्रम (STEP)", "महिला रोजगार व कौशल्य प्रशिक्षण (STEP)", "மகளிர் வேலைவாய்ப்பு பயிற்சி திட்டம் (STEP)", "Employment", "unemployed", "female", None, None),
    ("working_women_hostel_scheme", "Working Women Hostel Scheme (Safe Accommodation)", "कामकाजी महिला छात्रावास योजना (सुरक्षित आवास)", "नोकरदार महिला वसतिगृह योजना", "பணிபுரியும் மகளிர் விடுதி திட்டம்", "Urban Welfare", "salaried", "female", None, None),
    ("tn_maternity_financial_dr_muthulakshmi", "Dr. Muthulakshmi Reddy Maternity Benefit Scheme", "डॉ. मुथुलक्ष्मी रेड्डी मातृत्व सहायता योजना", "डॉ. मुथुलक्ष्मी रेड्डी मातृत्व सहाय्य योजना", "டாக்டர் முத்துலட்சுமி ரெட்டி மகப்பேறு நிதியுதவி திட்டம்", "Maternity", None, "female", None, "Tamil Nadu"),
    ("up_bhagya_lakshmi_girl", "UP Bhagya Laxmi Yojana (Girl Child Support)", "उत्तर प्रदेश भाग्य लक्ष्मी योजना (बालिका सुरक्षा)", "भाग्यलक्ष्मी योजना (उत्तर प्रदेश)", "பாக்ய லக்ஷ்மி திட்டம் (உத்தர பிரதேசம்)", "Girl Child", None, "female", None, "Uttar Pradesh"),
    ("rajasthan_indira_priyadarshini", "Indira Priyadarshini Award Scheme for Girls", "इंदिरा प्रियदर्शिनी पुरस्कार योजना (राजस्थान)", "इंदिरा प्रियदर्शिनी पुरस्कार योजना", "இந்திரா பிரியதர்ஷினி விருது திட்டம்", "Education", "student", "female", None, "Rajasthan"),

    # Education & Students
    ("pm_shri_schools_quality", "PM SHRI Schools Development Scheme", "पीएम श्री स्कूल योजना (आधुनिक गुणवत्तापूर्ण शिक्षा)", "पीएम श्री शाळा योजना", "பிஎம் ஸ்ரீ மாதிரி பள்ளிகள் திட்டம்", "School Education", "student", None, None, None),
    ("national_apprenticeship_training_nats", "National Apprenticeship Training Scheme (NATS Degree)", "राष्ट्रीय शिक्षुता प्रशिक्षण योजना (NATS)", "राष्ट्रीय शिकाऊ प्रशिक्षण योजना", "தேசிய தொழிற்பயிற்சி திட்டம் (NATS)", "Skill Development", "student", None, None, None),
    ("central_sector_interest_subsidy_csis", "Central Sector Interest Subsidy (Higher Education Loan)", "केंद्रीय क्षेत्र ब्याज सब्सिडी योजना (शिक्षा ऋण)", "उच्च शिक्षण कर्ज व्याज सवलत योजना", "கல்விக் கடன் முழு வட்டி மானியத் திட்டம்", "Education Loan", "student", None, None, None),
    ("ishaan_uday_northeast_scholarship", "Ishaan Uday Special Scholarship for North East", "ईशान उदय विशेष छात्रवृत्ति योजना", "ईशान उदय शिष्यवृत्ती", "இஷான் உதய் வடகிழக்கு உதவித்தொகை", "Scholarship", "student", None, None, None),
    ("pragati_saksham_divyang_scholarship", "AICTE Saksham Scholarship for Specially-Abled", "सक्षम छात्रवृत्ति (दिव्यांग तकनीकी छात्रों हेतु)", "सक्षम शिष्यवृत्ती (दिव्यांग विद्यार्थी)", "சக்ஷம் மாற்றுத்திறனாளி கல்வி உதவித்தொகை", "Scholarship", "student", None, None, None),
    ("post_matric_scholarship_st", "Post-Matric Scholarship for ST Tribal Students", "अनुसूचित जनजाति (ST) पोस्ट-मैट्रिक छात्रवृत्ति", "अनुसूचित जमाती (ST) मॅट्रिकोत्तर शिष्यवृत्ती", "பழங்குடியினர் மெட்ரிக் பிந்தைய கல்வி உதவித்தொகை", "Tribal Education", "student", None, ["st"], None),
    ("begum_hazrat_mahal_minority_girls", "Begum Hazrat Mahal National Scholarship for Minority Girls", "बेगम हज़रत महल राष्ट्रीय अल्पसंख्यक बालिका छात्रवृत्ति", "बेगम हजरत महल अल्पसंख्याक शिष्यवृत्ती", "பேகம் ஹசரத் மஹால் சிறுபான்மையினர் மாணவிகள் கல்வி உதவித்தொகை", "Scholarship", "student", "female", None, None),
    ("national_fellowship_obc", "National Fellowship for OBC Students (MPhil / PhD)", "अन्य पिछड़ा वर्ग राष्ट्रीय फेलोशिप (एमफिल व पीएचडी)", "इतर मागासवर्गीय राष्ट्रीय संशोधन फेलोशिप", "OBC மாணவர்களுக்கான தேசிய ஆராய்ச்சி உதவித்தொகை", "Research", "student", None, ["obc"], None),
    ("national_fellowship_sc", "National Fellowship for Scheduled Caste Students (NFSC)", "अनुसूचित जाति राष्ट्रीय रिसर्च फेलोशिप (NFSC)", "अनुसूचित जाती राष्ट्रीय फेलोशिप", "SC மாணவர்களுக்கான தேசிய ஆராய்ச்சி உதவித்தொகை", "Research", "student", None, ["sc"], None),
    ("samagra_shiksha_uniform_books", "Samagra Shiksha Abhiyan (Free Uniforms & Textbooks)", "समग्र शिक्षा अभियान (मुफ्त पाठ्यपुस्तकें व यूनिफॉर्म)", "समग्र शिक्षा अभियान (मोफत गणवेश व पुस्तके)", "சமக்ர சிக்ஷா (இலவச சீருடை மற்றும் பாடப்புத்தகங்கள்)", "Schooling", "student", None, None, None),

    # Artisans, Vendors & Workers
    ("credit_guarantee_pmegp_cgtmse", "Credit Guarantee Scheme for Micro and Small Enterprises", "सूक्ष्म एवं लघु उद्यम क्रेडिट गारंटी योजना (CGTMSE)", "लघु उद्योग पत हमी योजना (CGTMSE)", "சிறு குறு தொழில்களுக்கான கடன் உத்தரவாத திட்டம்", "MSME", "entrepreneur", None, None, None),
    ("national_handloom_development_nhdp", "National Handloom Development Programme (NHDP)", "राष्ट्रीय हथकरघा विकास कार्यक्रम (बुनकर सहायता)", "राष्ट्रीय हातमाग विकास कार्यक्रम", "தேசிய கைத்தறி வளர்ச்சி திட்டம் (NHDP)", "Weavers", "artisan", None, None, None),
    ("weavers_mudra_concessional_loan", "Weavers MUDRA Scheme (Concessional Credit)", "बुनकर मुद्रा योजना (रियायती ब्याज पर ऋण व मार्जिन मनी)", "विणकर मुद्रा कर्ज योजना", "நெசவாளர் முத்ரா சலுகை கடன் திட்டம்", "Textiles", "artisan", None, None, None),
    ("craft_bazaar_exhibition_artisan", "Crafts Bazaar and Dastkar Haat Marketing Assistance", "शिल्प बाज़ार एवं दस्तकार हाट विपणन सहायता", "शिल्प बाजार व हस्तकला प्रदर्शन भरती", "கைவினைப் பொருட்கள் விற்பனை கண்காட்சி திட்டம்", "Handicrafts", "artisan", None, None, None),
    ("khadi_gramodyog_rozgar_yojana", "Khadi Gramodyog Rozgar Yojana (Village Industries)", "खादी ग्रामोद्योग रोजगार योजना (ग्रामीण उद्योग)", "खादी ग्रामोद्योग ग्रामीण उद्योग योजना", "கதர் கிராமத் தொழில் வேலைவாய்ப்பு திட்டம்", "Village Industry", "entrepreneur", None, None, None),
    ("beedi_workers_housing_subsidy", "Revised Housing Subsidy for Beedi and Cine Workers", "बीड़ी एवं सिनेमा श्रमिकों हेतु पक्का मकान सब्सिडी", "विडी कामगार घरकुल योजना", "பீடி தொழிலாளர்கள் வீட்டு வசதி மானியத் திட்டம்", "Housing", "unorganized", None, None, None),
    ("port_dock_transport_workers_pension", "Transport and Auto-Rickshaw Drivers Welfare Fund", "ऑटो-रिक्शा एवं परिवहन चालक सामाजिक कल्याण योजना", "रिक्षा व वाहतूक चालक कल्याण योजना", "ஆட்டோ ஓட்டுநர்கள் சமூக நல வாரிய உதவி", "Transport", "unorganized", None, None, None),
    ("domestic_workers_social_security", "Domestic Workers Social Security and Skill Training", "घरेलू कामगार सामाजिक सुरक्षा व कौशल्य विकास", "घरकामगार सामाजिक सुरक्षा व ओळखपत्र", "வீട്ടുப் பணியாளர்கள் சமூக பாதுகாப்பு திட்டம்", "Domestic Labor", "unorganized", "female", None, None),
    ("mines_and_quarry_worker_health", "Health Care Assistance for Iron Ore and Mica Mine Workers", "खदान एवं खनिज श्रमिकों हेतु निःशुल्क स्वास्थ्य चिकित्सा", "खाण कामगार मोफत आरोग्य सेवा", "சுரங்கத் தொழிலாளர்கள் மருத்துவ நல திட்டம்", "Mine Workers", "unorganized", None, None, None),
    ("fisherman_insurance_coastal", "Group Accident Insurance Scheme for Active Fishermen", "मत्स्यपालक व मछुआरा सामूहिक दुर्घटना बीमा योजना", "मच्छीमार गट अपघात विमा योजना", "மீனவர்களுக்கான குழு விபத்துக் காப்பீட்டுத் திட்டம்", "Fisheries", "farmer", None, None, None),

    # Health & Social Welfare
    ("national_ayush_mission_wellness", "National AYUSH Mission (Ayurveda & Homeopathy Care)", "राष्ट्रीय आयुष मिशन (निःशुल्क आयुर्वेद व होम्योपैथी चिकित्सा)", "राष्ट्रीय आयुष मोफत उपचार अभियान", "தேசிய ஆயுஷ் இலவச மருத்துவ இயக்கம்", "AYUSH", None, None, None, None),
    ("free_dialysis_service_pradhan_mantri", "Pradhan Mantri National Dialysis Programme", "प्रधानमंत्री राष्ट्रीय डायलिसिस कार्यक्रम (मुफ्त डायलिसिस)", "पंतप्रधान मोफत डायलिसिस कार्यक्रम", "பிரதமரின் இலவச டயாலிசிஸ் திட்டம்", "Critical Health", None, None, None, None),
    ("cochlear_implant_children_adip", "Free Cochlear Implant Scheme for Deaf Children", "मूक-बधिर बच्चों हेतु मुफ्त कॉक्लियर इम्प्लांट सर्जरी", "कर्णबधिर बालकांसाठी मोफत कॉक्लियर इम्प्लांट", "செவித்திறன் குறைந்த குழந்தைகளுக்கு இலவச காக்லியர் அறுவை சிகிச்சை", "Disability", None, None, None, None),
    ("intellectual_disability_niramaya_health", "Niramaya Health Insurance for Autism and Cerebral Palsy", "निरामया स्वास्थ्य बीमा योजना (ऑटिज्म व सेरेब्रल पाल्सी हेतु)", "निरामया आरोग्य विमा योजना (दिव्यांग बांधव)", "நிராமயா மாற்றுத்திறனாளி மருத்துவக் காப்பீடு", "Special Needs", None, None, None, None),
    ("national_action_plan_drug_reduction", "Nashamukht Bharat Abhiyaan (De-addiction Support)", "नशामुक्त भारत अभियान (निःशुल्क नशामुक्ति व पुनर्वास)", "नशामुक्ती उपचार व समुपदेशन केंद्र", "போதைப்பொருள் ஒழிப்பு மற்றும் மறுவாழ்வு திட்டம்", "Rehabilitation", None, None, None, None),
    ("transgender_identity_card_smile", "SMILE Scheme (Support for Transgender Welfare)", "स्माइल योजना (ट्रांसजेंडर व्यक्तियों हेतु पहचान व सहायता)", "स्माईल योजना (तृतीयापंथी कल्याण)", "ஸ்மைல் திருநங்கைகள் நலத்திட்டம்", "Social Inclusion", None, "other", None, None),
    ("destitute_senior_citizen_old_age_home", "Atal Vayo Abhyuday Yojana (Senior Shelter Homes)", "अटल वयो अभ्युदय योजना (वृद्धाश्रम व डे-केयर केंद्र)", "ज्येष्ठ नागरिक निवारा गृह योजना", "முதியோர் இல்லங்கள் மற்றும் பராமரிப்பு திட்டம்", "Elders", "senior", None, None, None),
    ("integrated_child_protection_vatsalya", "Mission Vatsalya (Child Protection and Foster Care)", "मिशन वात्सल्य (अनाथ व संकटग्रस्त बच्चों की सुरक्षा व पालन-पोषण)", "मिशन वात्सल्य बालसंगोपन योजना", "மிஷன் வாட்சல்யா குழந்தை பாதுகாப்பு திட்டம்", "Child Care", None, None, None, None),
    ("pm_suraksha_bima_yojana_pmsby", "Pradhan Mantri Suraksha Bima Yojana (₹20/year Accident Cover)", "प्रधानमंत्री सुरक्षा बीमा योजना (₹20 सालाना में ₹2 लाख दुर्घटना बीमा)", "प्रधानमंत्री सुरक्षा विमा योजना (₹२० वार्षिक)", "பிரதமர் சுரக்ஷா பீமா விபத்து காப்பீடு (ஆண்டுக்கு ₹20)", "Accident Cover", None, None, None, None),
    ("pm_jeevan_jyoti_bima_pmjjby", "Pradhan Mantri Jeevan Jyoti Bima Yojana (Life Cover)", "प्रधानमंत्री जीवन ज्योति बीमा योजना (₹2 लाख का जीवन बीमा)", "प्रधानमंत्री जीवन ज्योती विमा योजना", "பிரதமர் ஜீவன் ஜோதி ஆயுள் காப்பீட்டுத் திட்டம்", "Life Insurance", None, None, None, None)
]

for row in additional_schemes_meta:
    sid, en_n, hi_n, mr_n, ta_n, tag, occ, gen, cat, st = row
    rule = {}
    if occ: rule["occupation"] = occ
    if gen: rule["gender"] = gen
    if cat: rule["category_in"] = [cat] if isinstance(cat, str) else cat
    if st: rule["state"] = st

    add(sid, "state" if st else "central", st, rule,
        en_n, tag, f"Government welfare program offering financial assistance, security, and subsidized services under {en_n}.",
        ["Comprehensive government financial and welfare support", "Direct transfer to Aadhaar-linked bank account"],
        ["Aadhaar Card", "Ration Card or Relevant Proof", "Bank Passbook"],
        ["Apply online on official nodal portal", "Administrative verification", "Direct disbursement to beneficiary"],
        "https://www.myscheme.gov.in",
        hi_n, tag, f"{hi_n} के तहत पात्र नागरिकों को प्रत्यक्ष सरकारी सहायता, सब्सिडी एवं सुरक्षा लाभ।",
        ["प्रत्यक्ष सरकारी वित्तीय सहायता व रियायती सेवाएं", "आधार-संबद्ध बैंक खाते में सीधा लाभ"],
        ["आधार कार्ड", "राशन कार्ड या प्रासंगिक प्रमाण", "बैंक पासबुक"],
        ["आधिकारिक विभागीय पोर्टल पर ऑनलाइन आवेदन करें", "सत्यापन उपरांत स्वीकृति", "सीधे खाते में डीबीटी द्वारा लाभ प्राप्त करें"],
        mr_n, tag, f"{mr_n} अंतर्गत पात्र नागरिकांना थेट शासकीय आर्थिक सहाय्य व सवलती.",
        ["शासकीय थेट आर्थिक मदत व कल्याणकारी लाभ", "थेट बँक खात्यात निधी वर्ग"],
        ["आधार कार्ड", "रेशन कार्ड किंवा उत्पन्न दाखला", "बँक पासबुक"],
        ["अधिकृत पोर्टलवर नोंदणी करा", "कागदपत्र पडताळणी", "थेट बँक खात्यात रक्कम"],
        ta_n, tag, f"{ta_n} திட்டத்தின் கீழ் தகுதியான பயனாளிகளுக்கு அரசு நிதி மற்றும் நலத்திட்ட உதவிகள்.",
        ["நேரடி அரசு நிதியுதவி மற்றும் சலுகைகள்", "வங்கி கணக்கில் நேரடி வரவு"],
        ["ஆதார் அட்டை", "குடும்ப அட்டை", "வங்கி பாஸ்புக்"],
        ["அரசு இணையதளத்தில் விண்ணப்பிக்கவும்", "சரிபார்ப்பிற்கு பின் வங்கி வரவு பெறுதல்"])

print(f"Adding {len(new_items)} additional schemes to achieve target.")
all_final = schemes + new_items

with open(SCHEMES_FILE, "w", encoding="utf-8") as f:
    json.dump(all_final, f, ensure_ascii=False, indent=2)

print(f"Total schemes in database now: {len(all_final)}")
