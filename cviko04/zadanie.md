##Cvičenie 4

### 1. Analýza synchronizačných úloh

- **vyhladovenie** - čidlá alebo monitory by sa mohli dostať do stavu vyhladovania
- **súčasný prístup ku zdieľaným dátam** - pri zisťovaní aktuálneho počtu aktívnych
 čidiel/monitorov
- **konzistencia** - čidlá aj monitory pracujú vždy za rovnakých podmienok
- **rôzne oprávnenia** - zapisovať dáta môže len čidlo, zatiaľ čo čítať môže aj monitor 

    
    
- 
### 2. Namapovanie synchronizačných úloh na zadanie
- problém vyhladovenia sa rieši extra turniketom pre čidlá, ktoré postupne vchádzajú po 1
(riadky 46-47)
- aby sa zabránilo čítaniu informácie o aktuálnom počte aktívnych čidiel počas zmeny tohto
 údaju, metóda *lock()* v Lightswitchi bola upravená a vracia aktuálnu hodnotu countera
 v momente zápisu (riadky 20-22)
- ďalší semafor je použitý na zabezpečenie konzistencie, ktorý povolí spustenie
čítania pre monitory len potom ako zapísali všetky čidlá (riadky 58-60)
    

    
-
### 3. Pseudokód
```
sensor():
    wait_random_interval()
    enter_turnstile()

    lock_data_access()
    increase_counter_in_turnstile()
    if all_sensors_active:
        signal_monitors()
    write()
    unlock_data_access()

monitor():
    wait_for_all_sensors_active()
    enter_turnstile()
    
    lock_data_access()
    read()
    signal_next()
    unlock_data_access()
    
```