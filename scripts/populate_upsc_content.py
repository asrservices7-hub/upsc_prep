#!/usr/bin/env python3
"""
Populate Firebase Realtime Database with comprehensive UPSC study material.
This script pushes book summaries, subject-wise notes, and study resources
directly into the app's database so aspirants have content from Day 1.

Usage: python3 populate_upsc_content.py
"""

import json
import time
import requests
from datetime import datetime

# Firebase Realtime Database REST API URL
DATABASE_URL = "https://upsc-prep-b2336-default-rtdb.firebaseio.com"

def push_to_db(path, data):
    """Push data to Firebase Realtime Database via REST API."""
    url = f"{DATABASE_URL}/{path}.json"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"  ✅ Pushed to {path}: {data.get('title', 'N/A')}")
    else:
        print(f"  ❌ Failed {path}: {response.text}")
    return response

def put_to_db(path, data):
    """PUT (overwrite) data to Firebase Realtime Database via REST API."""
    url = f"{DATABASE_URL}/{path}.json"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print(f"  ✅ Set {path}")
    else:
        print(f"  ❌ Failed {path}: {response.text}")
    return response

# ==============================================================================
# SECTION 1: UPSC Study Material (Books & Subject Notes)
# ==============================================================================

UPSC_STUDY_MATERIAL = [
    # ---- INDIAN POLITY (Laxmikant) ----
    {
        "title": "Indian Polity — Historical Background",
        "category": "Indian Polity",
        "summary": """Key Points from M. Laxmikant:
• The Indian Constitution draws from multiple sources: British (Parliamentary system, Rule of Law), US (Fundamental Rights, Judicial Review), Irish (DPSP), Canadian (Federation with strong Centre), Australian (Concurrent List).
• The Constituent Assembly was formed in 1946 under the Cabinet Mission Plan. Dr. Rajendra Prasad was the President, B.N. Rau was the Constitutional Adviser.
• The Constitution was adopted on 26 Nov 1949 and came into force on 26 Jan 1950.
• Originally had 395 Articles, 22 Parts, and 8 Schedules. Currently has about 470+ Articles, 25 Parts, and 12 Schedules.
• Preamble declares India as a Sovereign, Socialist, Secular, Democratic Republic. 'Socialist' and 'Secular' were added by the 42nd Amendment (1976).""",
    },
    {
        "title": "Indian Polity — Fundamental Rights (Art 12-35)",
        "category": "Indian Polity",
        "summary": """Key Points from M. Laxmikant:
• Part III of Constitution (Art 12-35) deals with Fundamental Rights.
• 6 Fundamental Rights: (1) Right to Equality (Art 14-18), (2) Right to Freedom (Art 19-22), (3) Right against Exploitation (Art 23-24), (4) Right to Freedom of Religion (Art 25-28), (5) Cultural & Educational Rights (Art 29-30), (6) Right to Constitutional Remedies (Art 32).
• Right to Property was removed by 44th Amendment (1978) — now a legal right under Art 300A.
• Art 32 is the 'Heart and Soul' of the Constitution (Dr. Ambedkar).
• Writs: Habeas Corpus (personal liberty), Mandamus (command to public authority), Certiorari (quash order of lower court), Prohibition (prohibit lower court), Quo Warranto (challenge authority of office holder).
• Fundamental Rights are justiciable — enforceable by courts.""",
    },
    {
        "title": "Indian Polity — DPSP and Fundamental Duties",
        "category": "Indian Polity",
        "summary": """Key Points from M. Laxmikant:
• Part IV (Art 36-51) — Directive Principles of State Policy. Borrowed from Irish Constitution.
• DPSPs are non-justiciable but fundamental in governance.
• Categories: (a) Socialistic — Art 38, 39, 41, 42, 43, 47; (b) Gandhian — Art 40, 43, 46, 47, 48; (c) Liberal-Intellectual — Art 44 (Uniform Civil Code), 45, 48, 48A, 49, 50, 51.
• Part IVA (Art 51A) — 11 Fundamental Duties added by 42nd Amendment (1976). 11th duty added by 86th Amendment (2002).
• Examples: Respect the Constitution, National Flag and Anthem; Safeguard public property; Develop scientific temper; Protect and improve natural environment.""",
    },
    {
        "title": "Indian Polity — Parliament and State Legislature",
        "category": "Indian Polity",
        "summary": """Key Points from M. Laxmikant:
• Parliament consists of President + Lok Sabha + Rajya Sabha.
• Lok Sabha: Max 552 members (530 states, 20 UTs, 2 Anglo-Indian — now discontinued). Term: 5 years.
• Rajya Sabha: Max 250 members (238 elected, 12 nominated by President). It is a permanent body; 1/3 members retire every 2 years.
• Money Bill can only be introduced in Lok Sabha (Art 110). Rajya Sabha can delay it by 14 days max.
• Joint Sitting (Art 108) — presided by Speaker of Lok Sabha. Not applicable for Money Bills or Constitutional Amendment Bills.
• Anti-Defection Law — 10th Schedule. Added by 52nd Amendment (1985).""",
    },
    {
        "title": "Indian Polity — Judiciary and Constitutional Bodies",
        "category": "Indian Polity",
        "summary": """Key Points from M. Laxmikant:
• Supreme Court: Chief Justice + 33 other judges (currently). Art 124. Original, Appellate, and Advisory jurisdiction.
• High Courts: Art 214. One for each state (or shared). Can issue writs under Art 226.
• Judicial Review (Art 13) — power to declare laws unconstitutional.
• Key Constitutional Bodies: Election Commission (Art 324), CAG (Art 148), UPSC (Art 315), Finance Commission (Art 280), National Commission for SCs/STs.
• Key Non-Constitutional Bodies: NITI Aayog, National Human Rights Commission, CBI, Lokpal.
• 73rd Amendment (1992) — Panchayati Raj (Part IX). 74th Amendment (1992) — Municipalities (Part IXA).""",
    },

    # ---- MODERN HISTORY ----
    {
        "title": "Modern History — Revolt of 1857",
        "category": "Modern History",
        "summary": """Key Points:
• First War of Independence (1857): Started on 10 May 1857 at Meerut. Immediate cause — greased cartridges (Enfield rifle).
• Leaders: Bahadur Shah Zafar (Delhi), Nana Sahib (Kanpur), Rani Lakshmibai (Jhansi), Tantia Tope, Kunwar Singh (Bihar).
• Causes: Political (Doctrine of Lapse), Economic (drain of wealth), Military (discrimination), Social (interference in customs).
• Failure reasons: Lack of unity, limited geographic spread, no common ideology, British military superiority.
• Consequences: End of EIC rule — British Crown took direct control (Government of India Act 1858). Queen's Proclamation promised non-interference in religion.""",
    },
    {
        "title": "Modern History — Indian National Movement",
        "category": "Modern History",
        "summary": """Key Points:
• INC founded in 1885 by A.O. Hume. First session in Bombay, presided by W.C. Bannerjee.
• Moderate Phase (1885-1905): Prayer, Petition, Protest. Leaders — Gokhale, Dadabhai Naoroji, Surendranath Banerjee.
• Extremist Phase (1905-1920): Swaraj, Swadeshi, Boycott. Leaders — Tilak, Bipin Chandra Pal, Lala Lajpat Rai.
• Gandhian Era: Non-Cooperation (1920-22), Civil Disobedience (1930-34), Quit India (1942).
• Key Events: Jallianwala Bagh (1919), Chauri Chaura (1922), Dandi March (1930), August Offer (1940), Cripps Mission (1942), Cabinet Mission (1946).
• Subhas Chandra Bose — INA (Azad Hind Fauj). Founded in 1943. Gave 'Delhi Chalo' and 'Jai Hind' slogans.""",
    },
    {
        "title": "Modern History — Social and Religious Reform Movements",
        "category": "Modern History",
        "summary": """Key Points:
• Raja Ram Mohan Roy: Founded Brahmo Samaj (1828). Fought against Sati, child marriage. Known as 'Father of Indian Renaissance'.
• Dayananda Saraswati: Founded Arya Samaj (1875). 'Back to Vedas'. Promoted widow remarriage, education.
• Swami Vivekananda: Founded Ramakrishna Mission (1897). Represented India at World Parliament of Religions, Chicago (1893).
• Jyotiba Phule: Founded Satya Shodhak Samaj (1873). Worked for lower caste education and women's rights.
• Sir Syed Ahmad Khan: Founded Aligarh Movement. Established MAO College (1875) → later AMU.
• Pandita Ramabai: Worked for women's education and widow welfare. Founded Arya Mahila Samaj.""",
    },

    # ---- GEOGRAPHY ----
    {
        "title": "Geography — Indian Physical Geography",
        "category": "Geography",
        "summary": """Key Points:
• India lies between 8°4'N to 37°6'N latitude and 68°7'E to 97°25'E longitude.
• Total area: 32.8 lakh sq km (7th largest country). Coastline: 7,516.6 km.
• Physical Divisions: (1) Northern Mountains (Himalayas), (2) Northern Plains (Indo-Gangetic), (3) Peninsular Plateau (Deccan), (4) Coastal Plains, (5) Islands.
• Himalayas: Greater Himalayas (Himadri) → Middle Himalayas (Himachal) → Outer Himalayas (Shiwaliks).
• Major Passes: Karakoram (J&K), Rohtang (HP), Shipki La (HP), Nathu La & Jelep La (Sikkim), Bom Di La (Arunachal).
• Rivers: Ganga system (Ganga + Yamuna + Brahmaputra), Peninsular rivers (Godavari, Krishna, Kaveri, Narmada, Tapti).
• Narmada & Tapti flow westward into Arabian Sea. All other major peninsular rivers flow eastward.""",
    },
    {
        "title": "Geography — Climate and Monsoon",
        "category": "Geography",
        "summary": """Key Points:
• India has tropical monsoon climate. 4 seasons: (1) Cold Weather (Dec-Feb), (2) Hot Weather (Mar-May), (3) Advancing Monsoon (Jun-Sep), (4) Retreating Monsoon (Oct-Nov).
• Southwest Monsoon brings ~75% of total rainfall. Two branches: Arabian Sea branch and Bay of Bengal branch.
• Mawsynram (Meghalaya) receives highest rainfall in the world.
• Western disturbances bring winter rainfall to North India (important for Rabi crops like wheat).
• El Niño: Warming of Pacific waters → weak monsoon in India. La Niña: Cooling → stronger monsoon.
• Indian Ocean Dipole (IOD): Positive IOD → good monsoon. Negative IOD → drought conditions.
• Jet Streams play a crucial role in onset and withdrawal of monsoon.""",
    },

    # ---- ECONOMY ----
    {
        "title": "Economy — Indian Economy Basics",
        "category": "Economy",
        "summary": """Key Points:
• India is a mixed economy — both public and private sectors coexist.
• GDP (Gross Domestic Product): Total value of goods & services produced. India is 5th largest economy (nominal GDP).
• Planning in India: Five Year Plans (1951-2017) by Planning Commission. Replaced by NITI Aayog in 2015.
• Sectors: Primary (Agriculture ~15% GDP), Secondary (Industry ~25% GDP), Tertiary (Services ~60% GDP).
• Agriculture employs ~42% of workforce but contributes only ~15% of GDP → disguised unemployment.
• Major Reforms: LPG Reforms (1991) — Liberalization, Privatization, Globalization under PM Narasimha Rao & FM Manmohan Singh.
• FRBM Act 2003: Fiscal Responsibility and Budget Management — targets fiscal deficit at 3% of GDP.""",
    },
    {
        "title": "Economy — Banking and Monetary Policy",
        "category": "Economy",
        "summary": """Key Points:
• RBI (Reserve Bank of India): Established 1935. Central bank. Regulates monetary policy, issues currency, manages forex reserves.
• Monetary Policy Committee (MPC): 6 members. Sets repo rate. Target: CPI inflation at 4% (±2%).
• Key Rates: Repo Rate (lending to banks), Reverse Repo (borrowing from banks), CRR (Cash Reserve Ratio), SLR (Statutory Liquidity Ratio), Bank Rate (long-term lending).
• Priority Sector Lending: 40% of total lending for domestic banks. Includes agriculture, MSMEs, education, housing, weaker sections.
• Financial Inclusion: Jan Dhan Yojana (2014), MUDRA Yojana, PM KISAN, Stand-Up India.
• NABARD: Refinancing for agriculture and rural development. SIDBI: For MSMEs.""",
    },

    # ---- ENVIRONMENT ----
    {
        "title": "Environment — Ecology and Biodiversity",
        "category": "Environment",
        "summary": """Key Points:
• India is one of 17 mega-diverse countries. Has 4 biodiversity hotspots: Western Ghats, Himalayas, Indo-Burma, Sundaland.
• Protected Areas: National Parks (106), Wildlife Sanctuaries (567), Biosphere Reserves (18), Tiger Reserves (54 as of 2024).
• Important NPs: Jim Corbett (first NP, 1936, Uttarakhand), Kaziranga (one-horned rhino, Assam), Gir (Asiatic lion, Gujarat), Ranthambore (tiger, Rajasthan).
• Wetlands: Ramsar Sites — India has 82+ Ramsar sites. Largest: Sundarbans (West Bengal).
• IUCN Red List Categories: Extinct → Extinct in Wild → Critically Endangered → Endangered → Vulnerable → Near Threatened → Least Concern.
• Key Laws: Wildlife Protection Act (1972), Forest Conservation Act (1980), Environment Protection Act (1986), Biological Diversity Act (2002).""",
    },
    {
        "title": "Environment — Climate Change and International Agreements",
        "category": "Environment",
        "summary": """Key Points:
• UNFCCC (1992): Framework Convention. Principle of CBDR (Common But Differentiated Responsibilities).
• Kyoto Protocol (1997): Binding emission reduction targets for developed countries. India ratified but no binding targets.
• Paris Agreement (2015): Goal to limit warming to 1.5-2°C. India's NDC: 45% emission intensity reduction by 2030, 50% non-fossil energy by 2030, Net Zero by 2070.
• COP = Conference of Parties. Annual meeting of UNFCCC signatories.
• India's Initiatives: National Action Plan on Climate Change (8 Missions), International Solar Alliance (ISA), Lifestyle for Environment (LiFE).
• Key terms: Carbon sink, Carbon footprint, Green hydrogen, Carbon credit, CDM (Clean Development Mechanism).""",
    },

    # ---- SCIENCE & TECH ----
    {
        "title": "Science & Tech — Space Technology",
        "category": "Science & Tech",
        "summary": """Key Points:
• ISRO (Indian Space Research Organisation): Founded 1969. HQ: Bengaluru. Chairman heads it.
• Launch Vehicles: PSLV (Polar Satellite Launch Vehicle — workhorse), GSLV (Geosynchronous — heavier payloads), LVM3 (formerly GSLV Mk III — heaviest).
• Key Missions: Chandrayaan-1 (2008 — found water on Moon), Mangalyaan/MOM (2013 — Mars orbiter, first attempt success), Chandrayaan-3 (2023 — soft landing on Moon's south pole).
• Navigation: NavIC (Navigation with Indian Constellation) — regional GPS alternative.
• Communication Satellites: INSAT series, GSAT series.
• Gaganyaan: India's first manned space mission (upcoming). Will carry 3 Indian astronauts (Vyomanauts) to LEO.
• Aditya-L1: India's first solar observatory at Sun-Earth Lagrange Point L1.""",
    },
    {
        "title": "Science & Tech — Defence Technology",
        "category": "Science & Tech",
        "summary": """Key Points:
• DRDO (Defence Research and Development Organisation): Under Ministry of Defence. HQ: Delhi.
• Missiles (IGMDP — Integrated Guided Missile Development Programme):
  - Agni series (IRBM/ICBM, nuclear capable), Prithvi (short range), BrahMos (supersonic cruise missile, India-Russia joint), Akash (SAM), Nag (ATGM).
• Tejas: Light Combat Aircraft (LCA). Made by HAL.
• INS Vikrant: India's first indigenous aircraft carrier (2022).
• Arjun: Main Battle Tank. Developed by DRDO.
• Key Defence Initiatives: Make in India (defence corridor in UP & Tamil Nadu), Strategic Partnership Model, Defence Acquisition Procedure (DAP) 2020.
• A-SAT (Anti-Satellite Test): Mission Shakti (2019) — India became 4th country to demonstrate ASAT capability.""",
    },
]


# ==============================================================================
# SECTION 2: Today's Current Affairs (Sample Seed Data)
# ==============================================================================

SAMPLE_CURRENT_AFFAIRS = [
    {
        "title": "India Achieves Record FDI Inflows in FY2026",
        "category": "Economy",
        "summary": "India attracted record Foreign Direct Investment (FDI) inflows of over $85 billion in FY2025-26, marking a 12% increase over the previous year. The sectors that received maximum FDI include services, computer software & hardware, telecommunications, and automobile. Singapore, USA, and Japan remained the top investor countries. The government's Production Linked Incentive (PLI) schemes and ease of doing business reforms are credited for the surge. This is significant for UPSC as it relates to Indian Economy, Balance of Payments, and Foreign Investment policies.",
        "source_url": "https://dpiit.gov.in/",
    },
    {
        "title": "Supreme Court Upholds Right to Privacy as Fundamental Right in Digital Age",
        "category": "Polity",
        "summary": "The Supreme Court in a landmark judgment reinforced the right to privacy in the context of digital data collection by government agencies. The 5-judge bench ruled that citizens' data collected through Aadhaar, DigiLocker, and other digital platforms must comply with the Data Protection Act 2023. The judgment cited the KS Puttaswamy case (2017) precedent and emphasised proportionality and necessity tests for any state surveillance. Important for Polity, Fundamental Rights, and Governance topics in UPSC.",
        "source_url": "https://main.sci.gov.in/",
    },
    {
        "title": "India's Forest Cover Increases by 2,261 sq km: ISFR 2025",
        "category": "Environment",
        "summary": "According to the India State of Forest Report (ISFR) 2025 released by the Forest Survey of India, India's total forest and tree cover now stands at 25.17% of the total geographical area. Madhya Pradesh has the largest forest cover followed by Arunachal Pradesh and Chhattisgarh. Mizoram has the highest percentage of forest cover. The report highlights improvements in mangrove forests but expresses concern about declining forest quality in the northeast. Key topic for Environment and Ecology in UPSC.",
        "source_url": "https://fsi.nic.in/",
    },
    {
        "title": "India and EU Sign Green Hydrogen Partnership Agreement",
        "category": "International Relations",
        "summary": "India and the European Union signed a strategic partnership agreement on green hydrogen production and trade. Under this agreement, the EU will invest €2 billion in India's National Green Hydrogen Mission. The partnership aims to establish India as a global hub for green hydrogen production by 2030. This aligns with India's net-zero targets by 2070 and the EU's Fit for 55 programme. Important for International Relations, Environment, and Economy topics.",
        "source_url": "https://www.mea.gov.in/",
    },
    {
        "title": "ISRO Successfully Tests Reusable Launch Vehicle Technology",
        "category": "Science & Tech",
        "summary": "ISRO achieved a major milestone with the successful autonomous landing test of its Reusable Launch Vehicle-Technology Demonstrator (RLV-TD). The vehicle was released from an IAF Chinook helicopter at 4.5 km altitude and landed autonomously on the runway at Aeronautical Test Range, Chitradurga. This technology will significantly reduce the cost of space launches. Once operational, it could bring down launch costs to 1/10th of current expenditure. Critical for Science & Technology section in UPSC.",
        "source_url": "https://www.isro.gov.in/",
    },
    {
        "title": "15th Finance Commission: States Demand Higher Share of Tax Devolution",
        "category": "Economy",
        "summary": "Several state governments have demanded an increase in tax devolution from the current 41% to 50% of the divisible pool during their submissions to the 16th Finance Commission. States argued that rising expenditure on health, education, and disaster management necessitates higher fiscal transfers. The Finance Commission, headed by Dr. Arvind Panagariya, will submit its report covering 2027-2032. This is a crucial topic for Polity (Centre-State Relations) and Economy (Fiscal Federalism) in UPSC.",
        "source_url": "https://fincomindia.nic.in/",
    },
    {
        "title": "UNESCO Inscribes New Indian Site on World Heritage List",
        "category": "History & Culture",
        "summary": "UNESCO has inscribed India's nomination of the Maratha Military Architecture (a serial nomination of 12 forts including Raigad, Rajgad, Shivneri, and Pratapgad) on the World Heritage List. This brings India's total UNESCO World Heritage Sites to 44 (36 Cultural, 7 Natural, 1 Mixed). India ranks 6th globally in total sites. The inscription recognizes the unique military engineering and strategic planning of the Maratha Empire. Important for Art & Culture and History sections.",
        "source_url": "https://whc.unesco.org/",
    },
    {
        "title": "New Criminal Laws: BNS, BNSS, BSA Fully Operational Across India",
        "category": "Polity",
        "summary": "The three new criminal laws — Bharatiya Nyaya Sanhita (BNS replacing IPC), Bharatiya Nagarik Suraksha Sanhita (BNSS replacing CrPC), and Bharatiya Sakshya Adhiniyam (BSA replacing Indian Evidence Act) — are now fully operational across all states and UTs. Key changes include mandatory FIR registration online, zero FIR, mandatory forensics for serious crimes, time-bound trials, and community service as punishment for petty offences. Critical for Polity and Governance in UPSC.",
        "source_url": "https://lddashboard.legislative.gov.in/",
    },
]


# ==============================================================================
# SECTION 3: Book Recommendations
# ==============================================================================

BOOK_RECOMMENDATIONS = {
    "Indian Polity": [
        {"name": "Indian Polity by M. Laxmikant", "description": "The Bible of UPSC Polity. Covers Constitution, Parliament, Judiciary, Local Govt, and all Constitutional/Non-Constitutional bodies. Must-read cover to cover."},
        {"name": "Introduction to the Constitution of India by D.D. Basu", "description": "More detailed and legalistic. Good for Mains GS-2 when you need deeper understanding of constitutional provisions."},
    ],
    "Modern History": [
        {"name": "India's Struggle for Independence by Bipan Chandra", "description": "Comprehensive coverage of the freedom movement from 1857 to 1947. Standard text for UPSC."},
        {"name": "A Brief History of Modern India by Rajiv Ahir (Spectrum)", "description": "Concise and exam-focused. Best for Prelims. Well-organized chapter-wise."},
    ],
    "Geography": [
        {"name": "Certificate Physical and Human Geography by G.C. Leong", "description": "World geography classic. Covers geomorphology, climatology, oceanography, biogeography."},
        {"name": "Indian Geography by Majid Husain", "description": "India-specific geography. Physical features, climate, agriculture, industries, population."},
        {"name": "Oxford School Atlas", "description": "Essential for map-based questions. Practice regularly."},
    ],
    "Economy": [
        {"name": "Indian Economy by Ramesh Singh", "description": "Comprehensive coverage of Indian economy for UPSC. Updated with latest budget and economic survey data."},
        {"name": "Indian Economy by Sankarganesh Karuppiah", "description": "Alternative to Ramesh Singh. Well-structured with flow charts and diagrams."},
        {"name": "Economic Survey (Annual)", "description": "Must-read government publication. Available free on indiabudget.gov.in."},
    ],
    "Environment": [
        {"name": "Environment by Shankar IAS", "description": "The most popular and comprehensive environment book for UPSC. Covers ecology, biodiversity, climate change, pollution, and environmental laws."},
    ],
    "Science & Tech": [
        {"name": "Science & Technology by Ravi P. Agrahari", "description": "Covers space, defence, biotech, nanotech, IT, nuclear technology and recent developments."},
        {"name": "NCERT Science (Class 6-10)", "description": "Foundation builder. Must be read before any advanced book."},
    ],
}


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("=" * 60)
    print("  UPSC Content Population Script")
    print("  Target: Firebase Realtime Database")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Populate Study Material (Notes) under UPSC exam
    print("\n📚 [STEP 1] Populating UPSC Study Material (Notes)...")
    for material in UPSC_STUDY_MATERIAL:
        data = {
            "title": material["title"],
            "category": material["category"],
            "summary": material["summary"].strip(),
            "timestamp": int(time.time() * 1000),
        }
        push_to_db("notes/UPSC", data)
        time.sleep(0.2)  # Rate limiting

    # 2. Populate Current Affairs (Seed Data)
    print("\n📰 [STEP 2] Populating Current Affairs (Seed Data)...")
    today_str = datetime.now().strftime("%b %d, %Y")
    for affair in SAMPLE_CURRENT_AFFAIRS:
        data = {
            "title": affair["title"],
            "category": affair["category"],
            "summary": affair["summary"].strip(),
            "source_url": affair.get("source_url", ""),
            "date": today_str,
            "timestamp": int(time.time() * 1000),
        }
        push_to_db("current_affairs/UPSC", data)
        time.sleep(0.2)

    # 3. Populate Book Recommendations
    print("\n📖 [STEP 3] Populating Book Recommendations...")
    put_to_db("books/UPSC", BOOK_RECOMMENDATIONS)

    print("\n" + "=" * 60)
    print("  ✅ ALL CONTENT POPULATED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
