import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_and_print_data(data):
    corrections = data.get("corrections", [])
    #print("Corrections:", corrections)
 
    for correction in corrections:
        if correction.get("name") == "2022Re-recoBCD_ScaleJSON":
            print("Found 2022Re-recoBCD_ScaleJSON")

            correction_data = correction.get("data", {}).get("content", [])

            #print("Correction Data:", correction_data)
            total_correction_values = {}
            total_uncertainty_values = {}

            for content in correction_data:
                key = content.get("key")
                print(f"Processing key: {key}") 
                if key == "total_correction":
                    total_correction_values = extract_multibinning_values(content.get("value", {}), gain_key=key)
                    print("total_corr=",total_correction_values)
                elif key == "total_uncertainty":
                    total_uncertainty_values = extract_multibinning_values(content.get("value", {}), gain_key=key)
                    print("total_cor_uncert=",total_uncertainty_values)
            
            ## print out total_correction and total_uncertainty
            for gain, corrections in total_correction_values.items():
                uncertainties = total_uncertainty_values.get(gain, [])
                for correction, uncertainty in zip(corrections, uncertainties):
                    # run low edge, run high edge, eta low edge, eta high edge, r9 low edge, r9 high edge, et low edge, et high edge, gain, total_correction, total_uncertainty
                    formatted_output = f"{correction[0]}\t{correction[1]}\t{correction[2]}\t{correction[3]}\t{correction[4]}\t{correction[5]}\t{correction[6]}\t{correction[7]}\t{gain}\t{correction[8]}\t{uncertainty[8]}"
                    #print(formatted_output)

## extracting multibinning data
def extract_multibinning_values(content):
    results = {}

    if content.get("nodetype") == "category":
        for sub_content in content.get("content", []):
            gain = sub_content.get("key")
            multibinning_data = sub_content.get("value", {})
            if multibinning_data.get("nodetype") == "multibinning":
                inputs = multibinning_data.get("inputs", [])
                edges = multibinning_data.get("edges", [])
                values = multibinning_data.get("values", [])

                input_indices = {input_name: index for index, input_name in enumerate(inputs)}

                num_bins = len(edges[0]) - 1 
                for i in range(num_bins):
                    combined_result = []

                    for input_name in ['run', 'eta', 'r9', 'et']:
                        if input_name in input_indices:
                            idx = input_indices[input_name]
                            combined_result.extend([edges[idx][i], edges[idx][i + 1]])
                        else:
                            combined_result.extend([None, None])

                    combined_result.append(values[i] if i < len(values) else None)

                    results[gain] = results.get(gain, []) + [combined_result]

    return results






#def extract_multibinning_values(content, gain_key):
#    results = {}
#    
#    if content.get("nodetype") == "category":
#        for sub_content in content.get("content", []):
#            gain = sub_content.get("key")
#            multibinning_data = sub_content.get("value", {})
#            if multibinning_data.get("nodetype") == "multibinning":
#                ## multibinning (run, eta, r9, et ...)
#                inputs = multibinning_data.get("inputs", [])
#                edges = multibinning_data.get("edges", [])
#                values = multibinning_data.get("values", [])
#
#                input_indices = {input_name: index for index, input_name in enumerate(inputs)}
#
#                print(f"Gain {gain} - Inputs: {inputs}")
#                print("Edges= ", edges)
#                print("Values= ", values)
#
#                for var in ['eta', 'r9', 'et']:
#                    if var not in input_indices:
#                        print(f"Warning: '{var}' is not in inputs.")
#
#                num_bins = len(edges[0]) - 1 
#                for i in range(num_bins):
#                    combined_result = []
#                    for input_name in ['run', 'eta', 'r9', 'et']:
#                        if input_name in input_indices:
#                            idx = input_indices[input_name]
#                            combined_result.extend([edges[idx][i], edges[idx][i + 1]])
#                        else:
#                            combined_result.extend([None, None])
#
#                    combined_result.append(values[i] if i < len(values) else None)
#                    results[gain] = results.get(gain, []) + [combined_result]
#


                #for i in range(len(edges[0]) - 1): 
                #    combined_result = []
                #    for j, input_name in enumerate(inputs):
                #        combined_result.extend([edges[j][i], edges[j][i + 1]])  # Low edge, High edge

                #    combined_result.append(values[i] if i < len(values) else None)  
                #    results[gain] = results.get(gain, []) + [combined_result]

                #for edge_set, value in zip(edges, values):
                #   combined_result = edge_set + [value]
                #   results[gain] = results.get(gain, []) + [combined_result]
                ##results[gain] = [edge + [value] for edge, value in zip(edges, values)]
    #return results

file_path = 'electronSS.json'

json_data = read_json_file(file_path)

parse_and_print_data(json_data)

