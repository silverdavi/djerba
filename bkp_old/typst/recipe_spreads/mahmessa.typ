// AUTO-GENERATED RECIPE SPREAD
// Recipe: Mahmessa
// Generated for multilingual cookbook

// ===== COLOR SCHEME =====
#let primary_color = rgb("#8B4513")    // Saddle brown
#let secondary_color = rgb("#D2B48C")  // Tan
#let accent_color = rgb("#DC143C")     // Crimson

#set page(
  paper: "a4",
  margin: (left: 1cm, right: 1cm, top: 1cm, bottom: 1cm),
  header: none,
  footer: none,
)

#set text(font: "Georgia", size: 10pt, lang: "en")

// ===== HELPER FUNCTIONS =====

#let floating_box(title, content, bg_color: rgb("#f5f5f5")) = {
  block(
    fill: bg_color,
    stroke: 1pt + rgb("#999"),
    radius: 6pt,
    inset: 0.6cm,
    [
      #text(size: 11pt, weight: "bold", fill: primary_color, title)
      #v(0.3cm)
      #text(size: 9pt, content)
    ]
  )
}

#let two_column_layout(left_content, right_content) = {
  grid(
    columns: (1fr, 1fr),
    gutter: 0.8cm,
    left_content,
    right_content,
  )
}

#let ingredient_item(name, amount: "", unit: "") = {
  text(size: 9pt)[
    • #name
    #if amount != "" {
      text(fill: gray, " (" + amount + " " + unit + ")")
    }
  ]
}

// ===== RECIPE DATA =====
#let recipe_name_en = "Mahmessa"
#let recipe_name_he = "מחמסה"
#let recipe_name_ar = "[TODO: Translate to Arabic]"
#let recipe_name_es = "[TODO: Translate to Spanish]"
#let recipe_category = "Main Dishes"
#let recipe_serves = "4-6 people"
#let recipe_prep = "20 min"
#let recipe_cook = "30 min"

// ===== PAGE 1: ENGLISH & LAYOUT =====

#align(center)[
  #text(size: 22pt, weight: "bold", fill: primary_color)[
    #recipe_name_en
  ]
  
  #v(0.2cm)
  
  #text(size: 10pt, fill: gray)[
    #recipe_name_he #h(1cm) #recipe_name_ar #h(1cm) #recipe_name_es
  ]
  
  #v(0.4cm)
  
  #line(length: 80%, stroke: 1.5pt + secondary_color)
]

#v(0.6cm)

#two_column_layout(
  // LEFT COLUMN
  [
    // ETYMOLOGY
    #floating_box(
      "Etymology",
      [
        The name \"Mahmessa\" (מחמסה) is believed to derive from Arabic or Maghrebi language origins, possibly linked to root words relating to mixing or a type of small pasta/grain[3]. In similar North African semitic dialects, such as the roots of “hamsa/khamsa,” the term relates to “five,” but in the context of food, extensions of this root or similar-sounding terms sometimes point toward grain shapes or actions like “to mix” or “to stew.” There is also a symbolic resonance with protection and abundanc
      ],
      bg_color: rgb("#e8f4f8")
    )
    
    #v(0.5cm)
    
    // INGREDIENTS
    #floating_box(
      "Ingredients",
      [
        #ingredient_item("small onion")
        #ingredient_item("of ptitim (Israeli couscous)", amount: "1", unit: "cup")
        #ingredient_item("sweet paprika", amount: "1", unit: "tablespoon")
        #ingredient_item("Black pepper to taste")
        #ingredient_item("chopped tomato")
        #ingredient_item("Vegetables of your choice")
        #ingredient_item("Water (1 and 1/4 cups for every cup of ptitim)")
      ],
      bg_color: rgb("#fff8e8")
    )
  ],
  
  // RIGHT COLUMN
  [
    // INSTRUCTIONS
    #floating_box(
      "Instructions",
      [
                1. For dry Mahmessa: Sauté a small onion until translucent.
        2. Add the ptitim (Mahmessa) and continue to sauté for a few more minutes. Then, add water according to the instructions: 1 and 1/4 cups of water for every cup of ptitim.
        3. For Mahmessa with sauce: Sauté a small onion until it starts to brown. Add 1 tablespoon of sweet paprika and sauté for a few seconds.
        4. Add the chopped tomato and any vegetables you desire. Season with salt, black pepper, and add boiling water.
        5. Stir in the ptitim.
        6. Bring to a boil, then reduce the heat, cover partially, and simmer until cooked through.
      ],
      bg_color: rgb("#f0e8ff")
    )
    
    #v(0.5cm)
    
    // DJERBAN TRADITION
    #floating_box(
      "Djerban Tradition",
      [
        Mahmessa is a traditional dish enjoyed in Tunisian-Djerban Jewish cuisine, often customized with various vegetables based on personal preference.
      ],
      bg_color: rgb("#ffe8f0")
    )
  ]
)

#pagebreak()

// ===== PAGE 2: HISTORY & MULTILINGUAL REFERENCE =====

#align(center)[
  #text(size: 18pt, weight: "bold", fill: primary_color)[
    History & Cultural Context
  ]
]

#v(0.4cm)

#floating_box(
  "Historical Background",
  [
    Mahmessa (מחמסה) is a traditional dish with roots in the Tunisian and Djerban Jewish communities, reflecting their unique blend of North African Jewish culinary traditions[6][13]. Jews have lived in Tunisia, including the island of Djerba, for more than 2,000 years, establishing deeply distinct cultural and foodways. While direct historical documentation specifically naming Mahmessa is limited, it
  ],
  bg_color: rgb("#e8e8f0")
)

#v(0.6cm)

#align(center, text(size: 12pt, weight: "bold", fill: primary_color)[
  Multilingual Reference
])

#v(0.3cm)

#floating_box(
  "Hebrew (עברית)",
  [
    *שם המתכון:* מחמסה
    
    This section would contain the full Hebrew version of the recipe.
  ],
  bg_color: rgb("#e8f4f8")
)

#v(0.3cm)

#floating_box(
  "Arabic (العربية)",
  [
    *اسم الوصفة:* [TODO: Translate to Arabic]
    
    This section would contain the full Arabic version of the recipe.
  ],
  bg_color: rgb("#f0e8ff")
)

#v(0.3cm)

#floating_box(
  "Spanish (Español)",
  [
    *Nombre de la Receta:* [TODO: Translate to Spanish]
    
    This section would contain the full Spanish version of the recipe.
  ],
  bg_color: rgb("#ffe8f0")
)

#v(0.6cm)

// FOOTER
#align(center, text(size: 8pt, fill: gray)[
  Mahmessa | Serves: 4-6 people | Prep: 20 min | Cook: 30 min | Main Dishes
])
