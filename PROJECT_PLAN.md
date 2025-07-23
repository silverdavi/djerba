# Vegan Djerban Family Cookbook - Project Plan

## 📖 Project Overview

**Goal**: Create a multilingual vegan cookbook preserving Djerban Jewish family recipes across generations

**Family Heritage Lines**:
- **Silver-Cohen-Trabelsi**: Traditional Tunisian/Djerban Jewish cuisine (David's maternal line - Ruth Cohen's mother Trabelsi from Djerba)
- **Kadoch-Muyal**: Traditional Moroccan Jewish cuisine from Tangier (Enny's maternal line - Kadoch's mother Muyal from Tangier, Morocco)
- **Silver**: Contemporary vegan adaptations (David & Enny's modern innovations)

**Output Languages**: Hebrew, English, Spanish, Tunisian Arabic (with Hebrew transliteration)

**Final Format**: Professional LaTeX cookbook with chapters, cultural context, and family heritage

---

## 🔄 AI Workflow Pipeline

### Phase 1: Research & Documentation
**AI Tools Chain**: Perplexity → Gemini → GPT-4o → Translation

#### Step 1: Etymology & Cultural Research (Perplexity)
**Prompt Template**:
```
Research the dish "[DISH_NAME]" in [ORIGIN] Jewish cuisine:
[For Djerban dishes: "in Tunisian Jewish cuisine from Djerba"]
[For Moroccan dishes: "in Moroccan Jewish cuisine from Tangier"]

1. Etymology and meaning of the name
2. Historical significance in [Djerban/Tangier] Jewish community  
3. Traditional preparation methods and ingredients
4. Cultural context (Sabbath, holidays, daily meals)
5. Regional variations across North African Jewish communities
6. Differences between Tunisian and Moroccan Jewish culinary traditions
7. Any connection to Sephardic or Mizrahi culinary traditions
```

#### Step 2: Veganization Research (Perplexity)
**Prompt Template**:
```
Find information about veganizing "[DISH_NAME]" - a traditional [DISH_TYPE] from [ORIGIN] Jewish cuisine:
[For Djerban dishes: "from Tunisian Jewish cuisine"]  
[For Moroccan dishes: "from Moroccan Jewish cuisine"]

1. Any existing traditional vegan versions in North African Jewish cooking
2. Common plant-based substitutions for [SPECIFIC_INGREDIENTS]
3. Techniques to maintain authentic flavors without animal products
4. Modern vegan adaptations while preserving cultural authenticity
5. Regional differences in ingredient availability (Tunisia vs Morocco)
6. Nutritional considerations for substitutions
```

#### Step 3: Information Synthesis (Gemini)
**Prompt Template**:
```
Compile and synthesize the following research about "[DISH_NAME]":

[PERPLEXITY_RESEARCH_1]
[PERPLEXITY_RESEARCH_2]

Create a structured report including:
1. Cultural Background & Etymology
2. Traditional Preparation Overview
3. Vegan Adaptation Strategy
4. Key Ingredients & Substitutions
5. Cultural Significance & Family Context
6. Preparation Tips & Techniques
```

#### Step 4: Recipe Generation (GPT-4o)
**Prompt Template**:
```
Create a complete vegan recipe for "[DISH_NAME]" based on this research:

[GEMINI_SYNTHESIS]

Format as markdown with:
1. Cultural background paragraph
2. Ingredient list with substitution notes
3. Step-by-step instructions
4. Serving suggestions
5. Cultural context and family notes
6. Preparation time and difficulty level
```

---

## 📚 Content Organization Structure

### Cookbook Chapters

#### Chapter 1: Heritage & History
- Family lineage and migration stories
- **Djerban Jewish culinary traditions** (Silver-Cohen-Trabelsi line from Tunisia)
- **Moroccan Jewish culinary traditions** (Kadoch-Muyal line from Tangier)
- Convergence of North African Jewish cuisines
- The art of plant-based adaptation

#### Chapter 2: Daily Breads & Foundations
- **Challah** (בצק לחלות) - Sabbath bread
- **Flatbread** (בצק לפיתות) - Taboon bread
- **Artisan Bread** (לחם ארטיזן)
- **Semolina Dishes** (שמיד, דייסת סולת)

#### Chapter 3: Sabbath Specialties
- **Tafina** (טפינה) - Sabbath stew
- **Hraimi** (חרימי) - Spiced fish substitute
- **Brodo** (ברודו) - Clear vegetable soup
- **Koklot** (קוקלות) - Sabbath dumplings

#### Chapter 4: Holiday Traditions
- **Couscous** (קוסקוס) with vegetable accompaniments
- **Sufganiyot** (סופגניות) - Hanukkah donuts
- **Festive Dishes** (דביח חגים) for special occasions
- **Brik** (בריקות) - Holiday pastries

#### Chapter 5: Everyday Comfort
- **Shakshuka** (שקשוקה) variations
- **Vegetable Soups** and stews
- **Ktaa** (קטעה) - Dumpling soup
- **Marmouma** (מרמומה) - Spicy vegetable dip

#### Chapter 6: Sweet Traditions
- **Sfenj** (שפינג׳ות) - Fried dough
- **YoYo** (יויו) - Sweet fritters
- **Modern Cakes** and desserts
- **Traditional Sweets** adaptations

#### Chapter 7: Modern Innovations
- **TVP Shawarma** (שווארמה סויה)
- **Tofu Fish** adaptations
- **Spice Blends** for vegan cooking
- **Contemporary Fusion** dishes

---

## 🌍 Translation Workflow

### Language Processing Pipeline

#### Primary Development Language: **English**
All research, compilation, and initial recipe generation in English

#### Translation Phase (Using AI):
1. **Hebrew** (עברית) - Family heritage language
2. **Spanish** (Español) - Wider accessibility  
3. **Tunisian Arabic** (تونسي) with Hebrew transliteration

#### Translation Prompt Template:
```
Translate this recipe for "[DISH_NAME]" into [TARGET_LANGUAGE]:

[ENGLISH_RECIPE]

Requirements:
- Maintain cultural authenticity in food terminology
- Keep original dish names with pronunciation guides
- Preserve cooking technique descriptions
- Include cultural context appropriately
- For Tunisian Arabic: provide Hebrew transliteration
```

---

## 📄 LaTeX Implementation Plan

### Document Structure

#### LaTeX Document Class & Packages
```latex
\documentclass[11pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage[hebrew,english,spanish,arabic]{babel}
\usepackage{polyglossia} % For multilingual support
\usepackage{fontspec} % For Hebrew/Arabic fonts
\usepackage{cookbook} % Custom cookbook formatting
\usepackage{graphicx} % For family photos
\usepackage{multicol} % For ingredient lists
\usepackage{fancyhdr} % Headers/footers
\usepackage{xcolor} % Colors for cultural elements
```

#### Custom LaTeX Environment Definitions
```latex
% Recipe environment
\newenvironment{recipe}[1]{
  \chapter{#1}
  \begin{center}
  \rule{\linewidth}{0.5pt}
  \end{center}
}{\newpage}

% Multilingual sections
\newcommand{\recipehebrew}[1]{\section*{עברית}\selectlanguage{hebrew}#1}
\newcommand{\recipeenglish}[1]{\section*{English}\selectlanguage{english}#1}
\newcommand{\recipespanish}[1]{\section*{Español}\selectlanguage{spanish}#1}
\newcommand{\recipearabic}[1]{\section*{العربية}\selectlanguage{arabic}#1}

% Cultural context boxes
\newenvironment{culturalcontext}{
  \begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black]
  \textbf{Cultural Heritage:}
}{
  \end{tcolorbox}
}
```

#### Chapter Template Structure
```latex
\chapter{Chapter Name}

% Chapter introduction
\section*{Heritage Context}
[Cultural background for this category of dishes]

% Individual recipes
\begin{recipe}{Dish Name}
  \begin{culturalcontext}
    [Historical and cultural background]
  \end{culturalcontext}
  
  % English version (primary)
  \recipeenglish{
    \subsection*{Ingredients}
    \begin{multicols}{2}
    \begin{itemize}
      \item [ingredients list]
    \end{itemize}
    \end{multicols}
    
    \subsection*{Instructions}
    \begin{enumerate}
      \item [step-by-step instructions]
    \end{enumerate}
  }
  
  % Hebrew version
  \recipehebrew{[Hebrew translation]}
  
  % Spanish version  
  \recipespanish{[Spanish translation]}
  
  % Tunisian Arabic version
  \recipearabic{[Arabic with transliteration]}
  
\end{recipe}
```

#### LaTeX Build Pipeline
1. **Content Generation**: Markdown recipes → LaTeX conversion
2. **Image Integration**: Family photos and food photography
3. **Font Configuration**: Hebrew/Arabic font setup
4. **Compilation**: XeLaTeX for Unicode support
5. **Index Generation**: Ingredient and cultural index
6. **Final Production**: Print-ready PDF

### LaTeX Project Structure
```
cookbook/
├── main.tex                 # Main document
├── chapters/
│   ├── 01-heritage.tex
│   ├── 02-breads.tex
│   ├── 03-sabbath.tex
│   ├── 04-holidays.tex
│   ├── 05-everyday.tex
│   ├── 06-sweets.tex
│   └── 07-modern.tex
├── recipes/
│   ├── english/
│   ├── hebrew/
│   ├── spanish/
│   └── arabic/
├── images/
│   ├── family-photos/
│   └── food-photos/
├── styles/
│   ├── cookbook.cls
│   └── cultural-elements.sty
└── fonts/
    ├── hebrew-fonts/
    └── arabic-fonts/
```

---

## 🚀 Implementation Timeline

### Phase 1: Foundation
- [ ] Set up project structure
- [ ] Create AI prompt templates
- [ ] Test workflow with 3 sample recipes
- [ ] Establish LaTeX template

### Phase 2: Core Content 
- [ ] Research and generate all traditional recipes
- [ ] Complete cultural context documentation
- [ ] Develop vegan adaptations
- [ ] Create English markdown versions

### Phase 3: Translation
- [ ] Translate all content to Hebrew, Spanish, Arabic
- [ ] Review and refine translations
- [ ] Cultural authenticity verification

### Phase 4: LaTeX Production
- [ ] Convert markdown to LaTeX
- [ ] Integrate multilingual content
- [ ] Add family photos and cultural elements
- [ ] Final compilation and review

### Phase 5: Finalization
- [ ] Proofreading and editing
- [ ] Print preparation
- [ ] Digital distribution setup

---

## 📋 Next Immediate Steps

1. **Select 3 Test Recipes** for workflow development:
   - One **Djerban traditional** (e.g., Couscous from Silver-Cohen-Trabelsi)
   - One **Moroccan traditional** (e.g., Koag'ada from Kadoch-Muyal)  
   - One **modern vegan** (e.g., TVP Shawarma from Silver)

2. **Create Project Directories**
3. **Test AI Research Pipeline**
4. **Develop LaTeX Template**
5. **Refine and Iterate**

**Ready to begin!** 🎯 