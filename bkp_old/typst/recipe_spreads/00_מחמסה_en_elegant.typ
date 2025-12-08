
// ELEGANT SPREAD FOR: Mahmessa

#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 1.5cm, left: 1.5cm, right: 1.5cm),
  header: none,
  footer: none
)

#set text(font: ("Times New Roman", "Arial"), size: 10pt, fill: rgb("#202020"))
#let accent_color = rgb("#8B4513")
#let border_color = rgb("#dddddd")

// --- FUNCTIONS ---

#let language_section(title, ingredients, instructions, story, dir, font) = {
  set text(font: font, dir: dir)
  block(
    height: 48%,
    width: 100%,
    inset: 1em,
    stroke: (bottom: 0.5pt + border_color),
    [
      #align(center, text(size: 18pt, weight: "bold", fill: accent_color, title))
      #v(1em)
      #grid(
        columns: if dir == rtl { (2fr, 1fr) } else { (1fr, 2fr) },
        gutter: 2em,
        
        // COL 1
        if dir == ltr {
           [
             #text(weight: "bold")[Ingredients]
             #v(0.5em)
             #ingredients
           ]
        } else {
           [
             #text(weight: "bold")[Preparation]
             #v(0.5em)
             #instructions
             #v(1em)
             #line(length: 100%, stroke: 0.5pt + border_color)
             #v(0.5em)
             #text(style: "italic", story)
           ]
        },

        // COL 2
        if dir == ltr {
           [
             #text(weight: "bold")[Preparation]
             #v(0.5em)
             #instructions
             #v(1em)
             #line(length: 100%, stroke: 0.5pt + border_color)
             #v(0.5em)
             #text(style: "italic", story)
           ]
        } else {
           [
             #text(weight: "bold")[Ingredients]
             #v(0.5em)
             #ingredients
           ]
        }
      )
    ]
  )
}

// --- VERSO (LEFT PAGE) - SEMITIC LANGUAGES ---

#language_section(
  "מחמסה", // Hebrew Title
  [- 1  small onion
- 1 cup of ptitim (Israeli couscous)
- 1 tablespoon sweet paprika
- Black pepper to taste
- 1  chopped tomato
- Vegetables of your choice
- Water (1 and 1/4 cups for every cup of ptitim)],
  [+ For dry Mahmessa: Sauté a small onion until translucent.
+ Add the ptitim (Mahmessa) and continue to sauté for a few more minutes. Then, add water according to the instructions: 1 and 1/4 cups of water for every cup of ptitim.
+ For Mahmessa with sauce: Sauté a small onion until it starts to brown. Add 1 tablespoon of sweet paprika and sauté for a few seconds.
+ Add the chopped tomato and any vegetables you desire. Season with salt, black pepper, and add boiling water.
+ Stir in the ptitim.
+ Bring to a boil, then reduce the heat, cover partially, and simmer until cooked through.],
  "The name \"Mahmessa\" (מחמסה) is believed to derive from Arabic or Maghrebi language origins, possibly linked to root words relating to mixing or a type of small pasta/grain[3]. In similar North African semitic dialects, such as the roots of “hamsa/khamsa,” the term relates to “five,” but in the context of food, extensions of this root or similar-sounding terms sometimes point toward grain shapes or actions like “to mix” or “to stew.” There is also a symbolic resonance with protection and abundanc Mahmessa (מחמסה) is a traditional dish with roots in the Tunisian and Djerban Jewish communities, reflecting their unique blend of North African Jewish culinary traditions[6][13]. Jews have lived in Tunisia, including the island of Djerba, for more than 2,000 years, establishing deeply distinct cultural and foodways. While direct historical documentation specifically naming Mahmessa is limited, it Mahmessa is a traditional dish enjoyed in Tunisian-Djerban Jewish cuisine, often customized with various vegetables based on personal preference.",
  rtl,
  "Arial" // Placeholder for Hebrew font
)

#v(1fr) // Spacer

#language_section(
  "المحمسة", // Arabic Title
  [- 1  small onion
- 1 cup of ptitim (Israeli couscous)
- 1 tablespoon sweet paprika
- Black pepper to taste
- 1  chopped tomato
- Vegetables of your choice
- Water (1 and 1/4 cups for every cup of ptitim)],
  [+ For dry Mahmessa: Sauté a small onion until translucent.
+ Add the ptitim (Mahmessa) and continue to sauté for a few more minutes. Then, add water according to the instructions: 1 and 1/4 cups of water for every cup of ptitim.
+ For Mahmessa with sauce: Sauté a small onion until it starts to brown. Add 1 tablespoon of sweet paprika and sauté for a few seconds.
+ Add the chopped tomato and any vegetables you desire. Season with salt, black pepper, and add boiling water.
+ Stir in the ptitim.
+ Bring to a boil, then reduce the heat, cover partially, and simmer until cooked through.],
  "The name \"Mahmessa\" (מחמסה) is believed to derive from Arabic or Maghrebi language origins, possibly linked to root words relating to mixing or a type of small pasta/grain[3]. In similar North African semitic dialects, such as the roots of “hamsa/khamsa,” the term relates to “five,” but in the context of food, extensions of this root or similar-sounding terms sometimes point toward grain shapes or actions like “to mix” or “to stew.” There is also a symbolic resonance with protection and abundanc Mahmessa (מחמסה) is a traditional dish with roots in the Tunisian and Djerban Jewish communities, reflecting their unique blend of North African Jewish culinary traditions[6][13]. Jews have lived in Tunisia, including the island of Djerba, for more than 2,000 years, establishing deeply distinct cultural and foodways. While direct historical documentation specifically naming Mahmessa is limited, it Mahmessa is a traditional dish enjoyed in Tunisian-Djerban Jewish cuisine, often customized with various vegetables based on personal preference.",
  rtl,
  "Arial" // Placeholder for Arabic font
)

#pagebreak()

// --- RECTO (RIGHT PAGE) - EUROPEAN LANGUAGES ---

#language_section(
  "Mahmessa", // English Title
  [- 1  small onion
- 1 cup of ptitim (Israeli couscous)
- 1 tablespoon sweet paprika
- Black pepper to taste
- 1  chopped tomato
- Vegetables of your choice
- Water (1 and 1/4 cups for every cup of ptitim)],
  [+ For dry Mahmessa: Sauté a small onion until translucent.
+ Add the ptitim (Mahmessa) and continue to sauté for a few more minutes. Then, add water according to the instructions: 1 and 1/4 cups of water for every cup of ptitim.
+ For Mahmessa with sauce: Sauté a small onion until it starts to brown. Add 1 tablespoon of sweet paprika and sauté for a few seconds.
+ Add the chopped tomato and any vegetables you desire. Season with salt, black pepper, and add boiling water.
+ Stir in the ptitim.
+ Bring to a boil, then reduce the heat, cover partially, and simmer until cooked through.],
  "The name \"Mahmessa\" (מחמסה) is believed to derive from Arabic or Maghrebi language origins, possibly linked to root words relating to mixing or a type of small pasta/grain[3]. In similar North African semitic dialects, such as the roots of “hamsa/khamsa,” the term relates to “five,” but in the context of food, extensions of this root or similar-sounding terms sometimes point toward grain shapes or actions like “to mix” or “to stew.” There is also a symbolic resonance with protection and abundanc Mahmessa (מחמסה) is a traditional dish with roots in the Tunisian and Djerban Jewish communities, reflecting their unique blend of North African Jewish culinary traditions[6][13]. Jews have lived in Tunisia, including the island of Djerba, for more than 2,000 years, establishing deeply distinct cultural and foodways. While direct historical documentation specifically naming Mahmessa is limited, it Mahmessa is a traditional dish enjoyed in Tunisian-Djerban Jewish cuisine, often customized with various vegetables based on personal preference.",
  ltr,
  "Times New Roman"
)

#v(1fr)

#language_section(
  "Mahmessa", // Spanish Title
  [- 1  small onion
- 1 cup of ptitim (Israeli couscous)
- 1 tablespoon sweet paprika
- Black pepper to taste
- 1  chopped tomato
- Vegetables of your choice
- Water (1 and 1/4 cups for every cup of ptitim)],
  [+ For dry Mahmessa: Sauté a small onion until translucent.
+ Add the ptitim (Mahmessa) and continue to sauté for a few more minutes. Then, add water according to the instructions: 1 and 1/4 cups of water for every cup of ptitim.
+ For Mahmessa with sauce: Sauté a small onion until it starts to brown. Add 1 tablespoon of sweet paprika and sauté for a few seconds.
+ Add the chopped tomato and any vegetables you desire. Season with salt, black pepper, and add boiling water.
+ Stir in the ptitim.
+ Bring to a boil, then reduce the heat, cover partially, and simmer until cooked through.],
  "The name \"Mahmessa\" (מחמסה) is believed to derive from Arabic or Maghrebi language origins, possibly linked to root words relating to mixing or a type of small pasta/grain[3]. In similar North African semitic dialects, such as the roots of “hamsa/khamsa,” the term relates to “five,” but in the context of food, extensions of this root or similar-sounding terms sometimes point toward grain shapes or actions like “to mix” or “to stew.” There is also a symbolic resonance with protection and abundanc Mahmessa (מחמסה) is a traditional dish with roots in the Tunisian and Djerban Jewish communities, reflecting their unique blend of North African Jewish culinary traditions[6][13]. Jews have lived in Tunisia, including the island of Djerba, for more than 2,000 years, establishing deeply distinct cultural and foodways. While direct historical documentation specifically naming Mahmessa is limited, it Mahmessa is a traditional dish enjoyed in Tunisian-Djerban Jewish cuisine, often customized with various vegetables based on personal preference.",
  ltr,
  "Times New Roman"
)

