import correctionlib

ceval = correctionlib.CorrectionSet.from_file("electronSS.json")

#"2022Re-recoE+PromptFG_ScaleJSON"
def get_corr(run, eta, r9, et, gain, valtype="total_correction"):
    try:
        correction_value  = ceval["2022Re-recoE+PromptFG_ScaleJSON"].evaluate(valtype, gain, run, eta, r9, et)
        uncertainty_value = ceval["2022Re-recoE+PromptFG_ScaleJSON"].evaluate("total_uncertainty", gain, run, eta, r9, et)

        return correction_value, uncertainty_value
    except Exception as e:
        print(f"Error evaluating correction: {e}")
        return None
 

run_values = [1,359569,359609,359685,359686,359691,359693,359694,359699,359718,359750,359751,359762,359763,359764,359776,
 359808,359810,359812,359814,359870,359887,360017,360075,360090,360116,360125,360126,360127,360128,360130,
 360141,360224,360225,360295,360296,360327,360390,360391,360393,360400,360413,360428,360432,360437,360458,
 360459,360460,360486,360490,360491,360737,360795,360797,360825,360826,360856,360887,360888,360889,360892,
 360895,360919,360920,360927,360941,360942,360945,360946,360948,360950,360951,360991,360992,361044,361045,
 361050,361054,361083,361105,361106,361108,361188,361193,361197,361223,361239,361240,361272,361280,361283,
 361297,361303,361318,361319,361320,361333,361361,361363,361366,361400,361417,361443,361468,361475,361512,
 361569,361573,361579,361580,361957,361971,361989,361990,361994,362058,362059,362060,362061,362062,362063,
 362064,362087,362091,362104,362105,362106,362107,362148,362153,362154,362159,362163,362166,362167,362437,
 362597,362614,362615,362616,362617,362618,362653,362654,362657,362695,362696,362698,362720,362727,362757,
 362758,362760]

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
