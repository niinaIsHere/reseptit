# pylint-report

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:111:7: E0606: Possibly using variable 'user_id' before assignment (possibly-used-before-assignment)
app.py:127:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:132:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:226:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:19:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module items
items.py:1:0: C0114: Missing module docstring (missing-module-docstring)
items.py:68:0: R0913: Too many arguments (6/5) (too-many-arguments)
items.py:68:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)

------------------------------------------------------------------
Your code has been rated at 9.64/10
```

## Missing module docstring
Moduulit eivät tekijän mielestä tarvitse kommentteja tiedostojen alkuun, joten jätetty laittamatta.

## Missing function or method docstring
Jätetty laittamatta pariin kohtaan, koska niissä ei tekijän mielestä niitä tarvittu.

## Using variable 'user_id' before assignment
Muuttujaa 'user_id' ei käytetä ennen, kun sille asetetaan arvo, se asetetaan aiemmassa if-sarakkeessa.

## Inconsistent return-statements
Return statementit ovat kaikki muotoa, jossa ohjataan jollekin sivulle. Lisäksi on abort-statementit, jotka keskeyttävät toiminnan ja niiden vuoksi kohtiin ei tarvita return-statementtejä.

## Dangerous default value [] as argument
Ainoastaan tiedosto db.py sisältää funktioita, joiden default value on []. Funktioita käytetään ainoastaan tietokantaan liittyvissä toiminnoissa koodin sisältä ja listalta ainoastaan luetaan parametrit.

## Too many arguments
Näissä funktioissa argumentteja vaadittiin 6, koska niissä muokataan tietokannan tietokohteita.
Jokainen arvo voi muuttua, joten jokaiselle arvolle on oltava paikka funktiossa, sillä ne on saatava järjestyksessä SQL-kyselyyn.
Ei korjattu, koska ei nähdä järkeväksi esimerkiksi pilkkoa funktiota moneen osaan.









