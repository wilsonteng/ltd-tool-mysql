from pathlib import Path
import json
import re
from datetime import datetime
import pathlib
import json

wave_values = {
    1 : 72,
    2 : 84,
    3 : 90,
}

unit_leak_dictionary = {
    "Crab" : 8,
    "Wale" : 7,
    "Hopper" : 5,
    "Snail" : 6,
    "Dragon Turtle" : 12,
    "Lizard" : 12,
    "Brute" : 15,
    "Fiend" : 18
}

def calculate_leak_percentages(data : list) -> int:
    """
    Takes in leak data and returns leak percentages as integer.
    """
    
    leak_percentages = []
    for wavenumber, wave in enumerate(data):
        wave_leak_value = 0
        for leaked_unit in wave:
            wave_leak_value += unit_leak_dictionary[leaked_unit]
            wave_leak_percent = round(wave_leak_value * 100 / wave_values[wavenumber + 1])
        leak_percentages.append(wave_leak_percent)

    return leak_percentages



def create_unit_dictionary() -> dict:
    """
    Returns a dictionary mapping units to their iconpath, and mercenaries to their mythiumcost. 
    Source file is located at assets/units.json
    """

    unit_json_path = "assets/units.json"

    with open(unit_json_path, "r") as f:
        json_data = json.loads(f.read())

    unit_dictionary = {} # unitname : { "iconpath" : iconpath }

    for unit in json_data:
        
        if unit["unitClass"] == "Fighter":
            unitname = unit["unitId"]
        else:
            unitname = unit["name"]
        
        unit_dictionary[unitname] = {}    
        unit_dictionary[unitname]["iconPath"] = unit["iconPath"]


    return unit_dictionary

unit_dictionary = create_unit_dictionary()

def get_unit_image(input: str) -> str:
    """
    Takes input unit name and changes to title case, removes underscores
    """

    iconpath = unit_dictionary[input]["iconPath"]
    unit_image = f'https://cdn.legiontd2.com/{iconpath}'

    return unit_image

def parse_unit_string(input: str, base_width : int) -> tuple:
    """
    Takes an input string and outputs unit_name, x, y as tuple. Calculates positioning of units on grid
    """
    first = re.split(":", input)
    unit_name = first[0]


    x, y = re.split("\|", first[1])
    y = re.split(":", y)[0]
    x = float(x) * base_width - (base_width // 2)
    y = float(y) * base_width - (base_width // 2)
    unit_url = get_unit_image(unit_name)
    return(unit_url, x, y)

def generate_inline_css(base_width):
    """
    Returns the inline css required to create the correctly sized board and cell widths.
    """
    
    string = f"""<style> 
        img {{ width: {base_width}px;}}

        .board {{
            height: {14 * base_width}px;
            width: { 9 * base_width}px;
            background-size: {base_width}px {base_width}px;
        }}
    
    </style>"""

    return string

def get_unit_string(input):
    """
    Takes entire unit string and returns only the unit name.
    """

    first = re.split("_", input)
    unit_name = first[0]

    if unit_name == "nekomata":
        return unit_name.capitalize() + " " + first[-1][-1]
    
    return unit_name.capitalize()

def build_output(filtered_data):
    """
    Builds the HTML output
    """

    path = pathlib.Path.cwd() / 'assets' / 'header.html'
    header = path.open("r").read()

    base_width = 40

    htmlpage = header
    counter = 1

    htmlpage += generate_inline_css(base_width)
    htmlpage += "</head><body>"
    
    for build in filtered_data:

        htmlpage += '<div class="row">'

        leak_percentages = calculate_leak_percentages(build['leaksPerWave'])
        total_average_leak = round(sum(leak_percentages) / len(leak_percentages))

        htmlpage += f"""<h3>{counter} – Game ID: {build['game_id']}</h3>""" # Game ID
        htmlpage += f"""<p>{build["playerName"]} // {build['queueType']} // {build['legion']} // {build['date']} // Version {build['version']} </p>""" # Player Name

        htmlpage += f"""<p class="leakpercent">Total Average Leak: <span>{total_average_leak}%</span></p>"""
        
        
        for wave in range(len(build["leaksPerWave"])):
            
            htmlpage += '<div class="column">'
            htmlpage += '<div class="board">'
            counter += 1

            for unit in build['buildPerWave'][wave]:
                unit_url, x, y = parse_unit_string(unit, base_width)
                htmlpage += f"""<img alt="{get_unit_string(unit)}" src='{unit_url}' style='bottom:{y}px; left:{x}px;'>"""

            htmlpage += '</div>\n' #end board

            htmlpage += f"""<p class="leakpercent">Wave {wave + 1}: <span>{leak_percentages[wave]}%</span></p>"""

            # text representation of build
            htmlpage += f"""<p class="buildtext">"""
            for index, unit in enumerate(build['buildPerWave'][wave]):
                htmlpage += get_unit_string(unit)
                if index < len(build['buildPerWave'][wave]) - 1:
                    htmlpage += ", "
            htmlpage += """</p>"""

            htmlpage += '<div class="sends">'
            htmlpage += '<p>Sends Received:</p>'
            if build['mercenariesReceivedPerWave'][wave]:
                for send in build['mercenariesReceivedPerWave'][wave]:
                    send_image = get_unit_image(send)
                    htmlpage += f"<img alt='{get_unit_string(send)}' src='{send_image}'>\n"
            htmlpage += '</div>\n' #end sends     

            htmlpage += '<div class ="leaks">'
            htmlpage += '<p>Leaks:</p>'
            for leak in build['leaksPerWave'][wave]:
                leak_image = get_unit_image(leak)
                htmlpage += f"""<img alt='{get_unit_string(leak)}' src='{leak_image}'>"""
            htmlpage += '</div>\n' #end leaks
            
            htmlpage += '</div>\n' #end col
        htmlpage += '</div>\n' #end row

    htmlpage += """</body></html>"""

    timestamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    dir = pathlib.Path.cwd() / 'output'
    dir.mkdir(mode=0o777, parents=True, exist_ok=True)
    outpath = dir / f'output{timestamp}.html'
    f = open(outpath, 'w')

    f.write(htmlpage)
    f.close()
    
    print (f"Successfully wrote file at {outpath}") 
    return True

import read_sql_data

data = read_sql_data.sql_query_to_list()

build_output(data)
