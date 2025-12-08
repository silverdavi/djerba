%% cookbook.cls - Custom document class for Vegan Djerban Family Cookbook
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cookbook}[2024/12/19 Vegan Djerban Family Cookbook Class]

% Base class
\LoadClass[11pt,a4paper,twoside]{book}

% Required packages
\RequirePackage[utf8]{inputenc}
\RequirePackage{fontspec}
\RequirePackage{polyglossia}
\RequirePackage[margin=2.5cm,top=3cm,bottom=3cm]{geometry}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{tcolorbox}
\RequirePackage{multicol}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{enumitem}
\RequirePackage{array}
\RequirePackage{booktabs}
\RequirePackage{microtype}
\RequirePackage{setspace}

% Language setup
\setmainlanguage{english}
\setotherlanguage{hebrew}
\setotherlanguage{spanish}
\setotherlanguage{arabic}

% Font setup
\setmainfont{Crimson Pro}[
    Path = fonts/,
    Extension = .ttf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic,
    BoldItalicFont = *-BoldItalic
]

\setsansfont{Inter}[
    Path = fonts/,
    Extension = .ttf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic
]

\newfontfamily\hebrewfont{SBL Hebrew}[
    Path = fonts/,
    Extension = .ttf,
    Script = Hebrew
]

\newfontfamily\arabicfont{Scheherazade New}[
    Path = fonts/,
    Extension = .ttf,
    Script = Arabic
]

% Color scheme
\definecolor{djerbaBlue}{RGB}{41, 128, 185}
\definecolor{tangierGold}{RGB}{241, 196, 15}
\definecolor{warmBrown}{RGB}{125, 102, 79}
\definecolor{oliveGreen}{RGB}{142, 152, 103}
\definecolor{lightBg}{RGB}{250, 250, 248}

% Custom environments
\newtcolorbox{culturalcontext}{
    colback=lightBg,
    colframe=djerbaBlue,
    boxrule=1.5pt,
    arc=3pt,
    left=10pt,
    right=10pt,
    top=8pt,
    bottom=8pt,
    fonttitle=\bfseries\sffamily,
    title=Cultural Heritage
}

\newtcolorbox{recipecard}{
    colback=white,
    colframe=warmBrown,
    boxrule=1pt,
    arc=2pt,
    left=15pt,
    right=15pt,
    top=10pt,
    bottom=10pt
}

% Recipe environment
\newenvironment{recipe}[1]{
    \chapter{#1}
    \thispagestyle{fancy}
}{
    \clearpage
}

% Multilingual recipe sections
\newcommand{\recipesection}[2]{
    \section*{\textcolor{djerbaBlue}{#1}}
    \selectlanguage{#2}
}

% Ingredient list styling
\newenvironment{ingredientlist}{
    \begin{multicols}{2}
    \begin{itemize}[leftmargin=*,itemsep=3pt]
}{
    \end{itemize}
    \end{multicols}
}

% Instructions styling
\newenvironment{instructions}{
    \begin{enumerate}[leftmargin=*,itemsep=5pt]
}{
    \end{enumerate}
}

% Header/footer styling
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\sffamily\small\leftmark}
\fancyhead[RO]{\sffamily\small\rightmark}
\fancyfoot[C]{\sffamily\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}

% Chapter styling
\titleformat{\chapter}[display]
{\sffamily\huge\bfseries\color{djerbaBlue}}
{\filright\large\color{tangierGold}Chapter \thechapter}
{20pt}
{\filleft}

\titlespacing*{\chapter}{0pt}{-30pt}{40pt}

% Section styling
\titleformat{\section}
{\sffamily\Large\bfseries\color{warmBrown}}
{\thesection}
{1em}
{}

\titleformat{\subsection}
{\sffamily\large\bfseries\color{oliveGreen}}
{\thesubsection}
{1em}
{}

% Custom commands
\newcommand{\recipetime}[1]{\textcolor{djerbaBlue}{\sffamily\textbf{Time:} #1}}
\newcommand{\recipeserves}[1]{\textcolor{djerbaBlue}{\sffamily\textbf{Serves:} #1}}
\newcommand{\recipedifficulty}[1]{\textcolor{djerbaBlue}{\sffamily\textbf{Difficulty:} #1}}

% Hebrew text command
\newcommand{\heb}[1]{\begingroup\hebrewfont\selectlanguage{hebrew}#1\endgroup}
\newcommand{\ar}[1]{\begingroup\arabicfont\selectlanguage{arabic}#1\endgroup}
