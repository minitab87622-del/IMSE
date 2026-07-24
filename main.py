import json
import os
import sys

# محاولة تحميل مكتبات تشكيل اللغة العربية
HAS_ARABIC = False
try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    HAS_ARABIC = True
except ImportError:
    HAS_ARABIC = False

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

# تحديد المسارات الأساسية للملفات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "font.ttf")
BG_PATH = os.path.join(BASE_DIR, "background.png")
ICON_PATH = os.path.join(BASE_DIR, "icon.png")

# إعداد وتسجيل الخط العربي
FONT_NAME = "Roboto"
if os.path.exists(FONT_PATH):
    try:
        LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
        FONT_NAME = "ArabicFont"
    except Exception:
        FONT_NAME = "Roboto"


def ar(text):
    if not text:
        return ""
    if HAS_ARABIC:
        try:
            reshaped_text = arabic_reshaper.reshape(str(text))
            return get_display(reshaped_text)
        except Exception:
            return str(text)
    return str(text)


# شاشة أساسية تعتمد صورة الخلفية background.png تلقائياً
class BaseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            if os.path.exists(BG_PATH):
                self.bg_rect = Rectangle(
                    source=BG_PATH, pos=self.pos, size=self.size
                )
                self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, instance, value):
        if hasattr(self, "bg_rect"):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size


CURRICULUM = {
    "المستوى الأول": {
        "الفصل الأول": [
            {"name": "مهارات الحاسوب", "hours": 3},
            {"name": "لغة عربية (1)", "hours": 2},
            {"name": "التفاضل والتكامل 1", "hours": 3},
            {"name": "الثقافة الإسلامية", "hours": 2},
            {"name": "اللغة الإنجليزية (1)", "hours": 2},
            {"name": "فيزياء عامة", "hours": 4},
            {"name": "رسم هندسي 1", "hours": 3},
        ],
        "الفصل الثاني": [
            {"name": "اللغة العربية (2)", "hours": 2},
            {"name": "اللغة الإنجليزية (2)", "hours": 2},
            {"name": "التفاضل والتكامل 2", "hours": 3},
            {"name": "أساسيات البرمجة", "hours": 3},
            {"name": "رسم هندسي 2", "hours": 3},
            {"name": "فيزياء هندسية", "hours": 4},
            {"name": "الجبر الخطي", "hours": 3},
        ],
    },
    "المستوى الثاني": {
        "الفصل الأول": [
            {"name": "تطبيقات الحاسوب في الهندسة", "hours": 2},
            {"name": "معادلات تفاضلية", "hours": 3},
            {"name": "ديناميكا حرارية", "hours": 3},
            {"name": "مبادئ هندسة كهربائية والكترونية", "hours": 4},
            {"name": "علم المواد", "hours": 3},
            {"name": "استاتيكا", "hours": 3},
            {"name": "التصميم بمساعدة الحاسوب CAD", "hours": 3},
        ],
        "الفصل الثاني": [
            {"name": "تحليل عددي", "hours": 3},
            {"name": "مقاومة مواد", "hours": 3},
            {"name": "بحوث عمليات 1", "hours": 3},
            {"name": "ديناميكا", "hours": 3},
            {"name": "عمليات صناعية 1", "hours": 3},
            {"name": "ميكانيكا الموائع", "hours": 3},
            {"name": "التصميم المنطقي الرقمي", "hours": 3},
        ],
    },
    "المستوى الثالث": {
        "الفصل الأول": [
            {"name": "الإحصاء والاحتمالات", "hours": 3},
            {"name": "التصميم التجريبي", "hours": 3},
            {"name": "عمليات صناعية 2", "hours": 3},
            {"name": "تخطيط الإنتاج والتحكم بالمخزون", "hours": 4},
            {"name": "بحوث عمليات 2", "hours": 3},
            {"name": "إدارة التسويق والمبيعات", "hours": 2},
        ],
        "الفصل الثاني": [
            {"name": "التحكم بالجودة الصناعية", "hours": 3},
            {"name": "إدارة سلاسل الإمداد", "hours": 3},
            {"name": "تصميم وتخطيط المرافق", "hours": 3},
            {"name": "الإدارة الصناعية", "hours": 3},
            {"name": "الصيانة الهندسية والموثوقية", "hours": 4},
            {"name": "محاسبة وتكاليف", "hours": 2},
        ],
    },
    "المستوى الرابع": {
        "الفصل الأول": [
            {"name": "إدارة الجودة الشاملة", "hours": 3},
            {"name": "تصميم أنظمة التحكم", "hours": 4},
            {"name": "قياسات وأدوات قياس", "hours": 3},
            {"name": "التصنيع بمساعدة الحاسوب CAM", "hours": 4},
            {"name": "أنظمة النمذجة والمحاكاة", "hours": 3},
            {"name": "إدارة مشاريع هندسية", "hours": 3},
        ],
        "الفصل الثاني": [
            {"name": "اقتصاد هندسي", "hours": 3},
            {"name": "هندسة العوامل البشرية والأمان", "hours": 3},
            {"name": "تكنولوجيا التصنيع المتقدم", "hours": 4},
            {"name": "طرق بحث", "hours": 2},
            {"name": "الذكاء الاصطناعي الصناعي", "hours": 3},
            {"name": "نظم المعلومات الصناعية", "hours": 2},
        ],
    },
    "المستوى الخامس": {
        "الفصل الأول": [
            {"name": "دراسة الحركة والوقت", "hours": 4},
            {"name": "اختياري 1", "hours": 3},
            {"name": "اختياري 2", "hours": 3},
            {"name": "مشروع تخرج 1", "hours": 2},
        ],
        "الفصل الثاني": [
            {"name": "الأتمتة الصناعية", "hours": 4},
            {"name": "اختياري 3", "hours": 3},
            {"name": "اختياري 4", "hours": 3},
            {"name": "مشروع تخرج 2", "hours": 2},
        ],
    },
}


class DataManager:

    def __init__(self):
        self.student_name = ""
        self.grades = {}

    def save_to_file(self):
        if not self.student_name:
            return False, "يرجى إدخال اسم الطالب أولاً"
        filename = f"{self.student_name}_gpa.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.grades, f, ensure_ascii=False, indent=4)
            return True, f"تم حفظ البيانات في {filename}"
        except Exception as e:
            return False, str(e)

    def load_from_file(self, name):
        filename = f"{name}_gpa.json"
        if not os.path.exists(filename):
            return False, "الملف غير موجود"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.grades = json.load(f)
            self.student_name = name
            return True, "تم تحميل البيانات بنجاح"
        except Exception as e:
            return False, str(e)

    def get_term_gpa(self, level, term):
        courses = CURRICULUM.get(level, {}).get(term, [])
        saved = self.grades.get(level, {}).get(term, {})
        pts, hrs = 0.0, 0
        for c in courses:
            cname = c["name"]
            chrs = c["hours"]
            if cname in saved:
                pts += saved[cname] * chrs
                hrs += chrs
        return (pts / hrs) if hrs > 0 else 0.0, hrs

    def get_year_gpa(self, level):
        pts, hrs = 0.0, 0
        for t in ["الفصل الأول", "الفصل الثاني"]:
            gpa, thrs = self.get_term_gpa(level, t)
            pts += gpa * thrs
            hrs += thrs
        return (pts / hrs) if hrs > 0 else 0.0, hrs

    def get_overall_gpa(self):
        pts, hrs = 0.0, 0
        for lvl in CURRICULUM.keys():
            gpa, yhrs = self.get_year_gpa(lvl)
            pts += gpa * yhrs
            hrs += yhrs
        return (pts / hrs) if hrs > 0 else 0.0, hrs


data_mgr = DataManager()


class MainScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(
            orientation="vertical", padding=15, spacing=10
        )

        top_box = BoxLayout(size_hint_y=0.12, spacing=5)
        self.name_input = TextInput(
            hint_text=ar("أدخل اسم الطالب"),
            font_name=FONT_NAME,
            multiline=False,
        )
        btn_save = Button(
            text=ar("حفظ"),
            font_name=FONT_NAME,
            size_hint_x=0.25,
            background_color=(0.1, 0.7, 0.3, 1),
        )
        btn_load = Button(
            text=ar("تحميل"),
            font_name=FONT_NAME,
            size_hint_x=0.25,
            background_color=(0.2, 0.5, 0.8, 1),
        )

        btn_save.bind(on_press=self.save_data)
        btn_load.bind(on_press=self.load_data)

        top_box.add_widget(self.name_input)
        top_box.add_widget(btn_save)
        top_box.add_widget(btn_load)
        self.layout.add_widget(top_box)

        self.layout.add_widget(
            Label(
                text=ar("اختر المستوى الدراسي:"),
                font_name=FONT_NAME,
                font_size="18sp",
                size_hint_y=0.08,
            )
        )
        for lvl in CURRICULUM.keys():
            btn = Button(
                text=ar(lvl),
                font_name=FONT_NAME,
                size_hint_y=0.12,
                font_size="16sp",
            )
            btn.bind(on_press=lambda b, l=lvl: self.select_level(l))
            self.layout.add_widget(btn)

        self.overall_label = Label(
            text=ar("المعدل التراكمي العام: 0.00%"),
            font_name=FONT_NAME,
            font_size="16sp",
            size_hint_y=0.12,
            color=(0.2, 0.9, 0.4, 1),
        )
        self.layout.add_widget(self.overall_label)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        gpa, hrs = data_mgr.get_overall_gpa()
        self.overall_label.text = ar(
            f"المعدل التراكمي لجميع السنين: {gpa:.2f}%\n(إجمالي الساعات: {hrs})"
        )

    def select_level(self, level):
        self.manager.get_screen("term").selected_level = level
        self.manager.current = "term"

    def save_data(self, instance):
        data_mgr.student_name = self.name_input.text.strip()
        ok, msg = data_mgr.save_to_file()
        Popup(
            title=ar("تنبيه"),
            content=Label(text=ar(msg), font_name=FONT_NAME),
            size_hint=(0.8, 0.4),
        ).open()

    def load_data(self, instance):
        name = self.name_input.text.strip()
        ok, msg = data_mgr.load_from_file(name)
        if ok:
            self.on_pre_enter()
        Popup(
            title=ar("تنبيه"),
            content=Label(text=ar(msg), font_name=FONT_NAME),
            size_hint=(0.8, 0.4),
        ).open()


class TermScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_level = "المستوى الأول"
        self.layout = BoxLayout(
            orientation="vertical", padding=15, spacing=15
        )

        self.title_lbl = Label(
            text="", font_name=FONT_NAME, font_size="18sp", size_hint_y=0.15
        )
        self.layout.add_widget(self.title_lbl)

        btn_t1 = Button(
            text=ar("الفصل الأول"),
            font_name=FONT_NAME,
            size_hint_y=0.18,
            font_size="16sp",
        )
        btn_t2 = Button(
            text=ar("الفصل الثاني"),
            font_name=FONT_NAME,
            size_hint_y=0.18,
            font_size="16sp",
        )

        btn_t1.bind(on_press=lambda b: self.select_term("الفصل الأول"))
        btn_t2.bind(on_press=lambda b: self.select_term("الفصل الثاني"))

        self.layout.add_widget(btn_t1)
        self.layout.add_widget(btn_t2)

        self.year_gpa_lbl = Label(
            text=ar("معدل السنة: 0.00%"),
            font_name=FONT_NAME,
            font_size="16sp",
            size_hint_y=0.15,
            color=(0.9, 0.7, 0.2, 1),
        )
        self.layout.add_widget(self.year_gpa_lbl)

        btn_back = Button(
            text=ar("← رجوع للمستويات"),
            font_name=FONT_NAME,
            size_hint_y=0.12,
            background_color=(0.6, 0.6, 0.6, 1),
        )
        btn_back.bind(on_press=lambda b: setattr(self.manager, "current", "main"))
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.title_lbl.text = ar(f"اختر الفصل - {self.selected_level}")
        gpa, hrs = data_mgr.get_year_gpa(self.selected_level)
        self.year_gpa_lbl.text = ar(
            f"معدل {self.selected_level}: {gpa:.2f}%\n(الساعات: {hrs})"
        )

    def select_term(self, term):
        gs = self.manager.get_screen("grade")
        gs.selected_level = self.selected_level
        gs.selected_term = term
        self.manager.current = "grade"


class GradeScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_level = ""
        self.selected_term = ""

        self.layout = BoxLayout(
            orientation="vertical", padding=10, spacing=10
        )
        self.header_lbl = Label(
            text="", font_name=FONT_NAME, font_size="16sp", size_hint_y=0.08
        )
        self.layout.add_widget(self.header_lbl)

        self.scroll = ScrollView(size_hint=(1, 0.65))
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        self.inputs = {}

        btn_calc = Button(
            text=ar("حساب ومزامنة معدل الترم"),
            font_name=FONT_NAME,
            size_hint_y=0.1,
            background_color=(0.1, 0.6, 0.9, 1),
        )
        btn_calc.bind(on_press=self.calculate)
        self.layout.add_widget(btn_calc)

        self.term_gpa_lbl = Label(
            text=ar("معدل الترم: 0.00%"),
            font_name=FONT_NAME,
            font_size="15sp",
            size_hint_y=0.08,
        )
        self.layout.add_widget(self.term_gpa_lbl)

        btn_back = Button(
            text=ar("← رجوع للفصول"),
            font_name=FONT_NAME,
            size_hint_y=0.09,
            background_color=(0.6, 0.6, 0.6, 1),
        )
        btn_back.bind(on_press=lambda b: setattr(self.manager, "current", "term"))
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.header_lbl.text = ar(
            f"{self.selected_level} - {self.selected_term}"
        )
        self.grid.clear_widgets()
        self.inputs = {}

        courses = CURRICULUM[self.selected_level][self.selected_term]
        saved_grades = (
            data_mgr.grades.get(self.selected_level, {})
            .get(self.selected_term, {})
        )

        for c in courses:
            row = BoxLayout(size_hint_y=None, height=40, spacing=5)
            lbl = Label(
                text=ar(f"{c['name']} ({c['hours']}س)"),
                font_name=FONT_NAME,
                font_size="14sp",
                size_hint_x=0.7,
            )
            inp = TextInput(
                text=str(saved_grades.get(c["name"], "")),
                font_name=FONT_NAME,
                multiline=False,
                input_filter="float",
                size_hint_x=0.3,
            )

            row.add_widget(lbl)
            row.add_widget(inp)
            self.grid.add_widget(row)
            self.inputs[c["name"]] = (inp, c["hours"])

        self.update_label()

    def calculate(self, instance):
        term_dict = {}
        for cname, (inp, hrs) in self.inputs.items():
            txt = inp.text.strip()
            if txt:
                try:
                    val = float(txt)
                    if 0 <= val <= 100:
                        term_dict[cname] = val
                    else:
                        Popup(
                            title=ar("خطأ"),
                            content=Label(
                                text=ar(
                                    f"الدرجة للمادة {cname} يجب أن تكون بين 0 و100"
                                ),
                                font_name=FONT_NAME,
                            ),
                            size_hint=(0.8, 0.4),
                        ).open()
                        return
                except ValueError:
                    pass

        if self.selected_level not in data_mgr.grades:
            data_mgr.grades[self.selected_level] = {}
        data_mgr.grades[self.selected_level][self.selected_term] = term_dict

        self.update_label()
        Popup(
            title=ar("تم الحساب"),
            content=Label(
                text=ar("تم الحساب وتحديث السجلات بنجاح!"),
                font_name=FONT_NAME,
            ),
            size_hint=(0.8, 0.4),
        ).open()

    def update_label(self):
        gpa, hrs = data_mgr.get_term_gpa(
            self.selected_level, self.selected_term
        )
        self.term_gpa_lbl.text = ar(
            f"معدل الترم: {gpa:.2f}% (إجمالي الساعات: {hrs})"
        )


class GPACalculatorApp(App):

    def build(self):
        # ربط الأيقونة
        if os.path.exists(ICON_PATH):
            self.icon = ICON_PATH

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(TermScreen(name="term"))
        sm.add_widget(GradeScreen(name="grade"))
        return sm


if __name__ == "__main__":
    GPACalculatorApp().run()
