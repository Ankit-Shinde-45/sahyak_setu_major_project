# -*- coding: utf-8 -*-
"""
Adds 25 more state and central flagship schemes to bring schemes.json to 184 schemes.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMES_FILE = os.path.join(BASE_DIR, "data", "schemes.json")

with open(SCHEMES_FILE, "r", encoding="utf-8") as f:
    schemes = json.load(f)

existing_ids = set(s["id"] for s in schemes)

more_schemes = [
    ("gujarat_kisan_suryodaya", "Gujarat Kisan Suryodaya Yojana (Daytime Power)", "किसान सूर्योदय योजना (गुजरात - दिन में बिजली)", "किसान सूर्योदय योजना (गुजरात)", "கிசான் சூர்யோதயா திட்டம் (குஜராத்)", "Agriculture", "farmer", None, None, "Gujarat"),
    ("gujarat_shramik_annapurna", "Shramik Annapurna Yojana (₹5 Hot Meals for Workers)", "श्रमिक अन्नपूर्णा योजना (गुजरात - ₹5 में भरपेट भोजन)", "श्रमिक अन्नपूर्णा योजना", "ஷ்ராமிக் அன்னபூர்ணா திட்டம் (குஜராத்)", "Workers", "unorganized", None, None, "Gujarat"),
    ("gujarat_vidya_deep_bima", "Vidya Deep Bima Yojana for Students", "विद्या दीप बीमा योजना (गुजरात - छात्र दुर्घटना सुरक्षा)", "विद्या दीप विमा योजना", "வித்யா தீப் மாணவர் காப்பீட்டுத் திட்டம்", "Education", "student", None, None, "Gujarat"),
    ("gujarat_mukhyamantri_yuva_swavalamban", "Mukhyamantri Yuva Swavalamban Yojana (MYSY Gujarat)", "मुख्यमंत्री युवा स्वावलंबन योजना (MYSY गुजरात)", "मुख्यमंत्री युवा स्वावलंबन योजना", "முதலமைச்சர் யுவ ஸ்வாவலம்பன் திட்டம்", "Scholarship", "student", None, None, "Gujarat"),
    ("gujarat_vahli_dikri", "Vahli Dikri Yojana (Support for Daughters)", "व्हाहली डिकरी योजना (गुजरात - बालिका सुरक्षा)", "व्हाहली डिकरी योजना", "வாஹ்லி திக்ரி திட்டம் (பெண் குழந்தைகள்)", "Girl Child", None, "female", None, "Gujarat"),

    ("telangana_kcr_kit_maternity", "KCR Kit Scheme for Mothers and Newborns", "केसीआर किट योजना (तेलंगाना - मातृत्व सहायता)", "केसीआर किट योजना", "கேசிஆர் கிட் தாய்-சேய் நலத் திட்டம்", "Maternity", None, "female", None, "Telangana"),
    ("telangana_kalyana_lakshmi", "Kalyana Lakshmi / Shaadi Mubarak Scheme", "कल्याण लक्ष्मी योजना (तेलंगाना - विवाह सहायता)", "कल्याण लक्ष्मी योजना", "கல்யாண லக்ஷ்மி திருமண உதவித் திட்டம்", "Marriage Aid", None, "female", None, "Telangana"),
    ("telangana_aasara_pension", "Aasara Pension Scheme for Elders, Widows, Weavers", "आसरा पेंशन योजना (तेलंगाना)", "आसरा निवृत्तीवेतन योजना", "ஆசரா ஓய்வூதியத் திட்டம் (தெலங்கானா)", "Social Security", "senior", None, None, "Telangana"),
    ("telangana_dalitha_bandhu", "Telangana Dalitha Bandhu (₹10 Lakh Grant for SC)", "दलित बंधु योजना (तेलंगाना - ₹10 लाख प्रत्यक्ष अनुदान)", "दलित बंधू योजना", "தலித் பந்து திட்டம் (தெலங்கானா)", "SC Empowerment", "entrepreneur", None, ["sc"], "Telangana"),

    ("karnataka_shakti_free_bus", "Shakti Scheme (Free Bus Travel for Women in Karnataka)", "शक्ति योजना (कर्नाटक - महिलाओं हेतु मुफ्त बस यात्रा)", "शक्ती मोफत बस प्रवास योजना", "சக்தி இலவச மகளிர் பேருந்து திட்டம்", "Transport", "homemaker", "female", None, "Karnataka"),
    ("karnataka_anna_bhagya_dbt", "Anna Bhagya Scheme (Free Rice & DBT in Karnataka)", "अन्न भाग्य योजना (कर्नाटक - निःशुल्क राशन व डीबीटी)", "अन्न भाग्य योजना", "அன்ன பாக்யா இலவச உணவு திட்டம்", "Food Security", None, None, None, "Karnataka"),
    ("karnataka_gruha_jyothi_free_power", "Gruha Jyothi (Up to 200 Units Free Electricity)", "गृह ज्योति योजना (कर्नाटक - 200 यूनिट तक मुफ्त बिजली)", "गृह ज्योती मोफत वीज योजना", "கிருஹ ஜோதி இலவச மின்சாரத் திட்டம்", "Energy", "homemaker", None, None, "Karnataka"),

    ("rajasthan_kamdhenu_dairy_bima", "Mukhyamantri Kamdhenu Pashu Bima Yojana", "मुख्यमंत्री कामधेनु पशु बीमा योजना (राजस्थान - ₹40,000 पशु बीमा)", "मुख्यमंत्री कामधेनू पशु विमा योजना", "காமதேனு கால்நடை காப்பீட்டுத் திட்டம்", "Animal Husbandry", "farmer", None, None, "Rajasthan"),
    ("rajasthan_indira_rasoi_food", "Indira Rasoi Yojana (Nutritious Thali at ₹8)", "इंदिरा रसोई योजना (राजस्थान - ₹8 में भरपेट पौष्टिक भोजन)", "इंदिरा रसोई योजना", "இந்திரா உணவகம் திட்டம் (ராஜஸ்தான்)", "Food Security", "unorganized", None, None, "Rajasthan"),
    ("rajasthan_kali_bai_scooty", "Kali Bai Bhil Medhavi Chhatra Scooty Yojana", "काली बाई भील मेधावी छात्रा स्कूटी योजना (राजस्थान)", "कालीबाई भील मेधावी विद्यार्थिनी स्कूटी योजना", "காளி பாய் மாணவிகள் ஸ்கூட்டர் திட்டம்", "Education", "student", "female", None, "Rajasthan"),

    ("up_abhyudaya_free_coaching", "Mukhyamantri Abhyudaya Yojana (Free IAS/NEET Coaching)", "मुख्यमंत्री अभ्युदय योजना (उत्तर प्रदेश - निःशुल्क आईएएस/नीट कोचिंग)", "मुख्यमंत्री अभ्युदय मोफत स्पर्धा परीक्षा मार्गदर्शन", "அப்யுதயா இலவச போட்டித் தேர்வு பயிற்சி", "Education", "student", None, None, "Uttar Pradesh"),
    ("up_shramik_ration_kit", "UP Building Workers Free Ration and Tool Kit", "उत्तर प्रदेश भवन श्रमिक राशन किट एवं आपदा सहायता", "उत्तर प्रदेश बांधकाम कामगार पोषण सहाय्य", "கட்டுமான தொழிலாளர் உதவித் திட்டம் (UP)", "Workers", "unorganized", None, None, "Uttar Pradesh"),
    ("up_destitute_women_pension", "Pati Ki Mrityuoparant Nirashrit Mahila Pension (UP)", "पति की मृत्युपरांत निराश्रित महिला पेंशन योजना (उत्तर प्रदेश)", "पतीच्या निधनानंतर निराधार महिला पेन्शन", "ஆதரவற்ற பெண்கள் ஓய்வூதியத் திட்டம் (UP)", "Widow Support", None, "female", None, "Uttar Pradesh"),

    ("bihar_har_ghar_nal_ka_jal", "Mukhyamantri Har Ghar Nal Ka Jal Yojana", "मुख्यमंत्री हर घर नल का जल योजना (बिहार - शुद्ध पेयजल)", "हर घर नळ पाणी योजना", "அனைத்து வீடுகளுக்கும் குடிநீர் திட்டம் (பீகார்)", "Drinking Water", None, None, None, "Bihar"),
    ("bihar_krishi_yantrikaran", "Bihar Krishi Yantrikaran Subsidy Scheme", "कृषि यंत्रीकरण योजना (बिहार - कृषि उपकरणों पर 50% से 80% अनुदान)", "बिहार कृषी यांत्रिकीकरण योजना", "பீகார் வேளாண் இயந்திரமயமாக்கல் திட்டம்", "Agriculture", "farmer", None, None, "Bihar"),
    ("bihar_kushal_yuva_program", "Kushal Yuva Program (KYP - IT, Language & Soft Skills)", "कुशल युवा कार्यक्रम (KYP बिहार - कंप्यूटर व भाषा कौशल)", "कुशल युवा कार्यक्रम", "திறன்மிகு இளைஞர் திட்டம் (பீகார்)", "Skill Development", "student", None, None, "Bihar"),

    ("tn_illam_thedi_kalvi", "Illam Thedi Kalvi (Education at Doorstep Tamil Nadu)", "इल्लम थेडी कल्लवी (घर-द्वार शिक्षा योजना - तमिलनाडु)", "इल्लम थेडी शिक्षण योजना", "இல்லம் தேடிக் கல்வி திட்டம்", "Education", "student", None, None, "Tamil Nadu"),
    ("tn_makkalai_thedi_maruthuvam", "Makkalai Thedi Maruthuvam (Healthcare at Doorstep)", "मक्कलाई थेडी मारुथुवम (घर-द्वार स्वास्थ्य जांच - तमिलनाडु)", "घरोघरी आरोग्य सेवा योजना", "மக்களைத் தேடி மருத்துவம் திட்டம்", "Doorstep Health", "senior", None, None, "Tamil Nadu"),
    ("tn_innuyir_kaappom_nammai_kaakkum_48", "Innuyir Kaappom - Nammai Kaakkum 48 (Road Accident Care)", "इन्नुयिर काप्पोम (तमिलनाडु - सड़क दुर्घटना में पहले 48 घंटे मुफ्त इलाज)", "रस्ता अपघात मोफत तात्काळ उपचार योजना", "இன்னுயிர் காப்போம் - நம்மைக் காக்கும் 48 திட்டம்", "Emergency Care", None, None, None, "Tamil Nadu"),
    ("tn_anbalayam_differently_abled", "Chief Minister Scheme for Differently Abled Special Care", "तमिलनाडु विशेष दिव्यांग देखभाल एवं पुनर्वास सहायता", "दिव्यांग विशेष पुनर्वसन व सहाय्य योजना", "மாற்றுத்திறனாளிகள் சிறப்பு பராமரிப்பு திட்டம்", "Disability", None, None, None, "Tamil Nadu")
]

added = 0
for row in more_schemes:
    sid, en_n, hi_n, mr_n, ta_n, tag, occ, gen, cat, st = row
    if sid in existing_ids:
        continue
    rule = {}
    if occ: rule["occupation"] = occ
    if gen: rule["gender"] = gen
    if cat: rule["category_in"] = cat
    if st: rule["state"] = st

    schemes.append({
        "id": sid,
        "scope": "state" if st else "central",
        "state": st,
        "rule": rule,
        "t": {
            "en": {
                "name": en_n, "tag": tag,
                "desc": f"Official government welfare program offering direct benefits, financial aid, and services under {en_n}.",
                "benefits": ["Direct government benefit transfer and subsidized service", "Protection and security under state government"],
                "documents": ["Aadhaar Card", "Ration Card or Relevant Proof", "Bank Passbook"],
                "steps": ["Apply on state portal or local administrative office", "Document scrutiny", "Direct benefit disbursement"],
                "link": "https://www.myscheme.gov.in"
            },
            "hi": {
                "name": hi_n, "tag": tag,
                "desc": f"{hi_n} के तहत पात्र नागरिकों को वित्तीय सहायता, सब्सिडी व जनकल्याणकारी सेवाएं।",
                "benefits": ["प्रत्यक्ष सरकारी सहायता एवं रियायती सेवाएं", "आधार लिंक्ड बैंक खाते में प्रत्यक्ष लाभ"],
                "documents": ["आधार कार्ड", "राशन कार्ड या आय प्रमाण", "बैंक पासबुक"],
                "steps": ["पोर्टल या निकटतम सरकारी कार्यालय में आवेदन करें", "सत्यापन उपरांत स्वीकृति", "खाते में लाभ प्राप्त करें"],
                "link": "https://www.myscheme.gov.in"
            },
            "mr": {
                "name": mr_n, "tag": tag,
                "desc": f"{mr_n} अंतर्गत पात्र नागरिकांना थेट आर्थिक मदत, सवलती व सामाजिक सुरक्षा लाभ.",
                "benefits": ["थेट शासकीय आर्थिक सहाय्य व कल्याणकारी योजनांचा लाभ", "थेट बँक खात्यात निधी वर्ग"],
                "documents": ["आधार कार्ड", "रेशन कार्ड किंवा उत्पन्न दाखला", "बँक पासबुक"],
                "steps": ["पोर्टलवर ऑनलाइन अर्ज करा", "कागदपत्र पडताळणी", "खात्यात थेट लाभ जमा"],
                "link": "https://www.myscheme.gov.in"
            },
            "ta": {
                "name": ta_n, "tag": tag,
                "desc": f"{ta_n} திட்டத்தின் கீழ் தகுதியான பயனாளிகளுக்கு அரசு நிதி உதவி மற்றும் நலத்திட்ட பலன்கள்.",
                "benefits": ["நேரடி அரசு நிதி உதவி மற்றும் நலத்திட்ட சேவைகள்", "வங்கி கணக்கில் நேரடி வரவு"],
                "documents": ["ஆதார் அட்டை", "குடும்ப அட்டை", "வங்கி பாஸ்புக்"],
                "steps": ["அரசு இணையதளத்தில் விண்ணப்பிக்கவும்", "சரிபார்ப்பிற்கு பின் ஒப்புதல்", "வங்கி வரவு பெறுதல்"],
                "link": "https://www.myscheme.gov.in"
            }
        }
    })
    existing_ids.add(sid)
    added += 1

with open(SCHEMES_FILE, "w", encoding="utf-8") as f:
    json.dump(schemes, f, ensure_ascii=False, indent=2)

print(f"Added {added} final schemes. Grand total: {len(schemes)}")
