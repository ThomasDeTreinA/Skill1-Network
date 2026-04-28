<div align="center">
  <h1>🌐 Network Simulator</h1>
  <p><i>Leer stap voor stap de basis van netwerkarchitectuur, bekabeling en IP-configuraties op een interactieve manier.</i></p>

</div>

---

## 🎮 Over het Project

Welkom bij de **Network Simulator**! Deze game is ontworpen om studenten en enthousiastelingen wegwijs te maken in de
wereld van netwerken. Van het trekken van de juiste kabels tot het configureren van ISP-gegevens en automatische
DHCP-servers.

### 📚 Level Uitleg

| Level       | Thema             | Wat je leert                                                                                        |
| :---------- | :---------------- | :-------------------------------------------------------------------------------------------------- |
| **Level 1** | 🔌 De Basis (LAN) | Gebruik van PC's, Hubs en Switches. Werken met **Straight-Through** kabels en kabelafstanden (Cat 5 vs Cat 5e). |
| **Level 2** | 🛠️ Routing & ISP  | Handmatige IP-configuratie, Subnet Masks en het instellen van **ISP-gegevens** op de router.        |
| **Level 3** | 🏢 DHCP & Crossover| Blueprint weergave, netwerk redundantie met 2 routers (**Crossover** kabel), en **DHCP** activatie. |
| **Level 4** | 🌍 Wi-Fi & Wereldkaart| **Wi-Fi** netwerken instellen op een Laptop en gebouwen verbinden via de Wereldkaart. |

---

## ⌨️ Bediening & Toolbar

In de simulator gebruik je de toolbar aan de boven- en rechterkant om je netwerk op te bouwen:

### Apparaten (Boven)

- **[PC]**: Vaste werkplek, vereist een kabelverbinding.
- **[Laptop]**: Draagbaar, verbindt draadloos via **Wi-Fi** (inclusief wachtwoord configuratie).
- **[Switch/Hub]**: Verdeelpunten voor je lokale netwerk.
- **[Router]**: Het hart van het netwerk voor routing en **DHCP**.
- **[Delete]**: Activeer de verwijder-modus (Toets `D`) voor kabels of apparaten.

### Kabels (Rechts)

- **Cat 5 / Straight-Through**: Voor verschillende apparaten (bijv. PC naar Switch).
- **Cat 5e**: Voor lange afstanden (snellere koperkabel).
- **Crossover**: Voor gelijke apparaten (bijv. Router naar Router).
- **WAN Fiber**: Voor verbindingen tussen gebouwen op de wereldkaart.

> **Tip:** Klik op een apparaat om het **OS-scherm** te openen. Hier vind je de IP-instellingen, DHCP-configuratie, een interactieve **Terminal** (ping, ipconfig) en de webbrowser om websites te bezoeken.

---

## 🛠️ Developer Shortcuts & Free Mode

- **Level Skip**: Houd `F` + `K` gedurende 2 seconden ingedrukt om direct naar Level 3 te springen. Of druk op `F3` om direct naar Level 3 op de wereldkaart te gaan.
- **Start**: Run het spel via `python network_sim5_V2.py` in je terminal.
- **🚀 Free Mode**: Na het voltooien van Level 4 speel je de Free Mode vrij. Hier kun je elk huis op de wereldkaart vrij inrichten zonder beperkingen!

---

## 💡 Tips voor Succes

1.  **Kabel Check**: Werkt de verbinding niet? Controleer of je de juiste kabel gebruikt (**Straight vs Crossover**).
2.  **ISP Gegevens**: Zorg dat je de juiste providergegevens invult op de router in Level 2 & 3 om internettoegang te krijgen.
3.  **DHCP**: In Level 3 hoef je IP's niet meer handmatig in te vullen; activeer DHCP op de router en de PC's regelen de rest.
4.  **Wereldkaart**: Je kunt alleen bouwen **binnen** in een huis. Gebruik de wereldkaart enkel om naar een ander gebouw te reizen.
5.  **Audio**: Zet je geluid aan voor handige audio-feedback bij het trekken van kabels, plaatsen van items en verwijderen!

---

<div align="center">
  <p>Gemaakt door Floor, Quinten, Yannick en Thomas 1ITF01 Thomas more Geel - 2026</p>
</div>
