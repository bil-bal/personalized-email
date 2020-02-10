Email Skript zum verschicken von personalisierten Emails mit
HTML Inhalt, mehreren pdf-Dateien als Anhang und Inline HTML Bildern an eine .csv Liste mit

name,nachname,email,nummer

Skript geschrieben um Lohnabrechnungen und Gehaltserklärungen automatisiert zu verschicken.

-Alle Pfade in relativem Pfad zum Ausführort angeben.
 "..\\muster\\" bedeutet dabei der Ordner muster im Übergeordneten Ordner des Ausuführortes.
 Wichtig bei Pfadangaben und falls nötig in Dateinamen: zwei Backslash benutzen (\\\\).

-Um mehr Dateien anzuhängen mit Komma getrennt und in Anführungszeichen innerhalb der eckigen Klammern entsprechend einfügen.
 z.B. um eine weitere PDF anzuhängen in 
 
  "file_name": ["bsp_name1.pdf", "bsp_name2.pdf", "neue_datei.pdf"]
  
  für den Pfad entsprechend das gleiche:
  
  "file_path": ["..\\bsp_ordner\\$datei_name$", "..\\bsp_ordner2\\$datei_name$", "..\\neuer_ordner\\$datei_name$"]

-In Pfaden und Dateinamen sowie im HTML Text werden die Variablen $monat$, $tag$, $jahr$, $datei_name$, $name$, $nachname$, $nummer$
 entsprechend ersetzt.

-Inline Images in der HTML werden über die Content-ID eingesetzt. 
 Hier auch weitere Bilder über das einfügen der Namen, Pfade, und Content-IDs an das Ende der Liste möglich.
 Content-ID als HTML Tag in <_> setzen:
	"<beispielID>"
-Inhalt der HTML als .txt datei im Ausführort speichern.

-Wenn fertig eingestellt 
	"setup_done": false 
 in settings.txt auf true setzen: 
	"setup_done": true
