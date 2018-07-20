import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

### DATA CLEANING ###

with open("languages_data.csv") as datafile:
    data = pd.read_csv(datafile)
    data.drop(columns=['native4', 'native5'])

language_typos = {'None': np.nan, '0': np.nan,'English ': 'English', 'Japanese ': 'Japanese', 'Spansih': 'Spanish',\
                  'Ger,Am': 'German', 'Mandarin Chinese': 'Mandarin', 'English (C2/Fluent?)': 'English',\
                  'Korean ': 'Korean', 'American Sign Language ': 'American Sign Language', 'Spanish ': 'Spanish',\
                  'Polski Kurwa': 'Polish', 'Chinese (Mandarin)': 'Mandarin', 'French B1': 'French',\
                  'Chinese': 'Mandarin', 'Japonese ': 'Japanese', 'Armenian ': 'Armenian', 'Portuguese ': 'Portuguese',\
                  'Romania': 'Romanian', 'Ingliĺ\xa0': 'English', 'German (Deutsch)': 'German', 'French ': 'French',\
                  'German ': 'German', 'Russian ': 'Russian', 'Portuguăşs (Portuguese)': 'Portuguese',\
                  "Spanish (I Learnt When I Was 9, So I'M Fluent But Not Technically Native)": 'Spanish',\
                  'Mandarin ': 'Mandarin', 'English, American': 'English', 'English (American)': 'English', \
                  'Englidh': 'English', 'Contonese': 'Cantonese', 'British English': 'English', 'Norway': 'Norwegian',\
                  'English Uk': 'English', 'American English': 'English'}

# Replace mistyped language names
foreign_cols = ['foreign1', 'foreign2', 'foreign3', 'foreign4', 'foreign5']
native_cols = ['native1', 'native2', 'native3']
for col in foreign_cols + native_cols:
    data[col] = data[col].str.title()
    data[col] = data[col].fillna(value=np.nan)
    for i, row in data[[col]].iterrows():
        cur_val = data.loc[i, col]
        if cur_val in language_typos:
            data.loc[i, col] = language_typos[cur_val]

# Fix rows where native_no value is different from number of native languages listed
native_count = data[native_cols].count(axis='columns')
data.loc[data['native_no'] != native_count, 'native_no'] = native_count

# Create additional column of count of other foreign languages
foreign_other = data['foreign_other'].unique()
foreign_dict = {}
for item in foreign_other:
    try:
        foreign_dict[item] = len(item.replace(" ", "").split(','))
    except:
        foreign_dict[item] = 0
data['foreign_other_count'] = data['foreign_other'].map(foreign_dict)

# Fix rows where foreign_no is different from number of foreign languages listed
foreign_count = data[foreign_cols].count(axis='columns') + data['foreign_other_count']
data.loc[(data['foreign_no'] != foreign_count) & (data['foreign_no'] <= 5), 'foreign_no'] = foreign_count

# Set the combined_no values to the sum of native_no and foreign_no
data['combined_no'] = data['native_no'] + data['foreign_no']

# Convert language level names to numbers
level_cols = ['foreign1_lvl', 'foreign2_lvl', 'foreign3_lvl', 'foreign4_lvl', 'foreign5_lvl']
level_to_number = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}
for col in level_cols:
    data[col] = data[col].map(level_to_number)

# Convert values of efficiency and enjoyment to numbers or NaN
eff_cols = ['eff_school', 'eff_course', 'eff_self', 'eff_textbook',
            'eff_online', 'eff_native', 'eff_media', 'eff_travel']
enj_cols = ['enj_school', 'enj_course', 'enj_self', 'enj_textbook',
            'enj_online', 'enj_native', 'enj_media', 'enj_travel']
quality_to_number = {"Don't know": np.nan, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
for col in eff_cols + enj_cols:
    data[col] = data[col].map(quality_to_number)

### ANALYSIS ###

# set up values for all graphs
hist_color = 'paleturquoise'
hist_color2 = 'darkslateblue'
hist_color3 = 'black'
scatter_color = 'cornflowerblue'
pie_color1 = 'dodgerblue'
pie_color2 = 'lightskyblue'
pie_color3 = 'powderblue'
pie_color4 = 'c'
pie_color5 = 'darkcyan'
pie_color6 = 'turquoise'
mean_color, median_color, mode_color = 'firebrick', 'salmon', 'navy'
mean_patch = mpatches.Patch(color=mean_color, label='Mean')
median_patch = mpatches.Patch(color=median_color, label='Median')
mode_patch = mpatches.Patch(color=mode_color, label='Mode')

# # plotting distributions of combined_no, native_no and foreign_no
# # set up some values
# number_cols = ['combined_no', 'native_no', 'foreign_no']
# com_mean, nat_mean, for_mean = data[number_cols].mean()
# com_median, nat_median, for_median = data[number_cols].median()
# com_max, nat_max, for_max = data[number_cols].max()
# com_min, nat_min, for_min = data[number_cols].min()
# modes = data[number_cols].mode()
# com_mode, nat_mode, (for_mode1, for_mode2) = modes['combined_no'][0], modes['native_no'][0], modes['foreign_no']
#
# # prepare a figure with 3 subplots
# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11,4))
# plt.legend(handles=[mean_patch, median_patch, mode_patch], bbox_to_anchor=(1,1), loc=2)
#
# ax1.hist(data['combined_no'], bins=int(com_max-com_min+1), range=(com_min,com_max+1),
#          color=hist_color, align='left', rwidth=0.9)
# ax1.set_title('Total number of languages')
# ax1.axvline(x=com_mean, color=mean_color)
# ax1.axvline(x=com_median+0.05, color=median_color)
# ax1.axvline(x=com_mode-0.05, color=mode_color)
#
# ax2.hist(data['native_no'], bins=int(nat_max-nat_min+1), range=(nat_min,nat_max+1),
#          color=hist_color, align='left', rwidth=0.9)
# ax2.set_title('Number of native languages')
# ax2.axvline(x=nat_mean, color=mean_color)
# ax2.axvline(x=nat_median+0.02, color=median_color)
# ax2.axvline(x=nat_mode-0.02, color=mode_color)
#
# ax3.hist(data['foreign_no'], bins=int(for_max-for_min+1), range=(for_min,for_max+1),
#          color=hist_color, align='left', rwidth=0.9)
# ax3.set_title('Number of foreign languages')
# ax3.axvline(x=for_mean, color=mean_color)
# ax3.axvline(x=for_median+0.04, color=median_color)
# ax3.axvline(x=for_mode1, color=mode_color)
# ax3.axvline(x=for_mode2-0.04, color=mode_color)
#
# #plt.show()
# plt.close()

# # find most popular languages
# # native_lang_counts = {}
# # foreign_lang_counts = {}
# # combined_lang_counts = {}
# # for col in native_cols:
# #     for lang_row in data[[col]].iterrows():
# #         lang = lang_row[1][col]
# #         if type(lang) != float:
# #             native_lang_counts[lang] = native_lang_counts.get(lang, 0) + 1
# #             combined_lang_counts[lang] = combined_lang_counts.get(lang, 0) + 1
# # for col in foreign_cols:
# #     for lang_row in data[[col]].iterrows():
# #         lang = lang_row[1][col]
# #         if type(lang) != float:
# #             foreign_lang_counts[lang] = foreign_lang_counts.get(lang, 0) + 1
# #             combined_lang_counts[lang] = combined_lang_counts.get(lang, 0) + 1
# # native_lang_sorted = sorted(native_lang_counts.items(), key=lambda kv: kv[1])
# # native_lang_desc, native_counts = zip(*native_lang_sorted)
# # native_lang_desc = ['Other'] + list(native_lang_desc[-15:])
# # native_counts = [sum(native_counts[:-15])] + list(native_counts[-15:])
# # plt.barh(native_lang_desc, native_counts, color=hist_color)
# # plt.title('Native languages by frequency')
# # plt.xlabel('Number of people')
# # plt.yticks(size='x-small')
# # #plt.show()
# # plt.close()
# # foreign_lang_sorted = sorted(foreign_lang_counts.items(), key=lambda kv: kv[1])
# # foreign_lang_desc, foreign_counts = zip(*foreign_lang_sorted)
# # foreign_lang_desc = ['Other'] + list(foreign_lang_desc[-15:])
# # foreign_counts = [sum(foreign_counts[:-15])] + list(foreign_counts[-15:])
# # plt.barh(foreign_lang_desc, foreign_counts, color=hist_color)
# # plt.title('Foreign languages by frequency')
# # plt.xlabel('Number of people')
# # plt.yticks(size='x-small')
# # #plt.show()
# # plt.close()
# # combined_lang_counts = sorted(combined_lang_counts.items(), key=lambda kv: kv[1])
# # combined_lang_desc, combined_counts = zip(*combined_lang_counts)
# # combined_lang_desc = ['Other'] + list(combined_lang_desc[-15:])
# # combined_counts = [sum(combined_counts[:-15])] + list(combined_counts[-15:])
# # plt.barh(combined_lang_desc, combined_counts, color=hist_color)
# # plt.title('All languages by frequency')
# # plt.xlabel('Number of people')
# # plt.yticks(size='x-small')
# # #plt.show()
# # plt.close()

# # compare levels of foreign languages
# # labels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
# # values = [[0 for i in range(6)] for j in range(5)]
# # for i, col in enumerate(level_cols):
# #     for level in range(1, 7):
# #         try:
# #             values[i][level-1] = data[col].value_counts()[level]
# #         except:
# #             pass
# # values_combined = [sum([values[row][col] for row in range(5)]) for col in range(6)]
# # print(values_combined)
# # plt.figure(figsize=(4,4))
# # plt.pie(values_combined, labels=labels, autopct='%1.2f%%',
# #         colors=[pie_color1, pie_color2, pie_color3, pie_color4, pie_color5, pie_color6])
# # plt.title('Share of language levels')
# # #plt.show()
# # plt.close()

data['level_means'] = data[level_cols].mean(axis=1)
print(data[['foreign_no', 'level_means']].corr())

data['level_max'] = data[level_cols].max(axis=1)
print(data[['foreign_no', 'level_max']].corr())

# # plotting distributions for 'foreign_no' for women and men
# women = data.loc[data['gender']=="Female", ['native_no','foreign_no']]
# men = data.loc[data['gender']=="Male", ['native_no','foreign_no']]
#
# women_nat_mean, women_for_mean = women.mean()
# men_nat_mean, men_for_mean = men.mean()
# women_nat_median, women_for_median = women.median()
# men_nat_median, men_for_median = men.median()
# women_nat_max, women_for_max = women.max()
# men_nat_max, men_for_max = men.max()
# women_nat_min, women_for_min = women.min()
# men_nat_min, men_for_min = men.min()
#
# # plot foreign languages
# plt.figure(figsize=(11, 4))
# plt.subplot(121)
# plt.hist(women['foreign_no'], bins=int(women_for_max-women_for_min+1), range=(women_for_min, women_for_max+1),
#          align='left', color=hist_color, width=0.9)
# plt.xticks(list(range(0,int(women_for_max+1))))
# plt.axvline(women_for_mean, color=mean_color)
# plt.axvline(women_for_median, color=median_color)
# plt.title('Women')
# plt.xlabel('Number of foreign languages')
# plt.subplot(122)
# plt.hist(men['foreign_no'], bins=int(women_for_max-women_for_min+1), range=(women_for_min, women_for_max+1),
#          align='left', color=hist_color, width=0.9)
# plt.xticks(list(range(0, int(women_for_max+1))))
# plt.axvline(men_for_mean, color=mean_color)
# plt.axvline(men_for_median, color=median_color)
# plt.title('Men')
# plt.xlabel('Number of foreign languages')
# plt.legend(handles=[mean_patch, median_patch], bbox_to_anchor=(1,1), loc=2)
# #plt.show()
# plt.close()
#
# # plot native languages
# plt.figure(figsize=(11,4))
# plt.subplot(121)
# plt.hist(women['native_no'], bins=int(women_nat_max-women_nat_min+1), range=(women_nat_min, women_nat_max+1),
#          align='left', color=hist_color, width=0.9)
# plt.xticks(list(range(0, int(women_nat_max+1))))
# plt.axvline(women_nat_mean, color=mean_color)
# plt.axvline(women_nat_median, color=median_color)
# plt.title('Women')
# plt.xlabel('Number of native languages')
# plt.subplot(122)
# plt.hist(men['native_no'], bins=int(men_nat_max-men_nat_min+1), range=(men_nat_min, men_nat_max+1),
#          align='left', color=hist_color, width=0.9)
# plt.xticks(list(range(0, int(men_nat_max+1))))
# plt.axvline(men_nat_mean, color=mean_color)
# plt.axvline(men_nat_median, color=median_color)
# plt.title('Men')
# plt.xlabel('Number of native languages')
# plt.legend(handles=[mean_patch, median_patch], bbox_to_anchor=(1,1), loc=2)
# #plt.show()
# plt.close()

# # find if there is a relationship between age and number of foreign languages
# age_defined = data['age'] != 0
# print(data[['foreign_no', 'age']].corr())
# plt.scatter(data.loc[age_defined, 'age'], data.loc[age_defined, 'foreign_no'], color=scatter_color)
# plt.title('Relationship between age and number of foreign languages')
# plt.xlabel('Age')
# plt.ylabel('Number of foreign languages')
# plt.grid()
# #plt.show()
# plt.close()

# age_defined = data['age'] != 0
# age_group = data['age'].map(lambda x: np.round(x, -1))
# grouped_ages = data['foreign_no'].groupby(age_group)
# groups = [10, 20, 30, 40, 50]
# ages_mean = [grouped_ages.get_group(group).mean() for group in groups]
# ages_median = [grouped_ages.get_group(group).median() for group in groups]
# bar_width = 0.3
# plt.bar([group//10-bar_width/2 for group in groups], ages_mean, width=bar_width, color=mean_color)
# plt.bar([group//10+bar_width/2 for group in groups], ages_median, width=bar_width, color=median_color)
# plt.xticks([group // 10 for group in groups], [str(age) + "-" + str(age+9) for age in groups])
# plt.title("Languages spoken by age")
# plt.xlabel("Age")
# plt.ylabel("Number of foreign languages")
# for i, mean in enumerate(ages_mean):
#     plt.text(i+0.75, mean+0.02, str(np.round(mean, 2)), size='x-small')
# for i, median in enumerate(ages_median):
#     plt.text(i+1.05, median+0.02, str(median), size='x-small')
# plt.legend(handles=[mean_patch, median_patch], bbox_to_anchor=(1,1), loc=1)
# #plt.show()
# plt.close()

# # compare native English speakers and non-native English speakers
# english_is_native = (data['native1'] == 'English') | (data['native2'] == 'English') | (data['native3'] == 'English')
# print(data.loc[english_is_native, 'foreign_no'].mean(), data.loc[english_is_native, 'foreign_no'].median())
# print(data.loc[~english_is_native, 'foreign_no'].mean(), data.loc[~english_is_native, 'foreign_no'].median())
# max = int(data['foreign_no'].max())
# min = int(data['foreign_no'].min())
# eng_patch = mpatches.Patch(color=hist_color, label='Native language is English')
# not_eng_patch = mpatches.Patch(color=hist_color2, label='Other native language')
# plt.hist(data.loc[~english_is_native, 'foreign_no'], bins=int(max-min+1), range=(min, max+1),
#          color=hist_color2, width=0.9, align='left', alpha=0.9)
# plt.hist(data.loc[english_is_native, 'foreign_no'], bins=int(max-min+1), range=(min, max+1),
#          color=hist_color, width=0.7, align='left', alpha=0.9)
# plt.title('Differences between native English speakers\nand native speakers of other languages')
# plt.xticks(list(range(min, max+1)))
# plt.xlabel('Number of languages')
# plt.legend(handles=[eng_patch, not_eng_patch], bbox_to_anchor=(1,1), loc=1)
# #plt.show()
# plt.close()

# # compare foreign languages by continent
# country_to_continent = {'Nigeria': 'Africa', 'Egypt': 'Africa', 'Algeria': 'Africa',
#                        'Brazil': 'South America', 'Bolivia': 'South America', 'Chile': 'South America',
#                        'Ecuador': 'South America',
#                        'Portugal': 'Europe', 'Poland': 'Europe', 'Italy': 'Europe', 'Austria': 'Europe',
#                        'Slovakia': 'Europe', 'Estonia': 'Europe', 'Germany': 'Europe', 'Netherlands': 'Europe',
#                        'Belgium': 'Europe', 'United Kingdom': 'Europe', 'Spain': 'Europe', 'Ireland': 'Europe',
#                        'Russia': 'Europe', 'France': 'Europe', 'Finland': 'Europe', 'Latvia': 'Europe',
#                        'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Romania': 'Europe', 'Norway': 'Europe',
#                        'Greece': 'Europe', 'Sweden': 'Europe',
#                        'Jordan': 'Asia', 'Saudi Arabia': 'Asia', 'India': 'Asia', 'Korea, South': 'Asia',
#                        'Hong Kong': 'Asia', 'United Arab Emirates': 'Asia', 'Turkey': 'Asia', 'Quatar': 'Asia',
#                        'Israel': 'Asia', 'Singapore': 'Asia', 'Malaysia': 'Asia', 'Syria': 'Asia',
#                        'Philippines': 'Asia', 'Vietnam': 'Asia', 'China': 'Asia', 'Japan': 'Asia',
#                        'United States': 'North America', 'Canada': 'North America',
#                        'Australia': 'Australia'}
# continents = ['Africa', 'Asia', 'Europe', 'South America', 'North America']
# continents_data = data['country'].map(country_to_continent)
# grouped_continents = data['foreign_no'].groupby(continents_data)
# max = int(data['foreign_no'].max())
# min = int(data['foreign_no'].min())
# europe_patch = mpatches.Patch(color=hist_color, label='Europe')
# namerica_patch = mpatches.Patch(color=hist_color2, label='North America')
# asia_patch = mpatches.Patch(color=hist_color3, label='Asia')
# plt.hist(grouped_continents.get_group('Europe'), bins=max-min+1, range=(min, max+1),
#          align='left', width=0.9, alpha=1, color=hist_color)
# plt.hist(grouped_continents.get_group('North America'), bins=max-min+1, range=(min, max+1),
#          align='left', width=0.6, alpha=0.8, color=hist_color2)
# plt.hist(grouped_continents.get_group('Asia'), bins=max-min+1, range=(min, max+1),
#          align='left', width=0.3, alpha=1, color=hist_color3)
# plt.title('Comparison of Europe, North America and Asia')
# plt.xticks(list(range(min, max+1)))
# plt.xlabel('Number of foreign languages')
# plt.legend(handles=[europe_patch, namerica_patch, asia_patch])
# #plt.show()
# plt.close()

# # compare which methods are most used for learning
# # get counts of each method
# methods = {}
# total_learners = 0
# for row in data[['methods']].iterrows():
#     if type(row[1]['methods']) != float:
#         total_learners += 1
#         row_methods = set(row[1]['methods'].split(';'))
#         for method in row_methods:
#             methods[method] = methods.get(method, 0) + 1
# other_keys = ['I live in Korea and only use English at my job.',
#               'Play computer games with English words', 'Living in foreign country',
#               'Conversation practice with other language learners', 'Duolingo app, watching TV/news in target languages',
#               'Online websites', 'German-speaking groups', 'Radio', 'Internet/social media', 'Videogames, News Articles',
#               'Relationship with native speaker', ' I acquired most of my English skills by simply using English websites like Reddit.',
#               'Online in general', 'I come from a multilingual country - foreign languages were part of my day-to-day life.',
#               'Duolingo', 'Apps such as Duolingo', 'Online learning (memrise, duolingo)', 'Mobile Applications',
#               'Apps: duolingo, memrise, tinycards', 'Apps (Duolingo, Memrise, Lingodeer, Tofu Lesen)', 'Mobile Apps',
#               'Udacity :-)', 'I donâ€™t actively study them anymore']
# for key in other_keys:
#     methods['Other'] = methods.get('Other', 0) + methods[key]
#     del methods[key]
# methods['Conversation with\nnative speaker'] = methods['One-to-one conversation with native speaker']
# del methods['One-to-one conversation with native speaker']
#
# methods_descending = sorted(methods.items(), key=lambda kv: kv[1])
# methods_list, count_list = zip(*methods_descending)
# rcParams.update({'figure.subplot.left': 0.23})
# plt.barh(methods_list, count_list, color=hist_color)
# plt.title('Methods of learning')
# plt.xlabel('Number of people using a specific method')
# plt.yticks(methods_list, size='x-small')
# #plt.show()
# plt.close()

# # plot relationship between efficiency and enjoyment
# eff_score = pd.Series(data[eff_cols].values.ravel('F'))
# enj_score = pd.Series(data[enj_cols].values.ravel('F'))
# values_exist = ~(eff_score.isna() | enj_score.isna())
# eff_enj = pd.DataFrame(data={'eff': eff_score[values_exist], 'enj': enj_score[values_exist]})
# eff_enj_groups = eff_enj.groupby(['eff', 'enj'])
# score_vals = [1.0, 2.0, 3.0, 4.0, 5.0]
# for eff in score_vals:
#     for enj in score_vals:
#         plt.scatter(eff, enj, s=eff_enj_groups.get_group((eff, enj)).count()['eff']*8,
#                     c=scatter_color, alpha=0.9, edgecolors='black', linewidths=0.8)
# plt.title('Relationship between indicated efficiency and\nenjoyment of a method of learning')
# plt.xlabel('Efficiency score')
# plt.ylabel('Enjoyment score')
# #plt.show()
# plt.close()

# # age of beginning of learning foreign languages
# mean = data['age_first'].mean()
# median = data['age_first'].median()
# print(mean, median, data['age_first'].mode())
# min = int(data['age_first'].min())
# max = int(data['age_first'].max())
# plt.hist(data['age_first'], bins=24, range=(min, max+1), color=hist_color, width=3)
# plt.axvline(mean, color=mean_color)
# plt.axvline(median, color=median_color)
# plt.legend(handles=[mean_patch, median_patch], bbox_to_anchor=(1,1), loc=1)
# plt.title('Age of starting to learn a foreign language')
# plt.xlabel('Age')
# #plt.show()
# plt.close()

# # hours devoted to studying per week
# data.loc[data['hours_week']==400, 'hours_week'] = np.nan
# mean = data['hours_week'].mean()
# median = data['hours_week'].median()
# min = int(data['hours_week'].min())
# max = int(data['hours_week'].max())
# print(mean, median, data['hours_week'].mode())
# plt.hist(data['hours_week'], bins=20, range=(min, max+1), color=hist_color, width=2.7)
# plt.axvline(mean, color=mean_color)
# plt.axvline(median, color=median_color)
# plt.legend(handles=[mean_patch, median_patch])
# plt.title('Hours devoted to studying per week')
# plt.xlabel('Hours')
# #plt.show()
# plt.close()

# # studying foreign languages
# plt.figure(figsize=(9,4))
# plt.subplot(121)
# labels = ['Yes', 'No']
# values = [data['study_cur'].value_counts()[label] for label in labels]
# plt.pie(values, labels=labels, explode=(0, 0.1), autopct='%1.2f%%',
#         colors=[pie_color1, pie_color2])
# plt.title('Do you study a foreign language at present?')
# plt.subplot(122)
# labels = ['Yes', 'No', 'Maybe']
# values = [data['study_future'].value_counts()[label] for label in labels]
# plt.pie(values, labels=labels, explode=(0, 0.15, 0.05), autopct='%1.2f%%',
#         colors=[pie_color1, pie_color2, pie_color3])
# plt.title('Do you plan to study a foreign\nlanguage in the future?')
# #plt.show()
# plt.close()

