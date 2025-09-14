import pandas as pd
from dataset_utils import map_variable, validate_variable, plot_weight_agg_over_time


def build_2024_anes(path="raw/anes_timeseries_2024_csv_20250808.csv"):
    raw_2024 = pd.read_csv(path)
    raw_2024 = raw_2024[raw_2024["V240107b"] != " "]
    df = raw_2024[[]].copy()
    df["year"] = 2024
    df["weight"] = map_variable(raw_2024["V240107b"], type_check=float)
    validate_variable(df["weight"], lambda x: x >= 0)
    df["age"] = map_variable(raw_2024["V241458x"], nulls=[-2])
    validate_variable(df["age"], lambda x: x >= 0 and x <= 120)
    df["female"] = map_variable(raw_2024["V241550"], nulls =[3,0,-9], mapping={1:0,2:1})
    validate_variable(df["female"], [0,1])
    df["race"] = map_variable(raw_2024["V241501x"], type_check=str, mapping={1:"White",2:"Black",3:"Hispanic",4:"Other",5:"Other",6:"Other"}, nulls=[-4,-8,-9])         
    validate_variable(df["race"], ["White","Black","Hispanic","Other"])
    df["strong_republican"] = map_variable(raw_2024["V241227x"], mapping={1:0,2:0,3:0,4:0,5:0,6:0,7:1})
    validate_variable(df["strong_republican"], [0,1])
    df["republican"] = map_variable(raw_2024["V241227x"], mapping={1:0,2:0,3:0,4:0,5:0,6:1,7:1})
    validate_variable(df["republican"], [0,1])
    df["lean_republican"] = map_variable(raw_2024["V241227x"], mapping={1:0,2:0,3:0,4:0,5:1,6:1,7:1})
    validate_variable(df["lean_republican"], [0,1])
    df["strong_democrat"] = map_variable(raw_2024["V241227x"], mapping={1:1,2:0,3:0,4:0,5:0,6:0,7:0})
    validate_variable(df["strong_democrat"], [0,1])
    df["democrat"] = map_variable(raw_2024["V241227x"], mapping={1:1,2:0,3:0,4:0,5:0,6:0,7:0})
    validate_variable(df["democrat"], [0,1])
    df["lean_democrat"] = map_variable(raw_2024["V241227x"], mapping={1:1,2:1,3:1,4:0,5:0,6:0,7:0})
    validate_variable(df["lean_democrat"], [0,1])
    df["party_3_narrow"] = map_variable(raw_2024["V241227x"], mapping={1:"D",2:"D",3:"I",4:"I",5:"I",6:"R",7:"R"}, type_check=str)
    validate_variable(df["party_3_narrow"], ["D","I","R"])
    df["party_3_broad"] = map_variable(raw_2024["V241227x"], mapping={1:"D",2:"D",3:"D",4:"I",5:"R",6:"R",7:"R"}, type_check=str)
    validate_variable(df["party_3_broad"], ["D","I","R"])
    df["conservative"] = map_variable(raw_2024["V241177"], mapping={1:1,2:1,3:1,4:0,5:0,6:0,7:0})
    validate_variable(df["conservative"], [0,1])
    df["vote_rep_pres"] = map_variable(raw_2024["V242067"], mapping={1:1,2:0})
    validate_variable(df["vote_rep_pres"], [0,1])
    df["prev_rep_pres"] = map_variable(raw_2024["V241104"], mapping={1:1,2:0})
    validate_variable(df["prev_rep_pres"], [0,1])
    df["blacks_lazy"] = map_variable(raw_2024["V242542"], nulls=[-1,-5,-6,-7,-9])
    validate_variable(df["blacks_lazy"], [1,2,3,4,5,6,7])
    df["therm_blacks"] = map_variable(raw_2024["V242516"], nulls=[-1,-4,-5,-6,-7,-9,200,998,999])
    validate_variable(df["therm_blacks"], range(100+1))
    df["therm_whites"] = map_variable(raw_2024["V242518"], nulls=[-1,-4,-5,-6,-7,-9,200.998,999])
    validate_variable(df["therm_whites"], range(100+1))
    df["therm_trans"] = map_variable(raw_2024["V242151"], nulls=[-1,-4,-5,-6,-7,-9,200,998,999])
    validate_variable(df["therm_trans"], range(100+1))
    df["therm_police"] = map_variable(raw_2024["V242150"], nulls=[-1,-4,-5,-6,-7,-9,200,998,999])
    validate_variable(df["therm_police"], range(100+1))
    df["anti_imm"] = map_variable(raw_2024["V242547"], nulls=[-1,-5,-6,-7,-9])
    validate_variable(df["anti_imm"], [1,2,3,4,5,6,7])
    df["college"] = map_variable(raw_2024["V242548"], mapping = {4: 1, 5: 1, 1: 0, 2: 0, 3: 0})
    validate_variable(df["college"], [0,1])
    df["no_guar_jobs"] = map_variable(raw_2024["V242549"], nulls = [-1,-5,-6,-7,-9])
    validate_variable(df["no_guar_jobs"], range(1,7+1))
    #df["distrust_5pt"] = map_variable(raw_2024["V242550"], nulls=[-1, -5, -6, -7, -9])
    #validate_variable(df["distrust_5pt"], [1,2,3,4,5])
    df["therm_delta"] = df.apply(lambda row: row["therm_whites"] - row["therm_blacks"], axis=1)
    df["age_group"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["age"]) else
        "18-29" if 18 <= int(row["age"]) <= 29 else
        "30-44" if 30 <= int(row["age"]) <= 44 else
        "45-64" if 45 <= int(row["age"]) <= 64 else
        "65+" if int(row["age"]) >= 65 else
        pd.NA
    ), axis=1)
    validate_variable(df["age_group"], ["18-29","30-44","45-64","65+"])
    df["resentment"] = raw_2024.apply(lambda row: (
        pd.NA if row["V242300"] < 0 or row ["V242301"] < 0 or row["V242302"] < 0 or row["V242303"] < 0 else # this are the missings
        int(-row["V242300"]) + int(row["V242301"]) + int(row["V242302"]) - int(row["V242303"])#+ 12 # if you want a 4-20 scale.
        # wait did they reverse the coding in 2024?
    ), axis=1) 
    validate_variable(df["resentment"], lambda x: -8 <= x <= +8) 
    df["race_edu_block"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["college"]) or pd.isna(row["race"]) else
        "NonWhite" if row["race"] in ("Black","Hispanic","Other") else
        "WhiteCollege" if row["race"] == "White" and row["college"] == 1 else
        "WhiteNonCollege" if row["race"] == "White" and row["college"] == 0 else
        pd.NA
    ), axis=1)
    df["race_party_block"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["race"]) or pd.isna(row["republican"]) or pd.isna(row["democrat"]) else
        "WhiteRep" if row["race"] == "White" and row["republican"] == 1 else
        "WhiteDem" if row["race"] == "White" and row["democrat"] == 1 else
        "WhiteInd" if row["race"] == "White" else
        "NonWhite" if row["race"] in ("Black","Hispanic","Other") else
        pd.NA
    ), axis=1)
    df["vote_prev_vote"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["prev_rep_pres"]) or pd.isna(row["vote_rep_pres"]) else
        "Rep-Rep" if row["prev_rep_pres"] == 1 and row["vote_rep_pres"] == 1 else
        "Rep-Dem" if row["prev_rep_pres"] == 1 and row["vote_rep_pres"] == 0 else
        "Dem-Rep" if row["prev_rep_pres"] == 0 and row["vote_rep_pres"] == 1 else
        "Dem-Dem" if row["prev_rep_pres"] == 0 and row["vote_rep_pres"] == 0 else
        pd.NA
    ), axis=1)
    return df

def build_2020_cumul_anes(path="raw/anes_timeseries_cdf_csv_20220916.csv"):
    raw_cdf = pd.read_csv(path)
    df = raw_cdf[[]].copy()
    df["year"] = raw_cdf["VCF0004"]
    df["weight"] = map_variable(raw_cdf["VCF0009z"], type_check=float)
    validate_variable(df["weight"], lambda x: x >= 0)
    df["age"] = map_variable(raw_cdf["VCF0101"], nulls=[-2])
    validate_variable(df["age"], lambda x: x >= 0 and x <= 120)
    df["female"] = map_variable(raw_cdf["VCF0104"], nulls =[3,0,-9], mapping={1:0,2:1})
    validate_variable(df["female"], lambda x: x in [0, 1])
    df["race"] = map_variable(raw_cdf["VCF0105a"], type_check=str, mapping={1:"White",2:"Black",5:"Hispanic",3:"Other",4:"Other",6:"Other"}, nulls=[-4,-8,-9])
    validate_variable(df["race"], lambda x: x in ["White", "Black", "Hispanic", "Other"])
    df["strong_republican"] = map_variable(raw_cdf["VCF0301"], mapping={1:0,2:0,3:0,4:0,5:0,6:0,7:1})
    validate_variable(df["strong_republican"], lambda x: x in [0, 1])
    df["republican"] = map_variable(raw_cdf["VCF0301"], mapping={1:0,2:0,3:0,4:0,5:0,6:1,7:1})
    validate_variable(df["republican"], lambda x: x in [0, 1])
    df["lean_republican"] = map_variable(raw_cdf["VCF0301"], mapping={1:0,2:0,3:0,4:0,5:1,6:1,7:1})
    validate_variable(df["lean_republican"], lambda x: x in [0, 1])
    df["strong_democrat"] = map_variable(raw_cdf["VCF0301"], mapping={1:1,2:0,3:0,4:0,5:0,6:0,7:0})
    validate_variable(df["strong_democrat"], lambda x: x in [0, 1])
    df["democrat"] = map_variable(raw_cdf["VCF0301"], mapping={1:1,2:0,3:0,4:0,5:0,6:0,7:0})
    validate_variable(df["democrat"], lambda x: x in [0, 1])
    df["lean_democrat"] = map_variable(raw_cdf["VCF0301"], mapping={1:1,2:1,3:1,4:0,5:0,6:0,7:0})
    validate_variable(df["lean_democrat"], lambda x: x in [0, 1])
    df["party_3_narrow"] = map_variable(raw_cdf["VCF0301"], mapping={1:"D",2:"D",3:"I",4:"I",5:"I",6:"R",7:"R"}, type_check=str)
    validate_variable(df["party_3_narrow"], lambda x: x in ["D", "I", "R"])
    df["party_3_broad"] = map_variable(raw_cdf["VCF0301"], mapping={1:"D",2:"D",3:"D",4:"I",5:"R",6:"R",7:"R"}, type_check=str)
    validate_variable(df["party_3_broad"], lambda x: x in ["D", "I", "R"])
    df["conservative"] = map_variable(raw_cdf["VCF0803"], mapping={1:0,2:0,3:0,4:0,5:0,6:1,7:1})
    validate_variable(df["conservative"], lambda x: x in [0, 1])
    df["therm_blacks"] = map_variable(raw_cdf["VCF0206"], nulls=[98,99])
    validate_variable(df["therm_blacks"], range(0,101))
    df["therm_whites"] = map_variable(raw_cdf["VCF0207"], nulls=[98,99])
    validate_variable(df["therm_whites"], range(0,101))
    df["therm_police"] = map_variable(raw_cdf["VCF0214"], nulls=[98,99])
    validate_variable(df["therm_police"], range(0,101))
    df["college"] = map_variable(raw_cdf["VCF0110"], mapping = {4: 1, 1: 0, 2: 0, 3:0})
    validate_variable(df["college"], lambda x: x in [0, 1])
    df["anti_imm"] = map_variable(raw_cdf["VCF0879"], nulls=[8,9,"8","9"])
    validate_variable(df["anti_imm"], [1,2,3,4,5,6,7])
    df["no_guar_jobs"] = map_variable(raw_cdf["VCF0809"], nulls = [0,9,"0","9"])
    validate_variable(df["no_guar_jobs"], lambda x: 1 <= x <= 7)
    #df["distrust"] = map_variable(raw_cdf["VCF0808"], mapping={1: 1, 2: 0}) # this variable is kinda garbage
    #validate_variable(df["distrust"], [0, 1])
    df["vote_rep_pres"] = map_variable(raw_cdf["VCF0704a"], mapping={1:1,2:0})
    validate_variable(df["vote_rep_pres"], lambda x: x in [0, 1])
    df["prev_rep_pres"] = map_variable(raw_cdf["VCF9027"], mapping={1:1,2:0})
    validate_variable(df["prev_rep_pres"], lambda x: x in [0, 1])   
    df["blacks_lazy"] = map_variable(raw_cdf["VCF9271"], nulls=[-8,-9])
    validate_variable(df["blacks_lazy"], lambda x: x in [1,2,3,4,5,6,7])
    df["therm_delta"] = map_variable(raw_cdf["VCF9272"], nulls=[-8,-9])
    validate_variable(df["therm_delta"], lambda x: x in [1,2,3,4,5,6,7])
    df["age_group"] = df.apply(lambda x: (
        pd.NA if pd.isna(x["age"]) else
        "18-29" if 18 <= x["age"] <= 29 else
        "30-44" if 30 <= x["age"] <= 44 else
        "45-64" if 45 <= x["age"] <= 64 else
        "65+"
    ), axis=1)
    df["therm_delta"] = df.apply(lambda x: (
        pd.NA if pd.isna(x["therm_whites"]) or pd.isna(x["therm_blacks"]) else
        x["therm_whites"] - x["therm_blacks"]
    ), axis=1)
    df["resentment"] = raw_cdf.apply(lambda row: (
        pd.NA if row["VCF9039"] == " " or row["VCF9040"] == " " or row["VCF9041"] == " " or row["VCF9042"] == " " else
        pd.NA if pd.isna(row["VCF9039"]) or pd.isna(row["VCF9040"]) or pd.isna(row["VCF9041"]) or pd.isna(row["VCF9042"]) else
        pd.NA if int(row["VCF9039"]) in (8,9) or int(row["VCF9040"]) in (8,9) or int(row["VCF9041"]) in (8,9) or int(row["VCF9042"]) in (8,9) else
        int(row["VCF9039"]) + int(row["VCF9042"]) - int(row["VCF9040"]) - int(row["VCF9041"]) #+ 12 # if you want a 4-20 scale. 
    ), axis=1) 
    validate_variable(df["resentment"], lambda x: -8 <= x <= +8)
    df["race_edu_block"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["college"]) or pd.isna(row["race"]) else
        "NonWhite" if row["race"] in ("Black","Hispanic","Other") else
        "WhiteCollege" if row["race"] == "White" and row["college"] == 1 else
        "WhiteNonCollege" if row["race"] == "White" and row["college"] == 0 else
        pd.NA
    ), axis=1)
    df["race_edu_block"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["college"]) or pd.isna(row["race"]) else
        "NonWhite" if row["race"] in ("Black","Hispanic","Other") else
        "WhiteCollege" if row["race"] == "White" and row["college"] == 1 else
        "WhiteNonCollege" if row["race"] == "White" and row["college"] == 0 else
        pd.NA
    ), axis=1)
    df["race_party_block"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["race"]) or pd.isna(row["republican"]) or pd.isna(row["democrat"]) else
        "WhiteRep" if row["race"] == "White" and row["republican"] == 1 else
        "WhiteDem" if row["race"] == "White" and row["democrat"] == 1 else
        "WhiteInd" if row["race"] == "White" else
        "NonWhite" if row["race"] in ("Black","Hispanic","Other") else
        pd.NA
    ), axis=1)
    df["vote_prev_vote"] = df.apply(lambda row: (
        pd.NA if pd.isna(row["prev_rep_pres"]) or pd.isna(row["vote_rep_pres"]) else
        "Rep-Rep" if row["prev_rep_pres"] == 1 and row["vote_rep_pres"] == 1 else
        "Rep-Dem" if row["prev_rep_pres"] == 1 and row["vote_rep_pres"] == 0 else
        "Dem-Rep" if row["prev_rep_pres"] == 0 and row["vote_rep_pres"] == 1 else
        "Dem-Dem" if row["prev_rep_pres"] == 0 and row["vote_rep_pres"] == 0 else
        pd.NA
    ), axis=1)
    return df


def build_2024_cumul_anes(year_cutoff=2000):
    data_cdf = build_2020_cumul_anes()
    data_2024 = build_2024_anes()
    df = pd.concat([data_cdf, data_2024], ignore_index=True)
    df = df[df["year"] >= year_cutoff]
    return df
