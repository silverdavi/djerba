#import "config.typ": *
#import "template.typ": *

#set document(title: cookbook-title, author: cookbook-author)
#set page(
  paper: "a4",
  margin: (left: 2cm, right: 2cm, top: 2cm, bottom: 2cm),
  header: align(right, text(size: 9pt, fill: gray, "Djerban Jewish Recipes")),
  footer: context align(center, text(size: 9pt, fill: gray, counter(page).display())),
)

#set text(font: "Georgia", size: 11pt, lang: "en")
#set heading(numbering: "1.1")

// Title Page
#page(
  header: none,
  footer: none,
)[
  #align(center, v(3cm))
  #align(center)[
    #heading(level: 1, "Recipes from Djerba")
    #text(size: 20pt, weight: "bold", "A Tunisian-Jewish Family Cookbook")
    
    #v(1cm)
    
    #text(size: 14pt, "Collected from the Safed Family")
    
    #v(2cm)
    
    #text(size: 12pt, "Traditional recipes preserved and translated for contemporary kitchens")
  ]
]

// Table of Contents
#pagebreak()
#outline(depth: 2, indent: 1em)

// Introduction
#pagebreak()
= Introduction

This cookbook preserves the culinary heritage of Tunisian-Djerban Jewish cuisine. Each recipe has been carefully researched and documented to honor the traditions of the Safed family and the broader Djerban Jewish community.

The island of Djerba has been home to one of the oldest Jewish communities in the world, dating back over two millennia. This cookbook celebrates the rich food traditions that have sustained this community through generations.

== About These Recipes

- All recipes are vegetarian-adaptable
- Traditional cooking methods are preserved
- Historical and cultural context is provided
- Ingredient substitutions and modern adaptations are suggested

== Structure of Each Recipe

Each recipe in this collection includes:
- **Name**: In English and Hebrew
- **Ingredients**: With traditional and modern measurements
- **Instructions**: Step-by-step preparation
- **Serves**: Number of servings
- **Time**: Preparation and cooking time
- **Cultural Notes**: Historical and traditional significance

// Recipes will be inserted here
#include "recipes-content.typ"

// Back Matter
#pagebreak()
= Appendices

== Ingredient Glossary

#table(
  columns: (1fr, 2fr),
  [*Ingredient*], [*Description*],
  [Harissa], [Spicy red pepper paste, fundamental to North African cuisine],
  [Malsouka], [Thin pastry sheets used in Brik and similar pastries],
  [Ptitim], [Israeli couscous, small pearls of wheat],
  [Caraway], [Seed spice with warm, slightly citrusy flavor, common in Maghrebi cooking],
  [Durum Wheat], [Hard wheat used for traditional couscous and pasta],
)

== Spice Profiles

=== Classic Maghrebi Spice Blend
- Caraway seeds
- Coriander
- Cumin
- Paprika (sweet and spicy)
- Cinnamon
- Ground coriander
- Turmeric
- Ground ginger
- Black pepper

== Bibliography & Sources

The recipes and historical information in this cookbook have been researched using:
- Family oral traditions from the Safed family
- Perplexity Pro Search with multi-step research
- Academic sources on North African and Jewish cuisine
- Historical documentation of Djerban Jewish culture

---

#align(center, text(size: 10pt, fill: gray, "Prepared with gratitude to the Safed family and the Djerban Jewish community"))

