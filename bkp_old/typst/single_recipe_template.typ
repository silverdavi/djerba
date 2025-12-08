// ===== COLOR SCHEME =====
#let primary_color = rgb("#8B4513")    // Saddle brown
#let secondary_color = rgb("#D2B48C")  // Tan
#let accent_color = rgb("#DC143C")     // Crimson

// ===== SINGLE RECIPE SPREAD TEMPLATE =====
// This template creates a beautiful two-page center fold with one recipe
// featuring all 4 languages in distinct sections with floating text boxes

#set page(
  paper: "a4",
  margin: (left: 1cm, right: 1cm, top: 1cm, bottom: 1cm),
  header: none,
  footer: none,
)

#set text(font: "Georgia", size: 10pt, lang: "en")

// ===== RECIPE DATA (In real version, this comes from JSON) =====

#let recipe_name_en = "Mahmessa"
#let recipe_name_he = "מחמסה"
#let recipe_name_ar = "المحمسة"
#let recipe_name_es = "Mahmessa"

#let recipe_category = "Main Dish"
#let recipe_serves = "4-6 people"
#let recipe_prep = "15 min"
#let recipe_cook = "30 min"

// ===== PAGE LAYOUT =====

#let two_column_layout(left_content, right_content) = {
  grid(
    columns: (1fr, 1fr),
    gutter: 0.8cm,
    left_content,
    right_content,
  )
}

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

#let ingredient_item(name, amount: "", unit: "") = {
  text(size: 9pt)[
    • #name
    #if amount != "" {
      text(fill: gray, " (" + amount + " " + unit + ")")
    }
  ]
}

// ===== MAIN CONTENT =====

// CENTER FOLD HEADER
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

// ===== LEFT PAGE (ENGLISH CONTENT) =====
#two_column_layout(
  
  // LEFT COLUMN CONTENT
  [
    // ETYMOLOGY SECTION
    #floating_box(
      "Etymology",
      [
        *Name Meaning:* 
        From Arabic/Maghrebi roots relating to mixing or grain preparation
        
        *Linguistic Roots:*
        Possibly connected to "hamsa" (five) or grain/mixing verbs in Semitic languages
        
        *Historical Reference:*
        A staple in North African Jewish cooking, particularly among Tunisian communities
      ],
      bg_color: rgb("#e8f4f8")
    )
    
    #v(0.5cm)
    
    // INGREDIENTS SECTION
    #floating_box(
      "Ingredients",
      [
        #ingredient_item("Small onion", amount: "1", unit: "")
        #ingredient_item("Israeli couscous (ptitim)", amount: "1", unit: "cup")
        #ingredient_item("Sweet paprika", amount: "1", unit: "tablespoon")
        #ingredient_item("Black pepper", unit: "to taste")
        #ingredient_item("Tomato, chopped", amount: "1", unit: "")
        #ingredient_item("Mixed vegetables", unit: "optional")
        #ingredient_item("Water", amount: "1.25", unit: "cups per cup ptitim")
        #ingredient_item("Salt", unit: "to taste")
      ],
      bg_color: rgb("#fff8e8")
    )
  ],
  
  // RIGHT COLUMN CONTENT
  [
    // INSTRUCTIONS SECTION
    #floating_box(
      "Instructions",
      [
        *Dry Version:*
        1. Sauté onion until translucent
        2. Add ptitim and sauté for a few minutes
        3. Add water and cook until tender
        
        *With Sauce:*
        1. Sauté onion until starting to brown
        2. Add paprika, then chopped tomato
        3. Season with salt and pepper
        4. Add ptitim and water
        5. Bring to boil, reduce heat, cover partially
        6. Simmer until cooked through
      ],
      bg_color: rgb("#f0e8ff")
    )
    
    #v(0.5cm)
    
    // DJERBAN TRADITION SECTION
    #floating_box(
      "Djerban Tradition",
      [
        *Role in Family:*
        A comfort food representing resourcefulness and heritage in Tunisian-Djerban Jewish cuisine
        
        *Occasions:*
        Served on weekdays and special occasions; part of Shabbat tradition
        
        *Cultural Meaning:*
        Symbol of familial continuity and adaptation. Hand-rolled ptitim connects generations through preparation and shared meals.
      ],
      bg_color: rgb("#ffe8f0")
    )
  ]
)

#pagebreak()

// ===== RIGHT PAGE (MULTILINGUAL LAYOUT) =====

#align(center)[
  #text(size: 18pt, weight: "bold", fill: primary_color)[
    Multilingual Reference
  ]
]

#v(0.4cm)

// HEBREW VERSION
#floating_box(
  "Hebrew (עברית)",
  [
    *שם המתכון:* מחמסה
    
    *מרכיבים:*
    • בצל קטן
    • כוס אחת קוסקוס ישראלי
    • כף אחת פפריקה מתוקה
    • מלח ופלפל שחור
    • עגבניה קצוצה
    
    *הוראות:*
    1. טגנו בצל עד שמתחיל להשחיר
    2. הוסיפו קוסקוס וטגנו כמה דקות
    3. הוסיפו מים וקדימו לרתיחה
  ],
  bg_color: rgb("#e8f4f8")
)

#v(0.4cm)

// ARABIC VERSION
#floating_box(
  "Arabic (العربية)",
  [
    *اسم الوصفة:* المحمسة
    
    *المكونات:*
    • بصلة صغيرة
    • كوب واحد من الكسكسي الإسرائيلي
    • ملعقة واحدة من البابريكا الحلوة
    • ملح وفلفل أسود
    • طماطم مفرومة
    
    *التعليمات:*
    1. قلِّ البصل حتى يبدأ بالتحول إلى البني
    2. أضف الكسكسي وقلِّه لعدة دقائق
  ],
  bg_color: rgb("#f0e8ff")
)

#v(0.4cm)

// SPANISH VERSION
#floating_box(
  "Spanish (Español)",
  [
    *Nombre de la Receta:* Mahmessa
    
    *Ingredientes:*
    • 1 cebolla pequeña
    • 1 taza de cúscus israelí
    • 1 cucharada de pimentón dulce
    • Sal y pimienta negra
    • 1 tomate picado
    
    *Instrucciones:*
    1. Saltee la cebolla hasta que empiece a dorarse
    2. Agregue el cúscus y saltee algunos minutos
    3. Agregue agua y lleve a ebullición
  ],
  bg_color: rgb("#ffe8f0")
)

#v(0.6cm)

// FOOTER WITH METADATA
#align(center, text(size: 8pt, fill: gray)[
  Mahmessa | Serves: #recipe_serves | Prep: #recipe_prep | Cook: #recipe_cook | Category: #recipe_category
])

