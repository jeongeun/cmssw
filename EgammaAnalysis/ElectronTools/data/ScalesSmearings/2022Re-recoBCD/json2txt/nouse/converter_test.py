import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_multibinning_values(content, parent_edges=[], parent_inputs=[]):
    results = []

    if content.get("nodetype") == "category":
        for sub_content in content.get("content", []):
            gain = sub_content.get("key")  # Get the gain value
            multibinning_data = sub_content.get("value", {})
            if multibinning_data.get("nodetype") == "multibinning":
                inputs = parent_inputs + multibinning_data.get("inputs", [])
                print("inputs", inputs)
                edges = multibinning_data.get("edges", [])
                values = multibinning_data.get("content", [])  # Use 'content' instead of 'values' for deeper nodes

                # Debugging output to understand structure
                print(f"Inputs: {inputs}, Edges: {edges}, Gain: {gain}")
                print(f"Current Inputs: {inputs}")
                if 'eta' in inputs:
                    print("Found eta in inputs")
                if 'r9' in inputs:
                    print("Found r9 in inputs")
                if 'et' in inputs:
                    print("Found et in inputs")

                # Iterate over the bins for this level
                for i in range(len(edges[0]) - 1):
                    current_edges = parent_edges + [edges[0][i], edges[0][i + 1]]

                    # Recursive case: Traverse deeper multibinning nodes
                    if isinstance(values, list) and len(values) > 0:
                        for value in values:
                            if isinstance(value, dict) and value.get("nodetype") == "multibinning":
                                results.extend(extract_multibinning_values(value, current_edges, inputs))
                            else:
                                # Base case: If it's a direct value (e.g., [1.0]), add the value to the result
                                combined_result = current_edges + [value, gain]
                                results.append(combined_result)

    return results

def parse_and_print_data(data):
    corrections = data.get("corrections", [])

    total_correction_values = []
    total_uncertainty_values = []

    for correction in corrections:
        if correction.get("name") == "2022Re-recoBCD_ScaleJSON":
            print("Found 2022Re-recoBCD_ScaleJSON")
            correction_data = correction.get("data", {}).get("content", [])

            for content in correction_data:
                key = content.get("key")
                print(f"Processing key: {key}")
                if key == "total_correction":
                    total_correction_values = extract_multibinning_values(content.get("value", {}))
                    print("Total Correction Values:")
                    for row in total_correction_values:
                        print("\t".join(map(str, row)))
                elif key == "total_uncertainty":
                    total_uncertainty_values = extract_multibinning_values(content.get("value", {}))
                    print("Total Uncertainty Values:")
                    for row in total_uncertainty_values:
                        print("\t".join(map(str, row)))

            # Now print out combined total_correction and total_uncertainty
            for correction_row, uncertainty_row in zip(total_correction_values, total_uncertainty_values):
                # Print all the fields, combining corrections and uncertainties
                formatted_output = "\t".join(map(str, correction_row[:-1])) + f"\t{correction_row[-1]}\t{uncertainty_row[-1]}"
                print(formatted_output)

file_path = 'electronSS.json'

json_data = read_json_file(file_path)
parse_and_print_data(json_data)

#import json
#
#def read_json_file(file_path):
#    with open(file_path, 'r') as file:
#        return json.load(file)
#
#def extract_multibinning_values(content, parent_edges=[]):
#    results = []
#
#    if content.get("nodetype") == "category":
#        for sub_content in content.get("content", []):
#            gain = sub_content.get("key")  # Get the gain value
#            multibinning_data = sub_content.get("value", {})
#            if multibinning_data.get("nodetype") == "multibinning":
#                inputs = multibinning_data.get("inputs", [])
#                edges = multibinning_data.get("edges", [])
#                values = multibinning_data.get("content", [])  # Use 'content' instead of 'values' for deeper nodes
#
#                print(f"Inputs: {inputs}, Edges: {edges}, Gain: {gain}")
#
#                # Base case: If this is the deepest multibinning node (i.e., contains a single value)
#                if not isinstance(values, list):
#                    for i in range(len(edges[0]) - 1):
#                        combined_result = parent_edges + [edges[0][i], edges[0][i + 1], values, gain]
#                        results.append(combined_result)
#                else:
#                    # Recursive case: Traverse deeper multibinning nodes
#                    for i in range(len(edges[0]) - 1):
#                        current_edges = parent_edges + [edges[0][i], edges[0][i + 1]]
#                        for value in values:
#                            if isinstance(value, dict) and value.get("nodetype") == "multibinning":
#                                results.extend(extract_multibinning_values(value, current_edges))
#                            else:
#                                # Handling case where values are directly within a list (e.g., [1.0])
#                                combined_result = current_edges + [value, gain]
#                                results.append(combined_result)
##    if content.get("nodetype") == "category":
##        for sub_content in content.get("content", []):
##            gain = sub_content.get("key")  # Get the gain value
##            multibinning_data = sub_content.get("value", {})
##            if multibinning_data.get("nodetype") == "multibinning":
##                inputs = multibinning_data.get("inputs", [])
##                edges = multibinning_data.get("edges", [])
##                values = multibinning_data.get("values", [])
##                print(f"Inputs: {inputs}, Edges: {edges}")
##                # Base case: If this is the deepest multibinning node (i.e., contains a single value)
##                if not isinstance(values, list):
##                    for i in range(len(edges[0]) - 1):
##                        combined_result = parent_edges + [edges[0][i], edges[0][i + 1], values, gain]
##                        results.append(combined_result)
##                else:
##                    # Recursive case: Traverse deeper multibinning nodes
##                    for i in range(len(edges[0]) - 1):
##                        current_edges = parent_edges + [edges[0][i], edges[0][i + 1]]
##                        for value in values:
##                            if isinstance(value, dict) and value.get("nodetype") == "multibinning":
##                                results.extend(extract_multibinning_values(value, current_edges))
##                            else:
##                                # Handling case where values are directly within a list (e.g., [1.0])
##                                combined_result = current_edges + [value, gain]
##                                results.append(combined_result)
#
#    return results
#
#def parse_and_print_data(data):
#    corrections = data.get("corrections", [])
#
#    total_correction_values = []
#    total_uncertainty_values = []
#
#    for correction in corrections:
#        if correction.get("name") == "2022Re-recoBCD_ScaleJSON":
#            print("Found 2022Re-recoBCD_ScaleJSON")
#            correction_data = correction.get("data", {}).get("content", [])
#
#            for content in correction_data:
#                key = content.get("key")
#                print(f"Processing key: {key}")
#                if key == "total_correction":
#                    total_correction_values = extract_multibinning_values(content.get("value", {}))
#                    print("Total Correction Values:")
#                    for row in total_correction_values:
#                        print("\t".join(map(str, row)))
#                elif key == "total_uncertainty":
#                    total_uncertainty_values = extract_multibinning_values(content.get("value", {}))
#                    print("Total Uncertainty Values:")
#                    for row in total_uncertainty_values:
#                        print("\t".join(map(str, row)))
#
#            ## Now print out combined total_correction and total_uncertainty
#            # Assuming total_correction_values and total_uncertainty_values have the same structure
#            for correction_row, uncertainty_row in zip(total_correction_values, total_uncertainty_values):
#                # The structure here assumes that both lists have gain, corrections, and uncertainties at the correct indices
#                formatted_output = f"{correction_row[0]}\t{correction_row[1]}\t{correction_row[2]}\t{correction_row[3]}\t{correction_row[4]}\t{correction_row[5]}\t{correction_row[6]}\t{correction_row[7]}\t{correction_row[8]}\t{uncertainty_row[8]}"
#                print(formatted_output)
#
#file_path = 'electronSS.json'
#
#json_data = read_json_file(file_path)
#parse_and_print_data(json_data)
#
