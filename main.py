import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

# ---------------------------------------------------------
# 1. الخطة الدراسية مع عدد الساعات المعتمدة لكل مادة
# ---------------------------------------------------------
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
            {"name": "التصميم بمساعدة الحاسوب (CAD)", "hours": 3},
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
            {"name": "التصنيع بمساعدة الحاسوب (CAM)", "hours": 4},
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


class AcademicGPACalculator:

    def __init__(self, root):
        self.root = root
        self.root.title("نظام حساب المعدل الأكاديمي - الهندسة الصناعية")
        self.root.geometry("550x650")
        self.root.configure(bg="#f4f6f9")

        # بيانات الطالب المحفوظة
        self.student_name = ""
        self.grades_data = {}

        # الحالة الحالية للملاحة
        self.selected_level = None
        self.selected_term = None
        self.entries = {}

        self.setup_main_frame()
        self.show_screen_1()

    def setup_main_frame(self):
        # الهيكل العام للواجهة
        self.header_frame = tk.Frame(self.root, bg="#1e293b", py=10)
        self.header_frame.pack(fill="x")

        self.title_label = tk.Label(
            self.header_frame,
            text="حاسبة المعدل الأكاديمي",
            fg="white",
            bg="#1e293b",
            font=("Arial", 16, "bold"),
        )
        self.title_label.pack()

        # إدخال اسم الشخص
        self.profile_frame = tk.Frame(self.root, bg="#f4f6f9", py=5)
        self.profile_frame.pack(fill="x", px=15)

        tk.Label(
            self.profile_frame,
            text="اسم الطالب:",
            font=("Arial", 11),
            bg="#f4f6f9",
        ).pack(side="right")
        self.name_entry = tk.Entry(
            self.profile_frame, font=("Arial", 11), width=20
        )
        self.name_entry.pack(side="right", px=5)

        tk.Button(
            self.profile_frame,
            text="حفظ البيانات",
            bg="#10b981",
            fg="white",
            command=self.save_data,
        ).pack(side="left", px=2)
        tk.Button(
            self.profile_frame,
            text="تحميل البيانات",
            bg="#3b82f6",
            fg="white",
            command=self.load_data,
        ).pack(side="left", px=2)

        self.container = tk.Frame(self.root, bg="#f4f6f9")
        self.container.pack(fill="both", expand=True, px=20, py=10)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # الشاشة الأولى: اختيار المستوى + المعدل التراكمي الكلي
    # ---------------------------------------------------------
    def show_screen_1(self):
        self.clear_container()

        tk.Label(
            self.container,
            text="اختر المستوى الدراسي:",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9",
        ).pack(py=10)

        for level in CURRICULUM.keys():
            btn = tk.Button(
                self.container,
                text=level,
                font=("Arial", 12),
                bg="#ffffff",
                fg="#1e293b",
                height=2,
                relief="groove",
                command=lambda l=level: self.select_level(l),
            )
            btn.pack(fill="x", py=5)

        # عرض المعدل التراكمي لجميع السنين
        overall_gpa, total_hrs = self.calculate_overall_gpa()
        gpa_card = tk.Frame(
            self.container,
            bg="#e2e8f0",
            py=15,
            highlightbackground="#cbd5e1",
            highlightthickness=1,
        )
        gpa_card.pack(fill="x", side="bottom", py=15)

        tk.Label(
            gpa_card,
            text=f"المعدل التراكمي الكلي لجميع السنين: {overall_gpa:.2f}%",
            font=("Arial", 13, "bold"),
            bg="#e2e8f0",
            fg="#0f172a",
        ).pack()
        tk.Label(
            gpa_card,
            text=f"إجمالي الساعات المكتسبة: {total_hrs} ساعة",
            font=("Arial", 10),
            bg="#e2e8f0",
            fg="#475569",
        ).pack()

    def select_level(self, level):
        self.selected_level = level
        self.show_screen_2()

    # ---------------------------------------------------------
    # الشاشة الثانية: اختيار الترم + معدل السنة
    # ---------------------------------------------------------
    def show_screen_2(self):
        self.clear_container()

        tk.Label(
            self.container,
            text=f"{self.selected_level} - اختر الترم:",
            font=("Arial", 14, "bold"),
            bg="#f4f6f9",
        ).pack(py=10)

        for term in CURRICULUM[self.selected_level].keys():
            btn = tk.Button(
                self.container,
                text=term,
                font=("Arial", 12),
                bg="#ffffff",
                fg="#1e293b",
                height=2,
                relief="groove",
                command=lambda t=term: self.select_term(t),
            )
            btn.pack(fill="x", py=8)

        # عرض معدل السنة المختارة
        year_gpa, year_hrs = self.calculate_year_gpa(self.selected_level)
        year_card = tk.Frame(
            self.container,
            bg="#e2e8f0",
            py=15,
            highlightbackground="#cbd5e1",
            highlightthickness=1,
        )
        year_card.pack(fill="x", side="bottom", py=15)

        tk.Label(
            year_card,
            text=f"معدل {self.selected_level}: {year_gpa:.2f}%",
            font=("Arial", 13, "bold"),
            bg="#e2e8f0",
            fg="#0f172a",
        ).pack()
        tk.Label(
            year_card,
            text=f"ساعات السنة: {year_hrs} ساعة",
            font=("Arial", 10),
            bg="#e2e8f0",
            fg="#475569",
        ).pack()

        # زر الرجوع
        tk.Button(
            self.container,
            text="← رجوع للقائمة الرئيسية",
            bg="#64748b",
            fg="white",
            command=self.show_screen_1,
        ).pack(side="bottom", anchor="w", py=5)

    def select_term(self, term):
        self.selected_term = term
        self.show_screen_3()

    # ---------------------------------------------------------
    # الشاشة الثالثة: إدخال درجات المواد وحساب معدل الترم
    # ---------------------------------------------------------
    def show_screen_3(self):
        self.clear_container()

        tk.Label(
            self.container,
            text=f"{self.selected_level} - {self.selected_term}",
            font=("Arial", 13, "bold"),
            bg="#f4f6f9",
        ).pack(py=5)
        tk.Label(
            self.container,
            text="أدخل الدرجة (من 100) مقابل كل مادة:",
            font=("Arial", 10),
            bg="#f4f6f9",
            fg="#64748b",
        ).pack(py=2)

        scroll_frame = tk.Frame(self.container, bg="#f4f6f9")
        scroll_frame.pack(fill="both", expand=True, py=5)

        self.entries = {}
        courses = CURRICULUM[self.selected_level][self.selected_term]

        for course in courses:
            row = tk.Frame(scroll_frame, bg="#ffffff", py=5, px=5)
            row.pack(fill="x", py=3)

            lbl_text = f"{course['name']} ({course['hours']} س)"
            tk.Label(
                row,
                text=lbl_text,
                font=("Arial", 10),
                bg="#ffffff",
                anchor="e",
            ).pack(side="right", fill="x", expand=True)

            ent = tk.Entry(row, font=("Arial", 10), width=8, justify="center")
            ent.pack(side="left", px=5)

            # ملء الدرجة المسبقة إن وجدت
            existing_grade = (
                self.grades_data.get(self.selected_level, {})
                .get(self.selected_term, {})
                .get(course["name"], "")
            )
            if existing_grade != "":
                ent.insert(0, str(existing_grade))

            self.entries[course["name"]] = (ent, course["hours"])

        # زر الحساب
        tk.Button(
            self.container,
            text="احسب معدل الترم",
            bg="#2563eb",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.process_term_calculation,
        ).pack(fill="x", py=8)

        # بطاقة النتيجة
        self.term_result_label = tk.Label(
            self.container,
            text="معدل الترم: -- %",
            font=("Arial", 12, "bold"),
            bg="#f4f6f9",
            fg="#1e293b",
        )
        self.term_result_label.pack(py=2)

        # حساب النتيجة الحالية إن كانت مدخلة
        self.update_term_label()

        # زر الرجوع للترمات
        tk.Button(
            self.container,
            text="← رجوع لقائمة الفصل",
            bg="#64748b",
            fg="white",
            command=self.show_screen_2,
        ).pack(side="bottom", anchor="w", py=5)

    def process_term_calculation(self):
        term_grades = {}
        for cname, (ent, hrs) in self.entries.items():
            val = ent.get().strip()
            if val != "":
                try:
                    score = float(val)
                    if 0 <= score <= 100:
                        term_grades[cname] = score
                    else:
                        messagebox.showwarning(
                            "خطأ", f"الدرجة للمادة {cname} يجب أن تكون بين 0 و 100"
                        )
                        return
                except ValueError:
                    messagebox.showerror(
                        "خطأ", f"قيمة غير صحيحة للمادة {cname}"
                    )
                    return

        # حفظ الدرجات الحالية في الذاكرة
        if self.selected_level not in self.grades_data:
            self.grades_data[self.selected_level] = {}
        self.grades_data[self.selected_level][
            self.selected_term
        ] = term_grades

        self.update_term_label()
        messagebox.showinfo("تم الحساب", "تم حساب وتحديث درجات الترم بنجاح!")

    def update_term_label(self):
        gpa, hrs = self.calculate_term_gpa(
            self.selected_level, self.selected_term
        )
        if hrs > 0:
            self.term_result_label.config(
                text=f"معدل الترم: {gpa:.2f}% ({hrs} ساعة)"
            )
        else:
            self.term_result_label.config(text="معدل الترم: -- %")

    # ---------------------------------------------------------
    # 2. معادلات الحساب (المعدل الموزون بالساعات)
    # ---------------------------------------------------------
    def calculate_term_gpa(self, level, term):
        courses = CURRICULUM.get(level, {}).get(term, [])
        saved_scores = self.grades_data.get(level, {}).get(term, {})

        total_points = 0.0
        total_hours = 0

        for c in courses:
            cname = c["name"]
            chrs = c["hours"]
            if cname in saved_scores:
                score = saved_scores[cname]
                total_points += score * chrs
                total_hours += chrs

        gpa = (total_points / total_hours) if total_hours > 0 else 0.0
        return gpa, total_hours

    def calculate_year_gpa(self, level):
        total_points = 0.0
        total_hours = 0

        for term in ["الفصل الأول", "الفصل الثاني"]:
            gpa, hrs = self.calculate_term_gpa(level, term)
            total_points += gpa * hrs
            total_hours += hrs

        year_gpa = (total_points / total_hours) if total_hours > 0 else 0.0
        return year_gpa, total_hours

    def calculate_overall_gpa(self):
        total_points = 0.0
        total_hours = 0

        for level in CURRICULUM.keys():
            gpa, hrs = self.calculate_year_gpa(level)
            total_points += gpa * hrs
            total_hours += hrs

        overall_gpa = (total_points / total_hours) if total_hours > 0 else 0.0
        return overall_gpa, total_hours

    # ---------------------------------------------------------
    # 3. حفظ واسترجاع البيانات باسم الشخص (JSON)
    # ---------------------------------------------------------
    def save_data(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning(
                "تنبيه", "يرجى كتابة اسم الشخص أولاً لحفظ البيانات باسمه!"
            )
            return

        file_name = f"{name}_data.json"
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(self.grades_data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo(
                "نجاح", f"تم حفظ درجات {name} بنجاح في الملف {file_name}"
            )
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر حفظ الملف: {str(e)}")

    def load_data(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning(
                "تنبيه", "يرجى كتابة اسم الشخص لتحميل بياناته!"
            )
            return

        file_name = f"{name}_data.json"
        if not os.path.exists(file_name):
            messagebox.showerror(
                "خطأ", f"لم يتم العثور على ملف سجلات باسم {name}"
            )
            return

        try:
            with open(file_name, "r", encoding="utf-8") as f:
                self.grades_data = json.load(f)
            messagebox.showinfo("نجاح", f"تم تحميل درجات {name} بنجاح!")
            self.show_screen_1()
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تحميل البيانات: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicGPACalculator(root)
    root.mainloop()
