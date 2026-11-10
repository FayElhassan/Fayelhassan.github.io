#!/usr/bin/env python3
"""Build the Arabic page (ar/index.html) from the English page (index.html).

Run from the repository root after editing index.html:

    python3 tools/build_ar.py

Text that has a translation below is swapped for Arabic; publication titles,
author lists and venues stay in English on purpose. Any new English text that
has no translation yet is listed at the end so it can be added to TEXT.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "index.html", ROOT / "ar" / "index.html"

# Exact text nodes: English -> Arabic (Modern Standard Arabic).
TEXT = {
    "Skip to content": "تخطَّ إلى المحتوى",
    "Research": "الأبحاث",
    "Publications": "المنشورات",
    "Projects": "المشاريع",
    "Community": "المجتمع",
    "Honours": "التكريمات",
    "Journey": "المسيرة",
    "CV": "السيرة الذاتية",
    "Participatory AI": "الذكاء الاصطناعي التشاركي",
    "Alignment &amp; Safety": "المواءمة والسلامة",
    "Clinical LLM Evaluation": "تقييم النماذج اللغوية في الطب",
    "AI for Global Health": "الذكاء الاصطناعي للصحة العالمية",
    "scroll": "مرِّر",
    "Read my work": "اقرأ أعمالي",
    "Get in touch": "تواصل معي",
    "Scholar": "Google Scholar",
    "Meroë pyramids · Kingdom of Kush": "أهرامات مروي · مملكة كوش",
    "Khartoum → Mbour → Tübingen → Lausanne": "الخرطوم ← مبور ← توبنغن ← لوزان",
    "Recently": "مستجدات",
    "What I work on": "ما أعمل عليه",
    "Participatory clinical evaluation": "التقييم السريري التشاركي",
    "Human-centred alignment &amp; safety": "مواءمة وسلامة محورها الإنسان",
    "Trustworthy &amp; open models": "نماذج موثوقة ومفتوحة",
    "Inspectable Bayesian reasoning, fully auditable open clinical LLMs, and watermarks embedded in model weights.":
        "استدلال بايزي قابل للفحص، ونماذج لغوية سريرية مفتوحة قابلة للتدقيق بالكامل، وعلامات مائية مدمجة في أوزان النماذج.",
    "Global health &amp; sustainability": "الصحة العالمية والاستدامة",
    "Papers &amp; preprints": "الأوراق والمسودات البحثية",
    "All": "الكل",
    "Clinical AI": "الذكاء الاصطناعي السريري",
    "Trustworthy ML": "تعلّم آلي موثوق",
    "Energy &amp; climate": "الطاقة والمناخ",
    "Research projects &amp; contributions": "المشاريع البحثية والإسهامات",
    "MOOVE: Massive Open Online Validation &amp; Evaluation": "MOOVE: منصة مفتوحة واسعة للتحقق والتقييم",
    "A participatory, clinician-in-the-loop platform for evaluating and aligning medical LLMs.":
        "منصة تشاركية يشارك فيها الأطباء في تقييم النماذج اللغوية الطبية ومواءمتها.",
    "Visit jointhemoove.org →": "زيارة jointhemoove.org ←",
    "A project of": "مشروع تابع لـ",
    "AI that reads antibiotic susceptibility tests in low-resource labs. I led the research in 2025.":
        "ذكاء اصطناعي يقرأ اختبارات حساسية المضادات الحيوية في المختبرات محدودة الموارد. قُدتُ البحث فيه عام 2025.",
    "Visit antibiogo.org →": "زيارة antibiogo.org ←",
    "MSF Foundation →": "مؤسسة أطباء بلا حدود ←",
    "Sankofa Initiative — STEM": "مبادرة سانكوفا — العلوم والتقنية",
    "Co-founded: culturally rooted STEM learning for children in underserved communities.":
        "شاركتُ في تأسيسها: تعليم للعلوم والتقنية متجذّر في ثقافة الأطفال في المجتمعات الأقل حظًا.",
    "Visit site →": "زيارة الموقع ←",
    "Multimodal weather forecasting with S4": "التنبؤ الجوي متعدد الوسائط باستخدام S4",
    "Contrastive self-supervised fusion of weather data with S4 sequence models.":
        "دمج بيانات الطقس بالتعلّم الذاتي التبايني باستخدام نماذج التسلسل S4.",
    "View code →": "عرض الشيفرة ←",
    "AI for sustainable agriculture": "الذكاء الاصطناعي للزراعة المستدامة",
    "PPO, A2C and SAC agents controlling a simulated tomato greenhouse.":
        "وكلاء PPO وA2C وSAC يتحكّمون في دفيئة طماطم محاكاة.",
    "DDPG &amp; TD3 in PyBullet": "DDPG وTD3 في PyBullet",
    "From-scratch JAX implementations for PyBullet robotics tasks.": "تنفيذ من الصفر بلغة JAX لمهام الروبوتات في PyBullet.",
    "LLM chatbots for data &amp; recommendations": "روبوتات محادثة بالنماذج اللغوية للبيانات والتوصيات",
    "A PostgreSQL LangChain chatbot and a hybrid recommender for AI coding assistants.":
        "روبوت محادثة مبني على PostgreSQL وLangChain، ونظام توصية هجين لمساعدي البرمجة بالذكاء الاصطناعي.",
    "Energy trading between microgrids": "تبادل الطاقة بين الشبكات الصغيرة",
    "Deep RL agents trading energy between off-grid villages in North Kordofan, Sudan. Became three IEEE papers.":
        "وكلاء تعلّم معزّز عميق يتبادلون الطاقة بين قرى غير متصلة بالشبكة في شمال كردفان بالسودان. نتجت عنه ثلاث أوراق في IEEE.",
    "Community &amp; talks": "المجتمع والمحاضرات",
    "Building rooms where more people belong": "نبني مساحات يجد فيها المزيد من الناس مكانهم",
    "Helping build the communities that made my own path possible.": "أساهم في بناء المجتمعات التي جعلت طريقي ممكنًا.",
    "University of Khartoum · 2022": "جامعة الخرطوم · 2022",
    "Women's Identity in Sudan": "هوية المرأة في السودان",
    "How social structures silence women's voices in Sudan and beyond, and what that costs.":
        "كيف تُسكِت البُنى الاجتماعية أصوات النساء في السودان وخارجه، وما ثمن ذلك.",
    "Watch on YouTube →": "شاهد على يوتيوب ←",
    "Leadership &amp; volunteering": "القيادة والتطوع",
    "IEEE Sudan": "IEEE السودان",
    "Chair · 2024–present": "الرئاسة · 2024 حتى الآن",
    "Co-founder and Chair of Communication &amp; Documentation · 2024–present": "مشاركة في التأسيس ورئاسة لجنة التواصل والتوثيق · 2024 حتى الآن",
    "Organiser for the main Indaba and adviser to IndabaX Sudan · 2022–25": "التنظيم في المؤتمر الرئيسي والاستشارة لـ IndabaX السودان · 2022–2025",
    "Co-founder of the Women in Machine Learning &amp; Data Science chapter · 2021–present": "مشاركة في تأسيس فرع «نساء في تعلّم الآلة وعلم البيانات» · 2021 حتى الآن",
    "Vice President": "نيابة الرئاسة",
    "Ambassador": "برنامج السفراء",
    "Talks &amp; panels": "المحاضرات والجلسات الحوارية",
    "TEDx University of Khartoum ·": "TEDx جامعة الخرطوم ·",
    "watch": "شاهد",
    "Teaching": "التدريس",
    "Teaching Assistant, University of Khartoum": "التدريس المساعد، جامعة الخرطوم",
    "Control system theory and computer-aided design for third- and fourth-year students": "نظرية أنظمة التحكّم والتصميم بمساعدة الحاسوب لطلاب السنتين الثالثة والرابعة",
    "Awards &amp; recognition": "الجوائز والتقدير",
    "Spotlight paper (top 5%)": "ورقة مميزة (أفضل 5%)",
    "ICLR 2026 ICBINB Workshop · Rio de Janeiro": "ورشة ICBINB في ICLR 2026 · ريو دي جانيرو",
    "EDIC Doctoral Fellowship": "زمالة الدكتوراه EDIC",
    "EPFL · 6–7% acceptance rate": "EPFL · نسبة قبول 6–7%",
    "CIFAR Inclusive AI Scholarship": "منحة CIFAR للذكاء الاصطناعي الشامل",
    "Canada": "كندا",
    "Positive Role Model Finalist": "الوصول إلى نهائيات جائزة القدوة الإيجابية",
    "12th Africa &amp; Middle East Gender Mainstreaming Awards": "الدورة الثانية عشرة لجوائز تعميم مراعاة النوع الاجتماعي في أفريقيا والشرق الأوسط",
    "AMMI Scholarship": "منحة AMMI",
    "AIMS Senegal, supported by Google &amp; Meta · 6% acceptance rate": "AIMS السنغال، بدعم من Google وMeta · نسبة قبول 6%",
    "Following the Nile": "على خُطى النيل",
    "From control systems in Khartoum to clinical AI in Lausanne. Scroll to sail downstream.":
        "من أنظمة التحكّم في الخرطوم إلى الذكاء الاصطناعي السريري في لوزان. مرِّر لتبحر مع التيار.",
    "Al-Mogran, Khartoum": "المقرن، الخرطوم",
    "Where the Blue and White Nile meet": "حيث يلتقي النيلان الأزرق والأبيض",
    "Khartoum": "الخرطوم",
    "B.Sc. (Hons) Electrical &amp; Electronic Engineering": "بكالوريوس الشرف في الهندسة الكهربائية والإلكترونية",
    "University of Khartoum": "جامعة الخرطوم",
    "Control systems, and my first RL papers on microgrids.": "أنظمة التحكّم، وأولى أوراقي في التعلّم المعزّز للشبكات الصغيرة.",
    "Data Scientist → BI Specialist → Project Manager": "علم البيانات ← ذكاء الأعمال ← إدارة المشاريع",
    "DAL Group": "مجموعة دال",
    "Forecasting, analytics and procurement automation.": "التنبؤ والتحليلات وأتمتة المشتريات.",
    "Remote": "عن بُعد",
    "ML Engineer · Principal Technical Lead": "هندسة تعلّم الآلة · القيادة التقنية",
    "LLM chatbots and AI pipelines.": "روبوتات محادثة بالنماذج اللغوية ومسارات عمل للذكاء الاصطناعي.",
    "Mbour, Senegal": "مبور، السنغال",
    "M.Sc. Mathematics, Machine Learning (AMMI)": "ماجستير الرياضيات، تخصص تعلّم الآلة (AMMI)",
    "African Institute for Mathematical Sciences": "المعهد الأفريقي للعلوم الرياضية",
    "Supported by Google and Meta.": "بدعم من Google وMeta.",
    "Tübingen, Germany": "توبنغن، ألمانيا",
    "Research Engineer": "هندسة الأبحاث",
    "Max Planck Institute for Intelligent Systems": "معهد ماكس بلانك للأنظمة الذكية",
    "LLM watermarking with Jonas Geiping and Antonio Orvieto.": "العلامات المائية للنماذج اللغوية مع يوناس غايبينغ وأنطونيو أورفييتو.",
    "Lausanne, Switzerland": "لوزان، سويسرا",
    "Master's Research Intern": "تدريب بحثي ضمن الماجستير",
    "LiGHT Lab · EPFL": "مختبر LiGHT · EPFL",
    "Antibiogo research with MSF.": "أبحاث Antibiogo مع أطباء بلا حدود.",
    "2025–now": "2025 حتى الآن",
    "PhD Student (EDIC), Doctoral Assistant": "الدكتوراه (EDIC) والمساعدة البحثية",
    "Research lead for MOOVE.": "قيادة الأبحاث في MOOVE.",
    "…and the river keeps flowing.": "…والنهر ما زال يجري.",
    "Certifications": "الشهادات المهنية",
    "Languages": "اللغات",
    "English · Arabic · French": "الإنجليزية · العربية · الفرنسية",
    "Let's talk": "لنتحدّث",
    "Research &amp; collaborations": "الأبحاث والتعاون",
    "I'm always glad to hear from people working on clinical AI evaluation, participatory design, or the alignment and safety of medical models, especially if you'd like to collaborate on MOOVE. Email is the best way to reach me.":
        "يسعدني دائمًا التواصل مع من يعملون على تقييم الذكاء الاصطناعي السريري، أو التصميم التشاركي، أو مواءمة النماذج الطبية وسلامتها، وخاصة من يرغب في التعاون في MOOVE. البريد الإلكتروني هو أفضل وسيلة للوصول إليّ.",
    "Students &amp; community": "الطلاب والمجتمع",
    "I've spent years mentoring through WiMLDS Khartoum, IEEE and the Deep Learning Indaba. If you're a student from Africa or anywhere else thinking about ML research, AMMI or a PhD, send me a short note about your background and what you'd like to work on.":
        "قضيتُ سنوات في الإرشاد عبر WiMLDS الخرطوم وIEEE وDeep Learning Indaba. إن كنتَ طالبًا أو طالبةً من أفريقيا أو من أي مكان آخر وتفكّر في أبحاث تعلّم الآلة أو AMMI أو الدكتوراه، فأرسل لي رسالة قصيرة عن خلفيتك وما تودّ العمل عليه.",
    "Download CV": "تحميل السيرة الذاتية",
    "Email": "البريد الإلكتروني",
    "Schedule a meeting": "حجز موعد",
    "Want to talk it through?": "تودّ أن نتحدّث؟",
    "Email me": "راسلني",
    "and we'll find a time.": "وسنجد وقتًا مناسبًا.",
    "Made with love from Sudan.": "صُنع بحبّ من السودان.",
    "Back to top ↑": "العودة للأعلى ↑",
    "Cookie settings": "إعدادات ملفات تعريف الارتباط",
    "University of Khartoum · 2022": "جامعة الخرطوم · 2022",
    "I Can't Believe It's Not Safer (spotlight talk)": "I Can't Believe It's Not Safer (عرض مميز)",
    "I Can't Believe It's Not Better (ICBINB) Workshop, ICLR 2026 · Rio de Janeiro, Brazil": "ورشة I Can't Believe It's Not Better (ICBINB)، ICLR 2026 · ريو دي جانيرو، البرازيل",
    "IEEE Region 8 Women in Engineering Panel": "جلسة IEEE Region 8 للنساء في الهندسة",
    "Panelist with Hazar Oklah and Dr. Neylan Tokerler · IEEE R8 Central European Students &amp; Young Professionals Congress (CEuSYP'25), Istanbul":
        "مشاركة في الجلسة مع هزار عقلة ود. نيلان توكرلر · مؤتمر IEEE R8 لطلاب وشباب وسط أوروبا (CEuSYP'25)، إسطنبول",
    "Student Branch Vitality: Administration, Programs &amp; Recognition": "حيوية الفروع الطلابية: الإدارة والبرامج والتقدير",
    "Panel, IEEE Region 8 SAC · IEEE R8 Student &amp; Young Professionals Congress (SYP), Grenoble, France":
        "جلسة حوارية، لجنة الأنشطة الطلابية في IEEE Region 8 · مؤتمر IEEE R8 للطلاب والشباب (SYP)، غرونوبل، فرنسا",
    "Embedding Subtle Watermarks in Large Language Models": "تضمين علامات مائية خفية في النماذج اللغوية الكبيرة",
    "CaCTüS Scientific Symposium, Max Planck Institute for Intelligent Systems · Tübingen": "ندوة CaCTüS العلمية، معهد ماكس بلانك للأنظمة الذكية · توبنغن",
    "AI for Sustainable Agriculture: Greenhouse Control Optimization": "الذكاء الاصطناعي للزراعة المستدامة: تحسين التحكّم في الدفيئات",
    "AMMI Scientific · Mbour, Senegal": "AMMI العلمي · مبور، السنغال",
    "An Introduction to Data Science": "مقدمة في علم البيانات",
    "Alzaiem Alazhari Computer Association · Khartoum": "جمعية الحاسوب بجامعة الزعيم الأزهري · الخرطوم",
    "How to turn your graduation project into a scientific paper": "كيف تحوّل مشروع تخرّجك إلى ورقة علمية",
    "Sudan University of Science &amp; Technology": "جامعة السودان للعلوم والتكنولوجيا",
    "Energy trading &amp; economic evaluation of islanded microgrids": "تبادل الطاقة والتقييم الاقتصادي للشبكات الصغيرة المعزولة",
    "Two paper presentations, ICCCEEE 2020 · Khartoum": "عرض ورقتين، ICCCEEE 2020 · الخرطوم",
    "Sankofa Initiative: STEM, What is in Hand? (IEEE Smart Village)": "مبادرة سانكوفا: العلوم والتقنية، ما في اليد؟ (IEEE Smart Village)",
    "IEEE Region 8 Student Activities Committee": "لجنة الأنشطة الطلابية في IEEE Region 8",
    "Arab Women in Computing (ArabWIC)": "النساء العربيات في الحوسبة (ArabWIC)",
    "WiMLDS Khartoum": "WiMLDS الخرطوم",
    "Blue Nile": "النيل الأزرق",
    "White Nile": "النيل الأبيض",
    "Al-Mogran · Khartoum": "المقرن · الخرطوم",
    "River Nile": "نهر النيل",
}

# Whole blocks that contain inline markup.
BLOCKS = [
    (r'<p class="me-bubble" role="status">.*?</p>',
     '<p class="me-bubble" role="status">أهلاً وسهلاً!</p>'),
    (r'<h2 class="hero-title">.*?</h2>',
     '<h2 class="hero-title">ذكاءٌ اصطناعيٌّ آمنٌ ومتوائم، يُصاغ <em>مع</em> الناس الذين يخدمهم.</h2>'),
    (r'<p class="lede">.*?</p>',
     '<p class="lede">أنا فيء (Fay) ماجد، أُعِدّ الدكتوراه في علوم الحاسوب والاتصالات (EDIC) في '
     '<a href="https://www.light-laboratory.org/">مختبر LiGHT</a> بقيادة البروفيسورة ماري-آن هارتلي في EPFL. '
     'أستخدم <b>التصميم التشاركي</b> لإشراك الأطباء في <b>مواءمة الذكاء الاصطناعي وسلامته</b>، ويكون التقييم جزءًا من الحلقة نفسها: '
     'فأحكام الخبراء التي تختبر النموذج تُرشدنا أيضًا إلى كيفية مواءمته. أقود الأبحاث في '
     '<a href="https://jointhemoove.org/"><b>MOOVE</b></a>.</p>'),
    (r'<ul class="news-list">.*?</ul>',
     '<ul class="news-list">\n'
     '    <li><time>2026</time><span>قُبلت ورقة <strong>MoBayes</strong> في <strong>المسار الرئيسي لمؤتمر NeurIPS 2026</strong> (بتأليف أول مشترك).</span></li>\n'
     '    <li><time>2026</time><span>نُشر بروتوكول <strong>hypMOOVE-PHC</strong> على medRxiv.</span></li>\n'
     '  </ul>'),
    (r'<p>Practising clinicians, not crowdworkers or AI judges, rate LLM answers to realistic cases on <a href="https://jointhemoove.org/"><b>MOOVE</b></a>, blind to the model\. They define what a good answer is; I turn their judgements into rankings and consensus\.</p>',
     '<p>يقيّم أطباء ممارسون، لا عمّال حشد ولا نماذج حَكَمة، إجابات النماذج اللغوية على حالات واقعية عبر <a href="https://jointhemoove.org/"><b>MOOVE</b></a> دون معرفة النموذج. هم من يحدّد ما الإجابة الجيدة، وأنا أحوّل أحكامهم إلى تصنيفات وإجماع.</p>'),
    (r'<p>The answer clinicians prefer isn\'t always the safest\..*?\(<a href="#publications">ICLR 2026 spotlight</a>\)\.</p>',
     '<p>الإجابة التي يفضّلها الأطباء ليست دائمًا الأكثر أمانًا. من 18,685 تصويتًا ثنائيًا أعمى أدلى بها 736 طبيبًا في أكثر من 28 دولة على 13 نموذجًا، وجدنا أن تصنيفات التفضيل لا تعكس السلامة بشكل موثوق، لذا أبني تصنيفات تعيد السلامة السريرية إلى الصدارة (<a href="#publications">عرض مميز في ICLR 2026</a>).</p>'),
    (r'<p>Previously led <a href="https://www.antibiogo.org/"><b>Antibiogo</b></a> research with MSF\. Earlier work: deep RL for microgrids in rural Sudan, greenhouse control and weather forecasting\.</p>',
     '<p>قُدتُ سابقًا أبحاث <a href="https://www.antibiogo.org/"><b>Antibiogo</b></a> مع أطباء بلا حدود. ومن أعمالي الأقدم: التعلّم المعزّز العميق للشبكات الصغيرة في ريف السودان، والتحكّم في الدفيئات، والتنبؤ الجوي.</p>'),
    (r'<p class="section-sub">\* marks equal contribution\. Full list on (<a [^>]+>)Google Scholar</a>\.</p>',
     r'<p class="section-sub">تشير * إلى مساهمة متساوية. القائمة الكاملة على \1Google Scholar</a>.</p>'),
    (r'<span>Communication &amp; Publicity Coordinator \(2025–26\) and past Chair of Digital Communications \(2024–25\)\. I designed and built the <a href="([^"]+)">R8 SAC website</a>\.</span>',
     r'<span>تنسيق التواصل والإعلام (2025–2026) ورئاسة سابقة للتواصل الرقمي (2024–2025). صمّمتُ وبنيتُ <a href="\1">موقع R8 SAC</a>.</span>'),
]

TAGS = {  # small labels ("tag" lines on project cards)
    "Research lead · LiGHT, EPFL · 2025–": "قيادة الأبحاث · LiGHT، EPFL · 2025–",
    "Past research lead · with Médecins Sans Frontières · 2025": "قيادة بحثية سابقة · مع أطباء بلا حدود · 2025",
    "Education · IEEE Smart Village · 2024–": "التعليم · IEEE Smart Village · 2024–",
    "Self-supervised learning · Climate · 2023–24": "التعلّم الذاتي · المناخ · 2023–2024",
    "Reinforcement learning · Agriculture · 2023": "التعلّم المعزّز · الزراعة · 2023",
    "Deep RL · Robotics · JAX · 2023": "التعلّم المعزّز العميق · الروبوتات · JAX · 2023",
    "LLMs · NLP · 2023": "النماذج اللغوية · معالجة اللغة · 2023",
    "Deep RL · Energy · 2018–20": "التعلّم المعزّز العميق · الطاقة · 2018–2020",
}

ATTRS = [  # attribute text
    ('data-label="publications"', 'data-label="منشورات"'),
    ('data-more="Show earlier projects"', 'data-more="عرض المشاريع الأقدم"'),
    ('data-label="talks &amp; panels"', 'data-label="محاضرات والجلسات"'),
    ('aria-label="Research areas"', 'aria-label="مجالات البحث"'),
    ('aria-label="Scroll to read more"', 'aria-label="مرّر لقراءة المزيد"'),
    ('aria-label="Fay waving hello"', 'aria-label="تحية من فيء"'),
    ('aria-label="Open menu"', 'aria-label="فتح القائمة"'),
    ('aria-label="Toggle dark mode" title="Toggle dark mode"', 'aria-label="تبديل الوضع الليلي" title="تبديل الوضع الليلي"'),
    ('aria-label="Profiles"', 'aria-label="الحسابات"'),
    ('alt="Fay Elhassan smiling at sunset by the sea"', 'alt="صورة فيء عند الغروب على شاطئ البحر"'),
    ('title="Colours of Kerma black-topped red pottery, Kingdom of Kush"', 'title="ألوان فخار كرمة الأحمر ذي الحافة السوداء، مملكة كوش"'),
]

HEAD = [
    ('<html lang="en">', '<html lang="ar" dir="rtl">'),
    ('<title>Fay Elhassan — PhD Student, EPFL</title>', '<title>فيء ماجد — الدكتوراه في EPFL</title>'),
]


def build():
    s = SRC.read_text(encoding="utf-8")
    for a, b in HEAD:
        s = s.replace(a, b, 1)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="فيء ماجد، مختبر LiGHT في EPFL: التصميم التشاركي لإشراك الأطباء والمجتمعات في مواءمة الذكاء الاصطناعي السريري وسلامته.">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               '<meta property="og:description" content="التصميم التشاركي لمواءمة الذكاء الاصطناعي وسلامته، مع التقييم البشري في صميم العملية. NeurIPS 2026، عرض مميز في ICLR 2026.">', s, count=1)
    s = s.replace('<link rel="canonical" href="https://fayelhassan.github.io/">',
                  '<link rel="canonical" href="https://fayelhassan.github.io/ar/">', 1)
    # Arabic fonts
    s = s.replace('<link rel="stylesheet" href="assets/site.css',
                  '<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">\n'
                  '<link rel="stylesheet" href="assets/site.css', 1)
    # relative paths one level down
    s = re.sub(r'(href|src)="(assets|images|files)/', r'\1="../\2/', s)
    s = s.replace('href="/images/', 'href="../images/')
    # language switch points back to English
    s = re.sub(r'<a class="lang-switch" href="ar/" hreflang="ar" lang="ar" title="[^"]*">(<svg.*?</svg>)<span>العربية</span></a>',
               r'<a class="lang-switch" href="../" hreflang="en" lang="en" title="Read in English · اقرأ بالإنجليزية">\1<span>English</span></a>', s, count=1, flags=re.S)
    # blocks with markup
    for pat, rep in BLOCKS:
        s, n = re.subn(pat, rep, s, count=1, flags=re.S)
        if not n:
            print("block not found:", pat[:60], file=sys.stderr)
    for a, b in ATTRS:
        s = s.replace(a, b)
    for en, ar in TAGS.items():
        s = s.replace(f'<p class="tag">{en}</p>', f'<p class="tag">{ar}</p>')
    # publications stay in English, laid out left-to-right
    s = s.replace('<ol class="pubs"', '<ol class="pubs" dir="ltr" lang="en"', 1)
    # exact text nodes (outside the publications list)
    a = s.index('<ol class="pubs"'); b = s.index('</ol>', a)
    head, pubs, tail = s[:a], s[a:b], s[b:]
    def swap(part):
        for en, ar in TEXT.items():
            part = re.sub(r">(\s*)" + re.escape(en) + r"(\s*)<", lambda m: ">" + m.group(1) + ar + m.group(2) + "<", part)
        return part
    s = swap(head) + pubs + swap(tail)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(s, encoding="utf-8")
    # report English text still left outside publications / proper names
    body = re.sub(r"<svg.*?</svg>|<script.*?</script>|<ol class=\"pubs\".*?</ol>", "", s[s.index("<body"):], flags=re.S)
    left = []
    for t in re.findall(r">([^<>]*[A-Za-z]{3,}[^<>]*)<", body):
        t = t.strip()
        if t and not re.search(r"[؀-ۿ]", t) and t not in left:
            left.append(t)
    print(f"wrote {OUT.relative_to(ROOT)}; English text kept ({len(left)}):")
    for t in left:
        print("  ", html.unescape(t))


if __name__ == "__main__":
    build()
