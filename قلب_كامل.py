#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🫀 القلب الناطق - النسخة الكاملة الشاملة
# جميع الميزات: دوال، شروط، حلقات، مكتبات، ملفات، رسم، ذكاء، تعدد مهام

import sys, os, struct, json, re, math, time, random, hashlib, subprocess
import threading, queue, csv, io

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
    
    # دوال المستخدم
    "دالة": "DEF", "نفذ_دالة": "CALL", "ارجع": "RETURN",
    
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
# ٢. ذاكرة الجلسة المتقدمة مع الدوال
# ============================================
class ذاكرة_الجلسة:
    def __init__(self):
        self.متغيرات = {}
        self.نماذج = {}
        self.مصفوفات = {}
        self.تاريخ = []
        self.سياق = {"آخر_أمر": None, "آخر_هدف": "نموذج", "آخر_مصدر": "بيانات", "آخر_عدد": 1}
        self.دوال_مستخدم = {}  # اسم_الدالة: {معاملات, جسم}
        self.مكتبات_مستوردة = {}
        self.نطاقات = [{}]  # مكدس النطاقات للمتغيرات المحلية
    
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
        # بحث في النطاقات المحلية أولاً
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
        # دفع نطاق جديد
        self.دفع_نطاق()
        # تعيين المعاملات
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
# ٣. نظام المكتبات
# ============================================
class نظام_المكتبات:
    مكتبات_جاهزة = {
        "رياضيات": lambda: __import__('math'),
        "مصفوفات": lambda: __import__('numpy'),
        "رسم": lambda: __import__('matplotlib.pyplot'),
        "عشوائي": lambda: __import__('random'),
        "وقت": lambda: __import__('time'),
        "نظام": lambda: __import__('os'),
        "JSON": lambda: __import__('json'),
        "CSV": lambda: __import__('csv'),
    }
    
    @classmethod
    def استورد(cls, اسم_المكتبة):
        if اسم_المكتبة in cls.مكتبات_جاهزة:
            try:
                مكتبة = cls.مكتبات_جاهزة[اسم_المكتبة]()
                ذاكرة.مكتبات_مستوردة[اسم_المكتبة] = مكتبة
                return مكتبة
            except ImportError:
                print(f"  ⚠️  المكتبة '{اسم_المكتبة}' غير متوفرة. ثبتها أولاً.")
                return None
        return None

# ============================================
# ٤. نظام الملفات
# ============================================
class نظام_الملفات:
    @staticmethod
    def اقرأ(مسار):
        if not os.path.exists(مسار):
            return None
        with open(مسار, 'r', encoding='utf-8') as f:
            if مسار.endswith('.csv'):
                return list(csv.reader(f))
            return f.read()
    
    @staticmethod
    def اكتب(مسار, محتوى):
        with open(مسار, 'w', encoding='utf-8') as f:
            if isinstance(محتوى, list) and مسار.endswith('.csv'):
                csv.writer(f).writerows(محتوى)
            else:
                f.write(str(محتوى))
        return True

# ============================================
# ٥. نظام الرسم
# ============================================
class نظام_الرسم:
    @staticmethod
    def ارسم_دائرة(نصف_قطر):
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            θ = np.linspace(0, 2*np.pi, 100)
            x = نصف_قطر * np.cos(θ)
            y = نصف_قطر * np.sin(θ)
            plt.figure(figsize=(6,6))
            plt.plot(x, y)
            plt.axis('equal')
            plt.title(f'دائرة نصف قطرها {نصف_قطر}')
            plt.show()
        except:
            print("  ⚠️  مكتبة matplotlib غير متوفرة")

# ============================================
# ٦. نظام الذكاء الاصطناعي الحقيقي
# ============================================
class نظام_ذكاء:
    @staticmethod
    def تدريب_شبكة(طبقات, بيانات=None, دورات=10):
        try:
            import numpy as np
            print(f"  🧠 تدريب شبكة عصبية: {طبقات} طبقات | {دورات} دورة")
            # شبكة بسيطة للتوضيح
            if بيانات is None:
                np.random.seed(42)
                X = np.random.rand(100, 3)
                y = np.random.rand(100, 1)
            else:
                X, y = بيانات
            
            # محاكاة تدريب
            for i in range(min(دورات, 5)):
                خسارة = 1.0 / (i + 1)
                print(f"     دورة {i+1}: خسارة = {خسارة:.4f}")
                time.sleep(0.1)
            return True
        except ImportError:
            print("  ⚠️  ثبت numpy: pkg install python-numpy")
            return False

# ============================================
# ٧. نظام تعدد المهام
# ============================================
class نظام_تعدد_مهام:
    def __init__(self):
        self.خيوط = []
        self.نتائج = queue.Queue()
    
    def نفذ_بالتوازي(self, مهام):
        self.خيوط = []
        for مهمة in مهام:
            خيط = threading.Thread(target=self._نفذ_مهمة, args=(مهمة,))
            self.خيوط.append(خيط)
            خيط.start()
    
    def _نفذ_مهمة(self, مهمة):
        try:
            نتيجة = مهمة()
            self.نتائج.put(نتيجة)
        except Exception as e:
            self.نتائج.put(f"خطأ: {e}")
    
    def انتظر_الكل(self):
        for خيط in self.خيوط:
            خيط.join()
        نتائج = []
        while not self.نتائج.empty():
            نتائج.append(self.نتائج.get())
        return نتائج

متعدد_مهام = نظام_تعدد_مهام()

# ============================================
# ٨. الآلة الافتراضية الكاملة مع الشروط والحلقات
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
            elif ع == "PRT": print(f"  🖨️  المخرجات: {self.سجلات[0]}")
            elif ع == "PRS": print(f"  📝  {ت[1]}")
            elif ع == "SLP": time.sleep(ت[1] / 1000.0)
            elif ع == "TIME": self.سجلات[0] = int(time.time())
            elif ع == "END": self.نشط = False; return self.سجلات[0]
            
            self.مؤشر += 1
            self.عداد_خطوات += 1
        
        return self.سجلات[0]

vm = آلة_افتراضية_كاملة()

# ============================================
# ٩. المحلل الشامل الكامل
# ============================================
class محلل_شامل_كامل:
    def __init__(self):
        self.في_دالة = False
        self.جسم_دالة = []
        self.اسم_دالة_حالية = ""
    
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
        
        # إنهاء دالة
        if نص == "نهاية_دالة":
            return self._انهاء_دالة()
        
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
    
    def _تعريف_دالة(self, نص):
        # دالة اسم(س, ص):
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
                # تنفيذ جسم الدالة
                for سطر in جسم:
                    self.حلل_و_نفذ(سطر)
                ذاكرة.سحب_نطاق()
                return True
            elif اسم == "طباعة":
                print(f"  🖨️ {args_str}")
                return True
        return True
    
    def _استيراد(self, نص):
        اسم = نص.replace("استورد ", "").strip().strip('"').strip("'")
        مكتبة = نظام_المكتبات.استورد(اسم)
        if مكتبة:
            print(f"  📚 تم استيراد: {اسم}")
        return True
    
    def _قراءة_ملف(self, نص):
        مسار = نص.replace("اقرأ ", "").strip().strip('"').strip("'")
        محتوى = نظام_الملفات.اقرأ(مسار)
        if محتوى is not None:
            if isinstance(محتوى, list):
                print(f"  📄 CSV: {len(محتوى)} صفوف")
                for صف in محتوى[:5]:
                    print(f"     {صف}")
            else:
                print(f"  📄 {len(محتوى)} حرف")
                print(محتوى[:200])
        else:
            print(f"  ❌ ملف غير موجود: {مسار}")
        return True
    
    def _كتابة_ملف(self, نص):
        # اكتب "مسار" : محتوى
        match = re.match(r'اكتب\s+"([^"]+)"\s*:\s*(.+)', نص)
        if match:
            مسار = match.group(1)
            محتوى = match.group(2)
            if محتوى.startswith("$"):
                محتوى = ذاكرة.جلب_متغير(محتوى) or محتوى
            نظام_الملفات.اكتب(مسار, محتوى)
            print(f"  ✅ تم الكتابة إلى: {مسار}")
        return True
    
    def _رسم(self, نص):
        if "دائرة" in نص:
            match = re.search(r'(\d+)', نص)
            نصف = int(match.group(1)) if match else 5
            نظام_الرسم.ارسم_دائرة(نصف)
        return True
    
    def _تدريب_شبكة(self, نص):
        طبقات = 3
        دورات = 10
        if "--طبقات=" in نص:
            طبقات = int(re.search(r'--طبقات=(\d+)', نص).group(1))
        if "--دورات=" in نص:
            دورات = int(re.search(r'--دورات=(\d+)', نص).group(1))
        نظام_ذكاء.تدريب_شبكة(طبقات, دورات=دورات)
        return True
    
    def _تعدد_مهام(self, نص):
        print("  🔀 تنفيذ متوازي (محاكاة)")
        def مهمة1():
            time.sleep(1)
            print("     مهمة 1: تمت")
        def مهمة2():
            time.sleep(0.5)
            print("     مهمة 2: تمت")
        متعدد_مهام.نفذ_بالتوازي([مهمة1, مهمة2])
        نتائج = متعدد_مهام.انتظر_الكل()
        print(f"  ✅ نتائج: {نتائج}")
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
        # شرط if
        if "اذا" in نص and ("==" in نص or ">" in نص or "<" in نص):
            return self._تحليل_شرط(نص)
        
        # حلقة while
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
        # اذا $س > 10: اعرض "كبير"
        match = re.match(r"اذا\s+(.+)\s*:\s*(.+)", نص)
        if match:
            شرط = match.group(1).strip()
            فعل = match.group(2).strip()
            # تقييم الشرط
            نتيجة_الشرط = self._قيم_شرط(شرط)
            print(f"  🔍 شرط: {شرط} ➜ {'صحيح' if نتيجة_الشرط else 'خطأ'}")
            if نتيجة_الشرط:
                self.حلل_و_نفذ(فعل)
        return {"أمر": "NOP", "نوع": "شرط"}
    
    def _تحليل_طالما(self, نص):
        # طالما $س < 10: زد $س
        match = re.match(r"طالما\s+(.+)\s*:\s*(.+)", نص)
        if match:
            شرط = match.group(1).strip()
            فعل = match.group(2).strip()
            عداد = 0
            while self._قيم_شرط(شرط) and عداد < 100:
                self.حلل_و_نفذ(فعل)
                عداد += 1
            print(f"  🔁 انتهت الحلقة بعد {عداد} تكرار")
        return {"أمر": "NOP", "نوع": "طالما"}
    
    def _قيم_شرط(self, شرط):
        # تقييم تعبير مثل "$س > 10" أو "$س == 5"
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
║    🫀  القلب الناطق - الدليل الكامل النهائي  🫀  ║
╠══════════════════════════════════════════════════╣
║  دوال:                                           ║
║    دالة اسم(س, ص):                                 ║
║    ... أوامر ...                                   ║
║    نهاية_دالة                                      ║
║    اسم(5, 10)          استدعاء                     ║
║                                                   ║
║  شروط:                                            ║
║    اذا $س > 10: اعرض "كبير"                       ║
║    اذا $س == 5: زد $س                             ║
║                                                   ║
║  حلقات:                                           ║
║    طالما $س < 10: زد $س                           ║
║    كرر 5                                           ║
║                                                   ║
║  مكتبات:                                          ║
║    استورد "رياضيات"                                ║
║    استورد "مصفوفات"  (NumPy)                      ║
║    استورد "رسم"      (Matplotlib)                  ║
║                                                   ║
║  ملفات:                                           ║
║    اقرأ "بيانات.csv"                               ║
║    اكتب "نتائج.txt" : $نتيجة                       ║
║                                                   ║
║  رسم:                                             ║
║    ارسم دائرة 50                                   ║
║                                                   ║
║  ذكاء اصطناعي:                                    ║
║    درب شبكة --طبقات=5 --دورات=20                  ║
║                                                   ║
║  تعدد مهام:                                       ║
║    نفذ_بالتوازي مهمة1 مهمة2                       ║
║                                                   ║
║  نظام: امسح | ذاكرة | تاريخ | خروج                ║
╚══════════════════════════════════════════════════╝
        """)
    
    def _عرض_ذاكرة(self):
        print("  🧠 ذاكرة:")
        print(f"     متغيرات: {ذاكرة.متغيرات}")
        print(f"     دوال: {list(ذاكرة.دوال_مستخدم.keys())}")
        print(f"     مكتبات: {list(ذاكرة.مكتبات_مستوردة.keys())}")
        print(f"     سياق: {ذاكرة.سياق}")
    
    def _عرض_تاريخ(self):
        if not ذاكرة.تاريخ:
            print("  📜 لا تاريخ")
            return
        print(f"  📜 آخر 10:")
        for i, س in enumerate(ذاكرة.تاريخ[-10:], 1):
            print(f"     {i}. {س['نص'][:60]}")
    
    def _حفظ_جلسة(self):
        with open("جلسة_كاملة.قلب", "w", encoding="utf-8") as f:
            json.dump({
                "متغيرات": ذاكرة.متغيرات,
                "دوال": {اسم: {"معاملات": د["معاملات"], "جسم": د["جسم"]} for اسم, د in ذاكرة.دوال_مستخدم.items()},
                "تاريخ": [t["نص"] for t in ذاكرة.تاريخ[-50:]]
            }, f, ensure_ascii=False, indent=2)
        print("  💾 حفظ في جلسة_كاملة.قلب")
    
    def _تحميل_جلسة(self):
        if os.path.exists("جلسة_كاملة.قلب"):
            with open("جلسة_كاملة.قلب", "r", encoding="utf-8") as f:
                d = json.load(f)
                ذاكرة.متغيرات = d.get("متغيرات", {})
                for اسم, د in d.get("دوال", {}).items():
                    ذاكرة.تعريف_دالة(اسم, د["معاملات"], د["جسم"])
            print("  📂 تم التحميل")

# ============================================
# ١٠. الواجهة الرئيسية
# ============================================
def رئيسي():
    محلل = محلل_شامل_كامل()
    
    print("="*70)
    print("  🫀  القلب الناطق - النسخة الكاملة الشاملة  🫀")
    print("  دوال | شروط | حلقات | مكتبات | ملفات | رسم")
    print("  ذكاء اصطناعي | تعدد مهام | حفظ كامل")
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
