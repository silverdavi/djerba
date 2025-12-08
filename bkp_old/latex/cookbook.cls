%% cookbook.cls - Simple document class for Djerba-Tanjir Vegan Cookbook

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cookbook}[2025/01/01 Multilingual Cookbook Class]

% Base class
\LoadClass[12pt,twoside,openright]{book}

% Required packages - simplified
\RequirePackage{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{tocloft}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{enumitem}
\RequirePackage{multicol}
\RequirePackage{afterpage}
\RequirePackage{tikz}
\RequirePackage{wrapfig}

% Page geometry for cookbook format (larger for double-page spreads)
\geometry{
    paperwidth=8.5in,
    paperheight=11in,
    inner=0.8in,
    outer=0.6in,
    top=0.8in,
    bottom=0.8in,
    marginparwidth=0.4in,
    marginparsep=0.1in
}

% Define cookbook colors
\definecolor{HebrewBlue}{RGB}{0,51,102}
\definecolor{ArabicGreen}{RGB}{0,102,51}
\definecolor{SpanishRed}{RGB}{153,51,0}
\definecolor{EnglishPurple}{RGB}{102,0,153}

% Custom commands for recipe elements
\newcommand{\recipetitle}[4]{%
    % #1: Hebrew, #2: English, #3: Arabic, #4: Spanish
    \chapter*{#2}
    \addcontentsline{toc}{chapter}{#2}
    \markboth{#2}{#2}
}

\newcommand{\etymology}[2]{%
    % #1: Root, #2: Meaning
    \begin{center}
        \textit{Etymology: #1 -- #2}
    \end{center}
}

\newcommand{\ingredients}[1]{%
    \section*{Ingredients}
    #1
}

\newcommand{\instructions}[1]{%
    \section*{Instructions}
    #1
}

\newcommand{\culturalnotes}[1]{%
    \section*{Cultural Notes}
    #1
}

% AMAZING DOUBLE-PAGE SPREAD COMMANDS

% Recipe title with dramatic multilingual presentation
\newcommand{\multilingualrecipetitle}[4]{%
    % #1: Hebrew, #2: English, #3: Arabic, #4: Spanish
    \chapter{#2}
    \thispagestyle{empty}
    
    % Dramatic title box
    \begin{center}
        \tikz[remember picture,overlay] \node[rectangle,fill=black!10,rounded corners=10pt,minimum width=\textwidth,minimum height=3cm] {};
        \vspace{0.5cm}
        
        {\Huge\bfseries\color{EnglishPurple} #2}
        
        \vspace{0.3cm}
        
        \begin{tabular}{c|c|c}
            {\Large\color{HebrewBlue} #1} & 
            {\Large\color{ArabicGreen} #3} & 
            {\Large\color{SpanishRed} #4} \\
            \small Hebrew & \small Arabic & \small Spanish
        \end{tabular}
        
        \vspace{0.5cm}
    \end{center}
}

% Left page: Etymology, culture, and image
\newcommand{\leftpagecontent}[6]{%
    % #1: Root, #2: Origin, #3: Meaning, #4: Description, #5: Cultural context, #6: Image filename
    
    \section*{\color{EnglishPurple}Etymology \& Heritage}
    
    \begin{tcolorbox}[colback=HebrewBlue!10,colframe=HebrewBlue,title=\textbf{Linguistic Roots}]
        \textbf{Root:} #1 \\
        \textbf{Origin:} #2 \\
        \textbf{Meaning:} #3 \\
        \textbf{Description:} #4
    \end{tcolorbox}
    
    \vspace{0.5cm}
    
    \begin{center}
        \includegraphics[width=0.85\textwidth]{assets/images/#6}
        \textit{\small Traditional M'hamsa from the Silver family kitchen}
    \end{center}
    
    \vspace{0.5cm}
    
    \begin{tcolorbox}[colback=ArabicGreen!10,colframe=ArabicGreen,title=\textbf{Cultural Heritage}]
        #5
    \end{tcolorbox}
}

% Right page: Four-language ingredients and instructions
\newcommand{\rightpagecontent}[8]{%
    % #1: Hebrew ingredients, #2: English ingredients, #3: Arabic ingredients, #4: Spanish ingredients
    % #5: Hebrew instructions, #6: English instructions, #7: Arabic instructions, #8: Spanish instructions
    
    \section*{\color{EnglishPurple}Ingredients \textbullet{} רכיבים \textbullet{} مكونات \textbullet{} Ingredientes}
    
    % Ingredients in beautiful boxes
    \begin{minipage}[t]{0.48\textwidth}
        \begin{tcolorbox}[colback=HebrewBlue!15,colframe=HebrewBlue,title=\textbf{עברית \textbullet{} Hebrew},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=HebrewBlue,enhanced,drop shadow]
            \begin{itemize}[leftmargin=0.3cm,itemsep=1pt,parsep=0pt,topsep=2pt]
                #1
            \end{itemize}
        \end{tcolorbox}
        
        \vspace{0.3cm}
        
        \begin{tcolorbox}[colback=ArabicGreen!15,colframe=ArabicGreen,title=\textbf{عربي \textbullet{} Arabic},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=ArabicGreen,enhanced,drop shadow]
            \begin{itemize}[leftmargin=0.3cm,itemsep=1pt,parsep=0pt,topsep=2pt]
                #3
            \end{itemize}
        \end{tcolorbox}
    \end{minipage}
    \hfill
    \begin{minipage}[t]{0.48\textwidth}
        \begin{tcolorbox}[colback=EnglishPurple!15,colframe=EnglishPurple,title=\textbf{English},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=EnglishPurple,enhanced,drop shadow]
            \begin{itemize}[leftmargin=0.3cm,itemsep=1pt,parsep=0pt,topsep=2pt]
                #2
            \end{itemize}
        \end{tcolorbox}
        
        \vspace{0.3cm}
        
        \begin{tcolorbox}[colback=SpanishRed!15,colframe=SpanishRed,title=\textbf{Español \textbullet{} Spanish},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=SpanishRed,enhanced,drop shadow]
            \begin{itemize}[leftmargin=0.3cm,itemsep=1pt,parsep=0pt,topsep=2pt]
                #4
            \end{itemize}
        \end{tcolorbox}
    \end{minipage}
    
    \vspace{0.5cm}
    
    \section*{\color{EnglishPurple}Instructions \textbullet{} הוראות \textbullet{} تعليمات \textbullet{} Instrucciones}
    
    % Instructions in beautiful boxes
    \begin{minipage}[t]{0.48\textwidth}
        \begin{tcolorbox}[colback=HebrewBlue!15,colframe=HebrewBlue,title=\textbf{עברית \textbullet{} Hebrew},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=HebrewBlue,enhanced,drop shadow]
            \begin{enumerate}[leftmargin=0.5cm,itemsep=2pt,parsep=0pt,topsep=3pt]
                #5
            \end{enumerate}
        \end{tcolorbox}
        
        \vspace{0.3cm}
        
        \begin{tcolorbox}[colback=ArabicGreen!15,colframe=ArabicGreen,title=\textbf{عربي \textbullet{} Arabic},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=ArabicGreen,enhanced,drop shadow]
            \begin{enumerate}[leftmargin=0.5cm,itemsep=2pt,parsep=0pt,topsep=3pt]
                #7
            \end{enumerate}
        \end{tcolorbox}
    \end{minipage}
    \hfill
    \begin{minipage}[t]{0.48\textwidth}
        \begin{tcolorbox}[colback=EnglishPurple!15,colframe=EnglishPurple,title=\textbf{English},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=EnglishPurple,enhanced,drop shadow]
            \begin{enumerate}[leftmargin=0.5cm,itemsep=2pt,parsep=0pt,topsep=3pt]
                #6
            \end{enumerate}
        \end{tcolorbox}
        
        \vspace{0.3cm}
        
        \begin{tcolorbox}[colback=SpanishRed!15,colframe=SpanishRed,title=\textbf{Español \textbullet{} Spanish},fonttitle=\bfseries\color{white},coltitle=white,colbacktitle=SpanishRed,enhanced,drop shadow]
            \begin{enumerate}[leftmargin=0.5cm,itemsep=2pt,parsep=0pt,topsep=3pt]
                #8
            \end{enumerate}
        \end{tcolorbox}
    \end{minipage}
}

% Beautiful closing with multilingual bon appétit
\newcommand{\recipeclosing}[6]{%
    % #1: Hebrew bon appétit, #2: Arabic, #3: Spanish, #4: English, #5: Family note, #6: Heritage note
    
    \vspace{1cm}
    \begin{center}
        \tikz[remember picture,overlay] \node[rectangle,fill=black!5,rounded corners=8pt,minimum width=0.9\textwidth,minimum height=2cm] {};
        \vspace{0.3cm}
        
        {\Large\color{HebrewBlue} #1} \textbullet{} 
        {\Large\color{ArabicGreen} #2} \textbullet{} 
        {\Large\color{SpanishRed} #3} \textbullet{} 
        {\Large\color{EnglishPurple} #4}
        
        \vspace{0.5cm}
        
        \textit{\small #5} \\
        \textit{\small #6}
        
        \vspace{0.3cm}
    \end{center}
}

% Legacy commands (kept for compatibility)
\newcommand{\etymologysection}[4]{%
    \section{Etymology \& Cultural Heritage}
    \textbf{Etymology:} #4
    \textbf{Root:} #1 (#2) -- #3
}

\newcommand{\culturalcontext}[3]{%
    \textbf{Cultural Context:} #1
    #2
    \textbf{Family Heritage:} #3
}

\newcommand{\recipeimage}[2][0.7\textwidth]{%
    \begin{center}
        \includegraphics[width=#1]{assets/images/#2}
    \end{center}
}

\newcommand{\fourlanguageingredients}[4]{%
    \section{Ingredients}
    \begin{multicols}{2}
        \subsection*{Hebrew \textbullet{} עברית}
        \begin{itemize}
            #1
        \end{itemize}
        \subsection*{English}
        \begin{itemize}
            #2
        \end{itemize}
        \columnbreak
        \subsection*{Arabic \textbullet{} عربي}
        \begin{itemize}
            #3
        \end{itemize}
        \subsection*{Spanish \textbullet{} Español}
        \begin{itemize}
            #4
        \end{itemize}
    \end{multicols}
}

\newcommand{\methodsection}[3]{%
    \subsection{#1 \textbullet{} #2 \textbullet{} #3}
}

\newcommand{\languageinstructions}[2]{%
    \subsubsection*{#1}
    \begin{enumerate}
        #2
    \end{enumerate}
}

\newcommand{\multilingualbonappetit}[4]{%
    \vspace{1cm}
    \begin{center}
        \textbf{#1 \textbullet{} #2 \textbullet{} #3 \textbullet{} #4}
    \end{center}
}

\newcommand{\familyattribution}[2]{%
    \vspace{0.5cm}
    \begin{center}
        \textit{#1}\\
        \textit{#2}
    \end{center}
}

% Recipe environment for double-page spread
\newenvironment{recipe}{%
    \cleardoublepage
    \thispagestyle{recipe}
}{%
    \clearpage
}

% Custom page style for recipes
\fancypagestyle{recipe}{%
    \fancyhf{}
    \fancyhead[LE,RO]{\thepage}
    \fancyhead[LO]{\leftmark}
    \fancyhead[RE]{\rightmark}
    \renewcommand{\headrulewidth}{0.5pt}
    \renewcommand{\footrulewidth}{0pt}
}

% Title page command
\renewcommand{\maketitle}{%
    \begin{titlepage}
        \centering
        \vspace*{2cm}
        
        {\Huge\bfseries Djerba-Tanjir Vegan Cookbook}
        
        \vspace{1cm}
        {\Large Traditional Recipes in Four Languages}
        
        \vspace{1cm}
        {\large Hebrew • English • Arabic • Spanish}
        
        \vspace{2cm}
        {\large David Silver \& Enny Silver}
        
        \vfill
        {\small A celebration of North African Jewish culinary heritage}
        
        \vspace{1cm}
    \end{titlepage}
} 