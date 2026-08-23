import urllib.request
import xml.etree.ElementTree as ET
import datetime
import re
import os

def clean_html(raw_html):
    if raw_html is None:
        return ''
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html))
    return cleantext[:350] + '...' if len(cleantext) > 350 else cleantext

print("Fetching news...")
rss_feeds = [
    'https://www.thehindu.com/news/national/feeder/default.rss',
    'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms', # National
    'https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml'
]

current_affairs = []
for feed_url in rss_feeds:
    try:
        req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            for item in root.findall('.//item')[:30]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                if title:
                    current_affairs.append({
                        'title': str(title).replace("'", "\\'").replace('"', '\\"').replace('$', '\\$'),
                        'category': 'National News',
                        'date': datetime.datetime.now().strftime('%b %d, %Y'),
                        'summary': clean_html(description).replace("'", "\\'").replace('"', '\\"').replace("\n", " ").replace('$', '\\$'),
                        'source_url': str(link).replace('$', '\\$')
                    })
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")

# Huge syllabus data for UPSC
notes = {
    'Indian Polity': [
        {'title': 'Historical Background', 'summary': 'Regulating Act 1773, Pitt’s India Act 1784, Charter Acts (1813, 1833, 1853). Crown Rule: Govt of India Act 1858, Indian Councils Acts, Morley-Minto Reforms 1909, Montagu-Chelmsford 1919, GOI Act 1935.'},
        {'title': 'Making of the Constitution', 'summary': 'Demand for Constituent Assembly (M.N. Roy, 1934). Cabinet Mission Plan. Drafting Committee headed by Dr. B.R. Ambedkar. Adopted on Nov 26, 1949.'},
        {'title': 'Salient Features & Preamble', 'summary': 'Lengthiest written constitution, drawn from various sources. Preamble is the identity card (N.A. Palkhivala). Sovereign, Socialist, Secular, Democratic, Republic. Berubari Union and Kesavananda Bharati cases.'},
        {'title': 'Union and its Territory', 'summary': 'Articles 1 to 4 under Part I. Article 3 allows Parliament to form new states. Dhar Commission, JVP Committee, Fazl Ali Commission for reorganization of states.'},
        {'title': 'Citizenship', 'summary': 'Part II (Articles 5-11). Citizenship Act 1955: Acquisition by Birth, Descent, Registration, Naturalization. Loss by Renunciation, Termination, Deprivation. CAA 2019.'},
        {'title': 'Fundamental Rights (Part III)', 'summary': 'Articles 12-35. Magna Carta of India. Right to Equality (14-18), Freedom (19-22), Against Exploitation (23-24), Religion (25-28), Cultural & Educational (29-30), Constitutional Remedies (32 - Writs).'},
        {'title': 'Directive Principles of State Policy', 'summary': 'Part IV (Articles 36-51). Novel features. Socialistic, Gandhian, Liberal-Intellectual principles. Fundamental in governance. Minerva Mills case.'},
        {'title': 'Fundamental Duties', 'summary': 'Part IVA, Article 51A. Added by 42nd Amendment (1976) via Swaran Singh Committee. 11th duty added by 86th Amendment (2002).'},
        {'title': 'President & Vice-President', 'summary': 'Union Executive (Articles 52-78). Election process, Electoral College. Veto powers, Pardoning powers (Art 72). Ordinance making power (Art 123). Impeachment process (Art 61).'},
        {'title': 'Prime Minister & Council of Ministers', 'summary': 'Real executive authority. Article 74 (CoM to aid and advise). Article 75 (Collective responsibility to Lok Sabha). Cabinet vs CoM.'},
        {'title': 'Parliament', 'summary': 'Rajya Sabha (Council of States) & Lok Sabha (House of the People). Sessions, Prorogation, Dissolution. Question Hour, Zero Hour. Bills: Ordinary, Money (Art 110), Finance, Constitutional Amendment (Art 368).'},
        {'title': 'Supreme Court of India', 'summary': 'Part V (Articles 124-147). Independence of Judiciary. Collegium system (Judges Cases). Original, Appellate, Advisory, Writ jurisdictions. Judicial Review and Judicial Activism.'},
        {'title': 'State Government', 'summary': 'Governor, Chief Minister, State Legislature. Ordinances (Art 213). High Courts and Subordinate Courts.'},
        {'title': 'Panchayati Raj & Municipalities', 'summary': 'Local Self Government. 73rd and 74th Amendments (1992). Balwant Rai Mehta, Ashok Mehta committees. 11th and 12th Schedules.'},
        {'title': 'Constitutional Bodies', 'summary': 'Election Commission (Art 324), UPSC (Art 315), Finance Commission (Art 280), CAG (Art 148), Attorney General (Art 76).'},
        {'title': 'Non-Constitutional Bodies', 'summary': 'NITI Aayog, NHRC, SHRC, CIC, SIC, CVC, CBI, Lokpal and Lokayuktas.'}
    ],
    'Modern History': [
        {'title': 'Advent of Europeans', 'summary': 'Portuguese (Vasco da Gama), Dutch, English (EIC 1600), French. Anglo-French Carnatic Wars. Battle of Plassey (1757) and Buxar (1764).'},
        {'title': 'British Expansion', 'summary': 'Anglo-Mysore Wars, Anglo-Maratha Wars, Anglo-Sikh Wars. Subsidiary Alliance (Wellesley) and Doctrine of Lapse (Dalhousie).'},
        {'title': 'Revolt of 1857', 'summary': 'First War of Independence. Causes: Economic exploitation, socio-religious reforms, greased cartridges. Leaders: Nana Saheb, Rani Lakshmibai, Kunwar Singh. Result: Crown takes over.'},
        {'title': 'Socio-Religious Reform Movements', 'summary': 'Brahmo Samaj (Raja Ram Mohan Roy), Arya Samaj (Dayanand Saraswati), Ramakrishna Mission (Vivekananda), Aligarh Movement (Syed Ahmed Khan).'},
        {'title': 'Formation of INC (1885)', 'summary': 'Founded by A.O. Hume. Moderate phase (1885-1905) led by Dadabhai Naoroji, G.K. Gokhale. Demand for constitutional reforms and economic critique (Drain Theory).'},
        {'title': 'Extremist Phase & Swadeshi (1905-1917)', 'summary': 'Partition of Bengal (Curzon, 1905). Lal-Bal-Pal. Swadeshi and Boycott movement. Surat Split (1907). Morley-Minto Reforms (1909) and separate electorates.'},
        {'title': 'Gandhian Era Begins', 'summary': 'Gandhi returns (1915). Champaran (1917), Kheda (1918), Ahmedabad Mill Strike. Rowlatt Act and Jallianwala Bagh Massacre (1919).'},
        {'title': 'Non-Cooperation & Khilafat (1920-22)', 'summary': 'Boycott of schools, courts, foreign goods. Surrender of titles. Chauri Chaura incident (1922) led to withdrawal.'},
        {'title': 'Civil Disobedience Movement', 'summary': 'Simon Commission (1927), Nehru Report (1928), Lahore Session (1929 - Purna Swaraj). Dandi March (1930) and Salt Satyagraha. Round Table Conferences. Gandhi-Irwin Pact (1931).'},
        {'title': 'Revolutionary Nationalism', 'summary': 'Bhagat Singh, Chandrashekhar Azad (HSRA). Surya Sen (Chittagong Armoury Raid). Kakori Conspiracy.'},
        {'title': 'Quit India Movement (1942)', 'summary': 'Failure of Cripps Mission. Gowalia Tank, Bombay. \'Do or Die\'. Parallel governments in Ballia, Tamluk, Satara.'},
        {'title': 'Towards Freedom & Partition', 'summary': 'INA and Subhas Chandra Bose. Cabinet Mission Plan (1946). Direct Action Day. Mountbatten Plan (June 3 Plan). Indian Independence Act 1947.'}
    ],
    'Geography': [
        {'title': 'Geomorphology', 'summary': 'Interior of Earth, Continental Drift Theory (Wegener), Plate Tectonics. Earthquakes and Volcanoes. Landforms formed by river, wind, and glaciers.'},
        {'title': 'Climatology', 'summary': 'Structure and composition of Atmosphere. Insolation and Heat Budget. Pressure belts and Wind systems (Planetary, Local). Cyclones (Tropical and Extra-Tropical).'},
        {'title': 'Oceanography', 'summary': 'Bottom relief of oceans. Temperature and salinity distribution. Ocean currents (Atlantic, Pacific, Indian). Tides and Coral Reefs.'},
        {'title': 'Physical Geography of India', 'summary': 'Geological structure. Physiographic divisions: Himalayas, Northern Plains, Peninsular Plateau, Indian Desert, Coastal Plains, Islands.'},
        {'title': 'Drainage System of India', 'summary': 'Himalayan Rivers (Indus, Ganga, Brahmaputra). Peninsular Rivers (East flowing: Mahanadi, Godavari, Krishna, Cauveri; West flowing: Narmada, Tapi).'},
        {'title': 'Climate of India', 'summary': 'Monsoon mechanism: Thermal concept, Jet Stream theory, El Nino & La Nina. Seasons in India. Distribution of rainfall.'},
        {'title': 'Soils and Natural Vegetation', 'summary': 'ICAR soil classification: Alluvial, Black (Regur), Red, Laterite. Types of forests: Tropical Evergreen, Deciduous, Thorny, Montane, Mangrove.'},
        {'title': 'Economic Geography', 'summary': 'Agriculture (Kharif, Rabi, Zaid, Green Revolution). Mineral resources (Iron, Coal, Petroleum). Industries (Iron & Steel, Cotton). Transport.'},
        {'title': 'Human Geography', 'summary': 'Population distribution, density, and growth. Demographic Transition Theory. Migration. Urbanization patterns.'}
    ],
    'Economy': [
        {'title': 'National Income', 'summary': 'Concepts of GDP, GNP, NDP, NNP at Factor Cost and Market Price. Real vs Nominal GDP. Methods of estimation (Value added, Income, Expenditure).'},
        {'title': 'Inflation and Business Cycles', 'summary': 'Types: Creeping, Galloping, Hyperinflation. Causes: Demand-pull, Cost-push. Measurement: WPI vs CPI. Impact of inflation. Phillips Curve.'},
        {'title': 'Money and Banking', 'summary': 'Functions of Money. RBI: Functions and Monetary Policy Instruments (Repo, Reverse Repo, CRR, SLR, OMO). Commercial Banks, NPA crisis, Basel Norms, NBFCs.'},
        {'title': 'Financial Markets', 'summary': 'Money Market (Treasury bills, Call money) vs Capital Market (Shares, Bonds, Debentures). SEBI functions.'},
        {'title': 'Public Finance & Budgeting', 'summary': 'Fiscal Policy. Components of Budget: Revenue and Capital account. Deficits: Fiscal, Revenue, Primary. FRBM Act. Taxation (Direct, Indirect, GST), Finance Commission.'},
        {'title': 'Balance of Payments (BoP)', 'summary': 'Current Account vs Capital Account. Convertibility of Rupee. Foreign Exchange Reserves. Exchange Rate systems (Fixed, Floating, Managed float).'},
        {'title': 'International Economic Organizations', 'summary': 'IMF (SDRs, Quota), World Bank (IBRD, IDA), WTO (Doha Round, Subsidies - Amber/Blue/Green box).'},
        {'title': 'Agriculture & Food Security', 'summary': 'Cropping patterns, MSP (Minimum Support Price), PDS (Public Distribution System), FCI, Subsidies. Food processing industries.'},
        {'title': 'Infrastructure & Investment Models', 'summary': 'Energy, Transport, Communication. PPP (Public-Private Partnership) models: BOT, HAM, EPC.'},
        {'title': 'Poverty and Unemployment', 'summary': 'Committees (Tendulkar, Rangarajan). Types of unemployment (Structural, Disguised, Frictional). Skill India, MGNREGA.'}
    ],
    'Environment': [
        {'title': 'Ecology and Ecosystem', 'summary': 'Components (Biotic, Abiotic). Ecotone, Niche, Edge Effect. Food chain, Food web, Ecological Pyramids. Biogeochemical cycles (Carbon, Nitrogen, Phosphorus).'},
        {'title': 'Biodiversity', 'summary': 'Levels (Genetic, Species, Ecosystem). Measurement (Alpha, Beta, Gamma). Biodiversity Hotspots. Causes of loss (Habitat destruction, Invasive species).'},
        {'title': 'Conservation Efforts', 'summary': 'In-situ (National Parks, Wildlife Sanctuaries, Biosphere Reserves). Ex-situ (Zoos, Seed banks). Project Tiger, Elephant, Rhino.'},
        {'title': 'Climate Change', 'summary': 'Greenhouse Effect, Global Warming, Ocean Acidification, Ozone Depletion (Montreal Protocol). Impact on agriculture, sea levels.'},
        {'title': 'International Conventions', 'summary': 'UNFCCC (COP summits, Kyoto, Paris). CBD (Convention on Biological Diversity, Cartagena, Nagoya). UNCCD (Desertification). CITES, CMS, Ramsar Convention.'},
        {'title': 'Environmental Legislation in India', 'summary': 'Wildlife Protection Act 1972, Water Act 1974, Air Act 1981, Environment Protection Act 1986, Forest Rights Act 2006. NGT (National Green Tribunal).'},
        {'title': 'Pollution', 'summary': 'Air (PM2.5, PM10, Smog, Acid Rain). Water (BOD, Eutrophication, Biomagnification). Soil, Noise, Radioactive, E-waste. Solid Waste Management Rules.'}
    ],
    'Science & Tech': [
        {'title': 'Space Technology', 'summary': 'Orbits (LEO, MEO, GEO, SSO). Launch Vehicles (SLV, ASLV, PSLV, GSLV, LVM3). ISRO Missions: Chandrayaan, Mangalyaan, Aditya-L1, Gaganyaan. Space debris.'},
        {'title': 'Biotechnology', 'summary': 'DNA, RNA, Gene Editing (CRISPR-Cas9). Recombinant DNA technology. GM Crops (Bt Cotton, Bt Brinjal, GM Mustard). Stem cells. Cloning.'},
        {'title': 'Information Technology & Computers', 'summary': 'Generations of computers. Supercomputers (Param). Internet of Things (IoT), Big Data, Cloud Computing, Artificial Intelligence (AI), Machine Learning, Blockchain technology, Web 3.0.'},
        {'title': 'Nanotechnology', 'summary': 'Nanomaterials (Carbon nanotubes, Graphene). Applications in medicine (targeted drug delivery), agriculture, electronics, and water purification.'},
        {'title': 'Nuclear Technology', 'summary': 'Nuclear Fission vs Fusion. India’s Three-Stage Nuclear Power Programme (Homi Bhabha). Fast Breeder Reactors. ITER project.'},
        {'title': 'Defense Technology', 'summary': 'IGMDP (Prithvi, Agni, Trishul, Nag, Akash). BrahMos cruise missile. Ballistic vs Cruise missiles. Submarines (Project 75 - Scorpene class), Aircraft Carriers.'},
        {'title': 'Health and Diseases', 'summary': 'Communicable vs Non-communicable diseases. Viruses, Bacteria, Protozoa. Vaccines (mRNA, Vector). Antimicrobial Resistance (AMR).'}
    ]
}

os.makedirs('lib/data', exist_ok=True)
dart_file_content = "class StaticData {\n"

# Write Notes
dart_file_content += "  static const Map<String, List<Map<String, String>>> notes = {\n"
for category, items in notes.items():
    dart_file_content += f"    '{category}': [\n"
    for item in items:
        title = item['title'].replace("'", "\\'").replace('$', '\\$')
        summary = item['summary'].replace("'", "\\'").replace('$', '\\$')
        dart_file_content += "      {\n"
        dart_file_content += f"        'title': '{title}',\n"
        dart_file_content += f"        'summary': '{summary}',\n"
        dart_file_content += "        'pdfUrl': ''\n"
        dart_file_content += "      },\n"
    dart_file_content += "    ],\n"
dart_file_content += "  };\n\n"

# Write Current Affairs
dart_file_content += "  static const List<Map<String, String>> currentAffairs = [\n"
for item in current_affairs:
    dart_file_content += "    {\n"
    dart_file_content += f"      'title': '{item['title']}',\n"
    dart_file_content += f"      'category': '{item['category']}',\n"
    dart_file_content += f"      'date': '{item['date']}',\n"
    dart_file_content += f"      'summary': '{item['summary']}',\n"
    dart_file_content += f"      'source_url': '{item['source_url']}'\n"
    dart_file_content += "    },\n"
dart_file_content += "  ];\n"

dart_file_content += "}\n"

with open('lib/data/static_data.dart', 'w') as f:
    f.write(dart_file_content)

print(f"Generated lib/data/static_data.dart successfully with {len(current_affairs)} news items!")
