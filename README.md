# **Dzīvnieku kāršu spēle**

## Ieinstalēšana/Spēles palaišana

---

1) No saites https://code.visualstudio.com/ instalējiet Visual Studio Code (tieši Windows versiju).
    a) Iekš Visual Studio Code apakšcilnes Extensions instalējiet Python extension.
2) Python mājaslapā https://www.python.org/downloads/ instalējiet Python jaunāko versiju.
3) Lai Pygame instalētu, atveriet saiti https://www.pygame.org/news un kopējiet jaunākā ieraksta kodu (piemēram, ```python -m pip install -U pygame==2.5.2 --user```), atveriet Windows PowerShell un iekopējiet kodu iekš PowerShell, spiediet Enter pogu. Tagad Pygame automātiski instalēsies jūsu datorā.
4) Atveriet linku https://github.com/22DP2SBiva/animal_card_game un spiediet uz pogas Code -> Download ZIP. Izpakojiet .zip failu un saglabājiet šo folderi viegli pieejamā vietā uz datora.
5) Lai sāktu spēli, iekš Visual Studio Code uzspiediet uz apakšcilnes File -> Open Folder un izvēlaties iepriekš saglabāto folderi ar spēli. Atveriet game.py un spiediet uz trijstūrveidīgas pogas Run Python File.



## Kā spēlē

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

Abu spēlētāju gājiena beigās, katru gājienu, spēlētājam kārtis pārvēršas uz lielāka līmeņa kārti, ja ir iespējams.

- Sienāzis pārvēršas par Vardi;
- Varde pārvēršas par Čūsku;
- Čūska pārvēršas par Vanagu;
- Vanags **nevar pārvērsties**, jo nav uz ko pārvērsties.

##### Gājiens

Paša 1. gājiena sākumā katram spēlētājam automātiski un nejauši tiek izvilktas 6 kārtis.
Katru nākošo gājienu katram izvilk 1 kārti, joprojām nejauši izvēlētu.

Katru gājienu jums ir arī izvēle Cīnīt un/vai Beigt gājienu.

##### Cīnīt

Ja izvēlaties cīnīt, tad tev ir jāizvēlas viena no savām kārtīm un viena no pretinieka, kuru cīnīs. (Ar kreiso peles pogu)
Pēc tam, algoritms automātiski izlems, pēc barības ķēdes, kurš šinī cīņā uzvarēja un to izvadīs.

##### Beigt gājienu

Ja izvēlaties beigt gājienu, tad algoritms aprēķina, vai jūs esat jau uzvarējuši vai zaudējuši, ja nē, tad sāk jaunu gājienu.

Pretējā gadījumā, jums iedod iespēju vai nu sākt spēli no jauna, vai nu beigt spēlēt.

##### Zaudēšana

Ja jums neviena kārts nav palikusi un pretiniekam ir vismaz viena kārts, tad jūs zaudējat.
Bet, ja abiem nav neviena kārts, tad abi zaudē.

##### Uzvarēšana

Ja jums ir vismaz viena kārts un jūs esat nosituši visas pretinieka kārtis, tad jūs uzvarat.
