# Translation Quality Review

## Overview
Automated review of all recipe text across 4 languages using Gemini 3.1 Pro.

## Goals
- Verify each language reads naturally to a native speaker
- Fix awkward phrasing, transliterations that don't work (e.g., "TVP (חלבון סויה מרקם)")
- Ensure cultural terms are used correctly per language
- Keep original length/meaning intact
- Fix minor grammar/spelling issues

## Process
1. Backup all recipe JSONs before changes
2. Send each recipe to Gemini 3.1 Pro for review (30-40 parallel workers)
3. Model reviews all 4 languages and returns corrected versions
4. Apply fixes, log all changes
5. Rebuild cookbook

## Status
- [ ] Backup created
- [ ] Review script written
- [ ] Review executed (87 recipes × 4 languages)
- [ ] Changes applied
- [ ] Manual spot-check
- [ ] Rebuild & deploy

## Change Log
_(populated after review runs)_


## Run Results (2026-02-20 23:03)
- Recipes reviewed: 87
- Successful: 20
- Errors: 67
- Total changes: 231
- Duration: 258.9s

### Changes Summary

**artichokemushroomsstew** (14 changes):
- `name.he`: Added 'תבשיל' (stew) to match the English name and accurately describe the dish.
- `description.he`: Fixed translation error ('דליל' means thin/watery, changed to 'עשיר' for rich) and added niqqud to Enny's name so it isn't read as 'I' (ani).
- `steps.he[2]`: Changed 'artichoke' to 'artichoke hearts' to match the ingredients list.
- `description.ar`: Changed 'light broth' to 'rich/thick sauce' to match the original meaning, using authentic Tunisian term 'خاثرة'.
- `ingredients.ar[0]`: Specified tablespoons (كبار) for clarity.
- `ingredients.ar[1]`: Used 'مهرسين' (crushed/minced) instead of 'مرحيين' (ground/powdered) which is more accurate for fresh garlic.
- `ingredients.ar[5]`: Specified tablespoons and 'freshly squeezed'.
- `ingredients.ar[7]`: Fixed phrasing for '5 1/2 cups' and specified 'quartered'.
- `ingredients.ar[8]`: Fixed phrasing for '2 1/3 cups' and specified 'artichoke hearts, quartered'.
- `steps.ar[0]`: Corrected spelling of frying pan in Tunisian dialect.
- `steps.ar[1]`: Replaced literal translation 'seasoned base' with a more natural culinary phrase.
- `steps.ar[4]`: Replaced awkward phrasing 'put in the plates' with 'before serving'.
- `description.es`: Improved natural phrasing ('sustancioso' instead of 'abundante', 'combina' instead of 'presenta').
- `steps.es[0]`: Used a more natural Spanish culinary phrase for 'until fragrant'.

**chickenfricasseestew** (22 changes):
- `name.he`: Match the full descriptive name used in English and Spanish
- `name.ar`: Match the full descriptive name used in English and Spanish
- `description.he`: Fix literal translations to sound more natural in Hebrew
- `ingredients.en`: Fix awkward measurement (1.1 cups)
- `ingredients.he`: Use standard volume measurements and fix phrasing
- `ingredients.he`: Fix repetitive phrasing
- `ingredients.he`: Fix awkward translation
- `ingredients.he`: Standardize flour measurement
- `ingredients.es`: Use standard volume measurements
- `ingredients.es`: Fix repetitive phrasing
- `ingredients.es`: Standardize flour measurement
- `ingredients.ar`: Clarify tablespoon size
- `ingredients.ar`: Fix repetitive phrasing
- `ingredients.ar`: Fix awkward measurement
- `steps.en`: Remove awkward slash option
- `steps.en`: Improve phrasing for dropping batter
- `steps.he`: Fix incorrect cooking term (steaming vs sautéing)
- `steps.he`: Fix incorrect cooking term
- `steps.he`: Improve flow and natural phrasing
- `steps.es`: Clarify liquid used for batter
- `steps.ar`: Improve dialect phrasing for dumplings
- `steps.ar`: Improve dialect phrasing for plural

**ciceritos** (11 changes):
- `description.he`: Changed 'plant-based' translation to sound more natural in Hebrew.
- `ingredients.he`: Converted metric measurements to standard volume measurements for natural cookbook reading.
- `steps.he`: Improved phrasing for frying until fragrant and mixing.
- `description.es`: Adapted vocabulary for Latin American Spanish and improved natural flow.
- `ingredients.es`: Converted metric measurements to standard volume measurements and used Latin American terms.
- `steps.es`: Changed 'Freír' to 'Sofreír' and improved mixing instructions.
- `description.ar`: Replaced literal translations with authentic Tunisian idioms.
- `ingredients.ar`: Clarified spoon sizes and canned pea phrasing.
- `steps.ar`: Minor grammatical tweak for reducing heat.
- `ingredients.en`: Changed decimal to fraction for standard recipe format.
- `steps.en`: Changed 'Fry' to 'Sauté' for better culinary terminology.

**dabikh_hagim** (20 changes):
- `description.ar`: Fixed Hebrew characters accidentally mixed into the Arabic word for parsley
- `description.es`: Improved natural phrasing
- `description.en`: Added missing word for better flow
- `ingredients.he`: Changed 'optional' to proper Hebrew cookbook term 'rashut', fixed redundant seitan chunks phrasing
- `ingredients.he`: Changed 'optional' to proper Hebrew cookbook term 'rashut'
- `ingredients.he`: Fixed redundant phrasing for seitan chunks
- `ingredients.ar`: Fixed Hebrew characters in parsley, used more natural Maghrebi word for cilantro
- `ingredients.ar`: Used more natural Maghrebi word for cilantro
- `ingredients.es`: Improved culinary terms and fixed redundant phrasing
- `ingredients.es`: Fixed redundant phrasing for seitan chunks
- `ingredients.en`: Fixed redundant phrasing for seitan chunks and improved frying term
- `ingredients.en`: Fixed redundant phrasing for seitan chunks
- `steps.he`: Improved natural phrasing for sautéing instead of steaming onions
- `steps.ar`: Used correct Tunisian term for sautéing instead of seasoning
- `steps.es`: Fixed awkward literal translation of 'steam/sauté' and 'soft' potatoes
- `steps.es`: Fixed awkward literal translation of 'steam together'
- `steps.es`: Used better culinary term for cooked potatoes
- `steps.en`: Fixed awkward 'steam/sauté' phrasing and 'soft' potatoes
- `steps.en`: Fixed awkward 'steam together' phrasing
- `steps.en`: Used better culinary term for cooked potatoes

**french_toast** (12 changes):
- `name.he`: Added the French name in parentheses to match the format of the other languages.
- `description.he`: Improved natural phrasing. 'כיכרות לחם יבשות' is less natural than 'שאריות לחם יבש'. 'מבוססי צמחים' is a literal translation; 'מהצומח' is the correct Hebrew culinary term.
- `ingredients.he`: Changed 'לפי הטעם' (to taste) to 'לפי הצורך' (as needed) since it refers to frying fat.
- `steps.he`: Improved phrasing for serving suggestions.
- `description.ar`: Used authentic Tunisian vocabulary ('فرينة' instead of 'دقيق') and improved the phrasing for plant-based kitchen.
- `ingredients.ar`: Fixed awkward measurements (0.6 cups), used Tunisian terms ('فرينة', 'زيت كوكو', 'خشان'), and changed 'حسب الذوق' to 'للقلي'.
- `steps.ar`: Replaced MSA/awkward terms with Tunisian dialect ('فرينة', 'القلاية', 'الشيرتين', 'سيرو' instead of honey for vegan).
- `description.es`: Changed 'masa' (dough) to 'batido' (batter) for accuracy.
- `ingredients.es`: Improved natural phrasing and word order. Changed 'al gusto' to 'para freír'.
- `steps.es`: Improved culinary terms ('integrados', 'batido', 'sirope').
- `ingredients.en`: Fixed awkward '0.6 cups' measurement, improved phrasing for pinch and slices, and changed 'to taste' to 'for frying'.
- `steps.en`: Changed 'mixture' to 'batter' for consistency with the description.

**greenbeanstomato_sauce** (9 changes):
- `description.he`: Fixed awkward phrasing for better flow in Hebrew.
- `ingredients.he`: Converted metric measurements to standard culinary spoons for oil and spices; fixed phrasing.
- `steps.he`: Fixed spelling of tomato and removed definite article from garlic for natural flow.
- `description.ar`: Replaced MSA and non-Tunisian terms with authentic Tunisian dialect.
- `ingredients.ar`: Used authentic Tunisian culinary terms and fixed awkward phrasing.
- `steps.ar`: Adjusted verbs and vocabulary for natural Tunisian flow.
- `ingredients.es`: Used precise culinary term (despuntadas) and converted small metric amounts to spoons.
- `description.en`: Improved flow of the blooming spices sentence.
- `ingredients.en`: Fixed awkward phrasing and unnatural measurements.

**honeycakelior_benmosheh** (10 changes):
- `name.he`: Added 'של' for natural possession and adjusted the translation of 'Date Honey' to be more natural.
- `description.he`: Changed 'ויוצרת' to 'ומהווה' for more natural phrasing in Hebrew.
- `ingredients.he`: Changed 'קמח רגיל' to 'קמח לבן' which is the standard term in Israeli baking.
- `steps.he`: 'בקערת ערבוב' is a bit literal; 'בקערה' is much more natural.
- `name.ar`: Used 'متاع' instead of 'لـ' for natural Tunisian possession.
- `description.ar`: Changed 'تبديلة' to 'نسخة' and 'مثالي' to 'هايل' for better Maghrebi flow.
- `ingredients.ar`: Replaced vague 'وشوية' with precise 'ومغرفة كبيرة' to match the English recipe, and added maple syrup to the brushing options.
- `steps.ar`: Fixed a Hebrew letter (ל) that crept into the Arabic text, and replaced 'عسل' with 'سيرو ديرابل' to keep the recipe vegan.
- `description.es`: Changed 'pan' to 'bizcocho' as 'pan' implies bread, whereas this is a cake/loaf cake.
- `ingredients.es`: Changed 'harina común' to 'harina de trigo (todo uso)' for broader Latin American clarity.

**kugel** (9 changes):
- `description.he`: Fixed awkward phrasing and grammar ('שם נגזר' -> 'ששמו נגזר', 'הכנת המנה כללה' -> 'המנה מכילה')
- `ingredients.he`: Fixed construct state grammar
- `steps.he`: Fixed grammar ('קמח התפוחי אדמה' -> 'קמח תפוחי האדמה') and dangerous translation error ('תנור פתוח' means open oven door, changed to 'ללא כיסוי' meaning uncovered)
- `description.es`: Improved natural phrasing
- `steps.es`: Fixed literal translation errors ('caramelo fresco' -> 'caramelo caliente', 'horno abierto' -> 'sin tapar', 'cake inglés' -> 'pan/budín')
- `description.ar`: Converted MSA to authentic Tunisian dialect
- `ingredients.ar`: Used Tunisian terms (جويدة for thin, شطر for half, تطييب for cooking)
- `steps.ar`: Translated to natural Tunisian dialect and fixed 'open oven' error
- `steps.en`: Fixed literal translation errors ('fresh caramel' -> 'hot caramel', 'English cake pans' -> 'loaf pans', 'open oven' -> 'uncovered')

**lintriya** (11 changes):
- `name.he`: Spelling consistency with the description
- `description.he`: Fixed awkward phrasing ('ערבית ימי-ביניימית', 'קוגנט', 'מוטגנות') and improved flow
- `ingredients.he`: More accurate translation of vegetable bouillon
- `steps.he`: Improved culinary terms ('מזהיבות' instead of 'משחימות') and flow
- `description.ar`: Replaced MSA with natural Tunisian/Maghrebi dialect terms
- `ingredients.ar`: Adjusted to natural Maghrebi phrasing and measurements
- `steps.ar`: Replaced MSA verbs and adjectives with Maghrebi dialect
- `description.es`: Improved flow and replaced 'cognado' with more natural phrasing
- `ingredients.es`: Added standard abbreviation periods and clarified bouillon
- `description.en`: Fixed awkward phrasing ('before cooking until') and prepositions
- `steps.en`: Added definite articles for smoother reading

**pancakes_soly** (11 changes):
- `description.he`: Improved natural phrasing and grammar
- `description.es`: Improved natural phrasing and correct kosher terminology
- `description.ar`: Replaced MSA/awkward words with natural Tunisian dialect
- `description.en`: Corrected kosher terminology spelling
- `ingredients.he`: Pinch of salt is more standard for baking than 'salt to taste'
- `ingredients.es`: Clarified flaxseed ingredient and salt measurement
- `ingredients.ar`: Used natural Tunisian measurements and clarified ingredients
- `ingredients.en`: Standardized fraction measurements for recipes
- `steps.he`: Fixed literal translations to standard Hebrew cooking terms
- `steps.es`: Used standard culinary Spanish for mixing
- `steps.ar`: Used natural Tunisian phrasing for cooking steps

**red_sauce_meatballs** (13 changes):
- `description.he`: More natural phrasing for plant-based ground meat and binding
- `ingredients.he`: Standardized terminology for plant-based meat, soup powder, and bread prep
- `steps.he`: Improved flow and clarity for mixing and shaping
- `name.ar`: Used authentic Tunisian term for meatballs in sauce
- `description.ar`: Adjusted to natural Tunisian dialect phrasing
- `ingredients.ar`: Corrected measurements and authentic Tunisian ingredient names
- `steps.ar`: Authentic Tunisian cooking verbs and expressions
- `description.es`: More natural culinary phrasing for binding
- `ingredients.es`: Standardized bouillon measurement to match other languages and improved bread description
- `steps.es`: Better culinary terms for mixing and shaping
- `description.en`: Improved flow and natural phrasing
- `ingredients.en`: Standardized bouillon measurement and clarified bread prep
- `steps.en`: Better flow and culinary terminology

**schnitzel** (12 changes):
- `description.he`: Improved phrasing for natural Hebrew flow. 'מגיע מהמילה' is a literal translation; 'מקור המילה' is better. Fixed 'זה נשאר מועדף' to 'הוא נשאר מנה אהובה'.
- `description.es`: Improved natural phrasing. 'Ave' changed to 'pollo' as it's more common for schnitzel. 'Un favorito' changed to 'uno de los platos favoritos'.
- `description.ar`: Fixed adjective agreement ('فريشكة' instead of 'فريشك') and improved flow.
- `description.en`: Improved flow and punctuation.
- `ingredients.he`: Fixed plural agreement ('פרוסים'), clarified flour type, and changed 'לפי הצורך' to 'לטיגון' for oil.
- `ingredients.es`: Removed redundant 'filetes de', clarified flour, and fixed oil description ('al gusto' is incorrect for frying oil).
- `ingredients.ar`: Improved dialect phrasing and fixed oil description.
- `ingredients.en`: Fixed capitalization, standardized fraction formats for cups, and clarified oil usage.
- `steps.he`: Improved culinary terminology and flow. Changed 'צלחות נפרדות' to 'קערות או צלחות עמוקות'.
- `steps.es`: Changed 'Golpee' to 'Aplane', 'rebozado' to 'empanizado', and improved overall flow.
- `steps.ar`: Fixed gender agreement for 'طرف' (masculine) and used better plural for plates ('صحنة').
- `steps.en`: Improved cookbook terminology ('dredging station with three shallow bowls', 'Dredge each cutlet').

**semolina_porridge** (7 changes):
- `description.he`: Fixed unnatural phrasing ('פודינג בחוש' and 'מאכל בוקר חלק')
- `ingredients.he`: Used standard Hebrew culinary term for 'optional'
- `description.es`: Fixed awkward literal translations ('pudín revuelto', 'desayuno suave terminado')
- `description.ar`: Removed Hebrew characters from Arabic text, fixed repetition of 'رطب', and improved natural flow
- `ingredients.ar`: Fixed unnatural machine-translated measurements (2.1 cups, 1.2 tbsp) to standard Maghrebi terms
- `description.en`: Fixed illogical phrasing ('this porridge means' -> 'the name of this porridge means')
- `ingredients.en`: Fixed awkward decimal measurements (2.1 cups, 1.2 tbsp)

**shakshukacaramelizedonion_sausage** (11 changes):
- `name.he`: Awkward phrasing. 'בצל מטוגן ארוך' is unnatural. Changed to match the English meaning.
- `name.es`: Adjusted preposition to match the English 'with' and sound more natural.
- `description.he`: Improved flow and phrasing to sound like natural Israeli Hebrew.
- `description.es`: Improved flow and natural phrasing.
- `description.ar`: Fixed Hebrew letter 'פ' that crept into the Arabic word for Tofu.
- `description.en`: Minor phrasing improvements for better cookbook flow.
- `ingredients.ar`: Fixed Hebrew letter 'פ' in Tofu.
- `steps.he`: Improved natural phrasing and culinary terms.
- `steps.es`: Removed clunky 'durante mucho tiempo' and improved culinary verbs.
- `steps.ar`: Fixed Hebrew letter 'פ' in Tofu, changed 'طنجرة' (pot) to 'مقلة' (pan) which is accurate for Shakshuka, and used more natural Tunisian phrasing.
- `steps.en`: Replaced 'fry... for a long time' with 'sauté' for better cookbook style.

**shlomit_perl_dressing** (12 changes):
- `description.he`: Improved natural phrasing and flow
- `steps.he[1]`: More natural cookbook phrasing in Hebrew
- `steps.he[3]`: Better phrasing for serving suggestion
- `description.ar`: Fixed weird translation 'جويجات' (little chickens) to 'سناك' (snacks) and improved Tunisian phrasing
- `ingredients.ar`: Clarified spoon sizes (tablespoon vs teaspoon) for accuracy in Tunisian Arabic
- `steps.ar[2]`: More natural Tunisian phrasing
- `steps.ar[3]`: Improved flow and vocabulary for Tunisian dialect
- `description.es`: Changed 'versión vegetal' to 'versión a base de plantas' for better culinary accuracy
- `steps.es[3]`: Changed 'cebollas verdes' to 'cebollín' which is more widely used in Latin American Spanish
- `description.en`: Matched the title name in the description
- `steps.en[2]`: Smoothed out the tip phrasing to match the tone of the other languages
- `steps.en[3]`: Corrected 'purple cabbage' to the standard culinary term 'red cabbage' and improved phrasing

**spice_mixes** (8 changes):
- `description.he`: Fixed awkward phrasing ('שואבות את שמן' to 'נקראות על שם', 'הפרופילים המלוחים' to 'פרופילי הטעם העשירים')
- `steps.he[2]`: Changed 'מקושקשת טופו' to the more natural 'טופו מקושקש'
- `description.es`: Changed 'perfiles sabrosos' to 'perfiles de sabor' for better culinary flow
- `steps.es`: Standardized casing (removed ALL CAPS), changed 'Combine' to 'Mezcle' for natural Spanish, and fixed gender agreement ('Úsela')
- `description.ar`: Fixed Hebrew letter typo in Arabic word ('يبנنوها' -> 'يبننوها'), changed 'الجبن' to 'الحليب' to match dairy, and made the ending more naturally Tunisian
- `ingredients.ar`: Clarified spoon sizes (tbsp vs tsp) and used standard Tunisian fractions ('شطر' instead of '1/2')
- `ingredients.en`: Changed decimal fractions to standard cookbook fractions
- `steps.en`: Standardized casing (removed ALL CAPS) and added missing articles for better flow

**sufganiyot** (7 changes):
- `description.he`: Fixed awkward phrasing ('מקבלות את שמן', 'יוצרת עיגולים') and unnatural passive voice ('נאכלות', 'מפודרות') to sound like authentic Israeli cookbook Hebrew.
- `ingredients.he`: Changed decimal to fraction for standard cookbook format and removed unnecessary comma.
- `description.es`: Fixed literal translation 'rondas' to 'bollos', changed 'Hanukkah' to the standard Spanish 'Jánuca', and specified 'azúcar glas'.
- `ingredients.es`: Changed decimal to fraction for standard cookbook format.
- `description.en`: Specified 'powdered sugar' instead of just 'sugar' for accuracy.
- `ingredients.en`: Changed decimal to fraction and fixed capitalization of spirits.
- `ingredients.ar`: Made measurements more precise in Tunisian dialect (added 'كبيرة' for tablespoon, 'شايحة' for dry yeast) and adjusted 'لتر' to 'ليترا'.

**tfina_stew** (11 changes):
- `description.he`: Improved etymology phrasing and changed 'rich seitan' to 'hearty/meaty seitan' which fits the context better.
- `ingredients.he`: Changed 1000g to 1 kg for natural cookbook phrasing.
- `steps.he`: Improved flow and translated 'simmer' more accurately.
- `ingredients.ar`: Fixed awkward decimal measurement (1.2 tbsp) to natural phrasing, and used authentic Tunisian terms for quantities.
- `steps.ar`: Replaced MSA/awkward phrasing with authentic Tunisian dialect ('عس عليه بالباهي' for 'watch carefully').
- `description.es`: Specified 'carne de res' for beef to match the English original.
- `ingredients.es`: Changed 1000g to 1 kg for standard recipe formatting.
- `steps.es`: Fixed 'cocine al vapor' which implies using a steamer, changing to cooking in its own juices.
- `description.en`: Added missing comma for better readability.
- `ingredients.en`: Removed redundant 'chunks' and fixed unnatural decimal tablespoon measurement.
- `steps.en`: Improved phrasing for steaming in own juices.

**vegancaesardressing** (10 changes):
- `description.he`: Fixed 'מי מלח' to 'מי צלפים' (caper brine) and improved phrasing for 'savory' to sound more natural.
- `ingredients.he`: Removed unnecessary comma.
- `steps.he`: Improved verbs and phrasing to match standard Israeli cookbook style.
- `description.es`: Translated 'plant-based adaptation' more accurately and changed 'salado' to 'sabroso' for 'savory'.
- `ingredients.es`: Fixed grammar for dried parsley and removed unnecessary comma.
- `steps.es`: Improved flow and grammar.
- `description.ar`: Replaced MSA phrasing with natural Tunisian dialect.
- `ingredients.ar`: Replaced numbers with natural Tunisian dialect words (زوز, شطر, ونص).
- `steps.ar`: Replaced MSA words with Tunisian dialect (روبو, كان لزم).
- `steps.en`: Capitalized Dijon.

**yoyotunisiandoughnuts** (11 changes):
- `description.he`: Fixed gender agreement and phrasing
- `description.es`: Changed 'festín' to 'delicia' for a more natural translation of 'treat'
- `description.ar`: Removed Hebrew characters that crept into the Arabic text
- `ingredients.he`: Converted small ml amounts to standard spoon measurements and 1000ml to 1 liter
- `ingredients.es`: Converted small ml amounts to standard spoon measurements and 1000ml to 1 litro
- `ingredients.ar`: Fixed Hebrew letter in Arabic word (קاطو -> ڨاطو) and fixed awkward 4.2 cups measurement
- `ingredients.en`: Fixed awkward 4.2 cups measurement
- `steps.he[0]`: Added missing baking powder to the first step
- `steps.es[0]`: Added missing baking powder to the first step
- `steps.ar[0]`: Added missing baking powder to the first step
- `steps.en[0]`: Added missing baking powder to the first step


## Run Results (2026-02-20 23:07)
- Recipes reviewed: 67
- Successful: 10
- Errors: 57
- Total changes: 96
- Duration: 182.1s

### Changes Summary

**adafinawheatside_dish** (6 changes):
- `ingredients.he`: Converted unnatural gram measurements for spices and oil into standard volume measurements (spoons/cups) typical for Israeli home cooking.
- `ingredients.es`: Converted gram measurements for spices and oil to standard culinary volume measurements (cucharadas/cucharaditas) for better readability.
- `steps.es`: Improved natural phrasing for caramelizing onions and tying the bag.
- `steps.ar`: Replaced MSA 'مقلاة' with the more authentic Tunisian 'قلاية'.
- `description.en`: Changed 'pudding' to 'side dish' as it is a more accurate culinary description for savory wheat berries.
- `steps.en`: Enhanced culinary vocabulary (skillet, sauté, caramelized) for professional cookbook tone.

**binasthicksourspicysoup** (8 changes):
- `description.he`: Improved flow and natural phrasing. Replaced awkward literal translation with natural Hebrew syntax.
- `steps.he`: Made cooking instructions more natural and professional.
- `description.ar`: Converted MSA to authentic Tunisian dialect (e.g., 'الزمني', 'مفوح', 'ولا').
- `steps.ar`: Used authentic Tunisian cooking terminology ('صحفة', 'ركض بالڨدا', 'تخثار', 'تسربي').
- `description.es`: Improved natural phrasing and flow in Spanish.
- `steps.es`: Removed awkward phrasing ('el agua principal') and improved clarity.
- `description.en`: Enhanced flow and readability for a professional cookbook tone.
- `steps.en`: Fixed awkward phrasing ('main water') and improved culinary terminology ('slurry', 'whisking').

**bread** (11 changes):
- `description.he`: Improved natural phrasing for cookbook style
- `ingredients.he`: Removed unnecessary commas and used standard metric notation
- `steps.he`: Used standard Hebrew baking terminology
- `description.es`: Improved translation and natural phrasing
- `ingredients.es`: Removed unnecessary commas
- `steps.es`: Improved natural culinary phrasing
- `description.ar`: Removed Hebrew characters from Arabic text and used more authentic Tunisian phrasing
- `ingredients.ar`: Used natural Tunisian fraction terms and specified spoon sizes
- `steps.ar`: Used authentic Tunisian baking vocabulary (تكشكش, تتكسل, من لوطة)
- `ingredients.en`: Used standard recipe fractions instead of decimals
- `steps.en`: Improved natural baking terminology

**dolce_de_leche_biscuits** (14 changes):
- `name.he`: In Israel, 'Dulce de Leche' is almost exclusively called 'ריבת חלב'.
- `description.he`: Changed to 'ריבת חלב' for natural Israeli phrasing.
- `ingredients.he`: Used 'פחית' (can) instead of 'קופסת' (box) for coconut cream, 'ריבת חלב' instead of 'דולצ׳ה דה לצ׳ה', and 'אינסטנט פודינג' which is the standard term.
- `steps.he`: Improved flow, used 'ריבת חלב', specified cm for diameter, and used 'יוצקים' (pour) instead of 'שופכים' (spill).
- `name.ar`: Used 'كيكة' instead of MSA 'كعكة'.
- `description.ar`: Replaced MSA terms with Tunisian dialect (من غير فور, شوكولاطة نوار, كرام كوكو).
- `ingredients.ar`: Used Tunisian measurements and terms (حكة for can, شطر for half, نوار for dark chocolate).
- `steps.ar`: Applied authentic Tunisian verbs and vocabulary (نحّيهم, افرشهم, طبق, كونجيلاتور).
- `description.es`: Minor flow improvements and added articles for natural phrasing.
- `ingredients.es`: Clarified 'pudín instantáneo' for no-bake recipes and added standard abbreviations.
- `steps.es`: Fixed grammar (el aceite), clarified pan size, and improved 'hasta derretir'.
- `description.en`: Improved sentence flow and grammar.
- `ingredients.en`: Clarified that it is instant pudding mix.
- `steps.en`: Enhanced culinary terminology (fold in, spread evenly, completely melted and smooth).

**dwida** (9 changes):
- `description.he`: Fixed literal translation of 'uses' and improved natural phrasing
- `steps.he`: Fixed tense consistency (הסמיך to מסמיך)
- `description.es`: More natural verb for pasta and better translation for plant-based
- `steps.es`: Changed 'salsa' to 'caldo' since it is a soup
- `ingredients.ar`: Standardized quantities to match metric measurements, replacing awkward cup fractions
- `description.ar`: Improved flow and authentic Tunisian phrasing
- `description.en`: Improved flow, punctuation, and phrasing
- `ingredients.en`: Standardized quantities to match other languages for clarity
- `steps.en`: Corrected 'sauce' to 'broth' as this is a soup

**greenpeasoup** (8 changes):
- `description.he`: Fixed literal translation of 'staple' and 'relies on' to sound like natural Israeli cookbook phrasing.
- `steps.he`: Changed infinitive verbs to plural present tense, which is the standard for Hebrew recipes.
- `description.es`: Adapted to Latin American Spanish ('arvejas') and improved flow.
- `steps.es`: Used more common Latin American culinary terms ('licuadora de inmersión', 'arvejas').
- `description.ar`: Removed awkward phrasing and incorrect term 'كعبر كركم' (turmeric balls), replacing with natural Tunisian dialect.
- `steps.ar`: Enhanced Tunisian dialect authenticity using common local cooking terms.
- `ingredients.en`: Fractions are more standard than decimals in English recipes.
- `steps.en`: Fixed awkward phrasing 'foam (spumas)' and '(not fried)'.

**msiyar** (8 changes):
- `description.he`: Fixed phrasing: 'המשייר נגזר' to 'השם משייר נגזר', and 'התוסס' (fermented/bubbly) to 'הססגוני' (vibrant).
- `steps.he`: Changed imperative verbs to present tense (חותכים, מקלפים, מוסיפים), which is the standard natural style for Israeli cookbooks.
- `description.ar`: Replaced MSA/awkward phrasing with natural Tunisian dialect. Changed 'يطيبو' (cook) to 'يترقدو' (pickle/cure). Changed 'الماكلة الثقيلة' to 'الماكلة الرزينة'.
- `steps.ar`: Fixed a major typo where Hebrew letters 'וח' were mixed into the Arabic word 'وفوّح' (season). Changed 'يطيبو' to 'يترقدو'.
- `name.es`: Changed 'Vegetales Encurtidos' to 'Verduras Encurtidas' which is more natural in culinary Spanish.
- `description.es`: Clarified that the *name* derives from the root. Changed 'guisos ricos' (tasty stews) to 'guisos sustanciosos' to properly translate 'rich stews'.
- `description.en`: Clarified that the *name* derives from the root, improving sentence flow.
- `ingredients`: Standardized measurements across all languages to include both cups/spoons and metric grams/ml for clarity.

**originaltollhousechocolatechip_cookies** (13 changes):
- `name.he`: Added Toll House to match other languages
- `description.he`: Fixed translation of plant-based/vegan and chewy center
- `ingredients.he`: Fixed phrasing for flax eggs and nuts
- `steps.he`: Fixed gender agreement and terminology (folding vs stirring)
- `name.ar`: Added Toll House to match other languages
- `description.ar`: Made dialect more natural
- `ingredients.ar`: Used authentic Tunisian measurements and phrasing
- `steps.ar`: Replaced MSA words with Tunisian dialect (e.g., ڨرياج instead of شباك)
- `description.es`: Improved translation of plant-based and chewy
- `ingredients.es`: Used more standard Latin American terms
- `steps.es`: Improved flow and clarity
- `ingredients.en`: Clarified flax egg mixture and nut chopping
- `steps.en`: Added missing articles for better flow

**soy_shawarma** (14 changes):
- `steps.he[4]`: Improved phrasing for crispiness in Hebrew
- `steps.he[5]`: Corrected preposition and phrasing for professional Hebrew
- `steps.he[6]`: More natural culinary term for 'tangy finish'
- `description.es`: Improved natural phrasing for 'street food favorite'
- `ingredients.es[1]`: Used liters instead of ml for large quantities
- `ingredients.es[2]`: Corrected culinary term for sliced onions (juliana instead of rodajas)
- `steps.es[1]`: Corrected singular/plural agreement for spice mix
- `steps.es[3]`: Matched the ingredient change to julienne
- `steps.es[5]`: Corrected singular/plural agreement for spice mix
- `steps.es[6]`: More natural culinary term for 'tangy finish'
- `ingredients.ar`: Adjusted to authentic Tunisian dialect (lfah instead of tabel, ghobra instead of marhi, chtar instead of 0.5)
- `steps.ar`: Replaced MSA terms with Tunisian dialect (qallaya for pan, mraq for broth, lfah for spices)
- `description.en`: Added quotes for clarity around the translation
- `ingredients.en`: Changed decimals to standard recipe fractions

**yellow_meat** (5 changes):
- `description.he`: Removed redundant and awkward transliteration typo '(בסר צהוב)'
- `description.ar`: Removed Hebrew characters and fixed transliteration to Arabic script
- `steps.ar`: Fixed typo 'بابיי' to 'بابيي' and used more authentic Tunisian cooking verbs like 'فوّح' and 'ذبل'
- `steps.es`: Changed 'carne vegetal' to 'seitán' for clarity and 'masajear' to 'frotar' for natural culinary phrasing
- `steps.en`: Replaced 'meat' with 'seitan roast' for accuracy and improved culinary phrasing ('sauté' instead of 'fry')


## Run Results (2026-02-20 23:11)
- Recipes reviewed: 57
- Successful: 22
- Errors: 35
- Total changes: 148
- Duration: 207.5s

### Changes Summary

**bakedpotatolevivot** (6 changes):
- `name.he`: Expanded the abbreviation 'תפו"א' to 'תפוחי אדמה' and added 'אפויות' (baked) to match the English title and professional cookbook style.
- `steps.he`: Changed 'הסינון' (straining) to 'הסחיטה' (squeezing) for culinary accuracy, and 'שחום' to 'זהוב' (golden) for standard Hebrew recipe phrasing.
- `name.es, description.es, ingredients.es, steps.es`: Changed 'patata' to 'papa' for Latin American Spanish. Simplified 'levadura química' to 'polvo de hornear'. Changed 'colar' to 'escurrir' for accurate culinary terminology.
- `description.ar`: Added the missing translation for 'patch' (رقعة) to ensure the etymology explanation matches the other languages.
- `ingredients.ar, steps.ar`: Changed 'مرحية' (ground/pureed) to 'مرابية' (grated), which is the authentic Tunisian term for grated vegetables. Used 'فرينة حمص' instead of 'دقيق حمص' for better dialect accuracy.
- `steps.en`: Changed 'straining' to 'squeezing them' for clarity. Added the missing 'egg replacer' note to step 3 to match the Hebrew and Arabic versions.

**banatagestuffedpotato_croquettes** (4 changes):
- `hebrew`: Corrected transliteration of the name to 'בנטאז', fixed the mistranslation of 'staple' from 'מנה עיקרית' (main dish) to 'מנת דגל' (flagship/staple dish), and improved overall culinary phrasing.
- `arabic`: Replaced unnatural decimal measurements ('0.8 كاس') with natural phrasing ('كاس غير ربع'), specified the water amount to match other languages, and ensured authentic Tunisian/Djerban dialect and vocabulary (e.g., 'زوز كيسان', 'زوزة', 'مفسوسة').
- `spanish`: Adapted 'patata' to 'papa' for broader Latin American appeal, changed the awkward 'hamburguesa' to 'tortita' for the croquette shape, and smoothed out the phrasing.
- `english`: Converted awkward decimal cup measurements (0.5, 0.8) to standard fractions (1/2, 3/4), and refined cookbook terminology (e.g., 'Deep-fry', 'Sauté').

**brodochickensoup** (9 changes):
- `description.he`: Improved phrasing to sound more natural in Hebrew. Changed 'משקם' to 'מחזק' (restorative) and 'צמחית' to 'טבעונית' (plant-based/vegan).
- `ingredients.he`: Converted awkward metric measurements (2000 ml, 30 ml) to standard cookbook measurements (2 liters, 2 tablespoons). Changed 'חתוכים לחתיכות' to 'חתוכים גס' for zucchini.
- `steps.he`: Changed imperative verbs to present tense plural (מניחים, מכסים), which is the standard convention for Hebrew recipes.
- `description.es`: Improved flow and natural phrasing. Changed 'restaurador' to 'reconfortante' and 'vegetal' to 'a base de plantas'.
- `ingredients.es`: Changed 'patatas' to 'papas' for Latin American Spanish. Converted 2000 ml and 30 ml to 2 litros and 2 cucharadas for natural recipe reading.
- `description.ar`: Refined the Tunisian dialect to flow more naturally. Changed 'نهار الجمعة في الليل' to 'ليلة السبت' which is the authentic term for Friday night in this cultural context.
- `ingredients.ar`: Fixed the awkward '8.3 cups' translation to 'زوز ليترو' (2 liters). Changed 'مرحيين' (ground) to 'مهروشين' (crushed) for the garlic. Replaced 'قرع بو طزينة' with the more universally understood 'قرع أخضر'.
- `ingredients.en`: Fixed the highly unnatural '8.3 cups' to '8 cups (2 liters)'. Changed '2.5 cups pumpkin' to '10 oz (300g) pumpkin' for better accuracy and consistency with other languages.
- `steps.en`: Smoothed out the instructions for better cookbook style (e.g., 'Bring to a boil' instead of 'Bring the pot to a boil').

**charoset** (3 changes):
- `description`: Hebrew: Fixed grammatical mismatch and dangling modifier. English: Added quotes to 'cheres' and improved flow. Spanish: Added commas for better flow and quotes around 'cheres'. Arabic: Replaced MSA with natural Tunisian phrasing (e.g., 'خذات اسمها من' instead of 'مسمية على').
- `ingredients`: Hebrew: Changed to more natural phrasing ('תמרי מג'הול', 'ללא הליבה'). Spanish: Replaced 'deshuesados' with 'sin carozo' and 'descorazonada' with 'sin corazón' for natural culinary Spanish. Arabic: Wrote out fractions in words, used 'زوزة' for walnuts and 'مرابية' for grated.
- `steps`: Hebrew: Converted imperative verbs to present plural (מגלענים, מקלפים), which is the standard format for Israeli recipes. English: Removed redundant 'in a food processor' in step 3. Spanish: Improved instructional flow ('Quite el carozo', 'procese con pulsos'). Arabic: Used authentic Tunisian cooking terms ('روبو', 'رابيها', 'حاجتك بيه').

**chocolate_balls** (3 changes):
- `description`: Hebrew: Changed 'מפגשי שבת' to 'ארוחות שבת' for natural phrasing. Arabic: Replaced MSA terms with authentic Tunisian dialect (e.g., 'نواد كوكو' for coconut, 'بنة زمنية' for nostalgic taste). Spanish: Improved flow and changed 'rodarlas' to 'rebozarlas'. English: Fixed awkward phrasing 'treat meaning chocolate balls' to parenthetical.
- `ingredients`: Arabic: Used Tunisian measurements ('ربع كاس', 'شطر كاس') and vocabulary ('نواد كوكو'). Spanish: Changed 'desmenuzadas' to 'trituradas' and clarified chocolate as 'picado'. English: Converted decimals (0.25, 0.5) to standard cookbook fractions (1/4, 1/2).
- `steps`: Hebrew: Replaced 'למספר שניות' with 'בפולסים קצרים' (standard culinary term). Arabic: Fully adapted to Tunisian dialect ('صحفة بلار', 'حكة مسكرة', 'فريجيدير'). Spanish: Used 'recipiente hermético' and 'reboce'. English: Changed 'glass bowl' to 'microwave-safe bowl' and 'sealed container' to 'airtight container'.

**chocolatepeanutbutter_muffins** (3 changes):
- `description`: Hebrew: Improved sentence flow and corrected literal translation. Spanish: Improved phrasing for natural reading. Arabic: Replaced MSA with authentic Tunisian phrasing (e.g., 'زريعة الكتان'). English: Clarified the opening sentence to avoid awkward transliteration.
- `ingredients`: Hebrew: Rephrased the flax egg instruction for clarity. Spanish: Added measurement clarification for baking powder. Arabic: Converted fractions to natural spoken Tunisian dialect (e.g., 'كاس ونص', 'شطر كاس'). English: Specified 'all-purpose flour' and 'granulated sugar' for professional cookbook standards.
- `steps`: Hebrew: Fixed phrasing to 'תערובת אחידה' and improved sentence structure. Spanish: Improved flow of mixing instructions. Arabic: Used authentic Tunisian cooking terms ('كوردون', 'عجينة', 'ركّض'). English: Changed 'mix' to 'whisk' and 'stir' where appropriate for standard culinary terminology.

**fricassee_rolls** (3 changes):
- `description`: Hebrew: Fixed awkward phrasing and changed 'מלאות' to 'ממולאות'. Spanish: Changed 'Fricassee' to 'fricasé' and improved natural flow. Arabic: Fixed Hebrew letters in 'طופو' to 'طوفو' and improved dialect phrasing. English: Minor flow improvements.
- `ingredients`: Hebrew: Formatted 1000g to 1kg, removed unnecessary commas. Spanish: Fixed formatting and clarified measurements. Arabic: Added 'كبيرة' to spoon measurements for clarity, fixed 'طופو' to 'طوفو'. English: Improved phrasing (e.g., 'warm water' instead of 'water, warm').
- `steps`: Hebrew: Improved phrasing and flow. Spanish: Changed 'rollos' to 'panecillos' for better culinary context. Arabic: Improved dialect phrasing and clarity. English: Removed redundant '(proof)' and improved frying instructions.

**hotfudgepudding_cake** (10 changes):
- `description.en`: Fixed awkward transliteration 'Ugat Fudge Hama' back to English 'Hot Fudge Pudding Cake' and added missing comma for better flow.
- `ingredients.en`: Converted decimal measurements (1.5, 0.5) to standard recipe fractions (1 1/2, 1/2) and changed 'to taste' to 'for serving' for the whipped cream.
- `steps.en`: Removed redundant 'do not mix it' in step 5 to improve readability.
- `description.he`: Improved phrasing for 'self-saucing' to sound more natural in Hebrew (שמייצרות רוטב בעצמן) and fixed grammar.
- `ingredients.he`: Corrected gender agreement for cocoa powder (לא ממותקת) and replaced the loanword 'אופציונלי' with the standard Hebrew recipe term 'רשות'.
- `steps.he`: Changed literal 'קערת ערבוב' to 'קערה', improved the flow of the batter mixing step, and changed 'בצדדים' to 'בשוליים' for baking terminology.
- `description.ar`: Added 'وصفة' before 'كلاسيكية عصرية' for better flow in Tunisian Arabic, and changed 'تبدل' to 'تعوض' (replaces).
- `ingredients.ar`: Made fraction phrasing more natural in Tunisian dialect (e.g., 'مغرفة ونص' instead of '1.5 مغرفة').
- `steps.ar`: Removed the word 'المرقـة' which is strictly used for savory stews in Tunisia, keeping just 'الصوص', and improved general flow.
- `ingredients.es`: Changed decimal point to a comma (7,5 g) to match standard Spanish formatting.

**humus_salad** (7 changes):
- `description.he`: Fixed unnatural phrasing ('פרופיל טעמים', 'מתאבן קמיה בסיסי') to sound more like authentic Israeli cookbook Hebrew.
- `ingredients.he`: Converted overly specific metric measurements (2.3g, 30ml) to standard culinary measures (spoons) for consistency and readability.
- `description.ar`: Replaced MSA terms with authentic Tunisian dialect ('زمنية' instead of 'ريفية', 'كسبر أخضر' instead of 'الكزبرة الطازجة', 'كيما' instead of 'كيف').
- `ingredients.ar`: Updated vocabulary to Tunisian dialect ('كسبر أخضر', 'فلفل زينة', 'زوز مغارف كبار').
- `description.es`: Improved natural flow and translated 'bright flavor profile' to a more natural Spanish culinary phrase ('sabor fresco y vibrante').
- `ingredients.es`: Converted exact gram/ml measurements to standard culinary spoons to match the other languages and standard cookbook formats.
- `description.en`: Minor phrasing improvements for better flow ('unlike the smooth puree' instead of 'rather than the smooth puree found in').

**kishke** (6 changes):
- `description.he`: Fixed awkward phrasing 'שמקורו במעי ממולא' to 'שבמקור מולא לתוך מעי' and changed 'קרום' to 'מעטפת' which is the correct culinary term for casing.
- `description.es`: Improved culinary terminology by changing 'se preparaba dentro de un intestino' to 'se embutía en tripa' and refined the flow of the text.
- `description.ar`: Adjusted vocabulary to natural Tunisian dialect (e.g., 'شادة روحها' instead of repeating 'متماسكة', 'شايحة ولا معجنة' instead of 'ناشفة ولا رخوة', and 'بابيي ألومينيوم').
- `description.en`: Polished phrasing for a more professional cookbook tone, changing 'intestinal casing' to 'a casing' and improving flow.
- `ingredients`: Standardized abbreviations in Spanish (cdta -> cucharadita), used authentic Tunisian terms in Arabic (فلفل زينة for paprika), and improved formatting across all languages.
- `steps`: Clarified the texture check in all languages (e.g., 'runny' instead of 'pours', 'جارية' instead of 'سايلة') and made the cooking actions sound more like professional recipe instructions.

**lentechalentilstew** (8 changes):
- `name.he`: Added '(נזיד עדשים)' to match the format of the other languages.
- `description.he`: Improved phrasing for natural flow (e.g., 'טבעוני מטבעו' instead of 'צמחי באופן טבעי', and 'הרתחת המרכיבים' instead of 'בישול המרכיבים').
- `steps.he`: Changed to standard Hebrew recipe imperative/present-tense phrasing (מניחים, מוסיפים, מביאים) instead of direct commands.
- `ingredients.ar`: Corrected 'أحمر' (red) to 'أسمر' (brown) to accurately match the English and Spanish ingredients. Changed 'نصف' to 'شطر' for authentic Tunisian dialect.
- `description.ar`: Refined the Tunisian dialect phrasing to sound more natural ('طبق كلاسيكي يدفّي', 'من غير ما نقليوهم').
- `steps.es`: Changed 'No fría nada' to 'No sofría ningún ingrediente' and 'esté espeso' to 'espese' for better culinary Spanish.
- `ingredients.en`: Changed decimal quantities (0.5) to fractions (1/2) which is standard in English recipes.
- `steps.en`: Added definite articles ('the lentils', 'the water') and improved culinary phrasing ('tender', 'thickened', 'stir in').

**nazhaherbomelet** (4 changes):
- `hebrew`: Changed instructions to present plural (standard in Israeli cookbooks). Improved phrasing in description ('ארומטית', 'ששמה נגזר'). Fixed ingredient names for natural flow ('גבעולי בצל ירוק', 'כורכום טחון').
- `arabic`: Adjusted to authentic Tunisian dialect (e.g., 'خميرة ڨطو', 'مقلة', 'عروق بصل', 'كسبر أخضر'). Improved sentence structure to sound like natural spoken Maghrebi rather than MSA.
- `spanish`: Improved flow and natural phrasing. Changed 'polvo de hornear' to 'polvo para hornear'. Used 'homogénea' instead of 'suave' for the batter, and 'firme' instead of 'estable' for the cooked omelet.
- `english`: Minor tweaks for flow and consistency. Used 'skillet' instead of 'frying pan', 'firm' instead of 'stable', and simplified 'green onions (scallions)' to just 'scallions'.

**pancakesefratshachor** (3 changes):
- `description`: Hebrew: Fixed pluralization and changed 'פשתן' to 'זרעי פשתן'. Spanish: Changed 'lino' to 'linaza' for natural phrasing. Arabic: Refined Tunisian dialect ('مالأونجلي'). English: Changed 'flax' to 'flaxseed' and improved flow.
- `ingredients`: Hebrew: Clarified sugar amount, changed 'לפי הטעם' to 'לפי הצורך' for frying oil. Spanish: Fixed gender agreement 'chispas veganas', changed 'al gusto' to 'necesario'. Arabic: Changed '1.7 كيسان' to 'كاس و 3/4', added 'كبار' to spoon measurements. English: Changed decimals to fractions (1 3/4 cups, 1/2 cup), fixed 'oil to taste' to 'oil, as needed'.
- `steps`: Hebrew: Improved phrasing for resting batter and frying depth. Spanish: Clarified deep-frying depth phrasing. Arabic: Added missing 'على نار متوسطة' (medium heat) to step 4, improved natural flow. English: Improved phrasing for frying depth and gooey interior.

**potachewhitebean_stew** (12 changes):
- `name.he`: Added the translation '(תבשיל שעועית לבנה)' to match the format of the other languages.
- `name.es`: Changed 'Alubias' to 'Frijoles' for broader Latin American Spanish appeal.
- `description.he`: Improved phrasing for natural Hebrew flow ('מערבבים היטב' instead of literal 'לאיחוד', 'נימוחה' instead of 'קרמית', and clarified Sephardic roots).
- `description.es`: Changed 'alubias' to 'frijoles' and replaced the literal translation 'presenta' with 'se prepara con'.
- `description.ar`: Enhanced Tunisian dialect authenticity by using terms like 'سلة سلة' (simmered) and 'تولي زبدة' (creamy/soft like butter).
- `description.en`: Fixed typo 'Potaches' to singular 'Potache' to match the title.
- `ingredients.ar`: Clarified 'مغارف كبار' (tablespoons) for the tomato paste and used 'مهروسين' for crushed garlic.
- `ingredients.en`: Changed '0.5 tsp' to '1/2 tsp' for standard cookbook formatting.
- `steps.he`: Changed 'קרמית' to 'נימוחה' which is the authentic culinary term for soft, melting beans in Hebrew.
- `steps.es`: Replaced 'Remover para combinar' with the more natural 'Mezclar bien'.
- `steps.ar`: Replaced 'طنجرة الضغط' with the more colloquial Tunisian 'الكوكوت' and improved the phrasing for mixing and cooking.
- `steps.en`: Added definite articles ('the') for better grammatical flow in cookbook English.

**sfenj** (11 changes):
- `name.he`: Changed 'שפינג׳ות' to the standard and widely used 'ספינג''.
- `description.he`: Improved phrasing for better flow, changed 'לביבות' to 'מאפים מטוגנים' as it fits the doughnut-like nature of sfenj better.
- `steps.he`: Made instructions more natural to Israeli cookbook style (e.g., 'עד להכפלת הנפח', 'העבירו לנייר סופג').
- `description.ar`: Replaced the unnatural loanword 'التكستير' with 'القوام', and replaced the Hebrew characters 'حנוכה' with the Arabic spelling 'عيد الحانوكا'.
- `ingredients.ar`: Adjusted measurements to natural Tunisian phrasing (e.g., 'كاس ونص', 'مغرفة كبيرة').
- `steps.ar`: Enhanced Maghrebi/Tunisian dialect authenticity using words like 'الشيرتين' (both sides) and 'طريف' (a piece).
- `description.es`: Refined phrasing for a more natural flow, changing 'masa de levadura simple' to 'sencilla masa con levadura'.
- `steps.es`: Improved grammatical flow and clarity, adding 'papel absorbente' for draining.
- `description.en`: Added missing comma and article for better grammatical flow.
- `ingredients.en`: Formatted '1.5 cups' to standard cookbook fraction '1 ½ cups' and added commas for clarity.
- `steps.en`: Clarified frying instructions ('a few inches of oil') and draining ('on paper towels').

**shlomittomatosalad** (4 changes):
- `English`: Changed '3.3 cups' to '3 1/3 cups' for standard cookbook formatting. Improved step phrasing for better flow ('Halve the cherry tomatoes', 'whisk together'). Changed 'named for' to 'named after'.
- `Hebrew`: Replaced the literal translation 'תוסס' (which implies fermented/bubbly in Hebrew food contexts) with 'מרענן' (refreshing). Fixed the spelling of 'חמנייה'. Improved the phrasing of 'תוספת קיצית מושלמת' to 'תוספת מושלמת לקיץ'.
- `Spanish`: Changed the decimal point to a comma in '12,5 g' to match standard Spanish formatting. Replaced 'vibrante' with 'refrescante' for a more natural culinary description. Changed 'bol' to 'recipiente' in step 2 to avoid repetition.
- `Arabic`: Replaced MSA and awkward phrasing with natural Tunisian dialect (e.g., 'متاع', 'تعمل الكيف', 'بالوقت'). Clarified spoon sizes ('مغارف كبار' vs 'مغرفة صغيرة'). Replaced 'حشيش' with 'أعشاب' to avoid ambiguity, as 'حشيش' can mean grass/weeds.

**shmid** (3 changes):
- `description`: Hebrew: Fixed spelling of 'Mhamsa' (מהמסה -> מחמסה) and improved sentence flow. Arabic: Rewrote to sound like natural Tunisian dialect rather than MSA. Spanish: Improved phrasing for natural flow. English: Minor punctuation and phrasing tweaks for better flow.
- `ingredients`: Hebrew: Changed 1500 ml to 1.5 liters. Arabic: Converted decimal quantities to natural fractions (e.g., 6.25 to 6 وربع) and used authentic dialect terms. Spanish: Changed 'patata' to 'papa' for Latin American Spanish and used comma for decimal (1,2 g). English: Converted decimal measurements to standard recipe fractions (0.5 to 1/2, 6.25 to 6 1/4, 1.2 to 1 1/4).
- `steps`: Hebrew: Improved flow and corrected grammar. Arabic: Replaced MSA words (يختار -> يخثار) and used natural Tunisian cooking expressions (تبقبق, كخيط جويد). Spanish: Improved phrasing for adding semolina ('en forma de hilo'). English: Fixed singular/plural agreement for the potato and improved phrasing.

**tbikha_tomatem** (6 changes):
- `name.he`: Fixed incorrect transliteration of 'Tbikha' from 'דביח' to the correct Judeo-Tunisian Hebrew spelling 'טביכה'.
- `ingredients`: Harmonized awkward metric measurements (45ml, 7g, 100g) in Hebrew and Spanish to standard spoon measurements (3 tbsp, 1 tbsp, 6 tbsp) to match English/Arabic and improve cookbook readability.
- `steps.en`: Replaced awkward 'steam/sauté' with the professional culinary term 'sweat', and improved phrasing for cooking out the tomato paste.
- `steps.es`: Removed unnatural 'al vapor/sofreír' and 'cocine (al vapor)' constructions, replacing them with natural Spanish culinary phrasing.
- `steps.ar`: Refined Tunisian dialect for better flow (e.g., 'تنحّي القروصية', 'ديريكت', 'سلة سلة').
- `steps.he`: Improved flow and culinary terminology, changing literal translations to natural Hebrew cooking instructions (e.g., 'מנטרל את החומציות').

**umami_mushrooms** (10 changes):
- `description.he`: Improved flow and fixed literal translations to sound more natural to an Israeli speaker.
- `steps.he`: Corrected spelling of 'להשריה' to 'משרים' and improved phrasing of baking instructions.
- `description.ar`: Replaced MSA and literal translations with authentic Tunisian dialect phrasing.
- `ingredients.ar`: Changed unnatural decimal measurements to natural fractions and specified 'مغارف كبار'.
- `steps.ar`: Used authentic Tunisian cooking terms like 'طبق متاع كوشة' and 'يشربوا التخليطة'.
- `description.es`: Corrected 'sabor salado' to 'sabor' as umami is savory, not salty. Improved sentence flow.
- `steps.es`: Changed 'remojar' to 'marinar' and 'fuego' to 'temperatura' for oven accuracy.
- `description.en`: Added missing commas and improved phrasing for a professional cookbook tone.
- `ingredients.en`: Converted unnatural decimal tablespoons to standard fractional tablespoons.
- `steps.en`: Changed 'soak' to 'marinate' and added missing articles for better flow.

**vegan_fried_rice** (7 changes):
- `ingredients.en`: Changed '0.5 tsp' to '1/2 tsp' to match standard English cookbook formatting.
- `description.he`: Fixed literal translation 'אורז... משתמש' to a natural Hebrew phrasing 'במתכון זה... משתמשים'. Changed 'תוסס' (ferments) to 'יבעבע' (sizzles/bubbles).
- `ingredients.he`: Converted milliliters to tablespoons (כפות) as is standard in Israeli recipes. Changed 'בצלים ירוקים' to 'גבעולי בצל ירוק' for natural phrasing.
- `name.es`: Changed 'Arroz Frito Vegano con Huevo' to 'Arroz Frito Vegano (Estilo Huevo)' to clarify it is vegan and does not contain actual egg.
- `ingredients.es`: Converted milliliters to tablespoons (cucharadas) to match the English measurements and standard Spanish cookbook style.
- `description.ar`: Fixed Hebrew letters 'طופו' that crept into the Arabic text, correcting it to 'توفو'. Adjusted phrasing to sound more naturally Tunisian ('هالروز المقلي النباتي نستعملو فيه...').
- `ingredients.ar`: Fixed Hebrew letters in tofu. Changed 'فطر' to 'شومبينيون' which is much more common in Tunisian dialect. Clarified 'مغارف' to 'مغارف كبار' (tablespoons) and 'بصلات خضر' to 'عروق بصل أخضر'.

**veganeggsalad** (12 changes):
- `description.he`: Changed 'פרשנות צמחית' to 'גרסה טבעונית' for natural phrasing. Improved flow and corrected literal translations.
- `ingredients.he`: Changed '2 בצלים ירוקים' to '2 גבעולי בצל ירוק' (2 stalks) which is the correct culinary term in Hebrew.
- `steps.he`: Improved grammar and flow, adding definite articles where necessary and making the instructions sound like a professional Israeli cookbook.
- `description.ar`: Replaced awkward literal translation 'هالتفسير' with 'هالنسخة' (this version). Improved Tunisian phrasing for 'exactly' (قد قد instead of بالظبط).
- `ingredients.ar`: Clarified spoon sizes by adding 'كبار' (tablespoons). Changed '2 بصلات خضر' to '2 عروق بصل أخضر' (2 stalks) for natural Maghrebi phrasing.
- `steps.ar`: Enhanced Tunisian dialect naturalness (e.g., 'اعصر التوفو مليح', 'كان تحب تستعملو').
- `description.es`: Improved natural flow, changing 'interpretación vegetal' to 'versión a base de plantas' and refining the sentence structure for better readability.
- `ingredients.es`: Changed '2 cebollas verdes' to '2 tallos de cebolla verde (cebollín)' for better Latin American/general Spanish culinary accuracy.
- `steps.es`: Refined verbs and phrasing (e.g., 'ajuste la sazón', 'eliminar el exceso de líquido') for professional cookbook style.
- `description.en`: Changed 'interpretation' to 'take' and refined phrasing to recreate a more natural, professional English cookbook tone.
- `ingredients.en`: Converted awkward decimal measurements (1.7, 0.5, 0.25) to standard English cookbook fractions (1 3/4, 1/2, 1/4).
- `steps.en`: Added missing definite articles ('the tofu', 'the paprika') for smoother reading.

**yeast_cake** (14 changes):
- `description.he`: Fixed typo 'ונתחם' to 'וגרידת' (zest). Improved overall flow.
- `ingredients.he`: Changed 'שמן קוקוס מוקשה' to 'שמן קוקוס מוצק' for natural culinary phrasing.
- `steps.he`: Changed colloquial 'על הגז' to 'על הכיריים' and clarified 'גרידה' to 'גרידת הדרים'.
- `name.es`: Changed 'Bizcocho' to 'Pastel' as bizcocho typically implies a sponge cake without yeast.
- `description.es`: Replaced 'bizcocho' with 'pastel' and 'jugoso' with 'húmedo' which is more natural for cakes.
- `ingredients.es`: Changed 'aceite de coco hidrogenado' to 'aceite de coco sólido' for standard recipe terminology.
- `steps.es`: Improved grammar and flow, replaced 'bizcocho' with 'pastel'.
- `name.ar`: Changed to 'كيكة بالخميرة' which is more natural in Maghrebi dialects than the MSA 'كعكة'.
- `description.ar`: Replaced MSA terms with Tunisian dialect (e.g., 'شيرة' to 'شحور', 'قشر الليمون' to 'قشور القارص', 'فريش' to 'طرية').
- `ingredients.ar`: Adapted to Tunisian dialect ('شطر كاس' for half cup, 'سكر أسمر' for brown sugar, 'شحور' for syrup).
- `steps.ar`: Rewrote steps using authentic Tunisian verbs and nouns ('حل العجينة', 'روليها', 'طبق', 'الغاز').
- `description.en`: Added commas for better sentence flow.
- `ingredients.en`: Changed 'hydrogenated coconut oil' to 'solid coconut oil' which is standard in English baking, added spaces to measurements.
- `steps.en`: Added missing articles ('the') and clarified instructions (e.g., 'roll up into a log', 'golden brown').


## Run Results (2026-02-20 23:12)
- Recipes reviewed: 35
- Successful: 9
- Errors: 26
- Total changes: 53
- Duration: 88.5s

### Changes Summary

**bkailatunisianstew** (6 changes):
- `description.he`: Changed 'לירק' to 'לעלים ירוקים' for better context of 'greens'. Changed 'עשירים' to 'בשרניים' (meaty/savory) as it fits seitan chunks better.
- `steps.he`: Improved phrasing: changed 'הופך דמוי קונפי' to 'הופך למרקם של קונפי' and 'ובשלו בבישול ארוך' to 'ובשלו בישול ארוך' for more natural Hebrew.
- `ingredients.ar`: Added gram measurements to seitan for clarity and consistency. Changed 'كزبر خضراء' to 'تابل أخضر (كزبرة)' which is the authentic Tunisian term for fresh coriander. Corrected spelling of dill to 'شبت'.
- `steps.ar`: Improved natural flow and grammar, changing 'مرق بالماء' to 'مرّق بالماء ولا بمرقة الخضرة' and updating herb names to match ingredients.
- `steps.es`: Changed 'cocer las hojas al vapor' to 'se cocinen en su propio jugo' because steaming implies added water. Improved 'durante mucho tiempo' to 'durante un tiempo prolongado' for professional cookbook tone.
- `steps.en`: Fixed the awkward and incorrect phrase 'simulate a long cook' to 'simmer gently for a long time'.

**chocolate_cake** (3 changes):
- `description`: Improved flow and natural phrasing across all languages. Clarified the explanation of the name 'Ugat Shokolad' and the concept of 'pareve'.
- `ingredients`: Fixed 'margarine to taste' to 'margarine (for greasing the pan)' as it is used for the pan, not for flavor. Clarified flax egg instructions and standardized measurements.
- `steps`: Hebrew: Changed infinitive verbs to present-plural (e.g., מחממים, מערבבים) which is the standard professional format in Israeli cookbooks. Arabic: Used authentic Tunisian terminology (كوشة, زريعة الكتان, شايح). Spanish & English: Standardized the 'toothpick test' phrasing to professional cookbook standards.

**kataa_soup** (4 changes):
- `Hebrew`: Fixed literal translations to natural culinary Hebrew (e.g., 'מרק מלוח' to 'מרק עשיר', 'מגובה קל' to 'בזרם דק'). Aligned step quantities with the ingredient list (using grams instead of cups).
- `Arabic`: Replaced MSA terms with authentic Tunisian/Djerban dialect ('حساء طازج' to 'شربة عجين دياري', 'ديريكت' to 'طول'). Improved culinary phrasing ('تتكعبرش', 'تعقاد وتخثار').
- `Spanish`: Improved flow and professional culinary terminology ('agente espesante' to 'espesante', 'desde cierta altura' to 'en forma de hilo'). Aligned step quantities with the ingredient list.
- `English`: Polished phrasing for a professional cookbook tone ('throw them' to 'drop them', 'liquid slurry' to 'smooth slurry', 'from a slight height' to 'in a thin stream').

**kouklotsemolinadumplings** (5 changes):
- `en.ingredients`: Changed awkward '0.9 cups' to 'Scant 1 cup' for natural English cookbook measurements.
- `es.name`: Changed 'Bolas' to 'Albóndigas' for a more appetizing and accurate culinary term in Spanish.
- `ar.description`: Replaced MSA 'دقيق' with Tunisian 'فرينة' and improved dialect phrasing and word order.
- `he.steps`: Made step 1 actionable to mix the chickpea flour and water, rather than assuming it is pre-mixed.
- `all.steps`: Improved flow and clarity across all languages, ensuring step 1 clearly instructs to mix the egg replacer.

**marmouma** (8 changes):
- `description.he`: Improved flow and natural phrasing for Israeli Hebrew (e.g., 'שואבת את שמה', 'במטבח של יהודי ג'רבה').
- `steps.he`: Used more authentic culinary terms (e.g., 'שהגירו הירקות' instead of 'שהופרשו', 'הידבקות לתחתית').
- `description.es`: Improved natural flow and phrasing ('cocina judía de Djerba', 'rica mermelada').
- `steps.es`: Changed 'rebanados' to 'en rodajas' and 'quemar' to 'pegue' for better culinary Spanish.
- `description.ar`: Enhanced Tunisian dialect authenticity ('الكوجينة متاع يهود جربة', 'البنة متاعها').
- `steps.ar`: Used more natural Tunisian cooking terms ('يغلي سلة سلة', 'ينشح').
- `description.en`: Minor flow improvements ('Unlike matbucha', 'long cooking time').
- `steps.en`: Changed 'burning' to 'sticking' and improved phrasing.

**mufleta** (10 changes):
- `description.he`: Improved phrasing for natural Hebrew flow. Changed 'השם מגיע מהערבית המרוקאית למילה מקופלת' to 'השם נגזר מהמילה 'מקופלת' בערבית מרוקאית'.
- `steps.he`: Replaced 'מערבבים' with 'לשים' for dough hook. Reordered step 2 for better chronological flow. Changed 'דבש תמרים' to the standard Israeli term 'סילאן'.
- `description.ar`: Adjusted vocabulary to authentic Tunisian/Maghrebi dialect (e.g., 'هالورقات الرهاف', 'سخان').
- `ingredients.ar`: Used standard Tunisian measurements ('كاس وربع', 'شطر مغرفة', 'مغرفة كبيرة').
- `steps.ar`: Converted MSA and generic Arabic to Tunisian dialect ('كعبر', 'شايحة', 'صحفة', 'مقلة', 'رب التمر', 'سيرو ديرابل').
- `description.es`: Fixed pluralization ('Las mufletas son'). Clarified 'Pascua' to 'Pésaj (Pascua judía)' for cultural accuracy. Improved translation of the name's origin.
- `steps.es`: Changed 'fría' to 'cocine' as mufletas are griddled/pan-fried, not deep-fried. Improved flow and natural phrasing of the stacking method.
- `description.en`: Fixed pluralization ('Mufletas are'). Improved phrasing of the name's origin ('the Moroccan Arabic word for').
- `ingredients.en`: Changed decimal fractions (0.5) to standard recipe fractions (1/2).
- `steps.en`: Changed 'Mix' to 'Knead' for dough hook. Improved chronological flow in step 2. Added standard terminology ('date syrup (silan)').

**shepherdpienorth_african** (9 changes):
- `description.he`: Fixed gender agreement ('שכבות' is feminine, so 'הצהובות') and removed awkward phrasing.
- `steps.he`: Changed 'שמן' (noun) to 'שמנו' (imperative verb). Replaced 'מחית' with 'פירה' for more natural Israeli Hebrew. Improved general flow.
- `description.ar`: Replaced 'فرشيلو' with 'لحم مرحي نباتي' as it is the standard Tunisian term for plant-based mince.
- `ingredients.ar`: Changed 'فلفل أحمر (بابريكا)' to 'فلفل زينة' which is the authentic Tunisian term for sweet paprika. Changed 'ثوم مرحي' to 'ثوم غبرة' for garlic powder.
- `steps.ar`: Replaced 'ارحيها' (grind) with 'ارفسها' (mash), which is the correct Tunisian verb for mashing potatoes. Replaced 'حلحل' with 'فتفتو' for breaking apart the meat.
- `description.es`: Replaced 'infundidas' (literal translation of infused) with 'sazonadas'. Changed 'Crea una cazuela' to 'El resultado es un pastel' for better flow.
- `steps.es`: Changed 'Arme el pastel' to 'Armado del pastel' and improved prepositional phrasing for a more natural cookbook style.
- `ingredients.en`: Changed awkward '17.6 oz' to standard '1 lb (500g)' and '0.5 tsp' to '1/2 tsp'.
- `steps.en`: Ensured ingredient names in steps match the ingredients list (e.g., using 'bouillon powder' instead of 'chicken seasoning', and 'plant-based mince' instead of 'ground meat').

**sourdoughbread_soly** (5 changes):
- `steps.ar[5]`: Removed the Hebrew word 'מתיחות' that accidentally crept into the Arabic text and replaced it with authentic Maghrebi phrasing ('تجبيدات').
- `steps.he[1]`: Corrected the translation of 'shaggy dough' from the unnatural 'בצק גבישי' to the standard baking term 'בצק גס ולא אחיד'.
- `ingredients`: Reformatted ingredient lists across all languages to remove awkward commas and improve readability (e.g., '1.25 cups water, warm' to '1 ¼ cups warm water').
- `description.es`: Improved natural phrasing, changing 'subir' to 'levar' and refining the description of the crumb.
- `steps.es`: Added standard baking terminology like 'autólisis', 'banetón', and 'olla de hierro fundido' for a more professional tone.

**vegetablesoupfor_couscous** (3 changes):
- `description`: English: Improved phrasing for 'derives from the root'. Hebrew: Improved flow and translated 'steamed grains' to 'couscous grains' for natural phrasing. Spanish: Improved flow and natural culinary phrasing. Arabic: Adjusted to sound like natural Tunisian dialect, explaining the Judeo-Arabic origin smoothly.
- `ingredients`: English: Changed awkward '1.2 cups' to '1 ¼ cups', and '7g' to '1 generous tbsp'. Hebrew: Converted clinical metric measurements (30ml, 7g) to standard culinary spoons (כפות) for home cooking. Spanish: Changed 'patatas' to 'papas' for broader Latin American appeal, converted ml/g to spoons. Arabic: Replaced cup measurements with grams to match the original recipe intent and local norms, used authentic Tunisian terms like 'بوطزينة' (zucchini) and 'مغارف' (spoons).
- `steps`: English: Improved culinary terms ('bloom it', 'fork-tender'). Hebrew: Used natural Israeli cooking terminology ('לפתוח את התבלין', 'להזיע'). Spanish: Improved flow and used natural terms ('hervir a fuego lento', 'tiernas'). Arabic: Enhanced Tunisian dialect phrasing ('تتذبل', 'سلة سلة', 'تتهرى').


## Run Results (2026-02-20 23:14)
- Recipes reviewed: 26
- Successful: 6
- Errors: 20
- Total changes: 35
- Duration: 90.0s

### Changes Summary

**apple_crumble** (5 changes):
- `ingredients`: Standardized unnatural exact gram measurements (e.g., 1.3g, 42.6g) in Hebrew and Spanish to standard volume measurements (cups/spoons) to match English/Arabic and read naturally for home cooks.
- `steps`: Fixed inconsistency in step 5 across all languages: changed 'margarine' to 'vegan butter or coconut oil' to match the ingredient list.
- `steps`: Changed 'Pour' to 'Sprinkle' (and equivalents in ES, HE, AR) in step 6, as a crumble topping is sprinkled, not poured.
- `description`: Refined the English and Spanish descriptions to clarify that 'Crumble Tapuchim' is the name being explained, fixing awkward phrasing.
- `ar`: Improved Tunisian Arabic phrasing, using authentic culinary terms like 'خميرة ڨاطو' (baking powder) and 'نرملوها' (to make crumbly/sandy) instead of literal translations.

**biscoti_judy** (7 changes):
- `description.he`: Changed 'שנאפו' to 'שנאפות' for correct present tense description of the cookies, and improved phrasing for 'extra crunch'.
- `ingredients.he`: Changed 'קמח רגיל' to 'קמח לבן' which is the standard term in Israeli baking.
- `description.es`: Changed 'crujido extra' to 'un toque extra crujiente' as 'crujido' literally means a cracking sound, not the culinary texture.
- `ingredients.es`: Changed 'azúcar blanca/morena' to 'azúcar blanco/moreno' for better standard Spanish, and specified 'harina de trigo común'.
- `steps.es`: Changed 'grumosa' (lumpy) to 'desmenuzable' (crumbly) to accurately reflect the dough's texture. Changed 'Presione' to 'Presionar' to maintain consistent infinitive mood.
- `ingredients.ar`: Replaced MSA 'منخولة' with Tunisian 'مغربلة'. Replaced 'حبيبات شوكولاتة' with the widely used 'بيبيت شوكولا' (pépites de chocolat).
- `steps.ar`: Removed 'الكوشة' as it refers to a commercial bakery, keeping 'الفور' for home oven. Replaced 'بودانات' with the authentic Tunisian baking term 'حرابيش' for dough logs.

**bshisha_bsisa** (3 changes):
- `ingredients`: English and Arabic: Converted awkward decimal measurements (1.3, 1.25) to natural fractions (1 1/3, 1 1/4). Arabic: Used authentic Tunisian terms like 'منقّي' (cleaned) and 'كعب' (whole seeds).
- `steps`: English: Changed 'Roast' to 'Toast' for dry pan cooking. Arabic: Used the authentic Tunisian term 'عرّج' for toasting grains. Hebrew: Improved phrasing, changed 'שריפה' to 'חריכה' (scorching), and made the text flow naturally. Spanish: Improved flow and clarity in the steps.
- `description`: Hebrew: Reworded to sound more natural to an Israeli speaker. Spanish: Changed 'mezcla con una llave' to 'remueve con una llave' for accurate stirring description. Arabic: Refined the dialect to sound naturally Tunisian/Djerban and added the missing 'energy food' translation.

**honeycakemami** (9 changes):
- `description.he`: Added niqqud to the name Enny (אֶנִי) to prevent confusion with the Hebrew word for 'I' (אני).
- `steps.he`: Improved phrasing for a more professional culinary tone (e.g., 'תערובת בהירה ואוורירית' instead of 'אחידה ואוורירית', and 'יש להיזהר מערבוב יתר').
- `description.ar`: Adjusted vocabulary to sound more naturally Tunisian/Maghrebi ('الوصفة المفضلة عند أم إيني', 'معناها', 'يستعملوها في برشا ثقافات').
- `ingredients.ar`: Fixed MSA terms to authentic Tunisian dialect (e.g., 'كاس' instead of 'كأس', 'سيرو أغاف', 'عود قرنفل').
- `steps.ar`: Rewrote steps to use natural Tunisian cooking verbs and phrasing ('على شيرة', 'بالركاضة', 'من لوطة لفوق', 'كيردون').
- `description.es`: Changed 'atesorada' to 'preciada' for a more natural flow in Spanish.
- `ingredients.es`: Clarified 'clavo molido' to 'clavo de olor molido' and 'harina común' to 'harina de trigo todo uso' for universal understanding.
- `steps.es`: Improved the description of the baking pans in step 1 and ensured consistent terminology.
- `steps.en`: Clarified 'mixer' to 'stand mixer' and 'agave/syrup' to 'agave or date syrup' for better readability.

**mhamsa** (7 changes):
- `ingredients`: Standardized measurements across all languages to use volume (cups/tablespoons) instead of mixed metric/volume, ensuring consistency. Fixed awkward transliterations.
- `description.he`: Improved phrasing for natural Hebrew flow ('השם מחמסה מגיע...' instead of 'מחמסה מגיעה...').
- `description.ar`: Replaced MSA words with authentic Tunisian dialect ('تواتي برشا' instead of 'مثالية', 'صوص' instead of 'مرقة' in this context).
- `steps.ar`: Used authentic Tunisian cooking terminology ('نمرقو', 'منفسة شوية', 'فلفل زينة').
- `steps.he`: Removed the '12 minutes' specification that was absent in other languages to maintain consistency. Improved culinary verbs ('להזהיב ולהתקרמל').
- `description.es`: Improved flow and natural phrasing ('El nombre Mhamsa proviene...', 'plato tradicional de Yerba').
- `steps.en`: Minor phrasing improvements for professional cookbook tone ('sauté', 'reduce the heat to low', 'simmer').

**tirshipumpkinsalad** (4 changes):
- `name`: Added '(סלט דלעת תוניסאי)' to the Hebrew name to match the format of the other languages.
- `description`: Hebrew: Fixed 'תוסס' (fermented) to 'ססגוני' (vibrant) and improved phrasing. Spanish: Changed 'El Tirshi deriva' to 'El nombre Tirshi deriva' and 'mesa' to 'comida'. Arabic: Changed 'مطيّبة' to 'طايبة' (cooked) and 'لصوص' to 'لتغميسة' (dip). English: Improved sentence flow.
- `ingredients`: Converted awkward metric measurements (30ml, 7g, 2.5g) to standard culinary spoons (tablespoons/teaspoons) in Hebrew, Spanish, and Arabic. Changed 'patata' to 'papa' in Spanish. Added 500g equivalent to English and Arabic for cross-language consistency.
- `steps`: Hebrew: Improved natural phrasing ('למנוע מהמטבל להיות מימי'). Spanish: Changed 'Triture' to 'Pise' for better culinary context. Arabic: Converted verbs to imperative form ('أسمط', 'قطّر', 'أرفس') for standard recipe instructions and used 'جاري' instead of 'مايه' for watery.


## Run Results (2026-02-20 23:16)
- Recipes reviewed: 20
- Successful: 0
- Errors: 20
- Total changes: 0
- Duration: 94.4s


## Run Results (2026-02-20 23:20)
- Recipes reviewed: 20
- Successful: 20
- Errors: 0
- Total changes: 107
- Duration: 218.1s

### Changes Summary

**adafina** (4 changes):
- `Hebrew`: Converted verbs to present plural (משרים, שמים) for standard Israeli cookbook style. Fixed '1000g' to '1 ק"ג'. Changed 'יחידות טופו' to 'גושי טופו' (blocks). Improved phrasing in description and steps.
- `Arabic`: Converted decimal measurements to natural fractions (e.g., 1.25 to cup and a quarter). Removed MSA phrasing and used authentic Tunisian/Maghrebi terms (كموسة, سلة سلة, قطيرة ماء). Fixed 'مريقة' to 'مرقة'.
- `Spanish`: Improved flow of description. Changed '1000g' to '1 kg'. Fixed 'unidades de tofu' to 'bloques de tofu'. Improved the caramel step warning and phrasing.
- `English`: Converted decimal measurements to fractions (1 ¼, ½). Changed 'units' to 'blocks' for tofu. Improved caramel warning and smoothed out the description.

**adamshusha** (3 changes):
- `ingredients`: Standardized measurements across languages (e.g., fixing the awkward '4.2 cups' to '4 cups (1 liter)' in English, adding volume/weight equivalents for clarity).
- `steps`: Clarified the vegan instructions (using tofu and chickpea batter) versus the traditional egg instructions to match the ingredient list, and integrated the missing Kala Namak into the final step.
- `description`: Polished phrasing in all languages for a more professional cookbook tone, ensuring authentic Tunisian Arabic vocabulary and natural Hebrew phrasing.

**banana_cake** (10 changes):
- `description.he`: Changed 'לחה' to 'עסיסית' (more natural for cakes) and 'בגרסה הצמחית' to 'בגרסה הטבעונית' (standard Hebrew term for vegan/plant-based).
- `description.ar`: Replaced MSA terms with authentic Tunisian dialect ('الموز' to 'البنان', 'بصوص التفاح' to 'بكومبوت التفاح', 'ولا باش تحلي فمك' to 'ولا باش تحلي بيها').
- `description.es`: Changed 'versión vegetal' to 'versión vegana' and 'capricho' to 'antojo dulce' for a more natural Latin American Spanish phrasing.
- `description.en`: Added 'or flaxseed' to match the other languages' descriptions which mention both applesauce and flax.
- `ingredients.ar`: Adjusted to Tunisian dialect ('كأس' to 'كاس', 'موز' to 'بنان', 'منخولة' to 'مغربلة', 'حبيبات شكلاطة' to 'بيبيت شكلاطة').
- `ingredients.es`: Changed 'harina de linaza' to 'linaza molida', 'pisadas' to 'hechas puré' (more universal than Argentine 'pisadas'), and 'harina común' to 'harina de trigo todo uso'.
- `steps.he`: Improved flow and clarity. Clarified 'מרפדים בנייר אפייה' (lining with parchment paper) and 'החלב המוחמץ' instead of 'החלב החמוץ'.
- `steps.ar`: Converted MSA phrasing into natural Tunisian dialect ('بابيي كويسون', 'ركض بالڨدا', 'كيردون', 'كلاصاج').
- `steps.es`: Clarified lining the pan ('papel para hornear') and changed 'leche agria' to 'leche cortada' which is the correct culinary term for milk mixed with vinegar.
- `steps.en`: Clarified 'sour milk mixture' to 'soy milk and vinegar mixture', 'butter batter' to 'butter mixture', and fixed capitalization in the final step.

**brikot** (5 changes):
- `ingredients`: Standardized measurements across languages, converting awkward metric volumes (15 ml capers, 30 g parsley) to natural culinary measurements (tablespoons, cups) for better readability.
- `hebrew`: Improved natural phrasing, adjusted measurements, and added 'עלי סיגר' as it is the most common Israeli term for brik/malsouka leaves.
- `arabic`: Replaced MSA intrusions with authentic Tunisian dialect (e.g., 'قلاية' instead of 'مقلاة', 'مذبّلة' for sautéed, 'بابيي نشّاف' for paper towels) and improved the natural flow of the steps.
- `spanish`: Refined sentence flow, corrected 'hebraizado' context, and adjusted measurements to standard Latin American/general Spanish culinary terms (tazas, cucharadas).
- `english`: Fixed grammatical number in the description ('Brikot is the Hebraized plural...') and refined step instructions for clarity.

**burekasthreeways** (3 changes):
- `description`: Hebrew: Improved flow and changed 'תרבות המאפיות' to a more natural phrasing. Arabic: Replaced MSA words with Tunisian dialect (e.g., 'تعداو' instead of 'سافروا', 'المعجنات' instead of 'الحلويات'). Spanish: Improved flow and vocabulary ('börek', 'cocina israelí'). English: Combined sentences for better flow and added umlaut to börek.
- `ingredients`: Hebrew: Fixed gender agreement ('פטרוזיליה מיובשת') and used standard local terms ('טחון מן הצומח'). Arabic: Added specific measurements ('مغارف كبار') and localized terms ('ثوم غبرة', 'فلوكون'). Spanish: Adapted to Latin American Spanish ('papa', 'molida') and clarified terms. English: Converted awkward decimals to standard recipe fractions (e.g., 2/3 cup, 1/4 tsp).
- `steps`: Hebrew: Replaced 'גליל' with 'רולדה' for pastry, added 'תנור שחומם מראש'. Arabic: Conjugated verbs to first-person plural ('نخلطو', 'ندهنو') and used authentic Maghrebi phrasing ('بالباهي', 'مزيان'). Spanish: Changed 'tronco' to 'rollo' or 'cilindro' for better culinary context, improved sealing instructions. English: Added Fahrenheit conversions, clarified slice thickness, and improved descriptive flow.

**cashew_cannelloni** (12 changes):
- `en.ingredients`: Converted decimal quantities to standard cookbook fractions (1/2, 1/4) for better readability.
- `en.description`: Corrected grammar from 'these tube-shaped pasta' to 'this tube-shaped pasta'.
- `en.steps`: Added definite articles ('the') for smoother, more natural instructional flow.
- `he.description`: Improved phrasing and word order to sound like natural Israeli cookbook text.
- `he.ingredients`: Changed 'צינורות' to 'גלילי' (more appropriate for pasta), and added 'עלי' to spinach and basil for culinary accuracy.
- `he.steps`: Refined cooking terminology (e.g., using 'רדיד אלומיניום' instead of 'נייר כסף', and 'שקית זילוף' instead of 'שק זילוף').
- `es.name`: Changed 'Anacardos' to 'Castañas de Cajú' to be more widely understood in Latin America.
- `es.ingredients`: Replaced 'marchitas' with 'salteadas' as 'marchita' sounds unappetizing in Spanish culinary contexts. Added 'castañas de cajú' for regional inclusivity.
- `es.steps`: Improved flow and clarity of instructions, ensuring natural Latin American phrasing.
- `ar.description`: Replaced MSA words with authentic Tunisian dialect (e.g., 'سبناخ' instead of 'سبانخ', 'صوص' instead of 'صالصة').
- `ar.ingredients`: Wrote out fractions naturally in dialect (e.g., 'زوز كيسان ونص', 'شطر') and clarified measurements.
- `ar.steps`: Replaced MSA culinary terms with common Tunisian equivalents ('ميكسور' instead of 'خلاط', 'بوش' instead of 'جيب حلواني').

**chocolatepeanutbuddy_bars** (10 changes):
- `name.ar`: Changed 'بارات' to 'مربعات' (squares) as it is much more natural for dessert bars in Arabic.
- `description.en`: Fixed awkward phrasing 'root to snatch' to 'root meaning to snatch'.
- `description.he`: Improved word order for 'chewy peanut butter blondie base' and added quotes around the root word for clarity.
- `description.es`: Changed 'base masticable' to 'base de blondie... de textura suave' for a more appetizing translation, and fixed 'huevos con lino' to 'huevos por linaza'.
- `description.ar`: Used authentic Tunisian vocabulary ('زريعة الكتان' instead of 'بذور الكتان', 'بلاش حليب' instead of 'من غير حليب').
- `ingredients.he`: Changed 'קמח רגיל' to 'קמח לבן' and clarified 'שוקולד צ'יפס טבעוני'.
- `ingredients.es`: Changed 'harina común' to 'harina de trigo todo uso' and 'harina de linaza' to 'linaza molida'.
- `ingredients.ar`: Adjusted to natural Tunisian measurements and terms ('كاس', 'مغارف كبار', 'زريعة كتان', 'حبيبات شوكولاتة').
- `steps.ar`: Fixed typo 'افرح' to 'أطرح' (spread) and ensured all verbs and grammar reflect authentic Tunisian dialect ('ركض', 'صحفة', 'لين يولّيو').
- `steps.es`: Clarified step 8 to say 'hasta que estén brillantes y suaves' instead of 'hasta que se ablanden'.

**cholent** (4 changes):
- `ar`: Fixed Hebrew characters mixed in Arabic text ('الشولנט' to 'الشولنت'), improved Tunisian dialect authenticity (e.g., 'طنجرة قاعها خشين', 'لين يحماروا'), and clarified measurements.
- `he`: Improved natural phrasing for Israeli Hebrew, corrected ingredient names (e.g., Kidney beans to 'שעועית אדומה'), and refined step instructions for better flow.
- `es`: Adjusted capitalization, changed 'alubias' to 'frijoles' for better Latin American Spanish alignment, and improved the flow of the cooking steps.
- `en`: Refined phrasing to match professional cookbook style, fixed redundant wording in ingredients (e.g., 'chunks... chunks'), and improved sentence structure in steps.

**chraimespicyfish_stew** (3 changes):
- `description`: Fixed awkward translation of 'a little forbidden' in Hebrew and Arabic. Corrected 'crumbled tofu' to 'sliced tofu' across all languages to match the ingredients list.
- `ingredients`: Converted awkward gram measurements for spices and small liquid amounts to standard spoons (tablespoons/teaspoons) in Hebrew and Spanish. Improved natural phrasing.
- `steps`: Fixed 'sotage' in English to 'sauté pan'. Improved culinary verbs (e.g., 'coat' instead of 'mix' for the tofu and nori) and ensured natural flow in all languages.

**cujada** (3 changes):
- `description`: Improved flow and natural phrasing across all languages. Made the Arabic version sound authentically Tunisian/Maghrebi (e.g., 'الصبليونية', 'تشد روحها', 'العظم'). Adapted Spanish to sound more natural.
- `ingredients`: Standardized formatting (e.g., '4 medium potatoes, peeled' instead of '4 potatoes, peeled (medium)'). Changed 'patatas' to 'papas' and 'levadura química' to 'polvo de hornear' for Latin American Spanish. Used 'فرينة' instead of 'دقيق' for Tunisian Arabic. Rounded awkward decimals in Spanish/Hebrew grams (e.g., 4.8g to 5g).
- `steps`: Clarified in all languages that the chickpea flour and water need to be mixed together *before* adding to the potatoes. Updated 'salt' to 'Kala Namak'/'black salt' in the seasoning step to match the ingredients list. Used Tunisian dialect terms like 'كيردون' (toothpick) and 'شقالة' (bowl).

**granola_cookies** (3 changes):
- `description`: Refined phrasing across all languages to make the etymological explanation ('Ugiot' meaning round baked goods/cookies) sound natural rather than like a literal, clunky translation. Improved flow and professional tone.
- `ingredients`: Corrected ingredient names to standard culinary terms in each language (e.g., 'זרעי פשתן טחונים' in Hebrew, 'linaza molida' and 'hojuelas de avena tradicional' in Spanish, 'زريعة كتان' and 'شوفان كعب' in Tunisian Arabic, 'old-fashioned rolled oats' in English).
- `steps`: Adjusted verbs and baking terminology to sound authentic to native speakers (e.g., 'מקרימים' and 'תלוליות' in Hebrew, 'تشد روحها' and 'بابيي كويسون' in Tunisian Arabic, 'accesorio de paleta' in Spanish, 'edges are set' in English).

**homemade_couscous** (4 changes):
- `ingredients`: Fixed unnatural decimal quantities (e.g., '2.1 cups' to '2 cups plus 2 tablespoons' in English, 'نص ليترا' in Arabic) and '0.25 cups' to standard fractional measurements.
- `description`: Improved phrasing across all languages to read like professional cookbook text. Fixed awkward literal translations (e.g., 'Homemade Couscous comes from the word...' changed to 'The word couscous comes from...').
- `steps`: Replaced literal verbs with proper culinary terms (e.g., 'sprinkle/drizzle' instead of 'pour' for water/oil, 'מנפים' instead of 'שופכים דרך נפה' in Hebrew, 'بخو' and 'فتل' in Tunisian Arabic).
- `name`: Added 'ביתי' to Hebrew and 'دياري' to Arabic to match the 'Homemade' aspect of the title.

**maakouda** (5 changes):
- `description.en`: Replaced awkward 'knotted' with 'bound together' for natural culinary English.
- `ingredients`: Changed '0.5' to '1/2' across all languages for standard recipe formatting.
- `hebrew_text`: Changed 'מחית' to 'פירה' and 'עוגה' to 'פשטידה' for natural Israeli phrasing. Improved sentence flow and clarified nutritional yeast.
- `spanish_text`: Changed 'patatas' to 'papas' for Latin American Spanish. Improved phrasing and changed 'pastel' to 'tortilla' in the flipping step.
- `arabic_text`: Enhanced Tunisian dialect (e.g., used 'شطر', 'قلاية', 'تحمار'). Removed MSA phrasing and clarified measurements ('مغارف كبار').

**mahshistuffedvegetables** (3 changes):
- `description`: Refined phrasing across all languages for better flow. In Hebrew, changed 'נזיד' to 'רוטב' which is more natural for stuffed vegetables. In Arabic, replaced MSA words with authentic Tunisian terms ('فاحات' instead of 'بهارات', 'مرقة خاثرة'). In English and Spanish, improved sentence structure for professional cookbook tone.
- `ingredients`: Fixed awkward fractional cup measurements in English and Arabic (e.g., 1.1 cups, 1.7 cups) to standard cookbook fractions with gram equivalents. In Arabic, used the specific Tunisian term for zucchini ('قرع بوطزينة'). In Hebrew, moved adjectives to sound more natural ('תפוחי אדמה בינוניים ואחידים').
- `steps`: Converted Hebrew steps to the standard present-plural tense used in Israeli cookbooks (מרוקנים, מכינים). In Arabic, used authentic Maghrebi cooking verbs ('ستّف' for arrange, 'تطيب سلة سلة' for simmer). Removed confusing mention of 'cabbage leaves' in English/Spanish since they are not hollowed out.

**mochajavacake** (3 changes):
- `description.es`: Changed 'decadente' to 'exquisito' as 'decadente' is a false friend in Spanish and means 'decaying' rather than 'indulgent'.
- `ingredients`: Converted decimal cup measurements to standard fractions in English and Arabic. Localized ingredient names (e.g., 'crema vegetal para batir' instead of 'nata', 'קמח לבן' instead of 'קמח רגיל', 'كسرونة' instead of 'طنجرة').
- `steps`: Replaced 'first/second portion' with specific references to the cake or glaze ingredients to avoid confusion. Improved natural flow and culinary terminology in all languages.

**nougatandpeanutcakemor_abergil** (3 changes):
- `description`: Hebrew: Reworded to avoid awkwardly explaining Hebrew words in Hebrew. Arabic: Transliterated the Hebrew name into Arabic script and fixed dialect phrasing. Spanish: Adapted to Latin American Spanish (maní, hojuelas de maíz). English: Improved flow.
- `ingredients`: English: Fixed awkward decimal measurements (0.7 cups -> 3/4 cup) and pluralization (1 cups -> 1 cup). Arabic: Fixed decimal measurements to natural fractions (كاس غير ربع) and used authentic terms. Spanish: Changed to Latin American terms (crema para batir, maní). Hebrew: Changed 'יחידה' to 'חבילה' for the pudding mix.
- `steps`: Arabic: Removed a Hebrew word ('والمמרحات') that accidentally crept into step 2 and used authentic Tunisian cookware terms (كسرونة). Spanish: Improved natural flow and used Latin American terminology. English: Clarified instructions (e.g., 'plant-based cream' instead of 'vegetable cream'). Hebrew: Improved phrasing for clarity and natural flow.

**pizza** (4 changes):
- `name`: Updated Hebrew and Arabic names to better reflect the English/Spanish titles, as 'פיצה' and 'بيتزا' were too generic.
- `description`: Fixed awkward phrasing in Hebrew ('שמשמעותם נגיסה'). Improved Tunisian Arabic vocabulary ('تبين', 'أستوس', 'متاع'). Refined Spanish and English flow for professional cookbook style.
- `ingredients`: Clarified quantities in Arabic (added 'كبار' for tablespoons, specified 'ثوم غبرة'). Fixed redundant 'sheet' in English nori ingredient. Standardized Spanish bouillon description.
- `steps`: Converted Hebrew steps to the standard present-plural tense (מחממים, מרדדים). Enhanced Tunisian Arabic dialect naturalness ('بابيي كويسون', 'مشّي الصالصة بالباهي'). Improved Spanish and English clarity and consistency.

**redstewedolives** (7 changes):
- `name.es`: Changed 'Aceitunas Guisadas Rojas' to 'Aceitunas Guisadas en Salsa Roja' for a more natural Spanish phrasing.
- `description.he`: Improved flow and natural phrasing for Israeli Hebrew speakers (e.g., 'זיתון משמעותו זית', 'מגש הקמיה').
- `description.es`: Refined phrasing to sound more like a professional Spanish cookbook (e.g., 'es el nombre de esta suave ensalada', 'mojar con pan fresco').
- `description.ar`: Adjusted to authentic Tunisian dialect, replacing awkward literal translations with natural Maghrebi phrasing (e.g., 'البنينة', 'صوص').
- `description.en`: Polished sentence structure for better flow ('is the name of this tender cooked salad', 'in this vegan version, blanched green olives are simmered').
- `ingredients`: Standardized decimal quantities to fractions (e.g., 0.5 to 1/2 or 'شطر'), added volume equivalents to grams for clarity, and used authentic regional ingredient names (e.g., 'فاح دجاج' instead of 'تابل دجاج' in Tunisian).
- `steps`: Refined cooking terminology across all languages for a professional tone (e.g., 'sofría' in Spanish, 'sauté' in English, 'לפתוח את התבלינים' in Hebrew, 'تتلبس بالزيتون' in Arabic).

**sfingh** (12 changes):
- `description.he`: Fixed gender agreement (סופגניות הן), corrected unnatural transliteration (שפינג'ות to ספנג'), and improved phrasing.
- `ingredients.he`: Changed 1000g/ml to 1 kg/1 liter for natural reading, changed 'hot water' to 'warm water' (חמימים).
- `steps.he`: Used proper culinary terms (קורצים instead of צובטים, נייר סופג) and improved flow.
- `description.es`: Improved natural phrasing (ramas de la familia instead of lados).
- `ingredients.es`: Changed 1000g/ml to 1 kg/1 litro for standard recipe format.
- `steps.es`: Improved culinary verbs (rebócelos, reposar, papel absorbente).
- `description.ar`: Replaced MSA with authentic Tunisian dialect (شيرات مختلفة, كعبات).
- `ingredients.ar`: Used Maghrebi terms (مغربلة instead of منخولة), fixed awkward decimal quantities (ربع كاس instead of 0.25).
- `steps.ar`: Used authentic Tunisian culinary terms (شقالة, كعبورة, هكاكة).
- `description.en`: Improved punctuation and flow.
- `ingredients.en`: Changed decimals to fractions (1/4 cup, 4 1/4 cups) and specified 'active dry yeast'.
- `steps.en`: Improved phrasing ('doubled in size', 'drain on paper towels').

**veganfishchraime** (6 changes):
- `description.he`: Fixed awkward phrasing. 'המנה נגזרת...' is an unnatural translation. Changed to 'מקור השם...' for a native flow.
- `steps.he`: Corrected minor grammar in step 2 (added definite articles where appropriate) and changed 'מחבת רחבה' to 'סיר רחב או מחבת עמוקה' which is more natural for Chraime.
- `description.es`: Changed 'caliente' to 'picante' as the English 'hot' meant spicy, not temperature. Fixed transliteration of 'ktzitzot'.
- `name.es, steps.es`: Changed 'albóndigas' (meatballs) to 'tortitas' (patties) to accurately reflect the flat shape of the dish. Changed 'abrir las especias' (literal translation) to 'tostar las especias'.
- `ingredients.ar, steps.ar`: Replaced MSA and literal translations with authentic Tunisian Maghrebi vocabulary (e.g., 'ثوم غبرة' for garlic powder, 'فلفل زينة' for paprika, 'صالصة' for sauce, 'تسيّب ماها' for releasing juices).
- `description.en, steps.en`: Fixed the awkward transliteration 'ktzi'tzot' to 'ktzitzot'. Changed the literal translation 'open the spices' to the correct English culinary term 'bloom the spices'.
