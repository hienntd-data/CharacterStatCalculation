import streamlit as st
import pandas as pd

# Function to safely convert values, handling empty strings and formats with spaces and symbols gracefully
def safe_convert(value):
    if isinstance(value, str):
        value = value.strip()
    try:
        return float(value) if value != '' else 0.0
    except ValueError:
        return 0.0

# Function to calculate percentage, allowing addition or subtraction
def calculate_percentage(before, percent_str):
    
    percent_str = percent_str.replace(" ", "")  # Remove spaces from the percentage string

    
    percent = float(percent_str.replace("%", ""))

    
    if before == 0:
        return percent  

    
    if percent_str.startswith("+"):
        
        return before * (1 + percent / 100)
    elif percent_str.startswith("-"):
        
        return before * (1 - percent / 100)
    
    
    return before

# Title

# List of stats
stats_data = {
    'Stat (Chinese)': [
        '生 命 值', '魔 法 值', '力 量', '智 力', '体 力', '精 神',
        '物 理 攻 击 力', '魔 法 攻 击 力', '物 理 防 御 力', '魔 法 防 御 力',
        '物 理 暴 击 率', '物 理 暴 击', '魔 法 暴 击 率', '魔 法 暴 击', '攻 击 速 度',
        '移 动 速 度', '命 中'
    ],
    'Stat (English)': [
        'Health Points', 'Mana Points', 'Strength', 'Intelligence', 'Stamina', 'Spirit',
        'Physical Attack Power', 'Magical Attack Power', 'Physical Defense Power',
        'Magical Defense Power', 'Physical Critical Rate', 'Physical Critical Damage',
        'Magical Critical Rate', 'Magical Critical Damage', 'Attack Speed',
        'Movement Speed', 'Accuracy'
    ]
}

# Convert stats data to a DataFrame
stats = pd.DataFrame(stats_data)

# Input character stats before equipping items
with st.expander("Character Stats Before Equip"):
    character_stats_before = {}
    clipboard_input_before = st.text_area("", height=500, key="before_equip")

    if clipboard_input_before:
        lines = clipboard_input_before.split('\n')
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) == 2:
                    stat_name = parts[0].strip()
                    value = safe_convert(parts[1].strip())
                    character_stats_before[stat_name] = value

# Input equipment stats
with st.expander("Equipment Stats"):
    equipment_stats = {}
    clipboard_input_equipment = st.text_area("", height=500, key="equipment_stats")

    if clipboard_input_equipment:
        lines = clipboard_input_equipment.split('\n')
        for line in lines:
            if line.strip():
                # Locate the last occurrence of "+" or "-" for a more reliable split
                plus_index = line.rfind("+")
                minus_index = line.rfind("-")
                
                # Determine the starting index of the value based on the last "+" or "-"
                value_start = max(plus_index, minus_index)
                
                # Extract stat name and value
                if value_start != -1:
                    stat_name = line[:value_start].strip()
                    value = line[value_start:].replace(" ", "").strip()  # Remove any extra spaces within the value
                    equipment_stats[stat_name] = value

# Input character stats after equipping items
with st.expander("Character Stats After Equip"):
    character_stats_after = {}
    clipboard_input_after = st.text_area("", height=500, key="after_equip")

    if clipboard_input_after:
        lines = clipboard_input_after.split('\n')
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) == 2:
                    stat_name = parts[0].strip()
                    value = safe_convert(parts[1].strip())
                    character_stats_after[stat_name] = value

# Button to calculate comparison
if st.button("Compare Stats"):
    comparison_results = []
    correct_stats = []
    incorrect_stats = []
    
    # HTML table for displaying results
    table_html = "<table style='width:100%; border-collapse: collapse;'><tr><th>Stat Name</th><th>Before Equip</th><th>Equipment Stats</th><th>After Equip</th><th>Result</th></tr>"
    
    for index, row in stats.iterrows():
        stat_name = row['Stat (Chinese)']
        before = safe_convert(character_stats_before.get(stat_name, ''))
        after = safe_convert(character_stats_after.get(stat_name, ''))
        equip_value = equipment_stats.get(stat_name, '0')

        if equip_value != "0":  # Only display if equipment stat is non-zero
            try:
                # Remove any spaces between the value and the percentage symbol
                equip_value = equip_value.replace(" ", "").replace("％", "%")  # Normalize the percent symbol

                # Check if the equip_value contains a percentage
                if "%" in equip_value:
                    after_calculated = calculate_percentage(before, equip_value)
                else:
                    # If the equip_value does not contain a percentage, handle it as a direct value
                    value = float(equip_value.replace("+", "").replace("-", ""))  # Remove + or - sign
                    if "-" in equip_value:
                        after_calculated = before - value  # Subtract value if negative
                    else:
                        after_calculated = before + value  # Add value if positive

            except ValueError:
                st.error(f"Invalid input for {stat_name}! Ensure proper format and try again.")
                continue
            
            # Check if the calculated value matches the 'after' value
            if abs(after_calculated - after) < 0.01:
                comparison_results.append([stat_name, before, equip_value, after, "Correct"])
                correct_stats.append(stat_name)
                table_html += f"<tr style='background-color: #d4edda;'><td>{stat_name}</td><td>{before}</td><td>{equip_value}</td><td>{after}</td><td>Correct</td></tr>" 
            else:
                comparison_results.append([stat_name, before, equip_value, after, f"Incorrect (Expected: {after_calculated:.1f})"])
                incorrect_stats.append(stat_name)
                table_html += f"<tr style='background-color: #f8d7da;'><td>{stat_name}</td><td>{before}</td><td>{equip_value}</td><td>{after}</td><td>Incorrect (Expected: {after_calculated:.1f})</td></tr>"
    
    table_html += "</table>"
    
    # Display results
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.write(f"Total of {len(correct_stats)} correct stats and {len(incorrect_stats)} incorrect stats.")

