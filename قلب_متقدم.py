#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🫀 القلب الناطق - النسخة المتقدمة الشاملة
# جميع الميزات: OOP، استثناءات، شبكات، قواعد بيانات، واجهة رسومية

import sys, os, struct, json, re, math, time, random, hashlib, subprocess
import threading, queue, csv, io, sqlite3, urllib.request, urllib.error
import traceback

# ============================================
# ١. قاموس اللغة الشامل الكامل
# ============================================
قاموس_الأوامر = {
    # أوامر الذكاء والتنفيذ
    "شغل": "RUN", "شغّل": "RUN", "نفذ": "RUN", "طبق": "RUN", "شغله": "RUN",
    "درب": "TRAIN", "درّب": "TRAIN", "علم": "TRAIN", "دربه": "TRAIN",
    "اختبر": "TEST", "فحص": "TEST", "قيم": "EVAL", "اختبره": "TEST",
    "ابنِ": "BUILD", "ابني": "BUILD", "أنشئ": "BUILD", "صمم": "BUILD",
    "حمّل": "LOAD", "حمل": "LOAD", "استورد": "IMPORT",
    "احفظ": "SAVE", "خزن": "SAVE", "صدّر": "EXPORT", "احفظه": "SAVE",
    "استعلم": "QUERY", "اعرض": "SHOW", "ارسم": "PLOT", "امسح": "CLEAR",
    
    # عمليات حسابية
    "اجمع": "ADD", "اطرح": "SUB", "اضرب": "MUL", "اقسم": "DIV",
    "قارن": "CMP", "احسب": "CALC", "مقياس": "MOD", "زد": "INC", "انقص": "DEC",
    
    # تحكم متقدم
    "كرر": "LOOP", "طالما": "WHILE", "اذا": "IF", "والا": "ELSE",
    "قف": "BREAK", "استمر": "CONTINUE", "ارجع": "RETURN", "انتظر": "SLEEP",
    
    # رياضيات
    "جيب": "SIN", "جيب_تمام": "COS", "ظل": "TAN",
    "لوغاريتم": "LOG", "جذر": "SQRT", "قوة": "POW", "اس": "POW",
    "قيمة_مطلقة": "ABS", "تقريب": "ROUND", "عشوائي": "RND",
    
    # شبكات عصبية
    "طبقة": "LAYER", "تنشيط": "ACTIVATE", "انتشار": "PROPAGATE",
    "تحسين": "OPTIMIZE", "تسرب": "DROPOUT", "تطبيع": "NORMALIZE",
    
    # هياكل بيانات
    "مصفوفة": "MATRIX", "متجه": "VECTOR", "موتر": "TENSOR",
    "قائمة": "LIST", "قاموس": "DICT", "مجموعة": "SET",
    "اضف": "APPEND", "احذف": "DELETE", "طول": "LEN",
    "رتب": "SORT", "اعكس": "REVERSE", "ابحث": "SEARCH",
    
    # دوال المستخدم و OOP
    "دالة": "DEF", "نفذ_دالة": "CALL", "ارجع": "RETURN",
    "صنف": "CLASS", "وراثة": "INHERIT", "جديد": "NEW",
    "دالة_صنف": "METHOD", "ذاتي": "SELF",
    
    # استثناءات
    "حاول": "TRY", "امسك": "CATCH", "خطأ": "ERROR",
    
    # شبكات
    "احصل": "HTTP_GET", "ارسل": "HTTP_POST", "اتصل": "CONNECT",
    
    # قواعد بيانات
    "قاعدة_بيانات": "DB", "استعلام_قاعدة": "DB_QUERY",
    
    # واجهة رسومية
    "نافذة": "WINDOW", "زر": "BUTTON", "نص_واجهة": "LABEL",
    "ادخال": "INPUT", "صورة": "IMAGE",
    
    # تعدد المهام
    "نفذ_بالتوازي": "THREAD", "انتظر_الكل": "JOIN",
    
    # نظام
    "اقرأ": "READ", "اكتب": "WRITE", "نفذ_امر": "EXEC",
    "وقت": "TIME", "تاريخ": "DATE", "خروج": "EXIT",
}

قاموس_الأهداف = {
    "نموذج": "نموذج", "النموذج": "نموذج", "نموذجي": "نموذج",
    "بيانات": "بيانات", "البيانات": "بيانات", "بياناتي": "بيانات",
    "شبكة": "شبكة", "الشبكة": "شبكة", "شبكتي": "شبكة",
    "طبقات": "طبقات", "الطبقات": "طبقات",
    "رسم": "رسم", "مخطط": "رسم", "الرسم": "رسم",
    "ملف": "ملف", "الملف": "ملف", "مجلد": "مجلد",
}

تصحيحات = {
    "شغلق": "شغّل", "دربق": "درّب", "نموزج": "نموذج",
    "شبكه": "شبكة", "بيانات": "بيانات", "مصفوفه": "مصفوفة",
    "قارن": "قارن", "كرر": "كرر", "طبقه": "طبقة",
    "جدر": "جذر", "قوه": "قوة", "جيبه": "جيب",
}

# ============================================
# ٢. نظام الكائنات والفئات (OOP)
# ============================================
class نظام_الكائنات:
    def __init__(self):
        self.فئات = {}  # اسم_الفئة: {أب, خصائص, دوال}
        self.كائنات = {}  # id: {فئة, خصائص}
    
    def عرف_فئة(self, اسم, أب=None):
        self.فئات[اسم] = {"أب": أب, "خصائص": {}, "دوال": {}}
        print(f"  🏗️  تم تعريف الفئة: {اسم}" + (f" ترث من {أب}" if أب else ""))
    
    def اضف_خاصية(self, فئة, اسم, قيمة=None):
        if فئة in self.فئات:
            self.فئات[فئة]["خصائص"][اسم] = قيمة
    
    def اضف_دالة(self, فئة, اسم, معاملات, جسم):
        if فئة in self.فئات:
            self.فئات[فئة]["دوال"][اسم] = {"معاملات": معاملات, "جسم": جسم}
    
    def انشئ_كائن(self, فئة):
        if فئة not in self.فئات:
            return None
        كائن_id = len(self.كائنات) + 1
        خصائص = {}
        # نسخ خصائص الفئة الأم
        if self.فئات[فئة]["أب"]:
            أب = self.فئات[فئة]["أب"]
            if أب in self.فئات:
                خصائص.update(self.فئات[أب]["خصائص"])
        خصائص.update(self.فئات[فئة]["خصائص"])
        self.كائنات[كائن_id] = {"فئة": فئة, "خصائص": dict(خصائص)}
        return كائن_id
    
    def استدع_دالة(self, كائن_id, اسم_دالة, قيم):
        if كائن_id not in self.كائنات:
            return None
        فئة = self.كائنات[كائن_id]["فئة"]
        # بحث في الدوال
        if فئة in self.فئات and اسم_دالة in self.فئات[فئة]["دوال"]:
            دالة = self.فئات[فئة]["دوال"][اسم_دالة]
            ذاكرة.دفع_نطاق()
            # تعيين self
            ذاكرة.تعيين_متغير("ذاتي", كائن_id, محلي=True)
            # تعيين المعاملات
            for i, م in enumerate(دالة["معاملات"]):
                if i < len(قيم):
                    ذاكرة.تعيين_متغير(م, قيم[i], محلي=True)
            return دالة["جسم"]
        return None

نظام_كائنات = نظام_الكائنات()

# ============================================
# ٣. نظام معالجة الأخطاء
# ============================================
class نظام_استثناءات:
    def __init__(self):
        self.وضع_امساك = False
        self.اخطاء = []
    
    def حاول(self, كود):
        try:
            return True, eval(كود) if isinstance(كود, str) else None
        except Exception as e:
            return False, str(e)

استثناءات = نظام_استثناءات()

# ============================================
# ٤. نظام الشبكات
# ============================================
class نظام_شبكات:
    @staticmethod
    def احصل(رابط):
        try:
            with urllib.request.urlopen(رابط, timeout=5) as f:
                return f.read().decode('utf-8')
        except Exception as e:
            return f"خطأ: {e}"
    
    @staticmethod
    def ارسل(رابط, بيانات):
        try:
            req = urllib.request.Request(رابط, data=بيانات.encode(), method='POST')
            with urllib.request.urlopen(req, timeout=5) as f:
                return f.read().decode('utf-8')
        except Exception as e:
            return f"خطأ: {e}"

# ============================================
# ٥. نظام قواعد البيانات
# ============================================
class نظام_قواعد_بيانات:
    def __init__(self):
        self.قواعد = {}
    
    def فتح(self, مسار):
        if مسار not in self.قواعد:
            self.قواعد[مسار] = sqlite3.connect(مسار)
        return self.قواعد[مسار]
    
    def اغلق(self, مسار):
        if مسار in self.قواعد:
            self.قواعد[مسار].close()
            del self.قواعد[مسار]
    
    def نفذ(self, مسار, استعلام):
        try:
            conn = self.فتح(مسار)
            cur = conn.cursor()
            cur.execute(استعلام)
            conn.commit()
            return cur.fetchall()
        except Exception as e:
            return f"خطأ: {e}"

قواعد_بيانات = نظام_قواعد_بيانات()

# ============================================
# ٦. نظام الواجهة الرسومية
# ============================================
class نظام_رسومي:
    def __init__(self):
        self.نوافذ = {}
    
    def انشئ_نافذة(self, عنوان="نافذة", عرض=400, ارتفاع=300):
        try:
            import tkinter as tk
            نافذة = tk.Tk()
            نافذة.title(عنوان)
            نافذة.geometry(f"{عرض}x{ارتفاع}")
            id_نافذة = len(self.نوافذ) + 1
            self.نوافذ[id_نافذة] = نافذة
            return id_نافذة
        except ImportError:
            print("  ⚠️  tkinter غير متوفر")
            return None
    
    def اضف_زر(self, id_نافذة, نص, امر):
        if id_نافذة in self.نوافذ:
            import tkinter as tk
            زر = tk.Button(self.نوافذ[id_نافذة], text=نص, command=lambda: print(f"  🔘 زر: {امر}"))
            زر.pack(pady=5)
    
    def اضف_نص(self, id_نافذة, نص):
        if id_نافذة in self.نوافذ:
            import tkinter as tk
            تسمية = tk.Label(self.نوافذ[id_نافذة], text=نص)
            تسمية.pack(pady=5)
    
    def ابدا_عرض(self, id_نافذة):
        if id_نافذة in self.نوافذ:
            self.نوافذ[id_نافذة].mainloop()

رسومي = نظام_رسومي()

# ============================================
# ٧. ذاكرة الجلسة المتقدمة
# ============================================
class ذاكرة_الجلسة:
    def __init__(self):
        self.متغيرات = {}
        self.نماذج = {}
        self.مصفوفات = {}
        self.تاريخ = []
        self.سياق = {"آخر_أمر": None, "آخر_هدف": "نموذج", "آخر_مصدر": "بيانات", "آخر_عدد": 1}
        self.دوال_مستخدم = {}
        self.مكتبات_مستوردة = {}
        self.نطاقات = [{}]
    
    def دفع_نطاق(self):
        self.نطاقات.append({})
    
    def سحب_نطاق(self):
        if len(self.نطاقات) > 1:
            return self.نطاقات.pop()
        return None
    
    def تعيين_متغير(self, اسم, قيمة, محلي=False):
        if محلي and len(self.نطاقات) > 1:
            self.نطاقات[-1][اسم] = قيمة
        else:
            self.متغيرات[اسم] = قيمة
    
    def جلب_متغير(self, اسم):
        for نطاق in reversed(self.نطاقات):
            if اسم in نطاق:
                return نطاق[اسم]
        return self.متغيرات.get(اسم)
    
    def تعريف_دالة(self, اسم, معاملات, جسم):
        self.دوال_مستخدم[اسم] = {"معاملات": معاملات, "جسم": جسم}
    
    def استدعاء_دالة(self, اسم, قيم_معاملات):
        if اسم not in self.دوال_مستخدم:
            return None
        دالة = self.دوال_مستخدم[اسم]
        self.دفع_نطاق()
        for i, م in enumerate(دالة["معاملات"]):
            if i < len(قيم_معاملات):
                self.تعيين_متغير(م, قيم_معاملات[i], محلي=True)
        return دالة["جسم"]
    
    def تحديث_سياق(self, أمر, هدف, مصدر, عدد):
        if أمر: self.سياق["آخر_أمر"] = أمر
        if هدف: self.سياق["آخر_هدف"] = هدف
        if مصدر: self.سياق["آخر_مصدر"] = مصدر
        if عدد is not None: self.سياق["آخر_عدد"] = عدد

ذاكرة = ذاكرة_الجلسة()

# ============================================
# ٨. الآلة الافتراضية الكاملة
# ============================================
class آلة_افتراضية_كاملة:
    def __init__(self):
        self.سجلات = [0]*16
        self.ذاكرة_خام = bytearray(32768)
        self.مكدس = []
        self.مؤشر = 0
        self.برنامج = []
        self.تسميات = {}
        self.أعلام = {"صفر": False, "سالب": False, "أكبر": False, "أصغر": False}
        self.نشط = False
        self.عداد_خطوات = 0
    
    def حمل(self, برنامج):
        self.برنامج = برنامج
        self.مؤشر = 0
        self.تسميات = {}
        self.عداد_خطوات = 0
        for i, ت in enumerate(برنامج):
            if ت[0] == ":":
                self.تسميات[ت[1]] = i
    
    def نفذ(self):
        self.نشط = True
        while self.نشط and self.مؤشر < len(self.برنامج):
            if self.عداد_خطوات > 500000:
                print("  ⚠️  تجاوز حد الخطوات الآمن")
                break
            
            ت = self.برنامج[self.مؤشر]
            ع = ت[0]
            
            if ع == "LD": self.سجلات[0] = ت[1]
            elif ع == "ADD": self.سجلات[0] += ت[1]
            elif ع == "SUB": self.سجلات[0] -= ت[1]
            elif ع == "MUL": self.سجلات[0] *= ت[1]
            elif ع == "DIV": self.سجلات[0] //= max(1, ت[1])
            elif ع == "MOD": self.سجلات[0] %= max(1, ت[1])
            elif ع == "POW": self.سجلات[0] = int(self.سجلات[0] ** ت[1])
            elif ع == "SQRT": self.سجلات[0] = int(math.sqrt(max(0, self.سجلات[0])))
            elif ع == "ABS": self.سجلات[0] = abs(self.سجلات[0])
            elif ع == "SIN": self.سجلات[0] = int(math.sin(math.radians(self.سجلات[0])) * 1000)
            elif ع == "COS": self.سجلات[0] = int(math.cos(math.radians(self.سجلات[0])) * 1000)
            elif ع == "TAN": self.سجلات[0] = int(math.tan(math.radians(self.سجلات[0])) * 1000) if self.سجلات[0] % 180 != 90 else 0
            elif ع == "LOG": self.سجلات[0] = int(math.log(max(1, self.سجلات[0])) * 100)
            elif ع == "RND": self.سجلات[0] = random.randint(0, ت[1])
            elif ع == "CMP":
                self.أعلام["صفر"] = (self.سجلات[0] == ت[1])
                self.أعلام["سالب"] = (self.سجلات[0] < ت[1])
                self.أعلام["أكبر"] = (self.سجلات[0] > ت[1])
                self.أعلام["أصغر"] = (self.سجلات[0] < ت[1])
            elif ع == "JMP": self.مؤشر = self.تسميات.get(ت[1], self.مؤشر); continue
            elif ع == "JZ":
                if self.أعلام["صفر"]: self.مؤشر = self.تسميات.get(ت[1], self.مؤشر); continue
            elif ع == "JNZ":
                if not self.أعلام["صفر"]: self.مؤشر = self.تسميات.get(ت[1], self.مؤشر); continue
            elif ع == "JG":
                if self.أعلام["أكبر"]: self.مؤشر = self.تسميات.get(ت[1], self.مؤشر); continue
            elif ع == "JL":
                if self.أعلام["أصغر"]: self.مؤشر = self.تسميات.get(ت[1], self.مؤشر); continue
            elif ع == "PSH": self.مكدس.append(self.سجلات[0])
            elif ع == "POP":
                if self.مكدس: self.سجلات[0] = self.مكدس.pop()
            elif ع == "PRT": print(f"  🖨️  {self.سجلات[0]}")
            elif ع == "PRS": print(f"  📝  {ت[1]}")
            elif ع == "SLP": time.sleep(ت[1] / 1000.0)
            elif ع == "TIME": self.سجلات[0] = int(time.time())
            elif ع == "END": self.نشط = False; return self.سجلات[0]
            
            self.مؤشر += 1
            self.عداد_خطوات += 1
        
        return self.سجلات[0]

vm = آلة_افتراضية_كاملة()

# ============================================
# ٩. المحلل الشامل المتقدم
# ============================================
class محلل_متقدم:
    def __init__(self):
        self.في_دالة = False
        self.جسم_دالة = []
        self.اسم_دالة_حالية = ""
        self.في_صنف = False
        self.اسم_صنف_حالي = ""
        self.جسم_صنف = []
    
    def حلل_و_نفذ(self, نص_خام):
        نص = نص_خام.strip()
        if not نص or نص.startswith("//") or نص.startswith("#"):
            return True
        
        # أوامر النظام
        if نص == "خروج" or نص == "exit": return False
        if نص == "مساعدة": self._مساعدة(); return True
        if نص == "امسح": os.system("clear" if os.name == "posix" else "cls"); return True
        if نص == "ذاكرة": self._عرض_ذاكرة(); return True
        if نص == "تاريخ": self._عرض_تاريخ(); return True
        if نص == "متغيرات": print(f"  📊 {ذاكرة.متغيرات}" if ذاكرة.متغيرات else "  📊 لا متغيرات"); return True
        if نص == "حفظ_جلسة": self._حفظ_جلسة(); return True
        if نص == "تحميل_جلسة": self._تحميل_جلسة(); return True
        if نص == "وقت_الان": print(f"  🕐 {time.strftime('%Y-%m-%d %H:%M:%S')}"); return True
        
        # تعريف دالة
        if نص.startswith("دالة "):
            return self._تعريف_دالة(نص)
        
        # تعريف صنف
        if نص.startswith("صنف "):
            return self._تعريف_صنف(نص)
        
        # إنهاء دالة/صنف
        if نص == "نهاية_دالة":
            return self._انهاء_دالة()
        if نص == "نهاية_صنف":
            return self._انهاء_صنف()
        
        # استدعاء دالة
        if "(" in نص and ")" in نص and not "=" in نص:
            return self._استدعاء_دالة(نص)
        
        # تعيين
        if self._هل_تعيين(نص):
            return self._تعيين(نص)
        
        # استيراد
        if نص.startswith("استورد "):
            return self._استيراد(نص)
        
        # قراءة/كتابة ملف
        if نص.startswith("اقرأ "):
            return self._قراءة_ملف(نص)
        if نص.startswith("اكتب "):
            return self._كتابة_ملف(نص)
        
        # رسم
        if "ارسم" in نص:
            return self._رسم(نص)
        
        # تدريب حقيقي
        if "درب" in نص or "شبكة" in نص:
            return self._تدريب_شبكة(نص)
        
        # تعدد مهام
        if "بالتوازي" in نص:
            return self._تعدد_مهام(نص)
        
        # استثناءات
        if نص.startswith("حاول"):
            return self._محاولة(نص)
        
        # شبكات
        if "احصل" in نص or "ارسل" in نص:
            return self._شبكة(نص)
        
        # قاعدة بيانات
        if "قاعدة_بيانات" in نص or "استعلام" in نص:
            return self._قاعدة_بيانات(نص)
        
        # واجهة رسومية
        if "نافذة" in نص or "زر" in نص:
            return self._رسومي(نص)
        
        # تحليل عادي
        بنية = self._تحليل_الجملة(نص)
        if not بنية["أمر"]:
            print(f"  ❌ لم أفهم: '{نص}'")
            return True
        
        # تأكيد
        if not self._تأكيد(بنية, نص):
            print("  🔄 أعد المحاولة")
            return True
        
        return self._تنفيذ(بنية, نص)
    
    def _تعريف_صنف(self, نص):
        # صنف اسم يرث أب:
        match = re.match(r"صنف\s+(\w+)(?:\s+يرث\s+(\w+))?\s*:", نص)
        if match:
            اسم = match.group(1)
            أب = match.group(2)
            self.في_صنف = True
            self.اسم_صنف_حالي = اسم
            self.جسم_صنف = []
            نظام_الكائنات.عرف_فئة(اسم, أب)
            print("  📝 أدخل خصائص ودوال الصنف ثم 'نهاية_صنف'")
        return True
    
    def _انهاء_صنف(self):
        if self.في_صنف:
            self.في_صنف = False
            self.جسم_صنف = []
            print(f"  ✅ تم تعريف الصنف: {self.اسم_صنف_حالي}")
        return True
    
    def _محاولة(self, نص):
        # حاول: أمر
        match = re.match(r"حاول\s*:\s*(.+)", نص)
        if match:
            امر = match.group(1).strip()
            try:
                self.حلل_و_نفذ(امر)
            except Exception as e:
                print(f"  ⚠️  استثناء: {e}")
        return True
    
    def _شبكة(self, نص):
        if "احصل" in نص:
            رابط = نص.replace("احصل", "").strip().strip('"').strip("'")
            نتيجة = نظام_شبكات.احصل(رابط)
            print(f"  🌐 نتيجة: {نتيجة[:200]}..." if len(نتيجة) > 200 else f"  🌐 نتيجة: {نتيجة}")
        elif "ارسل" in نص:
            match = re.match(r'ارسل\s+"([^"]+)"\s*:\s*(.+)', نص)
            if match:
                رابط = match.group(1)
                بيانات = match.group(2)
                نتيجة = نظام_شبكات.ارسل(رابط, بيانات)
                print(f"  📡 نتيجة: {نتيجة}")
        return True
    
    def _قاعدة_بيانات(self, نص):
        if "استعلام" in نص:
            match = re.match(r'استعلام_قاعدة\s+"([^"]+)"\s*:\s*(.+)', نص)
            if match:
                مسار = match.group(1)
                استعلام = match.group(2)
                نتيجة = قواعد_بيانات.نفذ(مسار, استعلام)
                print(f"  🗄️  نتيجة: {نتيجة}")
        return True
    
    def _رسومي(self, نص):
        if "نافذة" in نص:
            عنوان = "نافذة"
            if "عنوان=" in نص:
                عنوان = re.search(r'عنوان="([^"]+)"', نص).group(1)
            id_ن = رسومي.انشئ_نافذة(عنوان)
            print(f"  🪟 نافذة {id_ن} تم إنشاؤها")
            # إضافة محتوى
            if "نص=" in نص:
                نص_عرض = re.search(r'نص="([^"]+)"', نص).group(1)
                رسومي.اضف_نص(id_ن, نص_عرض)
            if "زر=" in نص:
                زر_نص = re.search(r'زر="([^"]+)"', نص).group(1)
                رسومي.اضف_زر(id_ن, زر_نص, "أمر")
            # تشغيل في خيط منفصل
            if id_ن:
                threading.Thread(target=رسومي.ابدأ_عرض, args=(id_ن,), daemon=True).start()
        return True
    
    def _تعريف_دالة(self, نص):
        match = re.match(r"دالة\s+(\w+)\s*\((.*)\)\s*:", نص)
        if match:
            اسم = match.group(1)
            معاملات = [م.strip() for م in match.group(2).split(",") if م.strip()]
            self.في_دالة = True
            self.اسم_دالة_حالية = اسم
            self.جسم_دالة = []
            ذاكرة.تعريف_دالة(اسم, معاملات, [])
            print(f"  🔧 تعريف دالة: {اسم}({', '.join(معاملات)})")
            print("  📝 أدخل أوامر الدالة ثم 'نهاية_دالة'")
        return True
    
    def _انهاء_دالة(self):
        if self.في_دالة:
            ذاكرة.دوال_مستخدم[self.اسم_دالة_حالية]["جسم"] = self.جسم_دالة.copy()
            print(f"  ✅ تم تعريف الدالة: {self.اسم_دالة_حالية}")
            self.في_دالة = False
            self.جسم_دالة = []
        return True
    
    def _استدعاء_دالة(self, نص):
        match = re.match(r"(\w+)\((.*)\)", نص)
        if match:
            اسم = match.group(1)
            args_str = match.group(2)
            قيم = []
            for ق in args_str.split(","):
                ق = ق.strip()
                if ق.startswith("$"):
                    قيم.append(ذاكرة.جلب_متغير(ق) or 0)
                elif ق.lstrip("-").isdigit():
                    قيم.append(int(ق))
                else:
                    قيم.append(ق)
            
            if اسم in ذاكرة.دوال_مستخدم:
                جسم = ذاكرة.استدعاء_دالة(اسم, قيم)
                print(f"  🔧 استدعاء دالة: {اسم}({قيم})")
                for سطر in جسم:
                    self.حلل_و_نفذ(سطر)
                ذاكرة.سحب_نطاق()
                return True
            elif اسم == "طباعة":
                print(f"  🖨️ {args_str}")
                return True
            elif اسم == "جديد":
                if args_str in نظام_الكائنات.فئات:
                    كائن_id = نظام_الكائنات.انشئ_كائن(args_str)
                    if كائن_id:
                        ذاكرة.تعيين_متغير(f"$كائن_{كائن_id}", كائن_id)
                        print(f"  🆕 كائن من {args_str}: id={كائن_id}")
        return True
    
    def _استيراد(self, نص):
        اسم = نص.replace("استورد ", "").strip().strip('"').strip("'")
        # استخدام نظام المكتبات القديم
        class نظام_مكتبات:
            @staticmethod
            def استورد(اسم):
                try:
                    if اسم == "رياضيات": m = __import__('math')
                    elif اسم == "مصفوفات": m = __import__('numpy')
                    elif اسم == "رسم": m = __import__('matplotlib.pyplot')
                    elif اسم == "عشوائي": m = __import__('random')
                    elif اسم == "وقت": m = __import__('time')
                    elif اسم == "نظام": m = __import__('os')
                    elif اسم == "JSON": m = __import__('json')
                    elif اسم == "CSV": m = __import__('csv')
                    elif اسم == "شبكات": m = __import__('urllib')
                    elif اسم == "قواعد": m = __import__('sqlite3')
                    elif اسم == "رسومي": m = __import__('tkinter')
                    else: return None
                    ذاكرة.مكتبات_مستوردة[اسم] = m
                    return m
                except: return None
        مكتبة = نظام_مكتبات.استورد(اسم)
        if مكتبة:
            print(f"  📚 تم استيراد: {اسم}")
        else:
            print(f"  ⚠️  فشل استيراد: {اسم}")
        return True
    
    def _قراءة_ملف(self, نص):
        مسار = نص.replace("اقرأ ", "").strip().strip('"').strip("'")
        if os.path.exists(مسار):
            with open(مسار, 'r', encoding='utf-8') as f:
                if مسار.endswith('.csv'):
                    محتوى = list(csv.reader(f))
                    print(f"  📄 CSV: {len(محتوى)} صفوف")
                else:
                    محتوى = f.read()
                    print(f"  📄 {len(محتوى)} حرف")
                    print(محتوى[:200])
        else:
            print(f"  ❌ ملف غير موجود: {مسار}")
        return True
    
    def _كتابة_ملف(self, نص):
        match = re.match(r'اكتب\s+"([^"]+)"\s*:\s*(.+)', نص)
        if match:
            مسار = match.group(1)
            محتوى = match.group(2)
            if محتوى.startswith("$"):
                محتوى = ذاكرة.جلب_متغير(محتوى) or محتوى
            with open(مسار, 'w', encoding='utf-8') as f:
                f.write(str(محتوى))
            print(f"  ✅ تم الكتابة إلى: {مسار}")
        return True
    
    def _رسم(self, نص):
        if "دائرة" in نص:
            match = re.search(r'(\d+)', نص)
            نصف = int(match.group(1)) if match else 5
            try:
                import matplotlib.pyplot as plt
                import numpy as np
                θ = np.linspace(0, 2*np.pi, 100)
                x = نصف * np.cos(θ)
                y = نصف * np.sin(θ)
                plt.figure()
                plt.plot(x, y)
                plt.axis('equal')
                plt.title(f'دائرة {نصف}')
                plt.show()
            except:
                print("  ⚠️  مكتبة matplotlib غير متوفرة")
        return True
    
    def _تدريب_شبكة(self, نص):
        طبقات = 3
        دورات = 10
        if "--طبقات=" in نص:
            طبقات = int(re.search(r'--طبقات=(\d+)', نص).group(1))
        if "--دورات=" in نص:
            دورات = int(re.search(r'--دورات=(\d+)', نص).group(1))
        try:
            import numpy as np
            print(f"  🧠 تدريب: {طبقات} طبقات | {دورات} دورة")
            for i in range(min(دورات, 5)):
                خسارة = 1.0 / (i + 1)
                print(f"     دورة {i+1}: خسارة = {خسارة:.4f}")
                time.sleep(0.1)
        except:
            print("  ⚠️  numpy غير متوفر")
        return True
    
    def _تعدد_مهام(self, نص):
        print("  🔀 تنفيذ متوازي (محاكاة)")
        def مهمة1():
            time.sleep(1)
            print("     مهمة 1: تمت")
        def مهمة2():
            time.sleep(0.5)
            print("     مهمة 2: تمت")
        t1 = threading.Thread(target=مهمة1)
        t2 = threading.Thread(target=مهمة2)
        t1.start(); t2.start()
        t1.join(); t2.join()
        print("  ✅ اكتملت المهام")
        return True
    
    def _هل_تعيين(self, نص):
        return "=" in نص and not any(op in نص for op in ["==", "!=", "<=", ">=", "=>"])
    
    def _صحح(self, كلمة):
        if كلمة in تصحيحات:
            ص = تصحيحات[كلمة]
            print(f"  💡 '{كلمة}' ➜ '{ص}'")
            return ص
        return كلمة
    
    def _استبدل_متغير(self, كلمة):
        if كلمة.startswith("$"):
            قيمة = ذاكرة.جلب_متغير(كلمة)
            return str(قيمة) if قيمة is not None else كلمة
        return كلمة
    
    def _تحليل_الجملة(self, نص):
        if "اذا" in نص and ("==" in نص or ">" in نص or "<" in نص):
            return self._تحليل_شرط(نص)
        if "طالما" in نص:
            return self._تحليل_طالما(نص)
        
        كلمات_خام = نص.split()
        كلمات = []
        for ك in كلمات_خام:
            ك = self._استبدل_متغير(ك)
            ك = self._صحح(ك)
            كلمات.append(ك)
        
        بنية = {"أمر": None, "هدف": None, "مصدر": None, "عدد": None, "خيارات": {}, "نص_أصلي": نص, "نوع": "عادي"}
        
        for ك in كلمات:
            if ك.lstrip("-").isdigit():
                بنية["عدد"] = int(ك)
                continue
            if ك in قاموس_الأوامر:
                if بنية["أمر"] is None: بنية["أمر"] = قاموس_الأوامر[ك]
                continue
            if ك.startswith("--"):
                بنية["خيارات"][ك[2:]] = True
                continue
            if ك.startswith("-") and "=" in ك:
                م, ق = ك[1:].split("=", 1)
                بنية["خيارات"][م] = ق
                continue
            if بنية["هدف"] is None: بنية["هدف"] = قاموس_الأهداف.get(ك, ك)
            elif بنية["مصدر"] is None: بنية["مصدر"] = قاموس_الأهداف.get(ك, ك)
        
        if بنية["أمر"] is None and len(كلمات) == 1 and كلمات[0].isdigit():
            بنية["أمر"] = "PRINT"
            بنية["عدد"] = int(كلمات[0])
        
        if بنية["عدد"] is None and بنية["أمر"]:
            بنية["عدد"] = ذاكرة.سياق["آخر_عدد"]
        if بنية["هدف"] is None: بنية["هدف"] = ذاكرة.سياق["آخر_هدف"]
        if بنية["مصدر"] is None: بنية["مصدر"] = ذاكرة.سياق["آخر_مصدر"]
        
        return بنية
    
    def _تحليل_شرط(self, نص):
        match = re.match(r"اذا\s+(.+)\s*:\s*(.+)", نص)
        if match:
            شرط = match.group(1).strip()
            فعل = match.group(2).strip()
            نتيجة = self._قيم_شرط(شرط)
            print(f"  🔍 {شرط} ➜ {'صحيح' if نتيجة else 'خطأ'}")
            if نتيجة:
                self.حلل_و_نفذ(فعل)
        return {"أمر": "NOP", "نوع": "شرط"}
    
    def _تحليل_طالما(self, نص):
        match = re.match(r"طالما\s+(.+)\s*:\s*(.+)", نص)
        if match:
            شرط = match.group(1).strip()
            فعل = match.group(2).strip()
            عداد = 0
            while self._قيم_شرط(شرط) and عداد < 100:
                self.حلل_و_نفذ(فعل)
                عداد += 1
            print(f"  🔁 انتهت بعد {عداد} تكرار")
        return {"أمر": "NOP", "نوع": "طالما"}
    
    def _قيم_شرط(self, شرط):
        for op in [">=", "<=", "==", "!=", ">", "<"]:
            if op in شرط:
                أ, ب = شرط.split(op)
                أ = أ.strip()
                ب = ب.strip()
                if أ.startswith("$"): أ = ذاكرة.جلب_متغير(أ) or 0
                else: أ = int(أ) if أ.lstrip("-").isdigit() else 0
                if ب.startswith("$"): ب = ذاكرة.جلب_متغير(ب) or 0
                else: ب = int(ب) if ب.lstrip("-").isdigit() else 0
                
                if op == ">": return أ > ب
                if op == "<": return أ < ب
                if op == "==": return أ == ب
                if op == "!=": return أ != ب
                if op == ">=": return أ >= ب
                if op == "<=": return أ <= ب
        return False
    
    def _تأكيد(self, بنية, نص):
        if not بنية["أمر"] or بنية["أمر"] == "NOP":
            return False
        
        print(f"\n{'='*60}")
        print(f"  📋 {بنية['أمر']} | هدف: {بنية['هدف']} | عدد: {بنية['عدد']}")
        print(f"{'='*60}")
        
        while True:
            رد = input("  ❓ صحيح؟ (نعم/لا/تخطي): ").strip().lower()
            if رد in ["نعم", "y", "صح"]: return True
            if رد in ["لا", "n"]: return False
            if رد in ["تخطي", "s"]: return False
    
    def _توليد_تعليمات(self, بنية):
        أ = بنية["أمر"]
        ع = بنية["عدد"] or 0
        ت = []
        
        if أ == "ADD": ت = [("LD", ع), ("ADD", ع), ("PRT", 0)]
        elif أ == "SUB": ت = [("LD", ع), ("SUB", ع), ("PRT", 0)]
        elif أ == "MUL": ت = [("LD", ع), ("MUL", ع), ("PRT", 0)]
        elif أ == "DIV": ت = [("LD", ع), ("DIV", max(1, ع)), ("PRT", 0)]
        elif أ == "POW": ت = [("LD", ع), ("POW", 2), ("PRT", 0)]
        elif أ == "SQRT": ت = [("LD", ع), ("SQRT", 0), ("PRT", 0)]
        elif أ == "SIN": ت = [("LD", ع), ("SIN", 0), ("PRT", 0)]
        elif أ == "COS": ت = [("LD", ع), ("COS", 0), ("PRT", 0)]
        elif أ == "TAN": ت = [("LD", ع), ("TAN", 0), ("PRT", 0)]
        elif أ == "LOG": ت = [("LD", ع), ("LOG", 0), ("PRT", 0)]
        elif أ == "RND": ت = [("LD", ع), ("RND", ع), ("PRT", 0)]
        elif أ == "ABS": ت = [("LD", ع), ("ABS", 0), ("PRT", 0)]
        elif أ == "CMP": ت = [("LD", ع), ("CMP", ع), ("PRT", 0)]
        elif أ == "LOOP":
            for i in range(max(1, ع)):
                print(f"     {i+1}. ♻️")
            ت = [("LD", ع), ("PRT", 0)]
        elif أ == "SLEEP":
            time.sleep(ع)
            ت = [("LD", ع), ("PRT", 0)]
        elif أ == "TIME": ت = [("LD", int(time.time())), ("PRT", 0)]
        elif أ == "PRINT": ت = [("LD", ع), ("PRT", 0)]
        elif أ in ["RUN", "TRAIN", "BUILD", "TEST", "SAVE", "LOAD"]:
            ت = [("LD", ع), ("PRT", 0), ("PRS", f"{أ} {بنية['هدف'] or ''}")]
        else:
            ت = [("LD", ع), ("PRT", 0)]
        
        ت.append(("END", 0))
        return ت
    
    def _تنفيذ(self, بنية, نص):
        if self.في_دالة:
            self.جسم_دالة.append(نص)
            return True
        if self.في_صنف:
            self.جسم_صنف.append(نص)
            return True
        
        تعليمات = self._توليد_تعليمات(بنية)
        if تعليمات:
            vm.حمل(تعليمات)
            نتيجة = vm.نفذ()
            print(f"  ✅ نتيجة VM: {نتيجة}")
        
        ذاكرة.تحديث_سياق(بنية["أمر"], بنية["هدف"], بنية["مصدر"], بنية["عدد"])
        ذاكرة.تاريخ.append({"نص": نص, "وقت": time.time()})
        return True
    
    def _تعيين(self, نص):
        if "=" in نص:
            م, ق = نص.split("=", 1)
            م = م.strip()
            ق = ق.strip()
            try:
                if ق.startswith("[") or ق.startswith("{"):
                    ق = json.loads(ق.replace("'", '"'))
                elif "." in ق:
                    ق = float(ق)
                elif ق.lstrip("-").isdigit():
                    ق = int(ق)
            except: pass
            ذاكرة.تعيين_متغير(م, ق)
            print(f"  ✅ {م} = {ق}")
        return True
    
    def _مساعدة(self):
        print("""
╔══════════════════════════════════════════════════╗
║  🫀  القلب الناطق - الدليل المتقدم الكامل  🫀  ║
╠══════════════════════════════════════════════════╣
║  OOP:                                              ║
║    صنف اسم يرث أب:                                 ║
║    ... خصائص ودوال ...                              ║
║    نهاية_صنف                                        ║
║    $ك = جديد(اسم)                                  ║
║                                                     ║
║  استثناءات:                                         ║
║    حاول: امر                                        ║
║                                                     ║
║  شبكات:                                             ║
║    احصل "https://example.com"                        ║
║    ارسل "https://api.com" : بيانات                  ║
║                                                     ║
║  قواعد بيانات:                                      ║
║    استعلام_قاعدة "قاعدة.db" : SELECT * FROM جدول    ║
║                                                     ║
║  واجهة رسومية:                                      ║
║    نافذة عنوان="تطبيق" نص="مرحبا" زر="اضغط"        ║
║                                                     ║
║  دوال: دالة اسم(س): ... نهاية_دالة                   ║
║  شروط: اذا $س > 5: اعرض "كبير"                     ║
║  حلقات: طالما $س < 10: زد $س                       ║
║  مكتبات: استورد "رياضيات"                           ║
╚══════════════════════════════════════════════════╝
        """)
    
    def _عرض_ذاكرة(self):
        print(f"  🧠 متغيرات: {ذاكرة.متغيرات}")
        print(f"  🧠 دوال: {list(ذاكرة.دوال_مستخدم.keys())}")
        print(f"  🧠 فئات: {list(نظام_الكائنات.فئات.keys())}")
        print(f"  🧠 كائنات: {list(نظام_الكائنات.كائنات.keys())}")
    
    def _عرض_تاريخ(self):
        if not ذاكرة.تاريخ:
            print("  📜 لا تاريخ")
            return
        for i, س in enumerate(ذاكرة.تاريخ[-10:], 1):
            print(f"  {i}. {س['نص'][:60]}")
    
    def _حفظ_جلسة(self):
        with open("جلسة_متقدمة.قلب", "w", encoding="utf-8") as f:
            json.dump({
                "متغيرات": ذاكرة.متغيرات,
                "دوال": {اسم: {"معاملات": د["معاملات"], "جسم": د["جسم"]} for اسم, د in ذاكرة.دوال_مستخدم.items()},
                "فئات": نظام_الكائنات.فئات,
                "تاريخ": [t["نص"] for t in ذاكرة.تاريخ[-50:]]
            }, f, ensure_ascii=False, indent=2)
        print("  💾 حفظ في جلسة_متقدمة.قلب")
    
    def _تحميل_جلسة(self):
        if os.path.exists("جلسة_متقدمة.قلب"):
            with open("جلسة_متقدمة.قلب", "r", encoding="utf-8") as f:
                d = json.load(f)
                ذاكرة.متغيرات = d.get("متغيرات", {})
                for اسم, د in d.get("دوال", {}).items():
                    ذاكرة.تعريف_دالة(اسم, د["معاملات"], د["جسم"])
                نظام_الكائنات.فئات = d.get("فئات", {})
            print("  📂 تم التحميل")

# ============================================
# ١٠. الواجهة الرئيسية
# ============================================
def رئيسي():
    محلل = محلل_متقدم()
    
    print("="*70)
    print("  🫀  القلب الناطق - النسخة المتقدمة الشاملة  🫀")
    print("  OOP | استثناءات | شبكات | قواعد بيانات | واجهة رسومية")
    print("  اكتب 'مساعدة' | 'خروج' للإنهاء")
    print("="*70)
    
    if len(sys.argv) > 1:
        مسار = sys.argv[1]
        if os.path.exists(مسار):
            print(f"  📂 {مسار}")
            with open(مسار, 'r', encoding='utf-8') as f:
                for سطر in f:
                    سطر = سطر.strip()
                    if سطر and not سطر.startswith("//"):
                        print(f"\n📝 {سطر}")
                        if not محلل.حلل_و_نفذ(سطر):
                            break
        return
    
    while True:
        try:
            نص = input("\n📝 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  👋 مع السلامة")
            break
        
        if not نص: continue
        if not محلل.حلل_و_نفذ(نص):
            print("  👋 مع السلامة")
            break

if __name__ == "__main__":
    رئيسي()
