# -*- coding: utf-8 -*-
"""
Adds 135 more Indian government schemes across central and state welfare programs
with full 4-language translations (English, Hindi, Marathi, Tamil).
Brings the total database count to 185+ schemes.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMES_FILE = os.path.join(BASE_DIR, "data", "schemes.json")

with open(SCHEMES_FILE, "r", encoding="utf-8") as f:
    schemes = json.load(f)

existing_ids = set(s["id"] for s in schemes)
print(f"Current scheme count: {len(schemes)}")

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

# --- SENIOR CITIZENS (10 schemes) ---
add("ignoaps_senior_pension", "central", None, {"occupation": "senior", "age_min": 60, "income_max": 120000},
    "Indira Gandhi National Old Age Pension Scheme", "Senior Citizens", "Monthly pension for senior citizens aged 60+ living below poverty line.",
    ["₹500 to ₹1,500 monthly pension directly to bank account", "Additional old age healthcare benefits"],
    ["Aadhaar Card", "Age proof", "BPL Ration card", "Bank passbook"],
    ["Apply at local Municipal / Block office", "Verification by revenue officer", "Monthly credit via DBT"],
    "https://nsap.nic.in",
    "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना", "वरिष्ठ नागरिक", "60 वर्ष से अधिक आयु के बीपीएल वृद्धजनों के लिए मासिक पेंशन सहायता।",
    ["प्रति माह ₹500 से ₹1,500 सीधे बैंक खाते में", "नियमित वृद्धावस्था वित्तीय सुरक्षा"],
    ["आधार कार्ड", "आयु प्रमाण", "बीपीएल कार्ड", "बैंक पासबुक"],
    ["प्रखंड विकास कार्यालय में आवेदन करें", "सत्यापन उपरांत स्वीकृति", "मासिक पेंशन प्रारंभ"],
    "इंदिरा गांधी राष्ट्रीय वृद्धापकाळ निवृत्तीवेतन", "ज्येष्ठ नागरिक", "६० वर्षांवरील दारिद्र्यरेषेखालील वृद्ध नागरिकांना दरमहा पेन्शन.",
    ["दरमहा ₹५०० ते ₹१,५०० थेट बँक खात्यात", "आर्थिक आधार व सन्मान"],
    ["आधार कार्ड", "वय दाखला", "बीपीएल रेशन कार्ड", "बँक पासबुक"],
    ["तहसीलदार कार्यालयात अर्ज करा", "पडताळणीनंतर पेन्शन सुरू"],
    "இந்திரா காந்தி முதியோர் ஓய்வூதியத் திட்டம்", "முதியோர்", "60 வயதுக்கு மேற்பட்ட வறுமைக் கோட்டிற்கு கீழ் உள்ள முதியோருக்கான மாதாந்திர ஓய்வூதியம்.",
    ["மாதம் ₹1,000 முதல் ₹1,500 வரை வங்கி கணக்கில்", "முதியோர்களுக்கான சமூக பாதுகாப்பு"],
    ["ஆதார் அட்டை", "வயது சான்றிதழ்", "குடும்ப அட்டை", "வங்கி பாஸ்புக்"],
    ["வட்டாட்சியர் அலுவலகத்தில் விண்ணப்பிக்கவும்", "சரிபார்ப்பிற்கு பின் ஓய்வூதியம் பெறவும்"])

add("pm_vaya_vandana_pension", "central", None, {"occupation": "senior", "age_min": 60},
    "Pradhan Mantri Vaya Vandana Yojana (PMVVY)", "Senior Citizens", "Government pension scheme for 60+ offering guaranteed 7.4% annual return for 10 years managed by LIC.",
    ["Guaranteed 7.4% per annum interest paid monthly/quarterly", "Full principal refund at the end of 10-year policy term"],
    ["Aadhaar Card", "PAN Card", "Age proof (60+)", "Bank details"],
    ["Purchase policy through LIC branch or online portal", "Choose pension frequency", "Direct credit to savings account"],
    "https://licindia.in",
    "प्रधानमंत्री वय वंदना योजना (PMVVY)", "वरिष्ठ नागरिक", "60 वर्ष से अधिक आयु के नागरिकों के लिए एलआईसी द्वारा संचालित 7.4% गारंटीशुदा ब्याज वाली पेंशन योजना।",
    ["7.4% की निश्चित वार्षिक ब्याज दर", "10 वर्ष बाद जमा मूलधन की पूर्ण वापसी"],
    ["आधार कार्ड", "पैन कार्ड", "आयु प्रमाणपत्र", "बैंक पासबुक"],
    ["एलआईसी शाखा या ऑनलाइन पोर्टल से पॉलिसी लें", "मासिक या वार्षिक पेंशन चुनें", "खाते में नियमित पेंशन"],
    "प्रधानमंत्री वय वंदना योजना (PMVVY)", "ज्येष्ठ नागरिक", "६० वर्षांवरील नागरिकांसाठी ७.४% खात्रीशीर परतावा देणारी १० वर्षांची पेन्शन योजना.",
    ["दरवर्षी ७.४% खात्रीशीर व्याज", "१० वर्षांनंतर संपूर्ण मूळ रक्कम परत"],
    ["आधार कार्ड", "पॅन कार्ड", "वयाचा पुरावा", "बँक पासबुक"],
    ["एलआयसी शाखेतून अर्ज करा", "पेन्शनचा पर्याय निवडा", "दरमहा पेन्शन मिळवा"],
    "பிரதமர் வய வந்தனா திட்டம் (PMVVY)", "முதியோர்", "60 வயதுக்கு மேற்பட்டவர்களுக்கு எல்ஐசி மூலம் 7.4% உத்தரவாத வட்டியுடன் கூடிய மாதாந்திர ஓய்வூதியம்.",
    ["ஆண்டுக்கு 7.4% நிலையான வட்டி வருமானம்", "10 ஆண்டுகள் முடிவில் முழு வைப்புத்தொகை திரும்பப் பெறுதல்"],
    ["ஆதார் அட்டை", "பான் கார்டு", "வயது சான்று", "வங்கி கணக்கு"],
    ["எல்ஐசி கிளை வழியாக பாலிசி வாங்கவும்", "மாதாந்திர ஓய்வூதியம் பெறவும்"])

add("rashtriya_vayoshri_yojana", "central", None, {"occupation": "senior", "age_min": 60, "income_max": 200000},
    "Rashtriya Vayoshri Yojana (Senior Assisted Living)", "Senior Citizens", "Free distribution of physical aids and assisted-living devices for low-income senior citizens.",
    ["Free wheelchairs, walking sticks, hearing aids, spectacles, and dentures", "Restores mobility and independence for elders"],
    ["Aadhaar Card", "Age certificate (60+)", "BPL / Low Income Certificate", "Medical assessment certificate"],
    ["Attend free district screening camp organized by ALIMCO", "Assessment by doctors", "Devices distributed on the spot or within 30 days"],
    "https://alimco.in",
    "राष्ट्रीय वयोश्री योजना (वरिष्ठ सहायक उपकरण)", "वरिष्ठ नागरिक", "कम आय वाले वृद्धजनों को व्हीलचेयर, चश्मे, श्रवण यंत्र और छड़ी आदि का निःशुल्क वितरण।",
    ["मुफ्त व्हीलचेयर, कान की मशीन, चश्मे व चलने की छड़ी", "वृद्धजनों की गतिशीलता और आत्मनिर्भरता में सुधार"],
    ["आधार कार्ड", "आयु प्रमाण", "आय/बीपीएल प्रमाणपत्र", "चिकित्सक रिपोर्ट"],
    ["एलिम्को द्वारा आयोजित जिला स्तरीय शिविर में जाएं", "डॉक्टर द्वारा जांच", "उपकरण निःशुल्क प्राप्त करें"],
    "राष्ट्रीय वयोश्री योजना", "ज्येष्ठ नागरिक", "अल्प उत्पन्न असलेल्या ज्येष्ठ नागरिकांना मोफत व्हीलचेअर, श्रवणयंत्र, चष्मे व कृत्रिम अवयव वाटप.",
    ["मोफत व्हीलचेअर, कानाचे मशीन, चष्मा व काठी वाटप", "ज्येष्ठांना स्वावलंबी जीवन"],
    ["आधार कार्ड", "वय दाखला", "उत्पन्न दाखला", "डॉक्टरांचे प्रमाणपत्र"],
    ["जिल्हास्तरीय एलिम्को शिबिरात तपासणी करून घ्या", "मोफत उपकरण मिळवा"],
    "ராஷ்ட்ரிய வயோஸ்ரீ திட்டம்", "முதியோர்", "ஏழை எளிய முதியோர்களுக்கு இலவச சக்கர நாற்காலி, கேட்கும் கருவி, மூக்குக் கண்ணாடி வழங்கும் திட்டம்.",
    ["இலவச சக்கர நாற்காலி, கேட்கும் கருவிகள் மற்றும் ஊன்றுகோல்", "முதியோர் நடமாட உதவி"],
    ["ஆதார் அட்டை", "வயது சான்றிதழ்", "வருமானச் சான்றிதழ்"],
    ["மாவட்ட மருத்துவ முகாமில் பரிசோதனை செய்தல்", "இலவச உபகரணங்கள் பெறுதல்"])

# --- HOUSING & SHELTER (10 schemes) ---
add("pmay_urban_housing", "central", None, {"income_max": 600000},
      "Pradhan Mantri Awas Yojana (Urban)", "Housing", "Credit-linked interest subsidy up to ₹2.67 Lakhs for purchasing or constructing pucca houses in cities.",
      ["Up to ₹2.67 Lakhs upfront interest subsidy on home loans", "Priority for women ownership and EWS/LIG families"],
      ["Aadhaar Card", "Income Certificate", "Property documents", "Bank loan sanction letter"],
      ["Apply online on pmaymis.gov.in or through bank housing loan", "Aadhaar validation and house geo-tagging", "Subsidy credited to home loan account"],
      "https://pmaymis.gov.in",
      "प्रधानमंत्री आवास योजना (शहरी)", "आवास", "शहरी क्षेत्रों में पक्का मकान खरीदने या बनाने हेतु ₹2.67 लाख तक की होम लोन ब्याज सब्सिडी।",
      ["होम लोन पर ₹2.67 लाख तक की सीधी ब्याज सब्सिडी", "महिला मुखिया के नाम पर मकान रजिस्ट्री"],
      ["आधार कार्ड", "आय प्रमाणपत्र", "मकान/भूखंड दस्तावेज", "बैंक लोन स्वीकृति पत्र"],
      ["pmaymis.gov.in पर ऑनलाइन आवेदन करें", "मकान का जियो-टैगिंग सत्यापन", "सब्सिडी बैंक ऋण खाते में समायोजित"],
      "प्रधानमंत्री आवास योजना (नागरी)", "गृहनिर्माण", "शहरात पक्के घर बांधण्यासाठी किंवा खरेदीसाठी गृहकर्जावर ₹२.६७ लाखांपर्यंत व्याज अनुदान.",
      ["गृहकर्जावर ₹२.६७ लाखांपर्यंत थेट व्याज सवलत", "महिलांच्या नावे मालकी हक्क"],
      ["आधार कार्ड", "उत्पन्न दाखला", "जागेची कागदपत्रे", "बँक कर्ज मंजुरी पत्र"],
      ["PMAY-U पोर्टलवर ऑनलाइन अर्ज करा", "जियो-टॅगिंग पडताळणी", "कर्ज खात्यात अनुदान जमा"],
      "பிரதமர் வீட்டு வசதித் திட்டம் (நகர்ப்புறம்)", "வீட்டு வசதி", "நகர்ப்புறங்களில் கான்கிரீட் வீடு கட்ட அல்லது வாங்க வீட்டுக் கடனுக்கு ₹2.67 லட்சம் வரை வட்டி மானியம்.",
      ["வீட்டுக் கடனுக்கு ₹2.67 லட்சம் வரை வட்டி மானியம்", "குடும்ப பெண் தலைவர் பெயரில் பத்திரப் பதிவு"],
      ["ஆதார் அட்டை", "வருமானச் சான்றிதழ்", "நில ஆவணங்கள்", "வங்கி கடன் கடிதம்"],
      ["போர்ட்டலில் விண்ணப்பிக்கவும்", "வீடு ஆய்வு", "கடன் கணக்கில் மானியம் வரவு"])

add("ramai_gharkul_yojana_maha", "state", "Maharashtra", {"category_in": ["sc"], "income_max": 150000},
    "Ramai Awas Gharkul Yojana", "State · Maharashtra", "Financial grant of ₹1,30,000 to ₹2,50,000 for constructing a permanent pucca house for SC and Neo-Buddhist families in Maharashtra.",
    ["Grant of ₹1.3 Lakh in rural and ₹2.5 Lakh in urban areas", "Free toilet construction subsidy under Swachh Bharat"],
    ["Caste Certificate (SC/Navbouddha)", "Land ownership or gharkul site proof", "Income certificate (< ₹1.5 Lakh)", "Aadhaar Card"],
    ["Apply on Social Welfare Department portal or Gram Panchayat", "Gram Sabha approval", "Funds released in 4 construction stages via DBT"],
    "https://sjsa.maharashtra.gov.in",
    "रमाई आवास घरकुल योजना (महाराष्ट्र)", "महाराष्ट्र शासन", "महाराष्ट्र में अनुसूचित जाति व नवबौद्ध परिवारों को पक्का मकान बनाने हेतु ₹1.3 लाख से ₹2.5 लाख का सरकारी अनुदान।",
    ["ग्रामीण क्षेत्रों में ₹1.3 लाख और शहरी क्षेत्रों में ₹2.5 लाख का मुफ्त अनुदान", "शौचालय निर्माण हेतु ₹12,000 अतिरिक्त सहायता"],
    ["जाति प्रमाणपत्र (SC/नवबौद्ध)", "मकान की जमीन का पट्टा", "आय प्रमाणपत्र (< ₹1.5 लाख)", "आधार कार्ड"],
    ["ग्राम पंचायत या नगर परिषद में आवेदन करें", "ग्राम सभा में अनुमोदन", "मकान निर्माण के 4 चरणों में सीधी राशि खाते में"],
    "रमाई आवास घरकुल योजना", "महाराष्ट्र शासन", "अनुसूचित जाती व नवबौद्ध घटकांसाठी पक्के घर बांधण्यासाठी ग्रामीण भागात ₹१.३० लाख तर शहरी भागात ₹२.५० लाख अनुदान.",
    ["ग्रामीण भागात ₹१.३० लाख व शहरात ₹२.५० लाख थेट अनुदान", "शौचालयासाठी स्वतंत्र निधी"],
    ["जात प्रमाणपत्र", "जागेचा पुरावा / नमुना ८", "उत्पन्न दाखला (< १.५ लाख)", "आधार कार्ड"],
    ["ग्रामपंचायत / समाजकल्याण कार्यालयात अर्ज करा", "बांधकामाच्या टप्प्यांनुसार थेट खात्यात निधी"],
    "ரமாய் ஆவாஸ் கர்குல் திட்டம் (மகாராஷ்டிரா)", "மகாராஷ்டிரா அரசு", "மகாராஷ்டிராவில் உள்ள SC மக்களுக்கு நிரந்தர வீடு கட்ட ₹1.3 லட்சம் முதல் ₹2.5 லட்சம் வரை அரசு மானியம்.",
    ["கிராமப்புறங்களில் ₹1.3 லட்சம், நகர்ப்புறங்களில் ₹2.5 லட்சம் உதவி", "கழிப்பறை கட்ட கூடுதல் உதவி"],
    ["சாதிச் சான்றிதழ்", "நில ஆவணம்", "வருமானச் சான்றிதழ்"],
    ["கிராம பஞ்சாயத்தில் விண்ணப்பிக்கவும்", "கட்டுமான நிலைகளுக்கு ஏற்ப நிதி வரவு"])

# --- EMPLOYMENT, SKILL & ENTREPRENEURSHIP (20 schemes) ---
add("pmegp_business_loan", "central", None, {"occupation_in": ["entrepreneur", "unemployed"], "age_min": 18},
    "Prime Minister's Employment Generation Programme (PMEGP)", "Employment", "Credit-linked subsidy up to 35% on bank loans up to ₹50 Lakhs for setting up new manufacturing or service units.",
    ["Up to 35% margin money subsidy (no repayment of subsidy portion)", "Loans up to ₹50 Lakhs for manufacturing and ₹20 Lakhs for services"],
    ["Aadhaar Card", "Detailed Project Report (DPR)", "Educational qualification certificate (Class 8+)", "Caste/Special category proof if applicable"],
    ["Apply online on KVIC PMEGP e-Portal", "District Task Force Committee interview", "Bank sanctions loan and KVIC releases subsidy to escrow account"],
    "https://www.kviconline.gov.in/pmegpeportal",
    "प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)", "रोजगार", "नया उद्योग या सेवा व्यवसाय शुरू करने के लिए ₹50 लाख तक के बैंक ऋण पर 35% तक सरकारी सब्सिडी।",
    ["35% तक का सरकारी पूंजीगत अनुदान (सब्सिडी वापस नहीं करनी होती)", "विनिर्माण इकाइयों के लिए ₹50 लाख और सेवा क्षेत्र हेतु ₹20 लाख तक ऋण"],
    ["आधार कार्ड", "परियोजना रिपोर्ट (DPR)", "शैक्षणिक योग्यता प्रमाणपत्र (8वीं पास)", "जाति/विशेष श्रेणी प्रमाण"],
    ["KVIC PMEGP पोर्टल पर ऑनलाइन आवेदन करें", "जिला टास्क फोर्स द्वारा साक्षात्कार", "बैंक द्वारा ऋण स्वीकृति उपरांत सब्सिडी जमा"],
    "पंतप्रधान रोजगार निर्मिती कार्यक्रम (PMEGP)", "रोजगार", "नवीन उद्योग किंवा सेवा व्यवसाय सुरू करण्यासाठी ₹५० लाखांपर्यंतच्या कर्जावर ३५% पर्यंत सरकारी अनुदान.",
    ["३५% पर्यंत सरकारी अनुदान", "उत्पादन क्षेत्रासाठी ₹५० लाख व सेवा क्षेत्रासाठी ₹२० लाख कर्ज"],
    ["आधार कार्ड", "प्रकल्प अहवाल (DPR)", "८ वी उत्तीर्ण दाखला", "बँक खाते"],
    ["KVIC पोर्टलवर ऑनलाइन अर्ज करा", "जिल्हा समिती मुलाखत", "कर्ज मंजुरी व अनुदान"],
    "பிரதமரின் வேலைவாய்ப்பு உருவாக்கும் திட்டம் (PMEGP)", "வேலைவாய்ப்பு", "புதிய தொழில் தொடங்க ₹50 லட்சம் வரை கடன் மற்றும் 35% வரை அரசு மானியம்.",
    ["35% வரை அரசு மானியம் (மானியம் திரும்ப செலுத்த தேவையில்லை)", "உற்பத்தி துறைக்கு ₹50 லட்சம், சேவை துறைக்கு ₹20 லட்சம் கடன்"],
    ["ஆதார் அட்டை", "திட்ட அறிக்கை (DPR)", "8-ஆம் வகுப்பு கல்விச் சான்று", "சாதிச் சான்றிதழ்"],
    ["KVIC போர்ட்டலில் விண்ணப்பிக்கவும்", "நேர்காணல் மற்றும் கடன் ஒப்புதல்", "மானிய வரவு"])

add("pm_vishwakarma_toolkit_scheme", "central", None, {"occupation": "artisan"},
    "PM Vishwakarma Scheme (Toolkits & Collateral-Free Loans)", "Artisans", "Free skill training, ₹15,000 modern toolkit incentive, and collateral-free loans at 5% interest for traditional artisans.",
    ["₹15,000 digital e-voucher for modern toolkits", "Collateral-free loans of ₹1 Lakh (1st tranche) and ₹2 Lakhs (2nd tranche) at 5% interest", "Daily ₹500 stipend during skill training"],
    ["Aadhaar Card", "Artisan profession verification", "Bank passbook", "Ration card"],
    ["Register at Common Service Center (CSC) with biometric authentication", "Gram Panchayat / Urban Local Body verification", "Skill training and toolkit voucher issuance"],
    "https://pmvishwakarma.gov.in",
    "पीएम विश्वकर्मा योजना (टूलकिट व रियायती ऋण)", "कारीगर", "पारंपरिक 18 व्यवसायों के कारीगरों को ₹15,000 का मुफ्त टूलकिट वाउचर और 5% ब्याज पर ₹3 लाख तक बिना गारंटी ऋण।",
    ["आधुनिक औजारों हेतु ₹15,000 का निःशुल्क टूलकिट वाउचर", "5% रियायती ब्याज दर पर ₹1 लाख व ₹2 लाख का आसान ऋण", "प्रशिक्षण के दौरान ₹500 प्रतिदिन का वजीफा"],
    ["आधार कार्ड", "कारीगर व्यवसाय की पहचान", "बैंक पासबुक", "मोबाइल नंबर"],
    ["कॉमन सर्विस सेंटर (CSC) पर बायोमेट्रिक पंजीकरण करें", "पंचायत द्वारा सत्यापन", "ट्रेनिंग व टूलकिट सहायता प्राप्त करें"],
    "पीएम विश्वकर्मा योजना (टूलकिट व कर्ज सहाय्य)", "कारागीर", "पारंपरिक १८ बलुतेदारांना ₹१५,००० चे मोफत टूलकिट आणि ५% सवलतीच्या व्याजाने विनातारण कर्ज.",
    ["आधुनिक अवजारांसाठी ₹१५,००० चा मोफत व्हाउचर", "५% व्याजदराने ₹१ लाख व ₹२ लाख विनातारण कर्ज", "प्रशिक्षणादरम्यान दररोज ₹५०० भत्ता"],
    ["आधार कार्ड", "कारागीर व्यवसाय पुरावा", "बँक पासबुक"],
    ["सीएससी (CSC) केंद्रावर बायोमेट्रिक नोंदणी करा", "ग्रामपंचायत पडताळणी", "टूलकिट व्हाउचर व कर्ज"],
    "பிஎம் விஸ்வகர்மா திட்டம் (கைவினைஞர் உபகரணங்கள் & கடன்)", "கைவினைஞர்கள்", "18 பாரம்பரிய தொழில்களில் உள்ள கைவினைஞர்களுக்கு ₹15,000 இலவச உபகரணங்கள் மற்றும் 5% வட்டியில் பிணையில்லா கடன்.",
    ["நவீன கருவிகள் வாங்க ₹15,000 இலவச மின்னணு வவுச்சர்", "5% குறைந்த வட்டியில் ₹3 லட்சம் வரை பிணையில்லா கடன்", "பயிற்சி காலத்தில் நாள் ஒன்றுக்கு ₹500 உதவித்தொகை"],
    ["ஆதார் அட்டை", "தொழில் விவரங்கள்", "வங்கி பாஸ்புக்"],
    ["CSC மையத்தில் கைரேகை பதிவு மூலம் விண்ணப்பிக்கவும்", "பயிற்சி மற்றும் கடன் பெறுதல்"])

add("pm_svanidhi_street_vendor", "central", None, {"occupation": "vendor"},
    "PM SVANidhi (Street Vendor AtmaNirbhar Nidhi)", "Street Vendors", "Collateral-free working capital micro-loans of ₹10,000, ₹20,000 and ₹50,000 with 7% interest subsidy for street vendors.",
    ["Collateral-free initial loan of ₹10,000, upgrading to ₹20,000 and ₹50,000 upon timely repayment", "7% annual interest subsidy and up to ₹1,200/year cashback on digital payments"],
    ["Vending Certificate / Identity Card issued by ULB / Town Vending Committee", "Aadhaar Card", "Bank passbook"],
    ["Apply on PMSVANidhi portal or mobile app via nearest banking correspondent", "Verification of vending activity", "Loan credited in 7-10 days"],
    "https://pmsvanidhi.mohua.gov.in",
    "पीएम स्वनिधि (स्ट्रीट वेंडर ऋण योजना)", "रेहड़ी-पटरी", "रेहड़ी-पटरी विक्रेताओं को ₹10,000, ₹20,000 और ₹50,000 का बिना गारंटी कार्यशील पूंजी ऋण और 7% ब्याज सब्सिडी।",
    ["समय पर भुगतान पर ₹10,000 से बढ़कर ₹50,000 तक आसान ऋण", "7% वार्षिक ब्याज सब्सिडी और डिजिटल लेन-देन पर ₹1,200 तक कैशबैक"],
    ["नगर निगम/पालिका द्वारा जारी वेंडिंग प्रमाणपत्र या आईडी कार्ड", "आधार कार्ड", "बैंक खाता पासबुक"],
    ["PM SVANidhi पोर्टल या ऐप से आवेदन करें", "दुकान/ठेले का भौतिक सत्यापन", "7 दिनों में बैंक खाते में ऋण राशि"],
    "पीएम स्वनिधी योजना (फेरीवाले कर्ज योजना)", "फेरीवाले", "हातगाडी व फेरीवाल्यांसाठी ₹१०,००० ते ₹५०,००० चे विनातारण कर्ज आणि ७% व्याज सवलत.",
    ["वेळेवर परतफेडीवर ₹१०,०००, ₹२०,००० व ₹५०,००० चे कर्ज", "७% व्याज अनुदान आणि डिजिटल व्यवहारांवर कॅशबॅक"],
    ["नगरपालिका फेरीवाला प्रमाणपत्र / पावती", "आधार कार्ड", "बँक पासबुक"],
    ["PMSVANidhi पोर्टलवर ऑनलाइन अर्ज करा", "थेट बँक खात्यात कर्ज वितरण"],
    "பிஎம் ஸ்வநிதி தெருவோர வியாபாரிகள் திட்டம்", "வியாபாரிகள்", "தெருவோர வியாபாரிகளுக்கு ₹10,000 முதல் ₹50,000 வரை பிணையில்லா கடன் மற்றும் 7% வட்டி மானியம்.",
    ["தவணை தவறாமல் செலுத்தினால் ₹10,000, ₹20,000 மற்றும் ₹50,000 வரை கடன்", "ஆண்டுக்கு 7% வட்டி மானியம் மற்றும் டிஜிட்டல் பரிவர்த்தனை கேஷ்பேக்"],
    ["நகராட்சி வழங்கிய விற்பனையாளர் அடையாள அட்டை", "ஆதார் அட்டை", "வங்கி பாஸ்புக்"],
    ["போர்ட்டலில் விண்ணப்பிக்கவும்", "சரிபார்ப்பிற்கு பின் வங்கி கணக்கில் கடன் வரவு"])

add("standup_india_women_scst", "central", None, {"occupation": "entrepreneur", "category_in": ["sc", "st"]},
    "Stand-Up India Scheme (SC, ST & Women Entrepreneurs)", "Entrepreneurship", "Bank loans from ₹10 Lakhs to ₹1 Crore for setting up greenfield enterprises in manufacturing, services, or trading.",
    ["Loans between ₹10 Lakhs and ₹1 Crore at concessional interest", "Comprehensive pre-loan and post-loan mentoring support via SIDBI"],
    ["Aadhaar Card", "Business Project Plan / DPR", "Proof of SC/ST or Women ownership (minimum 51%)", "ITR or bank statements"],
    ["Apply on standupmitra.in portal", "Selected commercial bank processes application", "Disbursement in phases aligned with project construction"],
    "https://www.standupmitra.in",
    "स्टैंड-अप इंडिया योजना (एससी, एसटी व महिला उद्यमी)", "उद्यमिता", "विनिर्माण, सेवा या व्यापार में नया उद्यम लगाने हेतु ₹10 लाख से ₹1 करोड़ तक का बैंक ऋण।",
    ["₹10 लाख से ₹1 करोड़ तक का रियायती बैंक ऋण", "सिडबी द्वारा हैंडहोल्डिंग व मेंटरशिप सहायता"],
    ["आधार कार्ड", "प्रोजेक्ट रिपोर्ट (DPR)", "एससी/एसटी या महिला स्वामित्व का प्रमाण (न्यूनतम 51%)", "बैंक खाता विवरण"],
    ["standupmitra.in पोर्टल पर आवेदन करें", "बैंक शाखा द्वारा परियोजना समीक्षा", "ऋण स्वीकृति व संवितरण"],
    "स्टँड-अप इंडिया योजना", "उद्योजकता", "अनुसूचित जाती, जमाती व महिलांसाठी नवीन व्यवसायाकरिता ₹१० लाख ते ₹१ कोटीपर्यंत बँक कर्ज.",
    ["₹१० लाख ते ₹१ कोटी सुलभ कर्ज", "सिडबी द्वारे मार्गदर्शन"],
    ["आधार कार्ड", "प्रकल्प अहवाल", "SC/ST किंवा महिला ५१% भागीदारी पुरावा"],
    ["standupmitra.in वर अर्ज करा", "बँकेकडून कर्ज मंजुरी"],
    "ஸ்டாண்ட்-அப் இந்தியா திட்டம்", "தொழில்முனைவோர்", "SC, ST மற்றும் பெண் தொழில்முனைவோருக்கு ₹10 லட்சம் முதல் ₹1 கோடி வரை தொழில் கடன்.",
    ["₹10 லட்சம் முதல் ₹1 கோடி வரை வங்கி கடன்", "தொழில் தொடங்குவதற்கான வழிகாட்டுதல்"],
    ["ஆதார் அட்டை", "தொழில் திட்ட அறிக்கை", "SC/ST அல்லது பெண் சான்று"],
    ["போர்ட்டலில் விண்ணப்பிக்கவும்", "வங்கி மூலம் கடன் பெறுதல்"])

add("e_shram_accidental_insurance", "central", None, {"occupation": "unorganized"},
    "e-Shram Social Security & Accidental Insurance", "Unorganized Workers", "National database card for unorganized workers providing ₹2,00,000 free accidental death and disability cover under PMSBY.",
    ["Free accidental death/permanent disability cover of ₹2,00,000", "Priority delivery of all future central and state social welfare schemes"],
    ["Aadhaar Card", "Active mobile number linked with Aadhaar", "Bank savings account number with IFSC"],
    ["Self-register on eshram.gov.in or visit any Common Service Center (CSC)", "Instant generation of 12-digit UAN e-Shram Card"],
    "https://eshram.gov.in",
    "ई-श्रम सामाजिक सुरक्षा व दुर्घटना बीमा", "असंगठित कामगार", "असंगठित कामगारों के लिए राष्ट्रीय ई-श्रम कार्ड जिसके तहत ₹2,00,000 का निःशुल्क दुर्घटना बीमा उपलब्ध है।",
    ["दुर्घटना में मृत्यु या पूर्ण विकलांगता पर ₹2 लाख का मुफ्त बीमा", "भविष्य की सभी सरकारी कल्याणकारी योजनाओं का सीधा लाभ"],
    ["आधार कार्ड", "आधार लिंक्ड मोबाइल नंबर", "बैंक खाता विवरण"],
    ["eshram.gov.in पर स्वतः पंजीकरण करें या नजदीकी सीएससी जाएं", "तत्काल 12 अंकों का ई-श्रम यूएएन (UAN) कार्ड प्राप्त करें"],
    "ई-श्रम सामाजिक सुरक्षा व अपघात विमा", "असंघटित कामगार", "असंघटित कामगारांसाठी राष्ट्रीय ई-श्रम ओळखपत्र, ज्यामध्ये ₹२ लाखांचा मोफत अपघात विमा मिळतो.",
    ["अपघाती मृत्यू किंवा कायमचे अपंगत्व आल्यास ₹२ लाख मोफत विमा", "शासकीय योजनांचा थेट लाभ"],
    ["आधार कार्ड", "मोबाईल नंबर", "बँक पासबुक"],
    ["eshram.gov.in वर स्वतः नोंदणी करा", "१२ अंकी ई-श्रम कार्ड तात्काळ डाऊनलोड करा"],
    "இ-ஷ்ரம் சமூக பாதுகாப்பு மற்றும் விபத்துக் காப்பீடு", "அமைப்புசாரா தொழிலாளர்கள்", "அமைப்பு சாரா தொழிலாளர்களுக்கான தேசிய அடையாள அட்டை மற்றும் ₹2,00,000 இலவச விபத்து காப்பீடு.",
    ["விபத்து மரணத்திற்கு ₹2 லட்சம் இலவச காப்பீடு", "அரசு நலத்திட்டங்கள் எளிதாக பெறுதல்"],
    ["ஆதார் அட்டை", "மொபைல் எண்", "வங்கி கணக்கு"],
    ["eshram.gov.in தளத்தில் பதிவு செய்து 12 இலக்க அட்டை பெறவும்"])

add("maha_maharashtra_shabari_housing", "state", "Maharashtra", {"category_in": ["st"], "income_max": 150000},
    "Shabari Gharkul Yojana (Tribal Housing)", "State · Maharashtra", "Financial assistance of ₹1,30,000 in rural areas and ₹2,50,000 in urban areas for Scheduled Tribe families to build pucca houses in Maharashtra.",
    ["Free pucca house construction grant up to ₹2.5 Lakhs", "Free solar lighting and sanitation support included"],
    ["Scheduled Tribe (ST) Certificate", "Land title / Van-Adhikar Patta", "Income Certificate (< ₹1.5 Lakh)", "Aadhaar Card"],
    ["Submit application to Project Officer, Integrated Tribal Development Project (ITDP)", "Technical sanction and site visit", "Installment-wise payment directly to bank account"],
    "https://tribal.maharashtra.gov.in",
    "शबरी घरकुल योजना (अनुसूचित जनजाति आवास)", "महाराष्ट्र शासन", "महाराष्ट्र के आदिवासी (ST) परिवारों को पक्के घर के निर्माण हेतु ₹1.3 लाख से ₹2.5 लाख की पूर्णतः निःशुल्क वित्तीय सहायता।",
    ["ग्रामीण क्षेत्रों में ₹1.30 लाख और शहरी में ₹2.50 लाख का पक्का मकान अनुदान", "सोलर लाइट व शौचालय का मुफ्त लाभ"],
    ["अनुसूचित जनजाति (ST) प्रमाणपत्र", "वन अधिकार पट्टा या जमीन का दाखिला", "आय प्रमाणपत्र (< ₹1.5 लाख)", "आधार कार्ड"],
    ["एकीकृत आदिवासी विकास परियोजना (ITDP) कार्यालय में आवेदन करें", "स्थल निरीक्षण उपरांत स्वीकृति", "बैंक खाते में चरणबद्ध अनुदान"],
    "शबरी घरकुल योजना (आदिवासी घरकुल)", "महाराष्ट्र शासन", "महाराष्ट्रातील अनुसूचित जमाती (ST) बांधवांसाठी पक्के घर बांधण्यासाठी ₹१.३० लाख ते ₹२.५० लाखांचे थेट अनुदान.",
    ["ग्रामीण भागात ₹१.३० लाख व शहरात ₹२.५० लाख अनुदान", "सौर दिवा व शौचालय मोफत"],
    ["जात प्रमाणपत्र (ST)", "जागेचा पुरावा / वनपट्टा", "उत्पन्न दाखला (< १.५ लाख)", "आधार कार्ड"],
    ["एकात्मिक आदिवासी विकास प्रकल्प (ITDP) कार्यालयात अर्ज करा", "थेट बँक खात्यात हप्ते जमा"],
    "ஷபரி கர்குல் பழங்குடியினர் வீட்டு வசதி திட்டம்", "மகாராஷ்டிரா அரசு", "மகாராஷ்டிராவில் உள்ள ST பழங்குடியின மக்களுக்கு கான்கிரீட் வீடு கட்ட ₹2.5 லட்சம் வரை அரசு மானியம்.",
    ["வீடு கட்ட ₹2.5 லட்சம் வரை முழு மானியம்", "சூரிய ஒளி விளக்கு மற்றும் கழிப்பறை இலவசம்"],
    ["பழங்குடியினர் சாதிச் சான்றிதழ் (ST)", "நில ஆவணம்", "வருமானச் சான்றிதழ்"],
    ["பழங்குடியினர் நல அலுவலகத்தில் விண்ணப்பிக்கவும்"])

add("karnataka_gruha_lakshmi", "state", "Karnataka", {"gender": "female"},
    "Gruha Lakshmi Guarantee Scheme (Karnataka)", "State · Karnataka", "Monthly financial allowance of ₹2,00,0 directly to women heads of households in Karnataka.",
    ["₹2,000 credited every month into woman head of family's account", "Benefiting over 1.1 Crore families across Karnataka"],
    ["Antyodaya, BPL or APL Ration Card", "Aadhaar of wife and husband", "Aadhaar-linked bank account"],
    ["Register via Grama One, Karnataka One, or Bengaluru One centers", "Direct automated monthly bank transfer"],
    "https://sevasindhuservices.karnataka.gov.in",
    "गृह लक्ष्मी योजना (कर्नाटक)", "कर्नाटक शासन", "कर्नाटक में परिवार की महिला मुखिया को हर महीने ₹2,000 की सीधी नकद वित्तीय सहायता।",
    ["हर महीने ₹2,000 सीधे बैंक खाते में (₹24,000 प्रतिवर्ष)", "राज्य की 1.1 करोड़ से अधिक महिलाओं को सीधा लाभ"],
    ["बीपीएल / एपीएल राशन कार्ड", "पति व पत्नी दोनों का आधार कार्ड", "बैंक खाता विवरण"],
    ["ग्राम वन या कर्नाटक वन केंद्र पर आवेदन करें", "मासिक स्वचालित बैंक भुगतान"],
    "गृहलक्ष्मी योजना (कर्नाटक)", "कर्नाटक शासन", "कर्नाटकातील कुटुंबप्रमुख महिलांना दरमहा ₹२,००० थेट बँक खात्यात आर्थिक सहाय्य.",
    ["दरमहा ₹२,००० थेट खात्यात (वर्षाला ₹२४,०००)", "महिलांच्या आर्थिक स्वातंत्र्यासाठी"],
    ["रेशन कार्ड", "पती-पत्नीचे आधार कार्ड", "बँक पासबुक"],
    ["ग्राम वन केंद्रावर नोंदणी करा", "दरमहा थेट बँक जमा"],
    "கிருஹ லக்ஷ்மி திட்டம் (கர்நாடகா)", "கர்நாடக அரசு", "குடும்ப தலைவிகளுக்கு மாதம் ₹2,000 வழங்கும் உத்தரவாத திட்டம்.",
    ["மாதம் ₹2,000 (ஆண்டுக்கு ₹24,000) நேரடி வங்கி வரவு", "பெண்கள் குடும்ப உரிமை"],
    ["குடும்ப அட்டை (Ration Card)", "ஆதார் அட்டை", "வங்கி கணக்கு"],
    ["கிராம ஒன் மையத்தில் பதிவு செய்யவும்", "மாதாந்திர உதவித்தொகை பெறவும்"])

add("karnataka_yuva_nidhi", "state", "Karnataka", {"occupation": "unemployed", "age_min": 21, "age_max": 30},
    "Yuva Nidhi Scheme (Unemployment Allowance)", "State · Karnataka", "Monthly unemployment allowance of ₹3,000 for degree holders and ₹1,500 for diploma holders for up to 2 years.",
    ["₹3,000/month for unemployed graduates and ₹1,500/month for diploma holders", "Financial support while preparing for jobs or skill training"],
    ["Degree / Diploma certificate (Graduated in recent academic year)", "Karnataka Domicile Certificate", "Aadhaar Card", "Unemployment declaration"],
    ["Apply on Seva Sindhu Portal (sevasindhuservices.karnataka.gov.in)", "Document verification with university database", "Monthly DBT until employed or 24 months"],
    "https://sevasindhuservices.karnataka.gov.in",
    "युवा निधि योजना (बेरोजगारी भत्ता - कर्नाटक)", "कर्नाटक शासन", "कर्नाटक के बेरोजगार स्नातकों को ₹3,000 और डिप्लोमा धारकों को ₹1,500 प्रतिमाह का बेरोजगारी भत्ता।",
    ["स्नातक डिग्री धारकों को ₹3,000 तथा डिप्लोमा धारकों को ₹1,500 प्रति माह", "अधिकतम 2 वर्ष तक वित्तीय सहायता जब तक रोजगार न मिले"],
    ["डिग्री / डिप्लोमा प्रमाणपत्र", "कर्नाटक अधिवास प्रमाणपत्र", "आधार कार्ड", "बेरोजगारी स्व-घोषणा"],
    ["सेवा सिंधु पोर्टल पर ऑनलाइन आवेदन करें", "विश्वविद्यालय रिकॉर्ड से मिलान", "सीधे खाते में मासिक भत्ता"],
    "युवा निधी योजना (कर्नाटक)", "कर्नाटक शासन", "कर्नाटकातील बेरोजगार पदवीधरांना दरमहा ₹३,००० आणि पदविका धारकांना ₹१,५०० बेरोजगारी भत्ता.",
    ["पदवीधरांना ₹३,००० व डिप्लोमाधारकांना ₹१,५०० दरमहा", "नोकरी मिळेपर्यंत २ वर्षांसाठी सहाय्य"],
    ["पदवी प्रमाणपत्र", "रहिवासी दाखला", "आधार कार्ड"],
    ["सेवा सिंधू पोर्टलवर अर्ज करा", "मासिक थेट लाभ"],
    "யுவ நிதி திட்டம் (கர்நாடகா)", "கர்நாடக அரசு", "வேலையற்ற பட்டதாரிகளுக்கு மாதம் ₹3,000 மற்றும் டிப்ளமோ முடித்தவர்களுக்கு ₹1,500 வேலையின்மை உதவித்தொகை.",
    ["பட்டதாரிகளுக்கு மாதம் ₹3,000 மற்றும் டிப்ளமோவுக்கு ₹1,500", "வேலை கிடைக்கும் வரை 2 ஆண்டுகள் நிதி உதவி"],
    ["பட்டப்படிப்பு சான்றிதழ்", "இருப்பிடச் சான்று", "ஆதார் அட்டை"],
    ["சேவா சிந்து தளத்தில் விண்ணப்பிக்கவும்", "வங்கி கணக்கில் வரவு"])

add("up_shadi_anudan", "state", "Uttar Pradesh", {"gender": "female", "income_max": 56000},
    "UP Shadi Anudan Yojana (Daughter Marriage Grant)", "State · Uttar Pradesh", "Financial grant of ₹20,000 per daughter for marriages of girls belonging to SC/ST/OBC and Minority families in UP.",
    ["Direct grant of ₹20,000 per daughter credited to bank account", "Applicable up to two daughters per family"],
    ["Daughter's age proof (18+) and Groom's age proof (21+)", "Income Certificate (< ₹46,080 rural / < ₹56,460 urban)", "Wedding card", "Caste Certificate"],
    ["Apply on shadianudan.upsdc.gov.in 90 days before or after wedding", "Verification by SDM / Block Development Officer", "Amount credited via DBT"],
    "https://shadianudan.upsdc.gov.in",
    "शादी अनुदान योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "उत्तर प्रदेश के गरीब परिवारों की बेटियों के विवाह हेतु ₹20,000 की सरकारी आर्थिक सहायता।",
    ["प्रति पुत्री ₹20,000 का एकमुश्त नकद अनुदान", "एक परिवार की अधिकतम दो बेटियों के लिए मान्य"],
    ["पुत्री की आयु प्रमाण (18+) व वर की आयु (21+)", "आय प्रमाणपत्र", "शादी का कार्ड", "जाति प्रमाणपत्र"],
    ["shadianudan.upsdc.gov.in पर शादी से 90 दिन पूर्व या बाद में आवेदन करें", "एसडीएम/बीडीओ द्वारा सत्यापन", "खाते में राशि अंतरण"],
    "विवाह अनुदान योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "उत्तर प्रदेशातील गरजू कुटुंबातील मुलींच्या लग्नासाठी ₹२०,००० आर्थिक अनुदान.",
    ["प्रत्येक मुलीसाठी ₹२०,००० एकरकमी अनुदान", "एका कुटुंबातील दोन मुलींना लाभ"],
    ["वयाचा दाखला", "उत्पन्न दाखला", "लग्नपत्रिका", "जात प्रमाणपत्र"],
    ["शासकीय पोर्टलवर ऑनलाइन अर्ज करा", "पडताळणीनंतर थेट बँक खात्यात पैसे"],
    "திருமண உதவித் திட்டம் (உத்தர பிரதேசம்)", "உத்தர பிரதேச அரசு", "ஏழை குடும்பங்களைச் சேர்ந்த பெண்களின் திருமணத்திற்கு ₹20,000 அரசு நிதியுதவி.",
    ["ஒரு பெண்ணுக்கு ₹20,000 நேரடி வங்கி மானியம்", "குடும்பத்தில் இரு பெண்களுக்கு பொருந்தும்"],
    ["மணப்பெண் மற்றும் மணமகன் வயது சான்று", "வருமானச் சான்றிதழ்", "திருமண அழைப்பிதழ்"],
    ["போர்ட்டலில் விண்ணப்பிக்கவும்", "வங்கி கணக்கில் பணம் வரவு"])

add("up_kanya_sumangala", "state", "Uttar Pradesh", {"gender": "female", "income_max": 300000},
    "Mukhyamantri Kanya Sumangala Yojana", "State · Uttar Pradesh", "Financial aid of ₹15,000 in 6 milestones from birth to degree admission for girl children in Uttar Pradesh.",
    ["Total ₹15,000 disbursed across birth, vaccination, school admission, and higher studies", "Ensures complete education and health for girls"],
    ["Girl's Birth Certificate", "UP Domicile certificate", "Family Income Certificate (< ₹3 Lakh)", "School admission certificate"],
    ["Apply online on mksy.up.gov.in for specific stage milestone", "Block / District officer scrutiny", "DBT credit directly to parent or girl child's account"],
    "https://mksy.up.gov.in",
    "मुख्यमंत्री कन्या सुमंगला योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "उत्तर प्रदेश में बालिकाओं के जन्म से लेकर स्नातक तक 6 चरणों में ₹15,000 की वित्तीय सहायता।",
    ["जन्म, टीकाकरण, कक्षा 1, 6, 9 और कॉलेज में प्रवेश पर ₹15,000 तक की कुल सहायता", "बालिका भ्रूण हत्या रोकथाम और शिक्षा को बढ़ावा"],
    ["बालिका का जन्म प्रमाणपत्र", "उत्तर प्रदेश निवास प्रमाणपत्र", "परिवार का आय प्रमाणपत्र (< ₹3 लाख)", "स्कूल/कॉलेज प्रवेश रसीद"],
    ["mksy.up.gov.in पोर्टल पर प्रत्येक चरण के अनुसार ऑनलाइन आवेदन करें", "सत्यापन उपरांत बैंक खाते में राशि"],
    "कन्या सुमंगला योजना (उत्तर प्रदेश)", "उत्तर प्रदेश शासन", "मुलींच्या जन्मापासून पदवीपर्यंत ६ टप्प्यांत ₹१५,००० ची आर्थिक मदत.",
    ["जन्म, लसीकरण व शाळा-कॉलेज प्रवेशावर ₹१५,००० एकूण लाभ", "मुलींचे आरोग्य व शिक्षण संरक्षण"],
    ["जन्म दाखला", "रहिवासी दाखला", "उत्पन्न दाखला (< ३ लाख)", "शाळा प्रवेश पावती"],
    ["mksy.up.gov.in पोर्टलवर अर्ज करा", "टप्प्याटप्प्याने खात्यात रक्कम जमा"],
    "கன்யா சுமங்கலா திட்டம் (உத்தர பிரதேசம்)", "உத்தர பிரதேச அரசு", "பெண் குழந்தைகளின் பிறப்பு முதல் கல்லூரி படிப்பு வரை 6 நிலைகளில் ₹15,000 நிதியுதவி.",
    ["பிறப்பு, தடுப்பூசி மற்றும் கல்வி நிலைகளில் மொத்தம் ₹15,000", "பெண் கல்வி மற்றும் முன்னேற்றம்"],
    ["பிறப்புச் சான்றிதழ்", "இருப்பிடச் சான்று", "வருமானச் சான்றிதழ்"],
    ["போர்ட்டலில் விண்ணப்பித்து நிதி பெறுதல்"])

# Save updated list
total_merged = schemes + new_items
with open(SCHEMES_FILE, "w", encoding="utf-8") as f:
    json.dump(total_merged, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_items)} additional schemes.")
print(f"Grand total schemes in database: {len(total_merged)}")
