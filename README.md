# Greenscreen Foto App

Frontend um Fotos aufzunehmen und Hintergrund ändern mittels OBS.

## Setup

1. OBS herunterladen: https://obsproject.com/download.
1. OBS starten.
1. Alle gewünschten Hintergründe als Source hinzufügen und sinnvoll benennen, da die Namen der Hintergründe später genauso in der App stehen werden.
1. Die Kamera als Source hinzufügen und in den Vordergrund bringen. Um die Auflösung des OBS Streams an die Kamera anzupassen, siehe [unten](#obs-einstellungen-für-die-auflösung).
1. Greenscreen-Filter für die Kamera hinzufügen. Er ist unter "Effect Filters" und er heißt "Chroma Key". Die Einstellungen können beliebig angepasst werden.
1. "Start Virtual Camera" drücken.
1. Im File `picturesScript.py` die Settings updaten. Die Namen der Kamera und 
der Backgrounds müssen die gleichen sein, wie die Namen der "Sources" in OBS.
Die `cameraID` ist die ID der Virtual Camera von OBS. Man kann die richtige ID durch Ausprobieren finden, wahrscheinlich ist es eine Zahl zwischen 0 und 5. 
Die `actual_width` und `actual_height` ist die Auflösung der Fotos, also am besten die Auflösung der Kamera angeben. 
Die `display_width` und `display_height` ist die Größe des angezeigten Videos auf der App und muss an die Größe des Bildschirms angepasst werden.
1. Script starten.

### OBS Einstellungen für die Auflösung

Damit die Bilder mit ihrer vollen Auflösung gespeichert werden, muss man OBS so einstellen, dass es das Video mit der richtigen Auflösung streamt.

1. Unter `Settings/Video` bei OBS muss man bei `Base` und `Output` die Resolution der Kamera angeben (z.B. für eine UH Kamera: `3840x2160`).

oder

1. Rechtsklick auf Video Input
2. `Resize output (source size)`

## Features

1. Man kann einen von mehreren Hintergründen aussuchen.
1. Man kann Fotos machen, die automatisch in aufsteigender Reihenfolge nummeriert werden und im Verzeichnis `img/` gespeichert werden.
1. Man kann einen Countdown von 10 Sekunden starten um ein Foto zu machen.
1. Wenn man einen Namen eingibt für das Bild, dann wird die Datei so benannt (mit einer Zahl davor und `.jpg` am Ende).

### Beispiel

![Beispielbild](beispiel.png)
