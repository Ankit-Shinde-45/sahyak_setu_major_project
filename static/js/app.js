/* ═══════════════════════════════════════════════════════════════════════════
   Sahayak Setu — Multilingual Voice Engine (English, Hindi, Marathi, Tamil)
   ═══════════════════════════════════════════════════════════════════════════ */

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

function getLang() {
  return window.SAHAYAK_LANG || document.documentElement.lang || 'en';
}

function getSpeechLang() {
  const lang = getLang();
  const map = { en: 'en-IN', hi: 'hi-IN', mr: 'mr-IN', ta: 'ta-IN' };
  return window.SAHAYAK_SPEECH_LANG || map[lang] || 'en-IN';
}

/* ── Preload and cache browser voices ───────────────────────────────────── */
let CACHED_VOICES = [];
function refreshVoices() {
  if (typeof speechSynthesis !== 'undefined') {
    CACHED_VOICES = speechSynthesis.getVoices() || [];
  }
}
if (typeof speechSynthesis !== 'undefined') {
  refreshVoices();
  speechSynthesis.onvoiceschanged = refreshVoices;
}

function getBestVoice(speechLang) {
  let voices = CACHED_VOICES.length ? CACHED_VOICES : (speechSynthesis.getVoices() || []);
  if (!voices || !voices.length) return null;

  const target = speechLang.toLowerCase().replace('_', '-');
  const prefix = target.split('-')[0];

  // 1. Exact match e.g. 'hi-in', 'mr-in', 'ta-in'
  let v = voices.find(x => x.lang.toLowerCase().replace('_', '-') === target);
  if (v) return v;

  // 2. Language prefix match e.g. 'hi', 'mr', 'ta'
  v = voices.find(x => x.lang.toLowerCase().startsWith(prefix));
  if (v) return v;

  // 3. Fallback for Marathi: if system has no mr-IN voice, use Hindi (hi-IN) voice
  // which natively reads Devanagari script accurately
  if (prefix === 'mr') {
    v = voices.find(x => x.lang.toLowerCase().startsWith('hi'));
    if (v) return v;
  }

  // 4. Any Indian accented voice
  v = voices.find(x => x.lang.toLowerCase().includes('in'));
  if (v) return v;

  return null;
}

/* ── Text-To-Speech (TTS) ────────────────────────────────────────────────── */
function speak(text, onEnd) {
  if (!text || typeof speechSynthesis === 'undefined') {
    if (onEnd) onEnd();
    return;
  }
  try {
    speechSynthesis.cancel();
    const speechCode = getSpeechLang();
    const u = new SpeechSynthesisUtterance(text);
    u.lang   = speechCode;
    u.rate   = 0.92;
    u.pitch  = 1.0;
    u.volume = 1.0;

    const chosenVoice = getBestVoice(speechCode);
    if (chosenVoice) {
      u.voice = chosenVoice;
    }

    let ended = false;
    let watchdogTimer = null;
    const done = () => {
      if (!ended) {
        ended = true;
        clearTimeout(watchdogTimer);
        try { speechSynthesis.cancel(); } catch (_) {}
        if (onEnd) onEnd();
      }
    };

    u.onend = done;
    u.onerror = done;

    // Safety watchdog: Chrome sometimes drops onend for non-English voices
    const maxSecs = Math.max(3, Math.ceil((text.length / 10) + 2));
    watchdogTimer = setTimeout(done, maxSecs * 1000);

    // Small delay fixes Chrome cancellation bug on consecutive speaks
    setTimeout(() => {
      try { speechSynthesis.speak(u); } catch (_) { done(); }
    }, 60);
  } catch (e) {
    if (onEnd) onEnd();
  }
}

/* ── Global Speech-To-Text Manager ──────────────────────────────────────── */
let CURRENT_RECOGNITION = null;

function stopCurrentRecognition() {
  if (CURRENT_RECOGNITION) {
    try {
      CURRENT_RECOGNITION.onresult = null;
      CURRENT_RECOGNITION.onerror = null;
      CURRENT_RECOGNITION.onend = null;
      CURRENT_RECOGNITION.abort();
    } catch (_) {}
    CURRENT_RECOGNITION = null;
  }
}

/* ── Speech-To-Text (STT) with Progressive Capture and Fallback ─────────── */
function listenOnce(ms) {
  ms = ms || 12000;
  return new Promise((resolve, reject) => {
    if (!SR) return reject('unsupported');

    // 1. Release previous recognizers and audio synthesis hardware
    stopCurrentRecognition();
    if (typeof wakeRec !== 'undefined' && wakeRec) {
      try { wakeRec.stop(); } catch (_) {}
    }
    if (typeof speechSynthesis !== 'undefined') {
      try { speechSynthesis.cancel(); } catch (_) {}
    }

    const primaryLang = getSpeechLang();
    let currentLang = primaryLang;
    let settled = false;
    let gatheredAlts = [];
    let silenceDebounce = null;
    let retriesLeft = 2;

    const finish = (ok, val) => {
      if (settled) return;
      settled = true;
      clearTimeout(overallTimer);
      clearTimeout(silenceDebounce);
      stopCurrentRecognition();
      if (ok && val && val.length > 0) {
        resolve(val);
      } else {
        reject(val || 'no-speech');
      }
    };

    const overallTimer = setTimeout(() => {
      if (gatheredAlts.length > 0) {
        finish(true, gatheredAlts);
      } else {
        finish(false, 'timeout');
      }
    }, ms);

    function startRecognizer() {
      if (settled) return;
      stopCurrentRecognition();

      try {
        const r = new SR();
        CURRENT_RECOGNITION = r;
        r.lang = currentLang;
        r.continuous = false;
        r.interimResults = true;
        r.maxAlternatives = 5;

        r.onresult = e => {
          let finalChunk = '';
          let interimChunk = '';
          const altsSet = new Set();

          for (let ri = 0; ri < e.results.length; ri++) {
            const res = e.results[ri];
            if (res.isFinal) {
              finalChunk += res[0].transcript + ' ';
            } else {
              interimChunk += res[0].transcript;
            }
            for (let ai = 0; ai < res.length; ai++) {
              const t = res[ai].transcript.trim();
              if (t) altsSet.add(t);
            }
          }

          const combined = (finalChunk + interimChunk).trim();
          if (combined) {
            gatheredAlts = [combined, ...Array.from(altsSet).filter(x => x !== combined)];
            if (VM && VM.showHeard) {
              VM.showHeard(combined);
            }

            // Debounce after segment is marked final so we don't cut off user mid-sentence
            if (e.results[e.results.length - 1].isFinal) {
              clearTimeout(silenceDebounce);
              silenceDebounce = setTimeout(() => {
                finish(true, gatheredAlts);
              }, 750);
            }
          }
        };

        r.onerror = ev => {
          clearTimeout(silenceDebounce);
          if (gatheredAlts.length > 0) {
            finish(true, gatheredAlts);
            return;
          }

          // If Marathi mr-IN throws error, seamlessly fallback to hi-IN
          if (currentLang === 'mr-IN' && (ev.error === 'language-not-supported' || ev.error === 'network' || ev.error === 'not-allowed-in-language')) {
            currentLang = 'hi-IN';
            setTimeout(startRecognizer, 120);
            return;
          }

          // If no-speech and timeout has not arrived, try listening again
          if (ev.error === 'no-speech' && retriesLeft > 0 && !settled) {
            retriesLeft--;
            setTimeout(startRecognizer, 120);
            return;
          }

          finish(false, ev.error);
        };

        r.onend = () => {
          clearTimeout(silenceDebounce);
          if (gatheredAlts.length > 0) {
            finish(true, gatheredAlts);
          } else if (!settled && retriesLeft > 0) {
            retriesLeft--;
            setTimeout(startRecognizer, 120);
          } else {
            finish(false, 'no-speech');
          }
        };

        r.start();
      } catch (err) {
        if (currentLang === 'mr-IN') {
          currentLang = 'hi-IN';
          setTimeout(startRecognizer, 120);
          return;
        }
        finish(false, String(err));
      }
    }

    // Small initial buffer gives Chrome's audio input pipeline time to open
    setTimeout(startRecognizer, 120);
  });
}

/* /* ── Number parsing with Devanagari & Tamil numeral normalization ────────── */
function normalizeNumerals(text) {
  if (!text) return '';
  return text
    // Devanagari numerals: ०-९ -> 0-9
    .replace(/[०-९]/g, d => String.fromCharCode(d.charCodeAt(0) - 0x0966 + 48))
    // Tamil numerals: ௦-௯ -> 0-9
    .replace(/[௦-௯]/g, d => String.fromCharCode(d.charCodeAt(0) - 0x0BE6 + 48));
}

const HINDI_MARATHI_NUMS = {
  // English
  'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,
  'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19,
  'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90,'hundred':100,'thousand':1000,'lakh':100000,'crore':10000000,
  // 1 to 100 Hindi & Marathi
  'शून्य':0,'एक':1,'दोन':2,'दो':2,'तीन':3,'चार':4,'पाच':5,'पाँच':5,'पांच':5,'सहा':6,'छह':6,'छः':6,'सात':7,'आठ':8,'नऊ':9,'नौ':9,
  'दहा':10,'दस':10,'अकरा':11,'ग्यारह':11,'बारा':12,'बारह':12,'तेरा':13,'तेरह':13,'चौदा':14,'चौदह':14,'पंधरा':15,'पंद्रह':15,
  'सोळा':16,'सोलह':16,'सतरा':17,'सत्रह':17,'अठरा':18,'अठारह':18,'एकोणीस':19,'उन्नीस':19,'वीस':20,'बीस':20,
  'एकवीस':21,'इक्कीस':21,'बावीस':22,'बाईस':22,'तेवीस':23,'तेईस':23,'चोवीस':24,'चौबीस':24,
  'पंचवीस':25,'पच्चीस':25,'सव्वीस':26,'छब्बीस':26,'सत्तावीस':27,'सत्ताईस':27,'अठ्ठावीस':28,'अट्ठाईस':28,'अट्ठावीस':28,
  'एकोणतीस':29,'उनतीस':29,'तीस':30,'एकतीस':31,'इकतीस':31,'बत्तीस':32,'तेहतीस':33,'तैंतीस':33,'चौतीस':34,
  'पस्तीस':35,'पैंतीस':35,'छत्तीस':36,'सदतीस':37,'सैंतीस':37,'अडतीस':38,'अड़तीस':38,'एकोणचाळीस':39,'उनतालीस':39,
  'चाळीस':40,'चालीस':40,'एकेचाळीस':41,'इकतालीस':41,'बेचाळीस':42,'बयालीस':42,'त्रेचाळीस':43,'तैंतालीस':43,
  'चव्वेचाळीस':44,'चवालीस':44,'पंचेचाळीस':45,'पैंतालीस':45,'शेहेचाळीस':46,'छियालीस':46,'सत्तेचाळीस':47,'सैंतालीस':47,
  'अट्ठेचाळीस':48,'अड़तालीस':48,'एकोणपन्नास':49,'उनचास':49,'पन्नास':50,'पचास':50,
  'एकावन्न':51,'इक्यावन':51,'बावन्न':52,'बावन':52,'त्रेपन्न':53,'तिरेपन':53,'चोपन्न':54,'चौवन':54,
  'पंचावन्न':55,'पचपन':55,'छप्पन्न':56,'छप्पन':56,'सत्तावन्न':57,'सत्तावन':57,'अठ्ठावन्न':58,'अट्ठावन':58,
  'एकोणसाठ':59,'उनसठ':59,'साठ':60,'एकसष्ठ':61,'एकसठ':61,'बासष्ठ':62,'बासठ':62,'त्रेसष्ठ':63,'तिरसठ':63,
  'चौसष्ठ':64,'चौंसठ':64,'पासष्ठ':65,'पैंसठ':65,'सहासष्ठ':66,'छियासठ':66,'सदसष्ठ':67,'सरसठ':67,'अडसष्ठ':68,'अड़सठ':68,
  'एकोणसत्तर':69,'उनहत्तर':69,'सत्तर':70,'एकाहत्तर':71,'इकहत्तर':71,'बहत्तर':72,'त्र्याहत्तर':73,'तिहत्तर':73,
  'चौहत्तर':74,'पंच्याहत्तर':75,'पचहत्तर':75,'शहात्तर':76,'छिहत्तर':76,'सत्याहत्तर':77,'सतहत्तर':77,
  'अठ्ठ्याहत्तर':78,'अठहत्तर':78,'एकोण्यांशी':79,'उन्यासी':79,'ऐंशी':80,'अस्सी':80,
  'एक्यांशी':81,'इक्यासी':81,'ब्यांशी':82,'बयासी':82,'त्र्यांशी':83,'तिरासी':83,'चौऱ्यांशी':84,'चौरासी':84,
  'पंच्यांशी':85,'पचासी':85,'शहांशी':86,'छियासी':86,'सत्यांशी':87,'सत्तासी':87,'अठ्ठ्यांशी':88,'अट्ठासी':88,
  'एकोणनव्वद':89,'नवाँसी':89,'नव्वद':90,'नब्बे':90,'एक्याण्णव':91,'इक्यानवे':91,'ब्याण्णव':92,'बानवे':92,
  'त्र्याण्णव':93,'तिरानवे':93,'चौऱ्याण्णव':94,'चौरानवे':94,'पंच्याण्णव':95,'पचानवे':95,'शहाण्णव':96,'छियानवे':96,
  'सत्याण्णव':97,'संतानवे':97,'अठ्ठ्याण्णव':98,'अट्ठानवे':98,'नव्व्याण्णव':99,'निन्यानवे':99,
  'शंभर':100,'सौ':100,'हजार':1000,'हज़ार':1000,'लाख':100000,'कोटी':10000000,'करोड़':10000000,
  // Fractions
  'दीड':1.5,'डेढ़':1.5,'अडीच':2.5,'ढाई':2.5,'अढ़ाई':2.5,
  // Tamil
  'ஒன்று':1,'இரண்டு':2,'மூன்று':3,'நான்கு':4,'ஐந்து':5,'ஆறு':6,'ஏழு':7,'எட்டு':8,'ஒன்பது':9,'பத்து':10,
  'இருபது':20,'இருபத்தைந்து':25,'முப்பது':30,'நாற்பது':40,'ஐம்பது':50,'அறுபது':60,'எழுபது':70,'எண்பது':80,'தொண்ணூறு':90,'நூறு':100,'ஆயிரம்':1000,'லட்சம்':100000
};

function extractNumber(text) {
  if (!text) return NaN;
  const s = normalizeNumerals(text).toLowerCase();

  // 1. Zero check
  if (/(शून्य|काही नाही|कुछ नहीं|\bzero\b|\bnone\b|\bnil\b|no income)/i.test(s)) return 0;

  // 2. Named fractions with lakh/thousand
  if (/(दीड|डेढ़)\s*(लाख|lakh)/i.test(s)) return 150000;
  if (/(अडीच|ढाई|अढ़ाई)\s*(लाख|lakh)/i.test(s)) return 250000;
  if (/(दीड|डेढ़)\s*(हजार|हज़ार|thousand)/i.test(s)) return 1500;
  if (/(अडीच|ढाई|अढ़ाई)\s*(हजार|हज़ार|thousand)/i.test(s)) return 2500;

  // 3. Multiplier with digits e.g. '1.5 lakh', '2 लाख', '50 हजार'
  const multMatch = s.match(/(\d+(?:\.\d+)?)\s*(लाख|lakh|हजार|हज़ार|thousand|करोड़|करोड|कोटी|crore|k)/i);
  if (multMatch) {
    const val = parseFloat(multMatch[1]);
    const unit = multMatch[2].toLowerCase();
    if (unit.includes('लाख') || unit.includes('lakh')) return Math.round(val * 100000);
    if (unit.includes('हजार') || unit.includes('हज़ार') || unit.includes('thousand') || unit === 'k') return Math.round(val * 1000);
    if (unit.includes('करोड़') || unit.includes('करोड') || unit.includes('कोटी') || unit.includes('crore')) return Math.round(val * 10000000);
  }

  // 4. Word number multiplier: e.g. 'दोन लाख', 'पाच लाख', 'पन्नास हजार', 'एक लाख'
  for (const [w, v] of Object.entries(HINDI_MARATHI_NUMS)) {
    if (v >= 10000000) continue;
    const reLakh = new RegExp('(?:^|\\s)' + w + '\\s*(?:लाख|lakh)', 'i');
    if (reLakh.test(s)) return Math.round(v * 100000);
    const reThous = new RegExp('(?:^|\\s)' + w + '\\s*(?:हजार|हज़ार|thousand)', 'i');
    if (reThous.test(s)) return Math.round(v * 1000);
  }

  // 5. Plain digits anywhere e.g. '25', '50000', 'माझे वय २५ आहे', 'मेरी उम्र 25 साल है'
  const digitMatch = s.replace(/,/g, '').match(/\d+/);
  if (digitMatch) {
    const n = parseInt(digitMatch[0], 10);
    if (!isNaN(n) && n >= 0) return n;
  }

  // 6. Word dictionary match across all tokens
  const tokens = s.replace(/[^a-zA-Z\u0900-\u097F\u0B80-\u0BFF0-9 ]/g, ' ').trim().split(/\s+/);
  for (const tok of tokens) {
    const v = HINDI_MARATHI_NUMS[tok];
    if (v !== undefined) return Math.round(v);
  }
  return NaN;
}

/* ── Multilingual Keyword Dictionary for Selects & States ───────────────── */
const KEYWORD_MAP = {
  /* Gender */
  male: [
    'male', 'man', 'boy', 'पुरुष', 'पुरूष', 'आदमी', 'नर', 'लड़का', 'मुलगा', 'पु',
    'मी पुरुष आहे', 'ஆண்', 'ஆண்கள்', 'purush', 'aadmi', 'mulga', 'aan'
  ],
  female: [
    'female', 'woman', 'girl', 'महिला', 'स्त्री', 'औरत', 'लड़की', 'मुलगी', 'बाई',
    'स्त्रीलिंग', 'बायको', 'मी महिला आहे', 'मी स्त्री आहे', 'गृहिणी',
    'பெண்', 'பெண்கள்', 'mahila', 'stri', 'aurat', 'mulgi', 'pen'
  ],
  other: [
    'other', 'others', 'अन्य', 'इतर', 'अन्यथा', 'மற்றவை', 'மூன்றாம் பாலினம்',
    'anya', 'itar', 'matruvai'
  ],

  /* Occupation */
  farmer: [
    'farmer', 'farming', 'agriculture', 'agriculture worker',
    'किसान', 'कृषि', 'खेती', 'काश्तकार',
    'शेतकरी', 'शेती', 'कृषी', 'मी शेतकरी आहे', 'शेती करतो',
    'விவசாயி', 'விவசாயம்', 'வேளாண்மை',
    'kisan', 'shetkari', 'krishi', 'vivasayi'
  ],
  student: [
    'student', 'study', 'studying', 'college', 'school',
    'छात्र', 'विद्यार्थी', 'छात्रा', 'पढ़ाई', 'पढ़ाई',
    'शिकत आहे', 'शिकतो', 'शिकते', 'अभ्यास', 'शाळा', 'कॉलेज', 'विद्यार्थिनी',
    'மாணவர்', 'மாணவி', 'படிப்பு',
    'chhatra', 'vidyarthi', 'maanavar'
  ],
  entrepreneur: [
    'entrepreneur', 'business', 'businessman', 'self employed', 'startup', 'shop',
    'उद्यमी', 'व्यापारी', 'व्यवसाय', 'दुकानदार', 'कारोबारी', 'कारोबार', 'बिजनेस',
    'उद्योजक', 'व्यापार', 'उद्योग', 'स्वतःचा व्यवसाय', 'दुकान', 'धंदा',
    'தொழில்முனைவோர்', 'வியாபாரி', 'சொந்த தொழில்',
    'udyami', 'udyojak', 'vyapari'
  ],
  unorganized: [
    'unorganized', 'labour', 'labor', 'daily wage', 'worker', 'construction',
    'असंगठित', 'मजदूर', 'दैनिक वेतन', 'श्रमिक', 'दिहाड़ी',
    'असंघटित', 'कामगार', 'मजूर', 'रोजंदारी', 'रोजंदार', 'हमाली',
    'அமைப்பு சாரா', 'தொழிலாளி', 'கூலி',
    'asangathit', 'mazdoor', 'kamgar', 'thozhilali'
  ],
  salaried: [
    'salaried', 'salary', 'job', 'employee', 'employed', 'service', 'office',
    'वेतनभोगी', 'कर्मचारी', 'नौकरी', 'सरकारी नौकरी', 'प्राइवेट नौकरी', 'सर्विस',
    'पगारदार', 'नोकरी', 'पगार', 'कर्मचारी', 'सेवा', 'सर्व्हिस',
    'சம்பள ஊழியர்', 'ஊழியர்', 'அரசு வேலை', 'வேலை',
    'vetanbhogi', 'pagardar', 'naukri', 'sambalam'
  ],
  homemaker: [
    'homemaker', 'housewife', 'home maker', 'domestic',
    'गृहिणी', 'घरेलू', 'घर का काम', 'हाउसवाइफ',
    'घरकाम', 'गृहिणी आहे', 'घरी असते', 'घरी असतो',
    'இல்லத்தரசி', 'வீட்டு வேலை',
    'grihini', 'illatharasi'
  ],
  senior: [
    'senior', 'retired', 'pension', 'pensioner', 'elderly', 'old',
    'वरिष्ठ नागरिक', 'सेवानिवृत्त', 'बुजुर्ग', 'पेंशनर', 'पेंशन', 'वृद्ध',
    'ज्येष्ठ नागरिक', 'निवृत्त', 'पेन्शनधारक', 'पेन्शन', 'म्हातारा', 'म्हातारी',
    'ஓய்வுபெற்றவர்', 'மூத்த குடிமகன்', 'முதியோர்',
    'varishtha', 'nivrutt', 'senior citizen'
  ],
  artisan: [
    'artisan', 'craft', 'craftsman', 'handicraft', 'weaver', 'potter', 'blacksmith',
    'शिल्पकार', 'कारीगर', 'दस्तकार', 'हस्तशिल्प', 'बुनकर',
    'कारागीर', 'हस्तकलाकार', 'विणकर', 'कुंभार', 'लोहार', 'सुतार',
    'கைவினைஞர்', 'நெசவாளர்',
    'shilpkar', 'karagir', 'kaivinainjar'
  ],
  vendor: [
    'vendor', 'street vendor', 'hawker', 'stall', 'thela',
    'रेहड़ी', 'पटरी', 'ठेला', 'ठेलेवाला', 'फेरीवाला',
    'हातगाडी', 'विक्रेता', 'दुकान', 'स्टॉल',
    'தெரு வியாபாரி', 'விற்பனையாளர்',
    'rehdi', 'feriwala', 'thela'
  ],
  unemployed: [
    'unemployed', 'jobless', 'no job', 'looking for work',
    'बेरोजगार', 'बेकार', 'नौकरी नहीं है', 'काम नहीं',
    'नोकरी नाही', 'काम नाही', 'बेरोजगार आहे', 'काम शोधतोय',
    'வேலையற்றவர்', 'வேலை இல்லை',
    'berozgar'
  ],

  /* Education */
  below10: [
    'below 10', 'below tenth', 'primary', 'no formal education',
    '10वीं से कम', 'दसवीं से कम', '5वीं', '8वीं', 'प्राथमिक', 'अनपढ़',
    '10वी पेक्षा कमी', 'दहावी पेक्षा कमी', 'पाचवी', 'आठवी', 'सातवी', 'शिक्षण नाही', 'अशिक्षित',
    '10ஆம் வகுப்புக்கு கீழ்', 'பத்தாம் வகுப்புக்கு கீழ்',
    'dasvi se kam'
  ],
  ten12: [
    '10th', '12th', 'tenth', 'twelfth', 'high school', 'secondary', 'intermediate',
    '10वीं', '12वीं', 'दसवीं', 'बारहवीं', 'मैट्रिक', 'इंटर',
    '10वी', '12वी', 'दहावी', 'बारावी', 'दहावी पास', 'बारावी पास', 'एसएससी', 'एचएससी',
    '10ஆம் வகுப்பு', '12ஆம் வகுப்பு', 'பத்தாம் வகுப்பு', 'பன்னிரண்டாம் வகுப்பு',
    'matric', 'inter', 'ssc', 'hsc'
  ],
  grad: [
    'graduate', 'graduation', 'degree', 'bachelor', 'ba', 'bsc', 'bcom', 'btech', 'be',
    'स्नातक', 'डिग्री', 'बीए', 'बीएससी', 'बीकॉम', 'बीटेक', 'इंजीनियरिंग',
    'पदवीधर', 'पदवी', 'ग्रेजुएट', 'ग्रेजुएशन', 'इंजिनिअरिंग',
    'பட்டதாரி', 'பட்டம்',
    'snatak', 'padvidhar', 'pattadhari'
  ],
  pg: [
    'postgraduate', 'post graduate', 'pg', 'masters', 'master', 'phd', 'msc', 'ma', 'mtech', 'mba',
    'स्नातकोत्तर', 'मास्टर्स', 'एमए', 'एमएससी', 'एमबीए', 'एमटेक', 'पीएचडी',
    'पदव्युत्तर', 'पोस्ट ग्रेजुएट', 'पीजी',
    'முதுகலை', 'முதுகலை பட்டம்',
    'snatakottar', 'mudhugalai'
  ],

  /* Category */
  general: [
    'general', 'open', 'open category', 'unreserved',
    'सामान्य', 'ओपन', 'अनारक्षित',
    'सर्वसाधारण', 'खुला प्रवर्ग', 'खुला', 'मराठा', 'ब्राह्मण',
    'பொது', 'பொதுப் பிரிவு',
    'samanya', 'sarvasadharan', 'maratha', 'pothu'
  ],
  obc: [
    'obc', 'other backward class', 'other backward',
    'ओबीसी', 'पिछड़ा वर्ग', 'अन्य पिछड़ा वर्ग',
    'इतर मागासवर्गीय', 'इतर मागास', 'मागास', 'माळी', 'तेली', 'कुणबी',
    'ஓபிசி', 'பிற்படுத்தப்பட்டோர்', 'இதர பிற்படுத்தப்பட்டோர்',
    'pichhada varg', 'maagasvarg', 'kunbi'
  ],
  sc: [
    'sc', 'scheduled caste', 'dalit',
    'अनुसूचित जाति', 'दलित', 'एससी',
    'अनुसूचित जाती', 'मातंग', 'बौद्ध', 'महार', 'चर्मकार',
    'பட்டியல் சாதி', 'எஸ்.சி',
    'anusuchit jati', 'pattiyal saathi'
  ],
  st: [
    'st', 'scheduled tribe', 'tribal', 'adivasi',
    'अनुसूचित जनजाति', 'आदिवासी', 'एसटी',
    'अनुसूचित जमाती', 'भिल्ल', 'गोंड',
    'பட்டியல் பழங்குடி', 'பழங்குடியினர்', 'எஸ்.டி',
    'anusuchit janjati', 'adivasi'
  ],
  other_cat: [
    'prefer not to say', 'dont want to say',
    'बताना नहीं चाहते', 'सांगायचे नाही', 'சொல்ல விரும்பவில்லை'
  ],

  /* States from states.json */
  'Maharashtra': [
    'maharashtra', 'महाराष्ट्र', 'महाराष्ट्रात', 'महा', 'मुंबई', 'पुणे', 'नागपूर', 'मराठी', 'nashik', 'नांदेड', 'ठाणे'
  ],
  'Tamil Nadu': [
    'tamil nadu', 'tamilnadu', 'तमिलनाडु', 'तमिल नाडु', 'तमिळनाडू', 'தமிழ்நாடு', 'சென்னை', 'தமிழ்', 'madurai'
  ],
  'Uttar Pradesh': [
    'uttar pradesh', 'उत्तर प्रदेश', 'यूपी', 'up', 'लखनऊ', 'वाराणसी', 'कानपुर'
  ],
  'Karnataka': [
    'karnataka', 'कर्नाटक', 'கர்நாடகா', 'बेंगलुरु', 'bangalore', 'बंगळुरू'
  ],
  'Gujarat': [
    'gujarat', 'गुजरात', 'குஜராத்', 'अहमदाबाद', 'सूरत'
  ],
  'Rajasthan': [
    'rajasthan', 'राजस्थान', 'ராஜஸ்தான்', 'जयपुर', 'जोधपुर'
  ],
  'Madhya Pradesh': [
    'madhya pradesh', 'मध्य प्रदेश', 'மத்திய பிரதேசம்', 'एमपी', 'भोपाल', 'इंदौर'
  ],
  'Bihar': [
    'bihar', 'बिहार', 'பீகார்', 'पटना'
  ],
  'West Bengal': [
    'west bengal', 'पश्चिम बंगाल', 'மேற்கு வங்கம்', 'बंगाल', 'कोलकाता'
  ],
  'Telangana': [
    'telangana', 'तेलंगाना', 'தெலங்கானா', 'हैदराबाद'
  ],
  'Andhra Pradesh': [
    'andhra pradesh', 'आंध्र प्रदेश', 'ஆந்திர பிரதேசம்', 'आंध्र', 'विजयवाड़ा'
  ],
  'Odisha': [
    'odisha', 'ओडिशा', 'उड़ीसा', 'उड़ीसा', 'ஒடிசா', 'भुवनेश्वर'
  ],
  'Other': [
    'other state', 'other', 'अन्य', 'इतर', 'மற்றவை'
  ]
};

function keywordMatch(select, transcripts) {
  const cands = Array.isArray(transcripts) ? transcripts : [transcripts];
  for (const raw of cands) {
    if (!raw) continue;
    const low = raw.toLowerCase().trim();
    for (const [targetVal, keywords] of Object.entries(KEYWORD_MAP)) {
      const realVal = targetVal === 'other_cat' ? 'other' : targetVal;
      for (const kw of keywords) {
        if (low.includes(kw.toLowerCase())) {
          for (const opt of select.options) {
            if (opt.value === realVal || opt.textContent.trim().toLowerCase() === realVal.toLowerCase()) {
              select.value = opt.value;
              return opt.textContent.trim();
            }
          }
        }
      }
    }
  }
  return null;
}

function matchSelect(select, transcripts) {
  // 1. Explicit keyword match
  const km = keywordMatch(select, transcripts);
  if (km) return km;

  // 2. Direct string inclusion in option label or value
  const cands = Array.isArray(transcripts) ? transcripts : [transcripts];
  for (const raw of cands) {
    if (!raw) continue;
    const low = raw.toLowerCase().trim();
    for (const opt of select.options) {
      if (!opt.value) continue;
      const lbl = opt.textContent.trim().toLowerCase();
      const val = opt.value.toLowerCase();
      if (low.includes(lbl) || (low.length >= 3 && lbl.includes(low)) || low.includes(val)) {
        select.value = opt.value;
        return opt.textContent.trim();
      }
    }
  }
  return null;
}

function matchInput(input, type, transcripts) {
  const cands = Array.isArray(transcripts) ? transcripts : [transcripts];
  for (const raw of cands) {
    if (!raw) continue;
    if (type === 'number') {
      const n = extractNumber(raw);
      if (!isNaN(n) && n >= 0) {
        input.value = n;
        return String(n);
      }
    } else {
      input.value = raw.trim();
      return raw.trim();
    }
  }
  return null;
}

/* ── Voice commands detection (all 4 languages) ─────────────────────────── */
const CMDS = {
  skip: {
    en: ['skip', 'next', 'pass', 'nothing'],
    hi: ['छोड़ें', 'छोड़ो', 'अगला', 'कुछ नहीं', 'आगे बढ़ें', 'skip'],
    mr: ['वगळा', 'पुढे', 'काही नाही', 'पुढे चला', 'skip'],
    ta: ['தவிர்', 'அடுத்து', 'ஒன்றுமில்லை', 'skip']
  },
  back: {
    en: ['go back', 'back', 'previous'],
    hi: ['पीछे', 'वापस', 'पिछला'],
    mr: ['मागे', 'परत', 'मागील'],
    ta: ['பின்', 'பின் செல்']
  },
  repeat: {
    en: ['repeat', 'again', 'say again'],
    hi: ['दोहराएँ', 'फिर से', 'दोबारा'],
    mr: ['पुन्हा सांगा', 'पुन्हा'],
    ta: ['மீண்டும்', 'திரும்ப']
  },
  startOver: {
    en: ['start over', 'restart', 'reset'],
    hi: ['फिर से शुरू', 'दोबारा शुरू'],
    mr: ['पुन्हा सुरू'],
    ta: ['மீண்டும் தொடங்கு']
  }
};

function detectCmd(transcripts) {
  const lang = getLang();
  for (const raw of (Array.isArray(transcripts) ? transcripts : [transcripts])) {
    const low = raw.toLowerCase().trim();
    for (const [cmd, map] of Object.entries(CMDS)) {
      const phrases = map[lang] || map.en;
      if (phrases.some(p => low.includes(p.toLowerCase()))) return cmd;
    }
  }
  return null;
}

function buildConfirm(value) {
  const lang = getLang();
  const map = {
    en: `Got it — ${value}.`,
    hi: `समझ गया — ${value}.`,
    mr: `समजले — ${value}.`,
    ta: `புரிந்தது — ${value}.`
  };
  return map[lang] || `Got it — ${value}.`;
}

/* ── Voice Modal UI Controller ──────────────────────────────────────────── */
const VM = {
  init() {
    this.modal    = document.getElementById('voiceModal');
    this.question = document.getElementById('vmQuestionText');
    this.stepLbl  = document.getElementById('vmStepLabel');
    this.progress = document.getElementById('vmProgressBar');
    this.micRing  = document.getElementById('vmMicRing');
    this.micDot   = document.getElementById('vmMicDot');
    this.stateLbl = document.getElementById('vmStateLabel');
    this.heardBox = document.getElementById('vmHeardBox');
    this.heardLbl = document.getElementById('vmHeardLbl');
    this.heardVal = document.getElementById('vmHeardVal');
    this.ansBox   = document.getElementById('vmAnswerBox');
    this.ansVal   = document.getElementById('vmAnswerVal');
    this.hint     = document.getElementById('vmHint');
    this.skipBtn  = document.getElementById('vmSkipBtn');
  },
  open()  { if (this.modal) this.modal.style.display = 'flex'; },
  close() { if (this.modal) this.modal.style.display = 'none'; this._clearActive(); },

  setStep(idx, total, label) {
    const lang = getLang();
    const vmu = window.SAHAYAK_VM?.[lang] || window.SAHAYAK_VM?.en || {};
    if (this.stepLbl)  this.stepLbl.textContent  = vmu.stepOf ? vmu.stepOf(idx, total) : `${idx}/${total}`;
    if (this.progress) this.progress.style.width = `${Math.round((idx / total) * 100)}%`;
    if (this.hint)     this.hint.textContent     = vmu.hint || '';
    if (this.skipBtn)  this.skipBtn.textContent  = vmu.skip || 'Skip';
    if (this.question) this.question.textContent = label;
    if (this.heardBox) this.heardBox.style.display = 'none';
    if (this.ansBox)   this.ansBox.style.display   = 'none';
    this.setMic('idle');
  },

  setMic(state) {
    const lang = getLang();
    const vmu = window.SAHAYAK_VM?.[lang] || window.SAHAYAK_VM?.en || {};
    if (!this.micRing) return;
    this.micRing.className = 'vmodal-mic-ring ' + state;
    if (state === 'listening') {
      this.micDot.textContent   = '🎤';
      this.stateLbl.textContent = vmu.listening || '🎤 Listening… speak now';
    } else if (state === 'thinking') {
      this.micDot.textContent   = '⏳';
      this.stateLbl.textContent = '';
    } else {
      this.micDot.textContent   = '🎙️';
      this.stateLbl.textContent = '';
    }
  },

  showHeard(text) {
    const lang = getLang();
    const vmu = window.SAHAYAK_VM?.[lang] || window.SAHAYAK_VM?.en || {};
    if (!this.heardBox) return;
    this.heardLbl.textContent   = vmu.heard || 'I heard:';
    this.heardVal.textContent   = '"' + text + '"';
    this.heardBox.style.display = 'flex';
    if (this.ansBox) this.ansBox.style.display = 'none';
  },

  showFilled(text) {
    const lang = getLang();
    const vmu = window.SAHAYAK_VM?.[lang] || window.SAHAYAK_VM?.en || {};
    if (!this.ansBox) return;
    this.ansVal.textContent     = (vmu.filled || 'Filled:') + ' ' + text;
    this.ansBox.style.display   = 'flex';
    this.setMic('idle');
  },

  showDone() {
    const lang = getLang();
    const vmu = window.SAHAYAK_VM?.[lang] || window.SAHAYAK_VM?.en || {};
    if (this.question) this.question.textContent = vmu.done || '✅ Done!';
    if (this.stepLbl)  this.stepLbl.textContent  = '';
    if (this.progress) this.progress.style.width = '100%';
    if (this.heardBox) this.heardBox.style.display = 'none';
    if (this.ansBox)   this.ansBox.style.display   = 'none';
    if (this.skipBtn)  this.skipBtn.style.display  = 'none';
    this.setMic('idle');
    if (this.micDot)   this.micDot.textContent    = '✅';
  },

  highlightField(name) {
    this._clearActive();
    const el = document.querySelector(`.voice-field[data-field="${name}"]`);
    if (el) {
      el.classList.add('vf-active');
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  },
  _clearActive() {
    document.querySelectorAll('.vf-active').forEach(e => e.classList.remove('vf-active'));
  }
};

/* ── Main Voice Walkthrough ──────────────────────────────────────────────── */
let _stopRequested = false;
let _skipRequested = false;

async function voiceWalkthrough() {
  const lang      = getLang();
  const T         = window.SAHAYAK_T      || {};
  const VW_FIELDS = window.SAHAYAK_FIELDS || [];
  const vmu       = window.SAHAYAK_VM?.[lang] || window.SAHAYAK_VM?.en || {};

  if (!SR) {
    alert(vmu.notSupported || 'Speech recognition not supported in this browser. Please use Google Chrome or Microsoft Edge.');
    return;
  }

  VM.init();
  _stopRequested = false;
  _skipRequested = false;

  if (VM.skipBtn) VM.skipBtn.onclick = () => { _skipRequested = true; };
  const closeBtn = document.getElementById('voiceModalClose');
  if (closeBtn) closeBtn.onclick = () => { _stopRequested = true; speechSynthesis.cancel(); };

  VM.open();

  const btn = document.getElementById('voiceWalkthroughBtn');
  if (btn) btn.disabled = true;

  // 1. Speak greeting in selected language
  const greet = T.greet || 'Namaste! I will ask a few quick questions.';
  VM.setStep(0, VW_FIELDS.length, greet);
  await new Promise(res => speak(greet, res));

  const total = VW_FIELDS.length;
  let i = 0;

  while (i < total) {
    if (_stopRequested) break;

    const meta = VW_FIELDS[i];
    const question = T[meta.qKey] || meta.name;

    VM.setStep(i + 1, total, question);
    VM.highlightField(meta.name);

    // 2. Speak the question in selected language
    await new Promise(res => speak(question, res));
    if (_stopRequested) break;

    // 3. Audio buffer pause: wait 500ms so speaker output finishes completely before mic starts
    await new Promise(res => setTimeout(res, 500));
    if (_stopRequested) break;

    // 4. Listen for response in selected language
    VM.setMic('listening');
    let transcripts = null;
    try {
      transcripts = await listenOnce(12000);
    } catch (e) {
      VM.setMic('idle');
      if (e === 'not-allowed') {
        const notAllowedMap = {
          en: '⚠️ Microphone blocked. Click the tune/lock icon 🎛️ in the URL bar, set Microphone to "Allow", and refresh.',
          hi: '⚠️ माइक की अनुमति बंद है। कृपया URL बार में 🎛️ आइकन पर क्लिक करके माइक को "Allow" करें और रिफ्रेश करें।',
          mr: '⚠️ माइक परवानगी बंद आहे. कृपया URL बारमधील 🎛️ आयकॉनवर क्लिक करून माइक "Allow" करा आणि रिफ्रेश करा.',
          ta: '⚠️ மைக்ரோஃபோன் அணுகல் தடுக்கப்பட்டுள்ளது. URL பட்டியில் உள்ள 🎛️ ஐகானைக் கிளிக் செய்து "Allow" செய்து புதுப்பிக்கவும்.'
        };
        const msg = notAllowedMap[lang] || notAllowedMap.en;
        VM.showHeard(msg);
        await new Promise(res => speak(msg, res));
        _stopRequested = true;
        break;
      }
      if (meta.optional) {
        i++;
        continue;
      }
      const retry = vmu.retry || "Sorry, didn't catch that. Please speak again.";
      VM.showHeard(retry);
      await new Promise(res => speak(retry, res));
      continue;
    }

    if (_stopRequested) break;

    VM.setMic('thinking');
    const heard = Array.isArray(transcripts) ? transcripts[0] : transcripts;
    VM.showHeard(heard);
    await new Promise(res => setTimeout(res, 350));

    // 5. Try to match and fill field FIRST before checking skip/back
    const container = document.querySelector(`.voice-field[data-field="${meta.name}"]`);
    let filled = null;
    if (container) {
      const sel = container.querySelector('select');
      const inp = container.querySelector('input');
      if (sel) {
        filled = matchSelect(sel, transcripts);
      } else if (inp) {
        filled = matchInput(inp, meta.type, transcripts);
      }
    }

    if (filled !== null) {
      VM.showFilled(filled);
      const confirmText = buildConfirm(filled);
      await new Promise(res => speak(confirmText, res));
      i++;
      continue;
    }

    // 6. If not filled, check for skip button or control commands
    if (_skipRequested) {
      _skipRequested = false;
      await new Promise(res => speak(T.skip || 'Skipped.', res));
      i++;
      continue;
    }

    const cmd = detectCmd(transcripts);
    if (cmd === 'skip') {
      await new Promise(res => speak(T.skip || 'Skipped.', res));
      i++;
      continue;
    }
    if (cmd === 'back') {
      await new Promise(res => speak(T.wentBack || 'Going back.', res));
      if (i > 0) i--;
      continue;
    }
    if (cmd === 'repeat') {
      continue;
    }
    if (cmd === 'startOver') {
      await new Promise(res => speak(T.startOver || 'Starting over.', res));
      i = 0;
      continue;
    }

    // If could not fill and not optional, politely ask once more
    if (meta.optional) {
      i++;
    } else {
      const retry = vmu.retry || "Sorry, didn't catch that. Please speak again.";
      await new Promise(res => speak(retry, res));
    }
  }

  // Done
  if (!_stopRequested) {
    VM.showDone();
    const doneMap = {
      en: 'Thank you! Finding the best government schemes for you now.',
      hi: 'धन्यवाद! अब आपके लिए सबसे उपयुक्त सरकारी योजनाएँ खोज रहे हैं।',
      mr: 'धन्यवाद! आता तुमच्यासाठी सर्वोत्तम शासकीय योजना शोधत आहोत.',
      ta: 'நன்றி! உங்களுக்கான சிறந்த அரசு திட்டங்களை இப்போது தேடுகிறேன்.'
    };
    const finalMsg = doneMap[lang] || doneMap.en;
    await new Promise(res => speak(finalMsg, res));
    await new Promise(res => setTimeout(res, 600));
    VM.close();
    document.getElementById('profileForm').submit();
  } else {
    VM.close();
    if (btn) btn.disabled = false;
  }

  VM._clearActive();
  if (btn && !_stopRequested) btn.disabled = false;
}

document.getElementById('voiceWalkthroughBtn')?.addEventListener('click', voiceWalkthrough);

/* ── Individual Field Mini Mic 🎤 ────────────────────────────────────────── */
document.querySelectorAll('.mic-mini').forEach(btn => {
  btn.addEventListener('click', async () => {
    const container = btn.closest('.voice-field');
    const fieldName = container?.dataset.field || '';
    btn.classList.add('on');

    try {
      const T = window.SAHAYAK_T || {};
      const qKey = (window.SAHAYAK_FIELDS || []).find(f => f.name === fieldName)?.qKey;
      const q = qKey ? (T[qKey] || '') : '';
      if (q) {
        await new Promise(res => speak(q, res));
        await new Promise(res => setTimeout(res, 400));
      }

      const transcripts = await listenOnce(8000);
      const sel = container.querySelector('select');
      const inp = container.querySelector('input');
      let filled = null;
      if (sel) filled = matchSelect(sel, transcripts);
      else if (inp) filled = matchInput(inp, container.dataset.type, transcripts);

      if (filled) {
        await new Promise(res => speak(buildConfirm(filled), res));
      }
    } catch (_) {}

    btn.classList.remove('on');
  });
});

/* ── OCR document handling ───────────────────────────────────────────────── */
document.querySelectorAll('[data-ocr-input]').forEach(input => {
  input.addEventListener('change', async () => {
    const docType  = input.dataset.ocrInput;
    const statusEl = document.querySelector(`[data-ocr-status="${docType}"]`);
    const wrapper  = input.closest('.ocr-upload');
    const file     = input.files[0];
    if (!file) return;
    statusEl.textContent = 'Reading…';
    statusEl.classList.remove('error');
    const fd = new FormData();
    fd.append('image', file);
    fd.append('doc_type', docType);
    try {
      const res  = await fetch('/api/ocr', { method: 'POST', body: fd });
      const data = await res.json();
      if (data.error) {
        statusEl.textContent = data.error;
        statusEl.classList.add('error');
        return;
      }
      const applied = applyOcrFields(data.fields || {});
      wrapper.classList.add('done');
      statusEl.textContent = applied.length
        ? `Filled: ${applied.join(', ')}`
        : (data.low_confidence ? 'Photo too blurry — retake or fill manually.' : 'Could not read needed data — fill manually.');
      if (!applied.length) statusEl.classList.add('error');
    } catch (e) {
      statusEl.textContent = 'Could not read this image.';
      statusEl.classList.add('error');
    }
  });
});

function applyOcrFields(f) {
  const applied = [];
  const set = (q, v) => {
    const el = document.querySelector(q);
    if (el) { el.value = v; applied.push(v); }
  };
  if (f.age) set('.voice-field[data-field="age"] input', f.age);
  if (f.income) set('.voice-field[data-field="income"] input', f.income);
  if (f.education) set('.voice-field[data-field="education"] select', f.education);
  if (f.gender) set('.voice-field[data-field="gender"] select', f.gender);
  if (f.state) {
    const el = document.querySelector('.voice-field[data-field="state"] select');
    if (el) {
      for (const o of el.options) {
        if (o.textContent.trim().toLowerCase() === f.state.toLowerCase()) {
          el.value = o.value;
          applied.push('state');
          break;
        }
      }
    }
  }
  if (f.name) applied.push(`name: "${f.name}"`);
  return applied;
}

/* ── Wake word & Navigation ──────────────────────────────────────────────── */
const WAKE_PHRASES = {
  en: ['hey sahayak', 'sahayak'],
  hi: ['हे सहायक', 'सहायक'],
  mr: ['हे सहाय्यक', 'सहाय्यक'],
  ta: ['ஏய் சகாயக்', 'சகாயக்']
};

const NAV_PHRASES = {
  browse: { en: ['browse', 'search schemes'], hi: ['सभी योजनाएँ'], mr: ['सर्व योजना'],     ta: ['தேடு'] },
  saved:  { en: ['saved'],                   hi: ['सहेजी गई'],    mr: ['जतन केलेल्या'],   ta: ['சேமிக்கப்பட்ட'] },
  find:   { en: ['find scheme'],             hi: ['योजना खोजें'],  mr: ['योजना शोधा'],      ta: ['திட்டம் தேடு'] },
  logout: { en: ['log out', 'logout'],        hi: ['लॉग आउट'],     mr: ['लॉग आउट'],         ta: ['வெளியேறு'] }
};

let wakeActive = false, wakeRec = null, wakeListen = false;
if (SR) {
  wakeRec = new SR();
  wakeRec.continuous    = true;
  wakeRec.interimResults = true;
  wakeRec.lang          = getSpeechLang();

  wakeRec.onresult = e => {
    const text = e.results[e.results.length - 1][0].transcript.toLowerCase();
    const lang = getLang();
    const phrases = WAKE_PHRASES[lang] || WAKE_PHRASES.en;
    if (phrases.some(p => text.includes(p))) onWake();
  };

  wakeRec.onend   = () => { wakeListen = false; if (wakeActive) setTimeout(startWake, 600); };
  wakeRec.onerror = () => { wakeListen = false; if (wakeActive) setTimeout(startWake, 1200); };
}

function startWake() {
  if (!wakeRec || wakeListen || !wakeActive) return;
  wakeListen = true;
  wakeRec.lang = getSpeechLang();
  try { wakeRec.start(); } catch (_) { wakeListen = false; }
}

async function onWake() {
  try { wakeRec.stop(); } catch (_) {}
  const T = window.SAHAYAK_T || {};
  await new Promise(res => speak(T.wakeGreeting || "Yes? I'm listening.", res));
  try {
    const alts = await listenOnce(6000);
    const text = (Array.isArray(alts) ? alts[0] : alts).toLowerCase();
    const lang = getLang();
    for (const [dest, map] of Object.entries(NAV_PHRASES)) {
      const phrases = map[lang] || map.en;
      if (phrases.some(p => text.includes(p))) {
        routeTo(dest);
        return;
      }
    }
    voiceWalkthrough();
  } catch (_) {}
  if (wakeActive) setTimeout(startWake, 500);
}

function routeTo(dest) {
  const u = { browse: '/browse', saved: '/saved', find: '/assistant', logout: '/logout' };
  if (u[dest]) location.href = u[dest];
}

document.getElementById('wakeToggleBtn')?.addEventListener('click', function () {
  wakeActive = !wakeActive;
  this.classList.toggle('on', wakeActive);
  if (wakeActive) startWake();
  else { try { wakeRec.stop(); } catch (_) {} }
});

/* ── Fresh login vocal greeting ──────────────────────────────────────────── */
if (window.SAHAYAK_FRESH_LOGIN && window.SAHAYAK_WELCOME) {
  if (window.SAHAYAK_NO_PROFILE && window.SAHAYAK_VOICE_HINT) {
    speak(window.SAHAYAK_WELCOME, () => speak(window.SAHAYAK_VOICE_HINT));
  } else {
    speak(window.SAHAYAK_WELCOME);
  }
} else if (window.SAHAYAK_NO_PROFILE && window.SAHAYAK_VOICE_HINT) {
  speak(window.SAHAYAK_VOICE_HINT);
}

/* ── Save and Apply Action Buttons ───────────────────────────────────────── */
function toast(text) {
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = text;
  document.getElementById('toastHost').appendChild(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => {
    el.classList.remove('show');
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

document.body.addEventListener('click', async e => {
  const btn = e.target.closest('.act-btn');
  if (!btn) return;
  const id = btn.dataset.id;
  if (btn.dataset.act === 'save') {
    const res = await fetch(`/api/toggle_save/${id}`, { method: 'POST' });
    const d   = await res.json();
    btn.classList.toggle('on', d.saved);
    btn.textContent = d.saved ? 'Saved ✓' : '☆ Save';
  } else if (btn.dataset.act === 'apply' && !btn.classList.contains('on')) {
    const res = await fetch(`/api/apply/${id}`, { method: 'POST' });
    const d   = await res.json();
    btn.classList.add('on');
    btn.textContent = '✓ Applied';
    toast(d.message);
  }
});

/* ── Feedback Box ────────────────────────────────────────────────────────── */
(function () {
  const box = document.getElementById('feedbackBox');
  if (!box) return;
  let sentiment = null;
  box.querySelector('#fbUp').onclick   = () => { sentiment = 'up';   box.querySelector('#fbUp').classList.add('on');   box.querySelector('#fbDown').classList.remove('on'); };
  box.querySelector('#fbDown').onclick = () => { sentiment = 'down'; box.querySelector('#fbDown').classList.add('on'); box.querySelector('#fbUp').classList.remove('on'); };
  box.querySelector('#fbSubmit').onclick = async () => {
    if (!sentiment) return;
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sentiment, comment: box.querySelector('#fbComment').value })
    });
    box.innerHTML = '<p style="margin:0;color:var(--ink-soft);font-size:13.5px;">Thanks for your feedback!</p>';
  };
})();

/* ── Dark / Light Theme Toggle ───────────────────────────────────────────── */
document.getElementById('themeToggle')?.addEventListener('click', () => {
  const dark = document.body.dataset.theme === 'dark';
  document.body.dataset.theme = dark ? 'light' : 'dark';
  document.getElementById('themeToggle').textContent = dark ? '🌙' : '☀️';
});
