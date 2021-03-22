##Cvičenie 5 - Divosi

### 1. Synchronizačné problémy

- **signalizácia** - v modeli vždy signalizuje len jeden zo skupiny vlákien
 (divoch alebo kuchár) na základe toho kto príde posledný
- **vzájomné vylúčenie** - ku kotlu vždy pristupuje len jedna skupina, nie obe súčasne
(Môže nastať stav, že kuchár, ktorý naplnil kotol už signalizoval začatie konzumácie pre divochov,
zatiaľ čo v tom čase iný kuchár ešte len dovaril svoju porciu. Aby bolo zabránené jeho prístupu,
 používa sa flag *shared.eating*)


### 2. Pseudokód
```
savage():
    start_function()
    wait_for_all_sibling_processes()

    ### CRITICAL AREA
    if all_sibling_processes_ready:
        check_available_servings()
        if pot_empty():
            signal_cooks()
            wait_for_full_pot()
        take_from_pot()
    ###

    return_back_to_front()

cook():
    wait_for_empty_pot_signal()
    prepare_serving()

    ### CRITICAL AREA
    put_serving_to_pot()
    if pot_full():
        signal_savages()
    ###

    wait_for_next_signal()    
```

### 3. Charakteristiky modelu
 - model reaguje inak v závislosti od parametrov
 - v prípade, že je viac kuchárov ako maximálny počet porcií v kotli
  (nepraktické použitie modelu),
 nadbytočný počet kuchárov už nie je schopný vložiť svoju porcii do kotla a ich práca je teda zbytočná
 - nastáva to kvôli vzájomnému vylúčeniu, kedy už po signalizovaní začatia konzumácie nemôžu ku kotlu
  pristupovať kuchári 
 - v prípade, že je menej kuchárov ako možných porcií, aby sa predošlo nekonečnému cyklu,
 kuchár pri vložení porcie signalizuje či je ešte potrebné variť ďalej
 - v tomto prípade sa už ale nesignalizuje všetkým kuchárom naraz, iba jednému ďalšiemu
  (ktorý môže signalizovať ďalej)
 