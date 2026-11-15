"""Validators of the UAE names and codes found in the opendata.fcsc.gov.ae files of
metacrafter-testdata.

The UAE open data portal of the Federal Competitiveness and Statistics Centre (FCSC; snapshot of
2024) gathers the statistics of the federal ministries and of the emirates, most of them with
every label in English and in Arabic (Emirate_EN, Emirate_AR): tables by emirate, by region of
the emirate of Abu Dhabi (Al Ain, Al Dhafra), by community of Dubai (Dubai Municipality and RTA
files: community_num 123, AL MUTEENA), and DEWA files by contract account.

Each function takes one value and returns True when it has the form of the name or code.
Field-name rules use them to check the values of a field; value rules use them as the pattern.
"""
import re

from metacrafterext.rules.ar.countries import fold_arabic, has_arabic

_PARENS = re.compile(r"\([^)]*\)")


def _latin_key(value):
    """Lower-case Latin letters and digits only: Umm Al - Quwain -> ummalquwain."""
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def _arabic_key(value):
    """Folded Arabic without spaces: أبو ظــبي -> ابوظبي."""
    return fold_arabic(value).replace(" ", "")


def _key(value):
    text = str(value).strip()
    return _arabic_key(text) if has_arabic(text) else _latin_key(text)


def _strip_emirate_word(value):
    """Emirate of Sharjah, Abu Dhabi Emirate, إمارة دبي -> the name alone."""
    text = re.sub(r"(?i)^\s*(?:the\s+)?emirate\s+of\s+|\s+emirate\s*$", "", str(value).strip())
    return re.sub(r"^\s*[إا]مار[ةه]\s+", "", text)


# The seven emirates, in English and Arabic, with the spellings and abbreviations of the
# federal statistics: Umm Al - Quwain, Umm Al Qaiwain, U.A.Q., UMQ; Ras Al-Khaimah, R.A.K.
_EMIRATES = {
    "abudhabi": "AZ", "auh": "AZ",
    "dubai": "DU", "dxb": "DU",
    "sharjah": "SH", "sharja": "SH", "alsharjah": "SH", "shj": "SH",
    "ajman": "AJ", "ajm": "AJ",
    "ummalquwain": "UQ", "ummalqaiwain": "UQ", "ummalqiwain": "UQ", "ummalquain": "UQ",
    "ummalqawain": "UQ", "ummalquwian": "UQ", "uaq": "UQ", "umq": "UQ",
    "rasalkhaimah": "RK", "rasalkhaima": "RK", "rasalkhaimeh": "RK", "rak": "RK",
    "fujairah": "FU", "alfujairah": "FU", "fujaira": "FU", "fujeira": "FU", "fujeirah": "FU", "fuj": "FU",
    "ابوظبي": "AZ", "دبي": "DU", "الشارقه": "SH", "شارقه": "SH", "عجمان": "AJ",
    "امالقيوين": "UQ", "راسالخيمه": "RK", "الفجيره": "FU", "فجيره": "FU",
}


def validate_ae_emirate(value):
    """One of the seven emirates of the UAE in English or Arabic (Abu Dhabi, أبوظبي, Ras Al-Khaimah,
    R.A.K., Umm Al - Quwain, أم القيوين), also as Emirate of Sharjah or إمارة دبي. A region of an
    emirate (Al Ain, Western Region) and the country (UAE, Total) are not emirates."""
    text = _strip_emirate_word(value)
    # A footnote number after the name (Sharjah1) is not part of it.
    return bool(text) and re.sub(r"(?<=[a-z])\d$", "", _key(text)) in _EMIRATES


# The three regions of the emirate of Abu Dhabi: Abu Dhabi (the capital region), Al Ain (the
# eastern region) and Al Dhafra, named the Western Region (المنطقة الغربية, Al Gharbia) until 2017.
_ABU_DHABI_REGIONS = {
    "abudhabi", "abudhabiregion", "abudhabicity", "capitalregion", "centralregion",
    "alain", "alainregion", "alaincity", "easternregion",
    "aldhafra", "aldhafraregion", "dhafra", "westernregion", "western", "algharbia", "algharbiya",
    "ابوظبي", "منطقهابوظبي", "مدينهابوظبي", "العين", "منطقهالعين", "مدينهالعين",
    "الظفره", "منطقهالظفره", "المنطقهالغربيه", "الغربيه",
}


def validate_ae_abu_dhabi_region(value):
    """A region of the emirate of Abu Dhabi: Abu Dhabi, Al Ain or Al Dhafra (Western Region),
    in English or Arabic (أبوظبي, العين, الظفرة, المنطقة الغربية), with or without the word
    Region. Other emirates are not."""
    text = str(value).strip()
    return bool(text) and _key(text) in _ABU_DHABI_REGIONS


# Communities of Dubai: code, English and Arabic name. The 226 communities of the Dubai Statistics
# Center (Population Bulletin, Emirate of Dubai, 2021), then the spellings of the RTA parking zone
# list (number of parking spaces per zone, 2017) of the FCSC snapshot, whose 83 codes are all
# among them.
_DSC_COMMUNITIES = """
101|Nakhlat Deira|نخلة ديرة
111|Al Corniche|الكورنيش
112|Al Ras|الراس
113|Al Dhagaya|الضغاية
114|Al Buteen|البطين
115|Al Sabkha|السبخة
116|Ayal Nasir|عيال ناصر
117|Al Murar|المرر
118|Naif|نايف
119|Al Rigga|الرقة
121|Corniche Deira|كورنيش ديرة
122|Al Baraha|البراحة
123|Al Muteena|المطينة
124|Al Muraqqabat|المرقبات
125|Rigga Al Buteen|رقة البطين
126|Abu Hail|أبو هيل
127|Hor Al Anz|هورالعنز
128|Al Khabisi|الخبيصي
129|Port Saeed|بور سعيد
131|Al Hamriya Port|ميناء الحمرية
132|Al Waheda|الوحيدة
133|Hor Al Anz East|هور العنز شرق
134|Al Mamzar|الممزر
213|Nad Shamma|ند شما
214|Al Garhoud|القرهود
215|Umm Ramool|أم رمول
216|Al Rashidiya|الراشدية
221|Dubai Airport|مطار دبي الدولي
226|Al Twar First|الطوار الأولى
227|Al Twar Second|الطوار الثانية
228|Al Twar Third|الطوار الثالثة
231|Al Nahda First|النهدة الأولى
232|Al Qusais First|القصيص الأولى
233|Al Qusais Second|القصيص الثانية
234|Al Qusais Third|القصيص الثالثة
241|Al Nahda Second|النهدة الثانية
242|Al Qusais Industrial First|القصيص الصناعية الأولى
243|Al Qusais Industrial Second|القصيص الصناعية الثانية
244|Muhaisnah Third|محيصنة الثالثة
245|Muhaisnah Fourth|محيصنة الرابعة
246|Al Qusais Industrial Third|القصيص الصناعية الثالثة
247|Al Qusais Industrial Fourth|القصيص الصناعية الرابعة
248|Al Qusais Industrial Fifth|القصيص الصناعية الخامسة
251|Mirdif|مردف
252|Mushraif|مشرف
261|Muhaisnah First|محيصنة الأولى
262|Al Mizhar First|المزهر الأولى
263|Al Mizhar Second|المزهر الثانية
264|Muhaisnah Second|محيصنة الثانية
265|Oud Al Muteen First|عود المطينة الأولى
266|Oud Al Muteen Second|عود المطينة الثانية
267|Muhaisnah Fifth|محصينة الخامسة
268|Oud Al Muteen Third|عود المطينة الثالثة
271|Wadi Alamardi|وادي العمردي
281|Al Khawaneej One|الخوانيج الأولى
282|Al Khawaneej Two|الخوانيج الثانية
283|Al Ayas|العياص
284|Al Ttay|الطي
302|Jumeirah Bay|شاطئ جميرا
303|World Islands|جزر العالم
304|Jumeirah Island 2|جزيرة جميرا 2
311|Al Shindagha|الشندغة
312|Al Souk Al Kabir|السوق الكبير
313|Al Hamriya|الحمرية
314|Umm Hurair First|أم هرير الأولى
315|Umm Hurair Second|أم هرير الأولى
316|Al Rifa|الرفاعة
317|Al Mankhool|المنخول
318|Al Karama|الكرامة
319|Oud Metha|عود ميثاء
321|Madinat Dubai Al Melaheyah (Al Mina)|مدينه دبي المالحيه
322|Al Hudaiba|الحضيبة
323|Al Jafiliya|الجافلية
324|Al Kifaf|الكفاف
325|Zabeel First|زعبيل الأولى
326|Al Jaddaf|الجداف
332|Jumeirah First|جميرا الأولى
333|Al Bada|البدع
334|Al Satwa|السطوة
335|Trade Centre 1|المركز التجاري الأولى
336|Trade Centre 2|المركز التجاري الثانية
337|Zabeel Second|زعبيل الثانية
342|Jumeirah Second|جميرا الثانية
343|Al Wasl|الوصل
345|Downtown Dubai|برج خليفة
346|Al Kalij Al Tejari (Business Bay)|الخليج التجاري
347|Al Markada|المركاض
352|Jumeirah Third|جميرا الثالثة
353|Al Safa First|الصفا الأولى
354|Al Quoz First|القوز الاولى
355|Al Quoz Second|القوز الثانية
356|Umm Suqeim First|أم سقيم الأولى
357|Al Safa Second|الصفا الثانية
358|Al Quoz Third|القوز الثالثة
359|Al Quoz Fourth|القوز الرابعة
362|Umm Suqeim Second|أم سقيم الثانية
363|Al Manara|المنارة
364|Al Quoz Industrial First|القوز الصناعية الأولى
365|Al Quoz Industrial Second|القوز الصناعية الثانية
366|Umm Suqeim Third|أم سقيم الثالثة
367|Umm Al Sheif|أم الشيف
368|Al Quoz Industrial Third|القوز الصناعية الثالثة
369|Al Quoz Industrial Fourth|القوز الصناعية الرابعة
372|Al Sufouh First|الصفوح الأولى
373|Al Barsha First|البرشاء الأولى
375|Al Barsha Third|البرشاء الثالثة
376|Al Barsha Second|البرشاء الثانية
381|Nakhlat Jumeira|نخلة جميرا
382|Al Sufouh Second|الصفوح الثانية
383|Al Thanyah First|الثنيه الأولى (قرية ربيع الصحراء)
384|Al Thanyah Second|الثنيه الثانية (مضمار جبل علي)
388|Al Thanyah Third|الثنيه الثالثة (تلال الامارات الثانية)
392|Marsa Dubai|مرسى دبي (الميناء السياحي)
393|Al Thanyah Fifth|الثنيه الخامسة (تلال الامارات الاولى)
394|Al Thanyah Fourth|الثنيه الرابعة (تلال الامارات الثالثة)
412|Al Kheeran|الخيران
413|Ras Al Khor|رأس الخور
415|Al Khairan First|الخيران الأولى
416|Nad Al Hammar|ند الحمر
421|Al Warqaa First|الورقاء الأولى
422|Al Warqaa Second|الورقاء الثانية
423|Al Warqaa Third|الورقاء الثالثة
424|Al Warqaa Fourth|الورقاء الرابعة
425|Al Warqaa Fifth|الورقاء الخامسة
431|Wadi Alshabak|وادي الشبك
501|Nakhlat Jabal Ali|نخلة جبل علي
502|Al Wajeha Al Bahriah|الواجهة البحرية
511|Hessyan First|حصيان الاولى
512|Hessyan Second|حصيان الثانية
513|Saih Shuaib 1|سيح شعيب 1
516|Jabal Ali Industrial Third|جبل علي الصناعية الثالثة
518|Jabal Ali Industrial Second|جبل علي الصناعية الثانية
521|Madinat Al Mataar|مدينة المطار
531|Saih Shuaib 2|سيح شعيب 2
532|Saih Shuaib 3|سيح شعيب 3
533|Saih Shuaib 4|سيح شعيب 4
591|Jabal Ali First|جبل علي الأولى
592|Jabal Ali Second|جبل علي الثانية
593|Jabal Ali Third|جبل علي الثالثة
594|Mena Jabal Ali|ميناء جبل علي
597|Dubai Investment Park Second|مجمع دبي للاستثمار الثاني
598|Dubai Investment Park First|مجمع دبي للاستثمار الأول
599|Jabal Ali Industrial First|جبل علي الصناعية الأولى
611|Bu Kadra|بو كدرة
612|Ras Al Khor Industrial First|رأس الخور الصناعية الأولى
613|Ras Al Khor Industrial Second|رأس الخور الصناعية الثانية
614|Ras Al Khor Industrial Third|رأس الخور الصناعية الثالثة
615|Nadd Al Shiba Second|ند الشبا الثانية
616|Nadd Al Shiba Third|ند الشبا الثالثة
617|Nadd Al Shiba Fourth|ند الشبا الرابعة
618|Nadd Al Shiba First|ند الشبا الأولى
621|Warsan First|ورسان الاولى
622|Warsan Second|ورسان الثانية
624|Warsan Fourth|ورسان الرابعة
626|Nadd Hessa|ند حصة
631|Hadaeq Sheikh Mohammed Bin Rashid|حدائق الشيخ محمد بن راشد
643|Wadi Al Safa 2|وادي الصفا 2
645|Wadi Al Safa 3|وادي الصفا 3
646|Wadi Al Safa 4|وادي الصفا 4
648|Wadi Al Safa 5|وادي الصفا 5
664|Wadi Al Safa 6|وادي الصفا 6
665|Wadi Al Safa 7|وادي الصفا 7
671|Al Barsha South First|البرشاء جنوب الاولى
672|Al Barsha South Second|البرشاء جنوب الثانية
673|Al Barsha South Third|البرشاء جنوب الثالثة
674|Al Hebiah First|الحبيه الاول
675|Al Hebiah Second|الحبيه الثانية
676|Al Hebiah Third|الحبيه الثالثة
677|Al Hebiah Sixth|الحبيه السادسة
681|Al Barsha South Fourth|البرشاء جنوب الرابعة
682|Al Hebiah Fourth|الحبيه الرابعة
683|Al Hebiah Fifth|الحبيه الخامسة
684|Al Barsha South Fifth|البرشاء جنوب الخامسة
685|Me'aisem First|معيصم الأول
686|Me'aisem Second|معيصم الثانية
711|Al Awir First|العوير الأولى
721|Al Awir Second|العوير الثانية
724|Enkhali|نخلي
727|Al Wohoosh|الوحوش
731|Lehbab First|لهباب الأولى
735|Al Meryal|المريال
736|Nazwah|نزوه
811|Warsan 3|ورسان الثالثة
812|Al Rowaiyah First|الرويه الأولى
813|Al Rowaiyah Second|الرويه الثانية
814|Al Rowaiyah Third|الرويه الثالثة
821|Mereiyeel|مرييل
824|Umm Al Daman|أم الدمن
826|Le Hemaira|الحميرا
831|Lehbab Second|لهباب الثانية
835|Umm Al Mo'meneen|أم المؤمنين
841|Margham|مرغم
845|Al Maha|المها
847|Umm Eselay|أم السلي
851|Remah|رماح
857|Margab|مرقب
861|Yaraah|يراح
891|Hatta|حتا
911|Umm Nahad First|أم نهد الأولى
912|Umm Nahad Second|أم نهد الثانية
913|Umm Nahad Third|أم نهد الثالثة
914|Umm Nahad Fourth|أم نهد الرابعة
915|Al Yufrah 1|اليفره 1
916|Al Yufrah 2|اليفره 2
917|Al Marmoom|المرموم
918|Al Yufrah 3|اليفره 3
919|Al Yufrah 4|اليفره 4
921|Al Yalayis 1|الياليس 1
922|Al Yalayis 2|الياليس 2
923|Al Yalayis 3|الياليس 3
924|Al Yalayis 4|الياليس 4
925|Al Yalayis 5|الياليس 5
931|Al Lesaily|الليسيلي
941|Grayteesah|قريطيسه
945|Al Fagaa|الفقع
951|Saih Al Salam|سيح السلم
956|Al Hathmah|الحثمة
961|Al Selal|الصلال
967|Ghadeer Barashy|غدير براشي
971|Saih Al Dahal|سيح الدحل
975|Al O'shoosh|العشوش
978|Saih Shua'alah|سيح شعيله
981|Mugatrah|مقطره
987|Al Layan 1|الليان 1
988|Al Layan 2|الليان 2
991|Hefair|حفير
"""
_RTA_COMMUNITIES = """
111|AL CORNICHE|الكورنيش
112|AL RAS|الراس
113|AL DAGHAYA|الضغاية
114|AL BUTEEN|البطين
115|AL SABKHA|السبخة
116|AYAL NASIR|عيال ناصر
117|AL MURAR|المرر
118|NAIF|نايف
119|AL RIGGA|الرقة
122|AL BARAHA|البراحة
123|AL MUTEENA|المطينة
124|AL MURAQQABAT|المرقبات
125|RIGGAT AL BUTEEN|رقة البطين
126|ABU HAIL|أبو هيل
127|HOR AL ANZ|هور العنز
128|AL KHABAISI|الخبيصي
129|PORT SAEED|بور سعيد
133|HOR AL ANZ EAST|هور العنز شرق
134|AL MAMZAR|الممزر
214|AL GARHOUD|القرهود
215|UMM RAMOOL|أم رمول
216|AL RASHIDIYA|الراشدية
221|DUBAI INT'L AIRPORT|مطار دبي الدولي
226|AL TWAR FIRST|الطوار الأولى
227|AL TWAR SECOND|الطوار الثانية
231|AL NAHDA FIRST|النهدة الأولى
232|AL QUSAIS FIRST|القصيص الأولى
233|AL QUSAIS SECOND|القصيص الثانية
241|AL NAHDA SECOND|النهدة الثانية
242|AL QUSAIS IND. FIRST|القصيص الصناعية الأولى
243|AL QUSAIS IND. SECOND|القصيص الصناعية الثانية
245|MUHAISANAH FOURTH|محيصنة الرابعة
246|AL QUSAIS IND. THIRD|القصيص الصناعية الثالثة
247|AL QUSAIS IND. FOURTH|القصيص الصناعية الرابعة
311|AL SHINDAGHA|الشندغة
312|AL SOUQ AL KABEER|السوق الكبير
313|AL HAMRIYA|الحمرية
314|UMM HURAIR FIRST|أم هرير الأولى
315|UMM HURAIR SECOND|أم هرير الثانية
316|AL RAFFA|الرفاعة
317|MANKHOOL|منخول
318|AL KARAMA|الكرامة
319|OUD METHA|عود ميثاء
321|MADINAT DUBAI AL MELAHEYAH|مدينة دبي الملاحية
322|AL HUDAIBA|الحضيبة
323|AL JAFILIYA|الجافلية
324|AL KIFAF|الكفاف
332|JUMEIRA FIRST|جميرا الأولى
333|AL BADA'|البدع
334|AL SATWA|السطوة
335|TRADE CENTER FIRST|المركز التجاري الأولى
336|TRADE CENTER SECOND|المركز التجاري الثانية
337|ZAA'BEEL SECOND|زعبيل الثانية
342|JUMEIRA SECOND|جميرا الثانية
343|AL WASL|الوصل
345|BURJ KHALIFA|برج خليفة
346|BUSINESS BAY|الخليج التجاري
352|JUMEIRA THIRD|جميرا الثالثة
353|AL SAFA FIRST|الصفا الأولى
354|AL QOUZ FIRST|القوز الأولى
356|UMM SUQEIM FIRST|أم سقيم الأولى
357|AL SAFA SECOND|الصفا الثانية
358|AL QOUZ THIRD|القوز الثالثة
359|AL QOUZ FOURTH|القوز الرابعة
362|UMM SUQEIM SECOND|أم سقيم الثانية
363|AL MANARA|المنارة
364|AL QOUZ IND.FIRST|القوز الصناعية الأولى
365|AL QOUZ IND.SECOND|القوز الصناعية الثانية
366|UMM SUQEIM THIRD|أم سقيم الثالثة
367|UMM AL SHEIF|أم الشيف
368|AL QOUZ IND.THIRD|القوز الصناعية الثالثة
369|AL QOUZ IND.FOURTH|القوز الصناعية الرابعة
372|AL SAFOUH FIRST|الصفوح الأولى
373|AL BARSHA FIRST|البرشاء الأولى
376|AL BARSHA SECOND|البرشاء الثانية
382|AL SAFOUH SECOND|الصفوح الثانية
388|AL THANYAH THIRD|الثنيه الثالثة
392|MARSA DUBAI|مرسى دبي
412|AL KHEERAN|الخيران
416|NADD AL HAMAR|ند الحمر
612|RAS AL KHOR IND. FIRST|رأس الخور الصناعية الأولى
613|RAS AL KHOR IND. SECOND|رأس الخور الصناعية الثانية
626|NADD HESSA|ند حصه
"""

_ORDINALS = {
    "first": "1", "one": "1", "second": "2", "two": "2", "third": "3", "three": "3",
    "fourth": "4", "four": "4", "fifth": "5", "five": "5", "sixth": "6", "six": "6",
    "seventh": "7", "seven": "7", "eighth": "8", "eight": "8",
    "الاولي": "1", "الاول": "1", "الاولى": "1", "الثانيه": "2", "الثاني": "2", "الثالثه": "3",
    "الثالث": "3", "الرابعه": "4", "الرابع": "4", "الخامسه": "5", "الخامس": "5",
    "السادسه": "6", "السادس": "6", "السابعه": "7", "السابع": "7", "الثامنه": "8", "الثامن": "8",
}


def _community_key(value):
    """A spelling-tolerant key of a community name. Latin: the consonants of the words without
    the article al and with ordinals as digits (AL DAGHAYA and Al Dhagaya -> dg, Muhaisnah
    Fourth and MUHAISANAH 4 -> msn4). Arabic: the folded words without the article (المنخول and
    منخول -> منخول, القوز الأولى -> قوز1)."""
    text = _PARENS.sub(" ", str(value)).strip()
    if has_arabic(text):
        words = [_ORDINALS.get(w, w) for w in fold_arabic(text).split()]
        return "".join(w[2:] if w.startswith("ال") and len(w) > 3 else w for w in words)
    words = re.findall(r"[a-z]+|\d+", text.lower().replace("'", ""))
    out = []
    for word in words:
        if word == "al" or word == "el":
            continue
        if word in _ORDINALS:
            out.append(_ORDINALS[word])
        elif word.isdigit():
            out.append(str(int(word)))
        else:
            skeleton = re.sub(r"[aeiouyhw]", "", word.replace("q", "k"))
            out.append(re.sub(r"(.)\1+", r"\1", skeleton))
    return "".join(out)


def _rows():
    for block in (_DSC_COMMUNITIES, _RTA_COMMUNITIES):
        for line in block.strip().splitlines():
            code, english, arabic = line.split("|")
            yield code, english, arabic


COMMUNITY_CODES = frozenset(code for code, _, _ in _rows())
COMMUNITY_KEYS = frozenset()


def _community_keys():
    keys = set()
    for _, english, arabic in _rows():
        for name in (english, arabic):
            key = _community_key(name)
            keys.add(key)
            # The community without its ordinal (Al Qusais for Al Qusais First, Second ...).
            base = re.sub(r"\d+$", "", key)
            if base and base != key:
                keys.add(base)
    return frozenset(k for k in keys if len(k) >= 2)


def _exact_names():
    names = set()
    for _, english, _ in _rows():
        base = re.sub(r"(?i)\s+(?:\d+|first|second|third|fourth|fifth|sixth|one|two|three)$", "", english)
        for name in (english, base):
            names.add(_latin_key(re.sub(r"(?i)\b(?:al|el)\s+", " ", _PARENS.sub(" ", name))))
    return frozenset(names)


COMMUNITY_KEYS = _community_keys()
# Latin names whose consonants are three letters or fewer (Al Ras: rs, Naif: nf, Al Mina: mn)
# must be written as listed: Rose and Main are not Al Ras and Al Mina.
_EXACT_NAMES = _exact_names()


def validate_ae_dubai_community_code(value):
    """A community number of Dubai: one of the 226 three-digit codes of the Dubai Statistics Center
    (111 Al Corniche ... 991); the first digit is the sector. A whole float (124.0) is taken."""
    text = str(value).strip()
    if re.fullmatch(r"\d{3}\.0", text):
        text = text[:-2]
    return text in COMMUNITY_CODES


def validate_ae_dubai_community(value):
    """The name of a community of Dubai in English or Arabic, as the Dubai Statistics Center and
    the RTA write it or close to it (AL DAGHAYA, Al Dhagaya, Al Barsha 2, Muhaisnah Fourth,
    المطينة, القوز الأولى). Numbers alone are not names."""
    text = str(value).strip()
    if not re.search(r"[A-Za-z؀-ۿ]", text) or len(text) > 60:
        return False
    key = _community_key(text)
    if key not in COMMUNITY_KEYS:
        return False
    if not has_arabic(text) and len(re.sub(r"\d", "", key)) <= 3:
        bare = re.sub(r"(?i)\b(?:al|el)\s+|\s+(?:\d+|first|second|third|fourth|fifth|sixth|one|two|three)$", " ", text)
        return _latin_key(_PARENS.sub(" ", bare)) in _EXACT_NAMES
    return True


def validate_ae_dewa_contract_account(value):
    """A contract account of the Dubai Electricity and Water Authority (DEWA): ten digits. Accounts
    of the 20 series carry a weighted check digit, weights 10 to 2 modulo 11 with a remainder of 10
    written as 0 (all 17 017 such accounts of the Shams Dubai, smart meter and move-in files of the
    snapshot pass it); the 30 series has no check this validator knows of."""
    text = str(value).strip()
    if re.fullmatch(r"\d{10}\.0", text):
        text = text[:-2]
    if not re.fullmatch(r"[23]0\d{8}", text):
        return False
    if text[0] == "3":
        return True
    total = sum(int(d) * w for d, w in zip(text[:9], range(10, 1, -1)))
    return (11 - total % 11) % 11 % 10 == int(text[9])


def validate_ae_po_box(value):
    """A P.O. Box number of a UAE address: one to six digits, alone or after P.O. Box (2623,
    PO Box 16080). Zero is not a box."""
    text = re.sub(r"(?i)^\s*(?:p\.?\s*o\.?\s*box|ص\.?\s*ب\.?)\s*:?\s*", "", str(value).strip())
    if text.endswith(".0"):
        text = text[:-2]
    return re.fullmatch(r"[1-9]\d{0,5}", text) is not None


# Towns of the UAE that are not the seat of an emirate, as UAE files write them, for city columns
# (aecity) beside the seven emirate capitals.
_CITIES = {
    "alain", "aldhafra", "madinatzayed", "zayedcity", "liwa", "liwaoasis", "algharbia", "alshamal",
    "ruwais", "alruwais", "ghayathi", "mirfa", "almirfa", "sila", "alsila", "delma", "dalma",
    "khorfakkan", "khorfakan", "khoorfakan", "khawrfakkan", "kalba", "dibba", "dibbaalhisn",
    "dibbaalfujairah", "aldhaid", "dhaid", "almadam", "hatta", "jebelali", "jabalali", "masafi",
    "alhamriyah", "dhadna", "alhisn", "alrams", "alain1",
    "العين", "الظفره", "مدينهزايد", "ليوا", "الرويس", "غياثي", "المرفا", "السلع", "دلما",
    "خورفكان", "كلباء", "كلبا", "دبا", "دباالحصن", "دباالفجيره", "الذيد", "المدام", "حتا",
    "جبلعلي", "مسافي", "الحمريه", "ضدنا",
}


def validate_ae_city(value):
    """A city or town of the UAE in English or Arabic: an emirate capital (Dubai, Abu Dhabi,
    الشارقة) or another town (Al Ain, Khor Fakkan, خورفكان, Madinat Zayed)."""
    text = str(value).strip()
    if not text:
        return False
    key = _key(text)
    return key in _CITIES or key in _EMIRATES
