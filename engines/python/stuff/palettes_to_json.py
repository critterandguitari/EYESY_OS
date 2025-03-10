import json
import color_palettes

# Convert list to JSON with new lines and commas
json_output = ",\n".join(json.dumps(entry, separators=(',', ':')) for entry in color_palettes.abcd_palettes)

# Wrap in brackets to make it a valid JSON array
json_output = "[\n" + json_output + "\n]"

print(json_output)
