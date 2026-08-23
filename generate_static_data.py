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
    return cleantext[:200] + '...' if len(cleantext) > 200 else cleantext

print("Fetching news...")
rss_feeds = [
    'https://www.thehindu.com/news/national/feeder/default.rss',
]

current_affairs = []
for feed_url in rss_feeds:
    try:
        req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            for item in root.findall('.//item')[:50]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                if title:
                    current_affairs.append({
                        'title': str(title).replace("'", "\\'").replace('"', '\\"'),
                        'category': 'National News',
                        'date': datetime.datetime.now().strftime('%b %d, %Y'),
                        'summary': clean_html(description).replace("'", "\\'").replace('"', '\\"').replace("\n", " "),
                        'source_url': str(link)
                    })
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")

notes = {
    'Indian Polity': [
        {'title': 'Making of the Constitution', 'summary': 'Cabinet Mission Plan, Constituent Assembly formation, Drafting Committee led by Dr. B.R. Ambedkar.'},
        {'title': 'Fundamental Rights (Part III)', 'summary': 'Articles 12-35. Magna Carta of India. Justiciable in nature.'},
        {'title': 'Directive Principles of State Policy', 'summary': 'Part IV. Non-justiciable. Inspired by the Irish Constitution.'},
        {'title': 'Parliament of India', 'summary': 'Rajya Sabha and Lok Sabha. Legislative procedures, budget passing, committees.'},
        {'title': 'Supreme Court of India', 'summary': 'Original, Appellate, and Advisory jurisdiction. Judicial Review.'},
    ],
    'Modern History': [
        {'title': 'Revolt of 1857', 'summary': 'First War of Independence. Causes: Doctrine of Lapse, Enfield Rifles, Economic exploitation.'},
        {'title': 'Formation of INC (1885)', 'summary': 'Founded by A.O. Hume. Early moderate phase led by Dadabhai Naoroji.'},
        {'title': 'Swadeshi Movement (1905)', 'summary': 'Response to Partition of Bengal by Lord Curzon. Boycott of foreign goods.'},
        {'title': 'Non-Cooperation Movement (1920)', 'summary': 'Led by Gandhi. Surrender of titles, boycott of schools/courts. Called off after Chauri Chaura.'},
        {'title': 'Quit India Movement (1942)', 'summary': 'Do or Die slogan. Spontaneous mass uprising across India.'},
    ],
    'Geography': [
        {'title': 'Physical Features of India', 'summary': 'Himalayas, Northern Plains, Peninsular Plateau, Coastal Plains, Islands.'},
        {'title': 'Indian Monsoon System', 'summary': 'Mechanism of South-West Monsoon, El Nino, La Nina impacts.'},
        {'title': 'Drainage Systems', 'summary': 'Himalayan Rivers (Ganga, Indus, Brahmaputra) vs Peninsular Rivers (Godavari, Krishna, Cauvery).'},
        {'title': 'Soils of India', 'summary': 'Alluvial, Black, Red, Laterite. Distribution and characteristics.'},
        {'title': 'Earthquakes and Volcanism', 'summary': 'Plate tectonics, Pacific Ring of Fire, measuring scales (Richter vs Mercalli).'},
    ],
    'Economy': [
        {'title': 'National Income Accounting', 'summary': 'GDP, GNP, NDP, NNP. Methods of calculation: Product, Income, Expenditure.'},
        {'title': 'Reserve Bank of India (RBI)', 'summary': 'Functions of RBI, Monetary Policy Tools (Repo Rate, CRR, SLR).'},
        {'title': 'Inflation', 'summary': 'Demand-pull, Cost-push. Measured by CPI and WPI.'},
        {'title': 'Taxation System in India', 'summary': 'Direct vs Indirect Taxes. GST (Goods and Services Tax) structure.'},
        {'title': 'Five Year Plans', 'summary': 'From Harrod-Domar model (1st plan) to Mahalanobis model (2nd plan). Replaced by NITI Aayog.'},
    ],
    'Environment': [
        {'title': 'Biodiversity Hotspots', 'summary': 'Western Ghats, Himalayas, Indo-Burma, Sundaland. Endemism.'},
        {'title': 'Climate Change Conferences', 'summary': 'UNFCCC, Kyoto Protocol, Paris Agreement (COP21), Net Zero targets.'},
        {'title': 'National Parks and Wildlife Sanctuaries', 'summary': 'Project Tiger (1973), Project Elephant. Biosphere Reserves.'},
        {'title': 'Pollution', 'summary': 'Air Quality Index (AQI), Smog, Eutrophication, Biomagnification.'},
        {'title': 'Renewable Energy in India', 'summary': 'Solar (ISA), Wind, Hydro. Targets of 500 GW non-fossil capacity by 2030.'},
    ],
    'Science & Tech': [
        {'title': 'Space Missions of ISRO', 'summary': 'Chandrayaan-3, Aditya-L1, Gaganyaan. Launch vehicles: PSLV, GSLV, LVM3.'},
        {'title': 'Biotechnology', 'summary': 'CRISPR-Cas9 gene editing, Genetically Modified (GM) crops, Stem cells.'},
        {'title': 'Artificial Intelligence (AI)', 'summary': 'Machine Learning, Deep Learning, Generative AI (LLMs). Applications and Ethics.'},
        {'title': 'Defense Technology', 'summary': 'Missile systems (Agni, BrahMos), Submarines (Project 75), Tejas LCA.'},
        {'title': 'Nanotechnology', 'summary': 'Carbon nanotubes, Graphene, targeted drug delivery.'},
    ]
}

os.makedirs('lib/data', exist_ok=True)
dart_file_content = "class StaticData {\n"

# Write Notes
dart_file_content += "  static const Map<String, List<Map<String, String>>> notes = {\n"
for category, items in notes.items():
    dart_file_content += f"    '{category}': [\n"
    for item in items:
        dart_file_content += "      {\n"
        dart_file_content += f"        'title': '{item['title']}',\n"
        dart_file_content += f"        'summary': '{item['summary']}',\n"
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
