import correctionlib

ceval = correctionlib.CorrectionSet.from_file("electronSS.json")
#2022Re-recoE+PromptFG_ScaleJSON
def get_corr(eta, r9, valtype="rho"):
    try:
        correction_value  = ceval["2022Re-recoE+PromptFG_SmearingJSON"].evaluate(valtype, eta, r9)
        uncertainty_value = ceval["2022Re-recoE+PromptFG_SmearingJSON"].evaluate("err_rho", eta, r9)

        return correction_value, uncertainty_value
    except Exception as e:
        print(f"Error evaluating correction: {e}")
        return None, None

eta_values = [-10,-2.0,-1.566,-1.442,-1.2,-1.0,0.0,1.0,1.2,1.442,1.566,2.0,10]
r9_values = [0.0, 0.96, 10.0]

#print("#category	Emean	err_Emean	rho	err_rho	phi	err_phi")

for i in range(len(eta_values) - 1):
    eta_low = eta_values[i]
    eta_high = eta_values[i + 1]
    eta_mid = (eta_low + eta_high) / 2 

    for j in range(len(r9_values) - 1):
        r9_low = r9_values[j]
        r9_high = r9_values[j + 1]
        r9_mid = (r9_low + r9_high) / 2 
    
        #print(f"\nProcessing r9 range ({r9_low}, {r9_high}) with r9_mid = {r9_mid}")
        corr_rho, err_rho = get_corr(eta_mid, r9_mid)
            
        if corr_rho is not None and err_rho is not None:
            print(f"Eta_{eta_low}_{eta_high}-R9_{r9_low}_{r9_high} 6.6   0.0   {corr_rho}  {err_rho}  M_PI_2	M_PI_2")
            #print(f"  Gain {gain_value}:")
            #print(f"  Run {run_low} -- {run_high}:")
            #print(f"  Eta {eta_low} -- {eta_high}:")
            #print(f"  Et {et_low} -- {et_high}:")
            #print(f"  R9 {r9_low} -- {r9_high}:")
            #print(f"  Correction value: {correction_result}")
            #print(f"  Uncertainty value: {uncertainty_result}")
        else:
            print(f"  Failed to retrieve correction and/or uncertainty values for eta {eta_mid} and r9_mid {r9_mid}.")
