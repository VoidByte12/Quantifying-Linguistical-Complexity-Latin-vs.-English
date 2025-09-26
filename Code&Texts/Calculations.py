import Functions
analysis_level = ''
for i in range(1,3):
    if i == 1:
        analysis_lvl = 'word'
    if i == 2:
        analysis_lvl = 'phoneme'
    # print(Functions.analyse("C_Julius_Caesar_De_bello_Gallico_COMMENTARIUS_PRIMUS_(bk1).txt", analysis_level = analysis_lvl))
    # print(Functions.analyse("C_Julius_Caesar_Gallic_War_bk1.txt", analysis_level = analysis_lvl))
test = {Functions.analyse("C_Julius_Caesar_De_bello_Gallico_COMMENTARIUS_PRIMUS_(bk1).txt", analysis_level = analysis_lvl)}
print(test)
    
