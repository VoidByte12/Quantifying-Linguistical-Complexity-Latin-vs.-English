import Functions
analysis_level = ''
list_text_names = ["C_Julius_Caesar_Gallic_War_bk1_english.txt", "C_Julius_Caesar_De_bello_Gallico_bk1_latin.txt", "Ammianus_Marcellinus_Rerum_Gestarum_bkXIV_english.txt", "Ammianus_Marcellinus_Rerum_Gestarum_bkXIV_latin.txt", "P_Vergilius_Maro_Aeneid_bk1_english.txt", "P_Vergilius_Maro_Aeneid_bk1_latin.txt"]
for i in range(1,3):
    if i == 1:
        analysis_lvl = 'word'
    if i == 2:
        analysis_lvl = 'phoneme'
    for text_name in list_text_names:
        Analysis_Data = Functions.analyse(text_name, analysis_level = analysis_lvl)
        print(f"Text Analysis Results for {text_name} at {analysis_lvl} level:")
        for analysis_method, analysis_result in Analysis_Data.items():
            if analysis_method != 'file_name':
                print(f" Method: {analysis_method}, Result: {analysis_result}")

    
