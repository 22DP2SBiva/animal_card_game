# **Animal card game**

###### - dzīvnieku kāršu spēle -

---

### Spēles pamata princips

Lietojot savas kārtis ir jācenšas nosist visas pretinieka (dators) kārtis, lai uzvarētu.

Katra kārts var nosist tikai sev zemāka vai vienāda līmeņa kārtis.

Ja visas jūsu kārtis ir nosistas, tad jūs zaudējat.

### Spēles noteikumi

##### Kārtis

Spēlē kārtis darbojas līdzīgi barības ķēdes hierarhijai:

> Sienāzis <- Varde <- Čūska <- Vanags

- Sienāzis var tikai nosist citu Sienāzi;
- Varde var nosist Sienāzi un citu Vardi;
- Čūska var nosist Sienāzi un Vardi, un citu Čūsku;
- Vanags var nosist visus pārejos un citu Vanagu.

Katrs kārts var **tikai vienu reizi** cīnīt citu kārti.

##### Kāršu pārvēršanās

Gājiena beigās, katru gājienu, spēlētājam kārtis pārvēršas uz lielāka līmeņa kārti, ja ir iespējams.

- Sienāzis pārvēršas par Vardi;
- Varde pārvēršas par Čūsku;
- Čūska pārvēršas par Vanagu;
- Vanags **nevar pārvērsties**, jo nav uz ko pārvērsties.

##### Gājiens

Paša 1. gājiena sākumā katram spēlētājam automātiski un nejauši tiek izvilktas 3 kārtis.
Katru nākošo gājienu katram izvilk 1 kārti, joprojām nejauši izvēlētu.

Katru gājienu jums ir arī izvēle Cīnīt un/vai Beigt gājienu.

Katra gājiena sākumā (neskaitot 1. gājienu) jums ir jāupurē viena kārts un tad automātiski tiek izvilkta jauna.

Pretiniekam nav jāupurē kārts, toties pretiniekam katru gājienu kārtis nepārvērtas par vienu līmeni lielākām.

##### Cīnīt

Ja izvēlaties cīnīt, tad tev ir jāizvēlas viena no savām kārtīm un viena no pretinieka, kuru cīnīs.
Pēc tam, algoritms automātiski izlems, pēc barības ķēdes, kurš šinī cīņā uzvarēja un to izvadīs.

##### Beigt gājienu

Ja izvēlaties beigt gājienu, tad algoritms aprēķina, vai jūs esat jau uzvarējuši vai zaudējuši, ja nē, tad sāk jaunu gājienu.

Pretējā gadījumā, jums iedod iespēju vai nu sākt spēli no jauna, vai nu beigt spēlēt, kas aiztaisīs termināli.

##### Zaudēšana

Ja jums ir neviena kārts palikusi un pretiniekam ir vismaz viena kārts, tad jūs zaudējat.
Bet, ja abiem nav neviena kārts, tad abi zaudē.

##### Uzvarēšana

Ja jums ir vismaz viens kārts un jūs esat nosituši visas pretinieka kārtis, tad uzvarat.
