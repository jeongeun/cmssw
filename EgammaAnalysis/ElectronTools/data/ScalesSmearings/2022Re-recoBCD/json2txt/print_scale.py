import correctionlib

ceval = correctionlib.CorrectionSet.from_file("electronSS.json")

def get_corr(run, eta, r9, et, gain, valtype="total_correction"):
    try:
        correction_value = ceval["2022Re-recoBCD_ScaleJSON"].evaluate(valtype, gain, run, eta, r9, et)
        uncertainty_value = ceval["2022Re-recoBCD_ScaleJSON"].evaluate("total_uncertainty", gain, run, eta, r9, et)

        return correction_value, uncertainty_value
    except Exception as e:
        print(f"Error evaluating correction: {e}")
        return None

run_values = [ 1, 355374, 355559, 355768, 355870, 355892, 355913, 355933, 356043, 356074, 356076, 356077,
 356135, 356322, 356371, 356381, 356383, 356428, 356433, 356434, 356523, 356531, 356568, 356570,
 356576, 356578, 356580, 356614, 356619, 356810, 356811, 356813, 356815, 356824, 356919, 356937,
 356946, 356947, 356948, 356949, 356951, 356954, 356955, 356956, 356969, 356970, 356998, 357000,
 357079, 357081, 357101, 357102, 357104, 357112, 357268, 357271, 357328, 357329, 357330, 357331,
 357333, 357401, 357406, 357438, 357440, 357441, 357442, 357447, 357482, 357538, 357550, 357611,
 357612, 357613, 357688, 357696, 357697, 357699, 357701, 357705, 357706, 357720, 357734, 357735,
 357754, 357756, 357757, 357759, 357766, 357777, 357778, 357779, 357781, 357803, 357804, 357806,
 357808, 357813, 357814, 357815, 357898, 357899, 357900 ]

eta_values = [-5.0,-2.0,-1.566,-1.442,-1.2,-1.0,0.0,1.0,1.2,1.442,1.566,2.0,5.0]
r9_values = [0.0, 0.96, 10.0]
et_values = [0.0, 14000.0]
gain_values = [1, 6, 12]

for q in range(len(run_values) - 1):
    run_low = run_values[q]
    run_high = run_values[q + 1]
    run_mid = (run_low + run_high) / 2

    for i in range(len(eta_values) - 1):
        eta_low = eta_values[i]
        eta_high = eta_values[i + 1]
        eta_mid = (eta_low + eta_high) / 2 
    
        for k in range(len(et_values) - 1):
            et_low = et_values[k]
            et_high = et_values[k + 1]
            et_mid = (et_low + et_high) / 2 
        
            #print(f"\nProcessing eta range ({eta_low}, {eta_high}) with eta_mid = {eta_mid}")
        
            for j in range(len(r9_values) - 1):
                r9_low = r9_values[j]
                r9_high = r9_values[j + 1]
                r9_mid = (r9_low + r9_high) / 2 
            
                #print(f"\nProcessing r9 range ({r9_low}, {r9_high}) with r9_mid = {r9_mid}")
                for gain_value in gain_values:
                    correction_result, uncertainty_result = get_corr(run_mid, eta_mid, r9_mid, et_mid, gain_value)
                    
                    if correction_result is not None and uncertainty_result is not None:
                        print(run_low, " ", run_high, f" {eta_low} {eta_high}  {r9_low}  {r9_high}  {et_low}  {et_high}  {gain_value}  {correction_result}  {uncertainty_result}")
                        #print(f"  Gain {gain_value}:")
                        #print(f"  Run {run_low} -- {run_high}:")
                        #print(f"  Eta {eta_low} -- {eta_high}:")
                        #print(f"  Et {et_low} -- {et_high}:")
                        #print(f"  R9 {r9_low} -- {r9_high}:")
                        #print(f"  Correction value: {correction_result}")
                        #print(f"  Uncertainty value: {uncertainty_result}")
                    else:
                        print(f"  Failed to retrieve correction and/or uncertainty values for gain {gain_value} and r9_mid {r9_mid}.")
