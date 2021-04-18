## Cvicenie 08 - Synchronne vs asynchronne programovanie

### Modelova aplikacia

- aplikacia vykonava simulaciu na 2 etapy
- v 1. kroku sa niekolkokrat (podla daneho parametra) zavola API
 na ziskanie nahodnej URL s obrazkom/gifom/videom psa
- v 2. kroku sa zavola samotna URL ktora sa ziskala v prvom kroku
- podla parametra *open_tab* v tasku *task_open_tab* je mozne nie len
 poslat request na danu URl ale ju aj priamo otvorit v Google Chrome
 
#### Synchronna verzia

 - pri inicializacii sa do *queue* vlozi rovnaka adresa **Random Dog API**
  v urcenom pocte (momentalne 20)
 - pri vykonavani ukonov z queue sa po ziskani odpovede zapise nova URL
 do 2.queue (*tab_queue*)
 - kedze oba tasky su spustane konkurentne, po vykonani prveho (a ulozeni 
 novej URL do 2. queue) sa hned spusti 2.task, ktory uz nema prazdnu queue
 a hned vykona request na ziskanu URL
 - takymto sposobom sa striedaju oba tasky
 
 Prikladovy vystup:
 ```text
Getting new dog
Getting dog elapsed time: 0.6
Opening tab, URL: https://random.dog/1186-4923-20498.jpg
Opening tab elapsed time: 0.7
Getting new dog
Getting dog elapsed time: 0.6
Opening tab, URL: https://random.dog/c5421793-3bfc-4f58-aae2-4c573100f162.jpg
Opening tab elapsed time: 0.7
Getting new dog
Getting dog elapsed time: 0.5
Opening tab, URL: https://random.dog/151d0e72-38b2-41c8-9edf-152540c4a0f1.mp4
Opening tab elapsed time: 0.7

Total elapsed time: 3.7
```

#### Asynchronna verzia

 - pracuje na rovnakom principe ako synchronna verzia
 - kedze oba tasky su spustene asynchronne, nastava tu problem:
    - *task_open_tab* skontroluje ci nie je queue prazdny v rovnakom case
     ako *task_get_dog*
    - kedze oba tasky bezia konkurente, necakalo sa najprv na blokujuce
     volanie (zavolanie URL) a queue v *task_get_tab* bol v tom case prazdny
    - aby sa predislo tomuto problemu, beh v 2. koroutine je zastaveny az do
     casu kym *tab_queue* nie je prazdna
     
 Prikladovy vystup:
 ```
Getting new dog
Getting dog elapsed time: 0.8
Getting new dog
Opening tab, URL: https://random.dog/609295d8-8497-45ed-9c2c-d3c4330109cb.mp4
Getting dog elapsed time: 0.1
Getting new dog
Getting dog elapsed time: 0.1
Opening tab elapsed time: 0.7
Opening tab, URL: https://random.dog/c6c7ab71-bf8c-4c1d-8bee-31cbdf5e2f5e.jpg
Opening tab elapsed time: 0.7
Opening tab, URL: https://random.dog/b69af17b-1812-4e95-adba-0e6d1b6d5064.jpg
Opening tab elapsed time: 0.7

Total elapsed time: 2.8
```

#### Zaver
 - z ukazky je viditelne ze v asynchronnom pripade necaka rychlejsi task
  (ziskanie URL s obrazkom psa) na dokoncenie pomalsieho tasku (otvorenie
  daneho URL), takze sa po dokonceni prveho requestu spustaju 2 sucasne
  a postupne dobehnu vsetky requesty v prvej queue, zatial co 2. este bezi
 - vykonanie prveho requestu v asynchronnom priklade bezne trvalo dlhsie
  ako vykonanie 1. requestu v synchronnom (pravdepodobne kvoli inicializovaniu
  session), nasledne volania su ale ovela rychlejsie, zatial co pri
  synchronnej verzii sa ich rychlost nemeni
 - v dosledku nutnosti cakania na dokoncenie 1. requestu v 1. tasku,
  na spustenie 2. tasku je rozdiel v rychlosti medzi verziami pri malom
  pocte requestov len minimalny
 - realny rozdiel je vidiet na velkom mnozstve requestov - pri 20 volaniach
  v oboch taskoch je to **14.3s** vs **25.2s** v prospech asynchronnej verzie