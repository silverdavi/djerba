// Recipe Template and Styling Functions

#import "config.typ": *

// Recipe Card Template
#let recipe(
  name,
  name_hebrew,
  serves: "",
  prep_time: "",
  cook_time: "",
  ingredients: (),
  instructions: (),
  notes: "",
  category: "Main Course"
) = {
  
  // Recipe Header
  heading(level: 2, name)
  
  text(size: 11pt, style: "italic", name_hebrew)
  
  // Meta information box
  grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 1em,
    [
      #text(size: 9pt, weight: "bold", "Category")
      #text(size: 10pt, category)
    ],
    [
      #text(size: 9pt, weight: "bold", "Serves")
      #text(size: 10pt, serves)
    ],
    [
      #text(size: 9pt, weight: "bold", "Time")
      #text(size: 10pt, prep_time + " / " + cook_time)
    ],
  )
  
  v(0.5cm)
  
  // Ingredients
  heading(level: 3, "Ingredients")
  list(
    ..ingredients.map(i => i)
  )
  
  v(0.3cm)
  
  // Instructions
  heading(level: 3, "Instructions")
  enum(
    ..instructions.map(step => step)
  )
  
  // Notes
  if notes != "" {
    v(0.3cm)
    block(
      fill: rgb("#f0f0f0"),
      inset: 0.5cm,
      radius: 4pt,
      [
        #text(size: 9pt, weight: "bold", "Notes: ")
        #text(size: 10pt, notes)
      ]
    )
  }
  
  v(1cm)
  pagebreak()
}

// Ingredient List Helper
#let ingredient(name, amount: "", unit: "") = {
  if amount != "" and unit != "" {
    name + " (" + amount + " " + unit + ")"
  } else if amount != "" {
    name + " - " + amount
  } else {
    name
  }
}

// Instruction Step Helper
#let step(text) = text

// Section with styling
#let recipe-section(title) = {
  heading(level: 2, title)
  v(0.5cm)
}

// Info box for cultural notes
#let cultural-note(title, content) = {
  block(
    fill: rgb("#e8f4f8"),
    inset: 0.8cm,
    radius: 4pt,
    [
      #text(size: 10pt, weight: "bold", title)
      
      #v(0.3cm)
      
      #text(size: 10pt, content)
    ]
  )
}

// Variation box
#let variation(title, content) = {
  block(
    fill: rgb("#fff8e8"),
    inset: 0.8cm,
    radius: 4pt,
    [
      #text(size: 10pt, weight: "bold", "Variation: " + title)
      
      #v(0.3cm)
      
      #text(size: 10pt, content)
    ]
  )
}

// Tips box
#let cooking-tip(tip) = {
  block(
    fill: rgb("#f0e8ff"),
    inset: 0.8cm,
    radius: 4pt,
    [
      #text(size: 9pt, "💡 Tip: " + tip)
    ]
  )
}

