import Functions
analysis_level = ''

texts_per_language = 0

list_text_names = ["C_Julius_Caesar_Gallic_War_bk1_english.txt", "C_Julius_Caesar_De_bello_Gallico_bk1_latin.txt", "Ammianus_Marcellinus_Rerum_Gestarum_bkXIV_english.txt", "Ammianus_Marcellinus_Rerum_Gestarum_bkXIV_latin.txt", "P_Vergilius_Maro_Aeneid_bk1_english.txt", "P_Vergilius_Maro_Aeneid_bk1_latin.txt"]


english_results = {'word_entropy': 0, 'word_entropy_normalised': 0, 'word_types': 0, 'word_tokens' : 0,'type_token_ratio' : 0, 'avg_word_length' : 0, 'Hapax_Legomena_Ratio(HLR)' : 0, 'word_redundancy_ratio' : 0, 'phoneme_entropy': 0, 'phoneme_entropy_normalised': 0, 'phoneme_types' : 0, 'phoneme_tokens' : 0, 'phoneme_redundancy': 0, 'phoneme_redundancy_ratio': 0}

latin_results = {'word_entropy': 0, 'word_entropy_normalised': 0, 'word_types': 0, 'word_tokens' : 0,'type_token_ratio' : 0, 'avg_word_length' : 0, 'Hapax_Legomena_Ratio(HLR)' : 0, 'word_redundancy_ratio' : 0, 'phoneme_entropy': 0, 'phoneme_entropy_normalised': 0, 'phoneme_types' : 0, 'phoneme_tokens' : 0, 'phoneme_redundancy': 0, 'phoneme_redundancy_ratio': 0}


keys = ['word_entropy', 'word_entropy_normalised', 'word_types', 'word_tokens', 
    'type_token_ratio', 'avg_word_length', 'Hapax_Legomena_Ratio(HLR)', 
    'word_redundancy_ratio', 'phoneme_entropy', 'phoneme_entropy_normalised', 
    'phoneme_types', 'phoneme_tokens', 'phoneme_redundancy', 'phoneme_redundancy_ratio']
counter = -1
language = 'english'
for text_name in list_text_names:
    print(f"Analyzing: {text_name}")
    counter += 1

    if counter%2 == 0:
        target_dict = english_results
        texts_per_language += 1
        language = 'english'      
    else:
        target_dict = latin_results
        language = 'latin'

    Analysis_Data = Functions.analyse(text_name,language=language)

    for key in keys:
        target_dict[key] += Analysis_Data[key]
for x in range(1,3):
    if x == 1:
        target_dict = english_results
    if x == 2:
        target_dict = latin_results
    for key in target_dict.keys():
        if key != 'file_name':  
            target_dict[key] /= texts_per_language
    
print("\n" + "="*70)
print("FINAL AVERAGED RESULTS")
print("="*70)

for b in range(1,3):
    if b == 1:
        target_dict = english_results
        language = "English"
    if b == 2:
        target_dict = latin_results
        language = "Latin"
    for analysis_method, analysis_result in target_dict.items():
        print(f" Language: {language},Method: {analysis_method}, Result: {analysis_result}")
        print("\n")
