// ELEGANT QUADRANT LAYOUT
// A sophisticated 4-language spread with equal treatment for all languages.

// ===== SETUP =====
#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 1.5cm, left: 1.5cm, right: 1.5cm),
  header: none,
  footer: none
)

// Fonts - Using standard available fonts for reliability
#set text(font: ("Times New Roman", "David", "Arial"), size: 10pt, fill: rgb("#202020"))

// Colors
#let border_color = rgb("#dddddd")
#let accent_color = rgb("#8B4513") // Subtle elegant brown for titles

// ===== LAYOUT FUNCTIONS =====

// A single language block (half page)
#let language_block(
  title,
  ingredients,
  instructions,
  story,
  direction: "ltr", // "ltr" or "rtl"
  font_family: "Times New Roman"
) = {
  set text(font: font_family, dir: if direction == "rtl" { rtl } else { ltr })
  
  block(
    height: 48%, // Takes up slightly less than half page to allow for spacing
    width: 100%,
    inset: (x: 1em, y: 1em),
    stroke: (bottom: 0.5pt + border_color), // Subtle divider
    [
      // TITLE
      #align(center)[
        #text(size: 16pt, weight: "bold", fill: accent_color, title)
      ]
      #v(0.5em)
      
      // CONTENT GRID
      #grid(
        columns: if direction == "rtl" { (2fr, 1fr) } else { (1fr, 2fr) }, // Ingredients on outer edge? Or inner? Let's do standard: Ingredients side, Body main.
        gutter: 1.5em,
        
        // INGREDIENTS COLUMN (Narrower)
        if direction == "ltr" {
           align(left)[
            #text(size: 9pt, weight: "bold", upper("Ingredients"))
            #v(0.5em)
            #set text(size: 9pt)
            #ingredients
          ]
        } else {
           align(right)[
            // In RTL, this is the Main Body slot (2fr)
            #text(size: 9pt, weight: "bold", "הוראות הכנה") // Instructions Header
            #v(0.5em)
            #instructions
            
            #v(1em)
            #line(length: 30%, stroke: 0.5pt + border_color)
            #v(0.5em)
            
            #text(style: "italic", story)
          ]
        },
        
        // MAIN BODY COLUMN (Wider)
        if direction == "ltr" {
          align(left)[
            #text(size: 9pt, weight: "bold", upper("Preparation"))
            #v(0.5em)
            #instructions
            
            #v(1em)
            #line(length: 30%, stroke: 0.5pt + border_color)
            #v(0.5em)
            
            #text(style: "italic", story)
          ]
        } else {
          align(right)[
            // In RTL, this is the Ingredients slot (1fr)
            #text(size: 9pt, weight: "bold", "מצרכים") // Ingredients Header
            #v(0.5em)
            #set text(size: 9pt)
            #ingredients
          ]
        }
      )
    ]
  )
}

// ===== GENERATED CONTENT START =====
// This part will be populated by the Python script

