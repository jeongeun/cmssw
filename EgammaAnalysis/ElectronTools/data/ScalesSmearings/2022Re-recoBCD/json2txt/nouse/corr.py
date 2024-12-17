import correctionlib
import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_multibinning_edges_and_values(content, parent_edges=[], parent_inputs=[], gain_key=None):
    results = []

    if content.get("nodetype") == "category":
        for sub_content in content.get("content", []):
            gain = sub_content.get("key")
            multibinning_data = sub_content.get("value", {})
            if multibinning_data.get("nodetype") == "multibinning":
                # Combine parent inputs with current inputs
                inputs = parent_inputs + multibinning_data.get("inputs", [])
                print("inputs = ", inputs)
                edges = multibinning_data.get("edges", [])
                print("edges = ", edges)
                values = multibinning_data.get("content", [])
                #print("values = ", values)

                # Iterate over the bins for this level
                for i in range(len(edges[0]) - 1):
                    current_edges = parent_edges + [edges[0][i], edges[0][i + 1]]
                    print("current_edges = ", current_edges)

                    # Recursive case: Traverse deeper multibinning nodes
                    if isinstance(values, list) and len(values) > 0:
                        print("pass isinstance(values, list) and len(values) > 0")
                        for value in values:
                            #print("value = ", value)
                            if isinstance(value, dict) and value.get("nodetype") == "multibinning":
                                results.extend(extract_multibinning_edges_and_values(value, current_edges, inputs, gain))
                            else:
                                # Base case: If it's a direct value (e.g., [1.0]), add the value to the result
                                combined_result = {
                                    'edges': current_edges,
                                    'inputs': inputs,
                                    'gain': gain,
                                    'value': value
                                }
                                results.append(combined_result)
                    else:
                        print("Not pass  isinstance(values, list) and len(values) > 0")
                        combined_result = {
                            'edges': current_edges,
                            'inputs': inputs,
                            'gain': gain,
                            'value': values
                        }
                        results.append(combined_result)

    return results

def parse_and_print_data(data):
    corrections = data.get("corrections", [])
    total_correction_values = []
    total_uncertainty_values = []

    for correction in corrections:
        if correction.get("name") == "2022Re-recoBCD_ScaleJSON":
            print("Found ==> 2022Re-recoBCD_ScaleJSON")
            correction_data = correction.get("data", {}).get("content", [])
            #print("correction_data = ",correction_data)

            for content in correction_data:
                key = content.get("key")
                print("key", key)
                if key == "total_correction":
                    print("yes total_correction key exist")
                    total_correction_values = extract_multibinning_edges_and_values(content.get("value", {}))
                    #print("total_correction_values = ", total_correction_values)
                elif key == "total_uncertainty":
                    print("yes total_uncertainty key exist")
                    total_uncertainty_values = extract_multibinning_edges_and_values(content.get("value", {}))
                    #print("total_uncertainty_values = ", total_uncertainty_values)

            # Now print the results
            if total_correction_values and total_uncertainty_values:
                for corr, unc in zip(total_correction_values, total_uncertainty_values):
                    # Print edges for run, eta, r9, et, gain key, total_correction, total_uncertainty
                    edges_dict = dict(zip(corr['inputs'], corr['edges']))
                    print(f"Run Edge: {edges_dict.get('run')}")
                    print(f"Eta Edge: {edges_dict.get('eta')}")
                    print(f"R9 Edge: {edges_dict.get('r9')}")
                    print(f"ET Edge: {edges_dict.get('et')}")
                    print(f"Gain Key: {corr['gain']}")
                    print(f"Total Correction: {corr['value']}")
                    print(f"Total Uncertainty: {unc['value']}")
                    print("Edges (run, eta, r9, et):", corr['edges'])
                    print("Gain Key:", corr['gain'])
                    print("Total Correction:", corr['value'])
                    print("Total Uncertainty:", unc['value'])
                    print("-" * 50)
            else:
                print("No values found for total_correction or total_uncertainty")

# Load the JSON file and parse data
file_path = 'electronSS.json'
json_data = read_json_file(file_path)
parse_and_print_data(json_data)







#import correctionlib
#
#ceval = correctionlib.CorrectionSet.from_file("electronSS.json")
#
#list(ceval.keys())
#for corr in ceval.values():
#    print(f"Correction {corr.name} has {len(corr.inputs)} inputs")
#    for ix in corr.inputs:
#        print(f"   Input {ix.name} ({ix.type}): {ix.description}")
#        print("____________________________")
##        if (ix.name == "gain"):
##            print(f"   Input {ix.name}: ")
##            print("____________________________")
#
#correction  = ceval["2022Re-recoBCD_ScaleJSON"].evaluate("total_correction", gain, run, eta, r9, et)
#uncertainty = ceval["2022Re-recoBCD_ScaleJSON"].evaluate("total_uncertainty", gain, run, eta, r9, et)
#
#print(f"Gain: {gain}")
#print(f"Run Edge: {run}")
#print(f"Eta Edge: {eta}")
#print(f"R9 Edge: {r9}")
#print(f"ET Edge: {et}")
#print(f"Correction: {correction}")
#print(f"Uncertainty: {uncertainty}")

#ceval["phimod"].evaluate(1.2, -1)
# will not work
# ceval["phimod"].evaluate(1.2, -1.0)

#import numpy as np
#ptvals = np.random.exponential(15.0, size=10)
#
#ceval["ptweight"].evaluate(ptvals, "nominal")
#
#import awkward as ak
#
#ptjagged = ak.Array([[10.1, 20.2, 30.3], [40.4, 50.5], [60.6]])
#
#ptflat, counts = ak.flatten(ptjagged), ak.num(ptjagged)
#weight = ak.unflatten(
#    ceval["ptweight"].evaluate(ptflat, "nominal"),
#    counts=counts,
#)
#weight
