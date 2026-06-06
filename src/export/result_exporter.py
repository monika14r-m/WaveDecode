import json
def export_analysis(analysis, filename="analysis.json"):
    with open(filename, "w") as file:
        json.dump(
            analysis,
            file,
            indent=4
        )
