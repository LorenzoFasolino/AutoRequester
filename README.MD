# ESECUZIONE
-   Avviare Wireshark

-   Eseguire prima il test selenium 'seleniumTest.py' indicando la durata del test in minuti
    -   es. 'python3 seleniumTest.py 25'

-   Stoppare wireshark ed esportare il file JSON

-   Copiarlo nella cartella 'jsonFIles'
    -   es. 'jsonFiles/25min.json'

-   Eseguire 'jsonAnalysis' passando come parametro il percorso del file da analizzare
    -   es. 'python3 jsonAnalysis.py jsonFiles/25min.json'

-   I risultati saranno visibili nella cartella result