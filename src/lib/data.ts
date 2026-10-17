/**
 * ─────────────────────────────────────────────────────────────────
 *  SINGLE SOURCE OF CONTENT — every value below is traced to the
 *  résumé (assets/documents/Mohammed_Shehzad_Khan_CV.pdf, v1.2).
 *  Nothing is fabricated. If it is not in the résumé, it is not here.
 * ─────────────────────────────────────────────────────────────────
 */

/** Prefix for hand-referenced files in /public (repo deploys at /mo-portfolio-v2/). */
export const ASSET = (p: string) => `/mo-portfolio-v2${p.startsWith("/") ? "" : "/"}${p}`;

export interface Profile {
  name: string;
  firstName: string;      // ghost word + signature
  initials: string;       // navigation mark
  role: string;           // exact résumé headline
  email: string;
  phone: string;
  phoneHref: string;
  location: string;
  resumeSummary: string;  // verbatim from the résumé
  summaryExtraLine: string;
  linkedin: string;
  linkedinLabel: string;
  portfolio: string;
  resumePath: string;
  availableFrom: string;  // availability line from the summary
}

export const PROFILE: Profile = {
  name: "Mohammed Shehzad Khan",
  firstName: "Mohammed",
  initials: "MSK",
  role: "International Primary EAL Educator",
  email: "mdshezkhn@hotmail.com",
  phone: "+86-131 3771 9002",
  phoneHref: "+8613137719002",
  location: "Zhengzhou, China",
  resumeSummary:
    "International Primary EAL educator with more than 10 years of experience supporting multilingual learners across India and China. Experienced in combining evidence-informed classroom practice with teacher development and instructional quality improvement, underpinned by postgraduate practitioner research in dialogic teaching and participation equity.",
  summaryExtraLine:
    "Practitioner research: questioning strategies and participation equity in bilingual primary classrooms.",
  linkedin: "https://www.linkedin.com/in/mdshezkhn",
  linkedinLabel: "LinkedIn",
  portfolio: "https://mdshezkhn.github.io/mo-portfolio-v2/",
  resumePath: "/resume/Mohammed_Shehzad_Khan_CV.pdf",
  availableFrom: "Available for primary teaching and instructional leadership opportunities from August 2027.",
};

/* ── Navigation ─────────────────────────────────────────────────── */

export interface NavItem { id: string; label: string; index: string; }

export const NAV: NavItem[] = [
  { id: "about",         label: "About",         index: "01" },
  { id: "skills",        label: "Skills",        index: "02" },
  { id: "work",          label: "Work",          index: "03" },
  { id: "experience",    label: "Experience",    index: "04" },
  { id: "achievements",  label: "Achievements",  index: "05" },
  { id: "contact",       label: "Contact",       index: "06" },
];

/* ── Skills — "the periodic table of my stack" ──────────────────── */

export type SkillFamily =
  | "Teaching & Learning"
  | "Curriculum & Leadership"
  | "Research & Evidence"
  | "Digital & Learning Technologies"
  | "Languages";

export interface Skill {
  symbol: string;         // 2-letter "element" symbol
  name: string;
  family: SkillFamily;
  logo?: string;          // brand key (public/logos/<key>.svg) — tech only
  note?: string;          // proficiency line for languages (from résumé)
}

export const SKILL_GROUPS: { family: SkillFamily; caption: string; skills: Skill[] }[] = [
  {
    family: "Teaching & Learning",
    caption: "Primary EAL · Multilingual Education · Differentiated Instruction · Formative Assessment · Literacy Development · Classroom Management",
    skills: [
      { symbol: "Ea", name: "Primary EAL", family: "Teaching & Learning" },
      { symbol: "Me", name: "Multilingual Education", family: "Teaching & Learning" },
      { symbol: "Di", name: "Differentiated Instruction", family: "Teaching & Learning" },
      { symbol: "Fa", name: "Formative Assessment", family: "Teaching & Learning" },
      { symbol: "Ld", name: "Literacy Development", family: "Teaching & Learning" },
      { symbol: "Cm", name: "Classroom Management", family: "Teaching & Learning" },
    ],
  },
  {
    family: "Curriculum & Leadership",
    caption: "Curriculum Design · Teacher Mentoring · Professional Development · Instructional Quality Assurance · Assessment Moderation",
    skills: [
      { symbol: "Cd", name: "Curriculum Design", family: "Curriculum & Leadership" },
      { symbol: "Tm", name: "Teacher Mentoring", family: "Curriculum & Leadership" },
      { symbol: "Pd", name: "Professional Development", family: "Curriculum & Leadership" },
      { symbol: "Qa", name: "Instructional Quality Assurance", family: "Curriculum & Leadership" },
      { symbol: "Am", name: "Assessment Moderation", family: "Curriculum & Leadership" },
    ],
  },
  {
    family: "Research & Evidence",
    caption: "Dialogic Teaching · Questioning Strategies · Translanguaging · Practitioner Research · Evidence-Informed Practice",
    skills: [
      { symbol: "Dt", name: "Dialogic Teaching", family: "Research & Evidence" },
      { symbol: "Qs", name: "Questioning Strategies", family: "Research & Evidence" },
      { symbol: "Tr", name: "Translanguaging", family: "Research & Evidence" },
      { symbol: "Pr", name: "Practitioner Research", family: "Research & Evidence" },
      { symbol: "Ep", name: "Evidence-Informed Practice", family: "Research & Evidence" },
    ],
  },
  {
    family: "Digital & Learning Technologies",
    caption: "Google Workspace · Microsoft 365 · Moodle · Canvas · Zoom · OBS Studio",
    skills: [
      { symbol: "Gw", name: "Google Workspace",  family: "Digital & Learning Technologies", logo: "google" },
      { symbol: "Ms", name: "Microsoft 365",     family: "Digital & Learning Technologies", logo: "microsoft" },
      { symbol: "Mo", name: "Moodle",            family: "Digital & Learning Technologies", logo: "moodle" },
      { symbol: "Cv", name: "Canvas",            family: "Digital & Learning Technologies", logo: "canvas" },
      { symbol: "Zm", name: "Zoom",              family: "Digital & Learning Technologies", logo: "zoom" },
      { symbol: "Ob", name: "OBS Studio",        family: "Digital & Learning Technologies", logo: "obsstudio" },
    ],
  },
  {
    family: "Languages",
    caption: "English · Hindi · Urdu · Marathi · Arabic · Mandarin Chinese",
    skills: [
      { symbol: "En", name: "English",          family: "Languages", note: "Fluent" },
      { symbol: "Hi", name: "Hindi",            family: "Languages", note: "Native" },
      { symbol: "Ur", name: "Urdu",             family: "Languages", note: "Professional Working" },
      { symbol: "Ma", name: "Marathi",          family: "Languages", note: "Limited Working" },
      { symbol: "Ar", name: "Arabic",           family: "Languages", note: "Elementary Reading" },
      { symbol: "Zh", name: "Mandarin Chinese", family: "Languages", note: "Basic Conversation" },
    ],
  },
];

export const ALL_SKILLS: Skill[] = SKILL_GROUPS.flatMap((g) => g.skills);

/* ── Work — accordion gallery (résumé: Selected Leadership Contributions) ── */

export interface Project {
  id: string;
  index: string;
  kicker: string;         // organisation · role (from résumé)
  title: string;
  description: string;    // résumé wording (publication-policy safe)
  features: string[];     // 2-column list, from the résumé bullets
  tech: string[];         // skills used (all exist above)
  github?: string;        // only when a link exists in the résumé — none do
  ui: "workshops" | "programmes" | "mentoring" | "moderation" | "demos";
}

export const PROJECTS: Project[] = [
  {
    id: "intl-workshops",
    index: "01",
    kicker: "GEDU Global Education · Training & Quality Lead",
    title: "International Pedagogical Workshops",
    description:
      "Developed and delivered professional development programmes and bespoke pedagogical workshops for international trainers across campuses in the UK, Dubai and Malta.",
    features: [
      "PD programmes across UK, Dubai & Malta campuses",
      "Bespoke workshops on rigorous assessment practices",
      "Quality assurance frameworks for instructional consistency",
      "Mentoring of trainers in pedagogical practice",
    ],
    tech: ["Professional Development", "Assessment Moderation", "Instructional Quality Assurance"],
    ui: "workshops",
  },
  {
    id: "training-programmes",
    index: "02",
    kicker: "WhiteHat Jr (BYJU'S) · Teacher Quality & Development",
    title: "Teacher Training Programmes",
    description:
      "Created teacher training programmes and curriculum resources for distributed teaching teams, strengthening instructional quality through coaching, observation and evidence-informed professional learning.",
    features: [
      "Coaching & quality assurance for distributed teams",
      "Classroom observations & LMS analytics insight",
      "Targeted PD on assessment practices",
      "Curriculum resources for teaching teams",
    ],
    tech: ["Teacher Mentoring", "Curriculum Design", "Evidence-Informed Practice"],
    ui: "programmes",
  },
  {
    id: "mentoring",
    index: "03",
    kicker: "Aoxin International School · EAL / English Teacher",
    title: "Early-Career Teacher Mentoring",
    description:
      "Mentored newly appointed teachers through induction and professional growth plans, supporting their successful integration and maintaining instructional quality.",
    features: [
      "Induction support for new teachers",
      "Professional growth planning",
      "Instructional quality maintained through integration",
      "Collaboration with Chinese co-teaching teams",
    ],
    tech: ["Teacher Mentoring", "Classroom Management", "Differentiated Instruction"],
    ui: "mentoring",
  },
  {
    id: "moderation",
    index: "04",
    kicker: "Aoxin International School · EAL / English Teacher",
    title: "Grade 5 Writing Moderation",
    description:
      "Directed Grade 5 writing moderation across multiple teaching teams, ensuring consistent assessment standards.",
    features: [
      "Moderation across multiple teaching teams",
      "Consistent assessment standards",
      "Formative assessment tracking",
      "Detailed written feedback to families",
    ],
    tech: ["Assessment Moderation", "Formative Assessment"],
    ui: "moderation",
  },
  {
    id: "demo-lessons",
    index: "05",
    kicker: "Eton House Kindergarten · ESL Teacher & Teacher Trainer",
    title: "Demonstration Lessons & Coaching",
    description:
      "Delivered demonstration lessons and pedagogical coaching for kindergarten ESL staff, strengthening early-years ESL practice through age-appropriate communicative activities.",
    features: [
      "Demonstration lessons for ESL staff",
      "Early-years immersive ESL instruction",
      "Age-appropriate communicative activities",
      "Colleague coaching & practice modelling",
    ],
    tech: ["Primary EAL", "Literacy Development", "Multilingual Education"],
    ui: "demos",
  },
];

/* ── Certifications — ink-flood index ───────────────────────────── */

export interface Certification { title: string; issuer: string; }

export const CERTIFICATIONS: Certification[] = [
  { title: "TESOL Certification (240 hours)", issuer: "Global TESOL College, Canada" },
  { title: "TEFL Certification (120 hours)", issuer: "Teacher Record" },
  { title: "Professional Development Certificates — Primary Education and Language Teaching", issuer: "British Council" },
];

/* ── Experience — education + employment as one path ────────────── */

export interface Stop {
  years: string;
  title: string;
  place: string;
  detail: string;
  kind: "work" | "education";
}

export const EXPERIENCE: Stop[] = [
  { years: "2024 — Present", title: "EAL / English Teacher", place: "Aoxin International School · Zhengzhou, China", detail: "Differentiated, curriculum-aligned EAL instruction for multilingual learners in Years 1–6, with formative assessment and evidence-informed questioning.", kind: "work" },
  { years: "2025 — 2026", title: "PGCE · Master's level (PGCE7002)", place: "University of Cumbria, UK", detail: "Postgraduate Certificate in Education with practitioner research into questioning strategies and participation equity.", kind: "education" },
  { years: "2022 — 2023", title: "Training & Quality Lead", place: "GEDU Global Education · UK, Dubai, Malta", detail: "Professional development programmes, trainer mentoring and quality assurance frameworks across international campuses.", kind: "work" },
  { years: "2022 — 2024", title: "Bachelor of Education (B.Ed.)", place: "University of Kashmir", detail: "Undergraduate education degree alongside full-time international teaching.", kind: "education" },
  { years: "2020 — 2022", title: "Assistant Manager — Teacher Quality & Development", place: "WhiteHat Jr (BYJU'S) · India (Remote)", detail: "Coaching, quality assurance and evidence-informed professional learning for distributed teaching teams.", kind: "work" },
  { years: "2018 — 2020", title: "EAL / English Teacher", place: "Aoxin International School · Zhengzhou, China", detail: "Foundational EAL for primary and lower-secondary learners; Grade 5 writing moderation; mentoring of new teachers.", kind: "work" },
  { years: "2017 — 2018", title: "ESL Teacher & Teacher Trainer (Early Years)", place: "Eton House Kindergarten · China", detail: "Immersive ESL for kindergarten learners; demonstration lessons and colleague mentoring.", kind: "work" },
  { years: "2016 — 2017", title: "ESL Teacher", place: "Zhejiang University · Helen China TEFL Network · Shenzhen & Huzhou", detail: "Teaching across school contexts from early years to secondary; communicative activities and continuous formative assessment.", kind: "work" },
  { years: "2014 — 2016", title: "English, Science & Mathematics Teacher", place: "Scholars Academy · Mumbai, India", detail: "Interdisciplinary instruction for upper primary and secondary; the foundation of the STEM-through-English approach.", kind: "work" },
  { years: "2007 — 2009", title: "M.A. English Language & Literature", place: "Harris University, USA", detail: "Postgraduate study of the English language and literature.", kind: "education" },
  { years: "2004 — 2007", title: "B.Sc. Physics", place: "Mumbai University", detail: "Undergraduate physics — the root of the cross-curricular STEM dimension.", kind: "education" },
];

/* ── Achievements — pinned horizontal gallery (verifiable counts only) ── */

export interface Achievement {
  tile: string;           // monogram tile letter(s) — organisations from the résumé
  label: string;
  caption: string;
  detail: string;
  number: number;         // count-up target
  suffix: string;         // "+", "h", "" …
  numberLabel: string;    // what the number means, right under it
}

export const ACHIEVEMENTS: Achievement[] = [
  { tile: "Ao", label: "Years in international education", caption: "Teaching and leading across international classrooms", detail: "India & China · 2014 → present", number: 11, suffix: "+", numberLabel: "years" },
  { tile: "GT", label: "TESOL certification", caption: "Global TESOL College, Canada", detail: "240 certified hours of TESOL training", number: 240, suffix: "h", numberLabel: "hours" },
  { tile: "CA", label: "British Council PD", caption: "Primary Education · Language Teaching", detail: "Professional development certificates", number: 3, suffix: "", numberLabel: "certifications" },
  { tile: "L6", label: "Languages of the classroom", caption: "English, Hindi, Urdu, Marathi, Arabic, Mandarin", detail: "Working across multilingual classrooms", number: 6, suffix: "", numberLabel: "languages" },
  { tile: "UC", label: "Qualifications", caption: "PGCE · B.Ed. · M.A. English · B.Sc. Physics", detail: "Postgraduate and undergraduate degrees", number: 4, suffix: "", numberLabel: "degrees" },
  { tile: "IC", label: "Countries taught in", caption: "India & China", detail: "International and bilingual school systems", number: 2, suffix: "", numberLabel: "countries" },
];

/* ── About — quick facts + ID card rows (all résumé-traced) ─────── */

export const QUICK_FACTS: { k: string; v: string }[] = [
  { k: "Location", v: "Zhengzhou, China" },
  { k: "Current role", v: "EAL / English Teacher — Aoxin International School" },
  { k: "Education", v: "PGCE, University of Cumbria (2025 – 2026)" },
  { k: "Email", v: PROFILE.email },
];

export const ID_CARD = {
  band: "TEACHER ID",
  idNo: "MSK-2014",             // design device: initials + first teaching year
  dept: "Primary EAL",
  validTill: "2026",            // PGCE completion year
  backTitle: "What I am",
  backLines: [
    "International Primary EAL Educator",
    "PGCE — University of Cumbria (2025–2026)",
    "TESOL · TEFL · British Council PD certified",
    "Mentor of early-career teachers",
    "Available from August 2027",
  ],
  strapText: `${PROFILE.name} · ${PROFILE.role}`,
};

export const ABOUT_QUOTE =
  "Combining evidence-informed classroom practice with teacher development and instructional quality improvement."; // paraphrase of the résumé summary

/* ── Research (résumé: Research section) ────────────────────────── */

export const RESEARCH = {
  title: "Questioning Strategies and Participation Equity in Bilingual Primary Classrooms",
  place: "University of Cumbria (2026)",
  summary:
    "Practitioner research investigating how structured questioning, extended wait time and purposeful follow-up prompts increased participation equity in bilingual primary classrooms, drawing on dialogic teaching and translanguaging frameworks.",
};
