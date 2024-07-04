import pandas as pd
import csv
import re

#Note: 
# change this to something else it is too similar scripture_value = scriptures_value
# add abreviation to form to deuteronomy in the patterns
patterns = [
            r'Bible',
            r'Old Testament',
            r'[bB]ooks of [A-Za-z]+ and [A-Za-z]+',
            r'Genesis (?:50|[1-4][0-9]|[1-9])|Genesis(?!\s*\d)',
            r'Gen. (?:50|[1-4][0-9]|[1-9])|Gen\.(?!\s*\d)',
            r'Exodus (?:40|[1-3][0-9]|[1-9])|Exodus(?!\s*\d)',
            r'Ex\. (?:40|[1-3][0-9]|[1-9])|Ex\.(?!\s*\d)',
            r'Leviticus (?:27|[1-2][0-9]|[1-9])|Leviticus(?!\s*\d)',
            r'Lev\. (?:27|[1-2][0-9]|[1-9])|Lev\.(?!\s*\d)',
            r'Numbers (?:36|[1-3][0-9]|[1-9])|Numbers(?!\s*\d)',
            r'Num\. (?:36|[1-3][0-9]|[1-9])|Num\.(?!\s*\d)',
            r'Deuteronomy (?:34|[1-3][0-9]|[1-9])|Deuteronomy(?!\s*\d)',
            r'Joshua (?:24|[1-2][0-9]|[1-9])|Joshua(?!\s*\d)',
            r'Josh\. (?:24|[1-2][0-9]|[1-9])|Josh\.(?!\s*\d)',
            r'Judges (?:21|[1-2][0-9]|[1-9])|Judges(?!\s*\d)',
            r'Judg\. (?:21|[1-2][0-9]|[1-9])|Judg\.(?!\s*\d)',
            r'Ruth (?:[1-4])|Ruth',
            r'Rut\. (?:[1-4])|Rut\.(?!\s*\d)',
            r'1 Samuel (?:31|[12][0-9]|[1-9])|1 Samuel(?!\s*\d)',
            r'1 Sam\. (?:31|[12][0-9]|[1-9])|1 Sam\.(?!\s*\d)',
            r'2 Samuel (?:24|[1-2][0-9]|[1-9])|2 Samuel(?!\s*\d)',
            r'2 Sam\. (?:24|[1-2][0-9]|[1-9])|2 Sam\.(?!\s*\d)',
            r'1 Kings (?:22|[1-2][0-9]|[1-9])|1 Kings(?!\s*\d)',
            r'2 Kings (?:25|[1-2][0-9]|[1-9])|2 Kings(?!\s*\d)',
            r'\'1 Chronicles (?:29|[1-2][0-9]|[1-9])\'|\'1 Chronicles(?!\s*\d)\'|1 Chronicles (?:29|[1-2][0-9]|[1-9])|1 Chronicles(?!\s*\d)',
            r'\'2 Chronicles (?:36|[1-3][0-9]|[1-9])\'|\'2 Chronicles(?!\s*\d)\'|2 Chronicles (?:36|[1-3][0-9]|[1-9])|2 Chronicles(?!\s*\d)',
            r'\'1 Chr. (?:29|[1-2][0-9]|[1-9])\'|\'1 Chr.(?!\s*\d)\'|1 Chr. (?:29|[1-2][0-9]|[1-9])|1 Chr.(?!\s*\d)',
            r'\'2 Chr. (?:36|[1-3][0-9]|[1-9])\'|\'2 Chr.(?!\s*\d)\'|2 Chr. (?:36|[1-3][0-9]|[1-9])|2 Chr.(?!\s*\d)',
            r'Ezra (?:10|[1-9])|Ezra',#removed Ezra
            r'Nehemiah (?:13|[1-9]|1[0-2])|Nehemiah(?!\s*\d)',
            r'Neh\. (?:13|[1-9]|1[0-2])|Neh\.(?!\s*\d)',
            r'Esther (?:10|[1-9])|Esther',#removed Esther
            r'Job (?:42|[1-3][0-9]|[1-9])|Job',#removed job
            r'Psalms (?:150|1[0-4][0-9]|[1-9][0-9]|[1-9])|Psalms(?!\s*\d)',
            r'Psalm (?:150|1[0-4][0-9]|[1-9][0-9]|[1-9])|Psalm(?!\s*\d)',
            r'Ps\. (?:150|1[0-4][0-9]|[1-9][0-9]|[1-9])|Ps\.(?!\s*\d)',
            r'Proverbs (?:31|[1-2][0-9]|[1-9])|Proverbs(?!\s*\d)',
            r'Prov\. (?:31|[1-2][0-9]|[1-9])|Prov\.(?!\s*\d)',
            r'Ecclesiastes (?:12|[1-9]|10|11)|Ecclesiastes(?!\s*\d)',
            r'Song of Solomon (?:[1-8])|Song of Solomon (?!\s*\d)|Song of Solomon',
            r'Song\. (?:[1-8])|Song\.(?!\s*\d)|Song.',
            r'Isaiah (?:66|[1-5][0-9]|[1-9])|Isaiah',#removed Isaiah
            r'Isa\. (?:66|[1-5][0-9]|[1-9])|Isa\.(?!\s*\d)',
            r'Jeremiah (?:52|[1-4][0-9]|[1-9])|Jeremiah',#removed Jeremiah
            r'Jer\. (?:52|[1-4][0-9]|[1-9])|Jer\.(?!\s*\d)',
            r'Lamentations (?:[1-5])|Lamentations(?!\s*\d)',
            r'Lam\. (?:[1-5])|Lam\.(?!\s*\d)',
            r'Ezekiel (?:48|[1-3][0-9]|[1-9])|Ezekiel(?!\s*\d)|Ezekiel',
            r'Ezek\. (?:48|[1-3][0-9]|[1-9])|Ezek.(?!\s*\d)',
            r'Daniel (?:12|[1-9]|10|11)|Daniel',#removed Daniel
            r'Dan\. (?:12|[1-9]|10|11)|Dan\.(?!\s*\d)',
            r'Hosea (?:14|[1-9]|10|11|12|13)|Hosea(?!\s*\d)',
            r'Joel (?:[1-3])|Joel',#removed Joel
            r'Amos (?:[1-9])|Amos(?!\s*\d)',
            r'Obadiah 1',
            r'Jonah (?:[1-4])|Jonah',#removed Jonah
            r'Micah (?:[1-7])|Micah(?!\s*\d)',
            r'Nahum (?:[1-3])|Nahum(?!\s*\d)',
            r'Habakkuk (?:[1-3])|Habakkuk(?!\s*\d)',
            r'Hab\. (?:[1-3])|Hab\.(?!\s*\d)',
            r'Zephaniah (?:[1-3])|Zephaniah(?!\s*\d)',
            r'Zeph\. (?:[1-3])|Zeph\.(?!\s*\d)',
            #Note: change haggai to Haggai (?:[1-2]) after testing
            r'Haggai (?:[1-3])|Haggai(?!\s*\d)',
            r'Hag\. (?:[1-2])|Hag\.(?!\s*\d)',
            r'Zechariah (?:14|[1-9]|10|11|12|13)|Zechariah(?!\s*\d)',
            r'Zech\. (?:14|[1-9]|10|11|12|13)|Zech\.(?!\s*\d)',
            r'Malachi (?:[1-4])|Malachi(?!\s*\d)',
            r'Mal\. (?:[1-4])|Mal\.(?!\s*\d)',
            r'1 Nephi (?:22|[12][0-9]|[1-9])|1 Nephi(?!\s*\d)',
            r'1 Ne\. (?:22|[12][0-9]|[1-9])|1 Ne\.(?!\s*\d)',
            r'2 Nephi (?:3[0-3]|[12][0-9]|[1-9])|2 Nephi(?!\s*\d)',
            r'2 Ne\. (?:3[0-3]|[12][0-9]|[1-9])|2 Ne\.(?!\s*\d)',
            r'Jacob (?:[1-7])|Jacob',#removed Jacob
            r'Enos 1',#removed Enos
            r'Jarom 1',#removed Jarom
            r'Omni 1',#removed Omni
            r'Words of Mormon',
            r'W of M',
            r'Mosiah (?:2[0-9]|[1-9])|Mosiah',#removed Mosiah
            r'Alma (?:6[0-3]|[1-5][0-9]|[1-9])|Alma',#removed Alma
            r'Helaman (?:1[0-6]|[1-9])|Helaman(?!\s*\d)|Helaman',#remove Helaman
            r'Hel\. (?:1[0-6]|[1-9])|Hel\.(?!\s*\d)',
            r'3 Nephi (?:30|[12][0-9]|[1-9])|3 Nephi(?!\s*\d)',
            r'3 Ne\. (?:30|[12][0-9]|[1-9])|3 Ne\.(?!\s*\d)',
            r'4 Nephi',
            r'4 Ne.',
            #r'Book of Mormon|Mormon (?:[1-9])|Mormon(?!\s+Church\b)(?!\s*\d)',
            ##removed Mormon for future code
            r'Book of Mormon',
            r'Morm\. (?:[1-9])|Morm\.(?!\s*\d)',
            r'Ether (?:1[0-5]|[1-9])|Ether',#removed Ether
            r'Moro\. (?:10|[1-9])|Moro\.(?!\s*\d)',
            r'Moroni (?:10|[1-9])|Moroni',#removed Moroni
            r'New Testament',
            r'Epistles of [A-Za-z]+,? [A-Za-z]+,? and [A-Za-z]+',
            r'Matthew (?:2[0-8]|1[0-9]|[1-9])|\bMatthew\b',#remove Matthew
            r'Matt\. (?:2[0-8]|1[0-9]|[1-9])|Matt\.(?!\s*\d)',
            r'Mark (?:1[0-6]|[1-9])|Mark',#removed Mark
            r'Luke (?:2[0-4]|1[0-9]|[1-9])|Luke',# removed Luke
            r'Gospels of John',
            #r'John (?:2[0-1]|1[0-9]|[1-9])|\bJohn\b',#removed John
            #Kind of works:
            #r'\bJohn\b(?: [1-9]| 1[0-9]| 2[0-1])?',
            #r'(?<!\s)John(?!\s)',
            #r'\bJohn(?: (?:1[0-9]|2[0-1]|[4-9]))?\b',
            r'\'\bJohn\b(?: [1-9]| 1[0-9]| 2[0-1])?\'|\bJohn\b(?: [1-9]| 1[0-9]| 2[0-1])?',
            r'Acts (?:2[0-8]|1[0-9]|[1-9])|Acts(?!\s*\d)',
            r'Epistles of Paul',
            r'Romans (?:1[0-6]|[1-9])|Romans (?!\s*\d)|Romans',#removed Romans
            r'Rom\. (?:1[0-6]|[1-9])|Rom\.(?!\s*\d)',
            r'1 Corinthians (?:1[0-6]|[1-9])|1 Corinthians(?!\s*\d)',
            r'1 Cor\. (?:1[0-6]|[1-9])|1 Cor\.(?!\s*\d)',
            r'2 Corinthians (?:1[0-3]|[1-9])|2 Corinthians(?!\s*\d)',
            r'2 Cor\. (?:1[0-3]|[1-9])|2 Cor\.(?!\s*\d)',
            r'Galatians (?:[1-6])|Galatians(?!\s*\d)',
            r'Gal\. (?:[1-6])|Gal\.(?!\s*\d)',
            r'Ephesians (?:[1-6])|Ephesians(?!\s*\d)',
            r'Eph\. (?:[1-6])|Eph\.(?!\s*\d)',
            r'Philippians (?:[1-4])|Philippians',#removed Philippians
            r'Philip\. (?:[1-4])|Philip.',#removed Philip
            r'Colossians (?:[1-4])|Colossians(?!\s*\d)',
            r'Col\. (?:[1-4])|Col\.(?!\s*\d)',
            r'1 Thessalonians (?:[1-5])|1 Thessalonians(?!\s*\d)',
            r'1 Thes\. (?:[1-5])|1 Thes\.(?!\s*\d)',
            r'2 Thessalonians (?:[1-3])|2 Thessalonians(?!\s*\d)',
            r'2 Thes\. (?:[1-3])|2 Thes\.(?!\s*\d)',
            r'1 Timothy (?:[1-6])|1 Timothy(?!\s*\d)',
            r'1 Tim\. (?:[1-6])|1 Tim\.(?!\s*\d)',
            r'2 Timothy (?:[1-4])|2 Timothy(?!\s*\d)',
            r'2 Tim\. (?:[1-4])|2 Tim\.(?!\s*\d)',
            r'Titus (?:[1-3])|Titus(?!\s*\d)',
            r'Philemon',
            r'Philem.',
            r'Hebrews (?:1[0-3]|[1-9])|Hebrews(?!\s*\d)',
            r'Heb\. (?:1[0-3]|[1-9])|Heb\.(?!\s*\d)',
            #r'(?<!King\s)James (?:[1-5])|(?<!King\s)James(?!\s*\d)',
            #removed James
            r'(?<!King\s)James (?:[1-5])|James',
            r'Epistles of Peter',
            r'1 Peter (?:[1-5])|1 Peter(?!\s*\d)',
            r'1 Pet\. (?:[1-5])|1 Pet\.(?!\s*\d)',
            r'2 Peter (?:[1-3])|2 Peter(?!\s*\d)',
            r'2 Pet\. (?:[1-3])|2 Pet\.(?!\s*\d)',
            r'1 John (?:[1-5])|1 John(?!\s*\d)',
            r'1 Jn\.(?:[1-5])|1 Jn\.(?!\s*\d)',
            r'2 John (?:[1-5])|2 John(?!\s*\d)',
            r'2 Jn\. (?:[1-5])|2 Jn\.(?!\s*\d)',
            r'3 John (?:[1-5])|3 John(?!\s*\d)',
            r'3 Jn\. (?:[1-5])|3 Jn\.(?!\s*\d)',
            r'Jude 1',#removed Jude
            r'Revelation (?:2[0-2]|1[0-9]|[1-9])|Revelation(?!\s*\d)',
            r'Rev\. (?:2[0-2]|1[0-9]|[1-9])|Rev\.(?!\s*\d)',
            r'Doctrine and Covenants (?:1[0-3][0-8]|[1-9][0-9]|[1-9])|Doctrine and Covenants(?!\s*\d)',
            r'D&C (?:1[0-3][0-8]|[1-9][0-9]|[1-9])|D&C(?!\s*\d)',
            r'Moses (?:[1-8])|Moses(?!\s*\d)',#removed Moses
            r'Abraham (?:[1-5])|Abraham',#removed Abraham
            r'Abr\. (?:[1-5])|Abr\.(?!\s*\d)',
            r'Facsimile (?:[1-3])|Facsimile(?!\s*\d)',
            r'Joseph Smith-Matthew',
            r'JS-M',
            r'Joseph Smith History',
            r'Joseph Smith—History',
            r'Articles of Faith',
            r'A of F',
            r'Joseph Smith Translation',
            r'JST',
            r'Ten Commandments',
            r'10 Commandments',
            r'Title Page of the Book of Mormon',
            r'Testimony of the Twelve Apostles from the Book of Mormon',
            ]
counts = {
    "bible_count":0,
    "old_testament_count": 0,
    "genesis_count": 0,
    "exodus_count": 0,
    "leviticus_count": 0,
    "numbers_count": 0,
    "deuteronomy_count": 0,
    "joshua_count": 0,
    "judges_count": 0,
    "ruth_count": 0,
    "first_samuel_count": 0,
    "second_samuel_count": 0,
    "first_kings_count": 0,
    "second_kings_count": 0,
    "first_chronicles_count": 0,
    "second_chronicles_count": 0,
    "ezra_count": 0,
    "nehemiah_count": 0,
    "esther_count": 0,
    "job_count": 0,
    "psalms_count": 0,
    "proverbs_count": 0,
    "ecclesiastes_count": 0,
    "song_of_solomon_count": 0,
    "isaiah_count": 0,
    "jeremiah_count": 0,
    "lamentations_count": 0,
    "ezekiel_count": 0,
    "daniel_count": 0,
    "hosea_count": 0,
    "joel_count": 0,
    "amos_count": 0,
    "obadiah_count": 0,
    "jonah_count": 0,
    "micah_count": 0,
    "nahum_count": 0,
    "habakkuk_count": 0,
    "zephaniah_count": 0,
    "haggai_count": 0,
    "zechariah_count": 0,
    "malachi_count": 0,
    "first_nephi_count": 0,
    "second_nephi_count": 0,
    "jacob_count": 0,
    "enos_count": 0,
    "jarom_count": 0,
    "omni_count": 0,
    "words_of_mormon_count": 0,
    "mosiah_count": 0,
    "alma_count": 0,
    "helaman_count": 0,
    "third_nephi_count": 0,
    "fourth_nephi_count": 0,
    "book_of_mormon_count": 0,
    "mormon_count": 0,
    "ether_count": 0,
    "moroni_count": 0,
    "new_testament_count": 0, 
    "matthew_count": 0,
    "mark_count": 0,
    "luke_count": 0,
    "john_count": 0,
    "acts_count": 0,
    "romans_count": 0,
    "first_corinthians_count": 0,
    "second_corinthians_count": 0,
    "galatians_count": 0,
    "ephesians_count": 0,
    "philippians_count": 0,
    "colossians_count": 0,
    "first_thessalonians_count": 0,
    "second_thessalonians_count": 0,
    "first_timothy_count": 0,
    "second_timothy_count": 0,
    "titus_count": 0,
    "philemon_count": 0,
    "hebrews_count": 0,
    "james_count": 0,
    "first_peter_count": 0,
    "second_peter_count": 0,
    "first_john_count": 0,
    "second_john_count": 0,
    "third_john_count": 0,
    "jude_count": 0,
    "revelation_count": 0,
    "doctrine_and_covenants_count": 0,
    "moses_count": 0,
    "abraham_count": 0,
    "facsimile_count": 0,
    "joseph_smith_matthew_count": 0,
    "joseph_smith_history_count": 0,
    "articles_of_faith_count": 0,
    "joseph_smith_translation_count": 0,
    "ten_commandments_count": 0,
    "title_page_of_the_book_of_mormon_count": 0,
    "testimony_of_the_twelve_apostles_from_the_book_of_mormon_count": 0
    }
matches_list = []




def prematch_preparation(row):
            matches_list = []
            #print("Row: " + str(row))
            scriptures_value = row.get('scriptures', "Unkown scripture")
            #numbers_value = row.get('numbers', "Unkown numbers")
            #print("scripture value "+str(scriptures_value))
            scriptures_value = scriptures_value.strip()
            if "," in scriptures_value:
                scriptures_value_list = scriptures_value.split(",")
                for scripture_value in scriptures_value_list:
                    scripture_value = scripture_value.strip()
                    #print(scripture_value)
                    for pattern in patterns:
                        matches = re.fullmatch(pattern, scripture_value)
                        if matches:
                            matches_list.append(scripture_value)
            else:
                for pattern in patterns:
                    matches = re.fullmatch(pattern, scriptures_value)
                    if matches:
                        matches_list.append(scriptures_value)
            #print("Matches List:" + str(matches_list))
            return matches_list

#def match(match):


def main_function():

    from_1_to_10_list_saved = []
    from_10_to_20_list_saved = []
    from_20_to_30_list_saved = []
    from_30_to_40_list_saved = []
    from_40_to_200_list_saved = []

    pattern_genesis = r'Gen(?:esis|.) (\d+)'
    #pattern_genesis = r'Genesis (\d+)|Gen. (\d+)'
    pattern_exodus = r'Ex(?:odus|.) (\d+)'
    #pattern_exodus = r'Exodus (\d+)|Ex. (\d+)'
    #pattern_leviticus = r'Leviticus (\d+)|Lev. (\d+)'
    pattern_leviticus = r'Lev(?:iticus|.) (\d+)'
    #pattern_numbers = r'Numbers (\d+)|Num. (\d+)'
    pattern_numbers = r'Num(?:bers|.) (\d+)'
    pattern_deuteronomy = r'Deuteronomy (\d+)'
    #pattern_joshua = r'Joshua (\d+)|Josh. (\d+)'
    pattern_joshua = r'Josh(?:ua|.) (\d+)'
    #pattern_judges = r'Judges (\d+)|Judg. (\d+)'
    pattern_judges = r'Judg(?:es|.) (\d+)'
    #pattern_ruth = r'Ruth (\d+)|Rut. (\d+)'
    pattern_ruth = r'Rut(?:h|.) (\d+)'
    #pattern_first_samuel = r'1 Samuel (\d+)|1 Sam. (\d+)'
    pattern_first_samuel = r'1 Sam(?:uel|.) (\d+)'
    #pattern_second_samuel = r'2 Samuel (\d+)|2 Sam. (\d+)'
    pattern_second_samuel = r'2 Sam(?:uel|.) (\d+)'
    pattern_first_kings = r'1 Kings (\d+)'
    pattern_second_kings = r'2 Kings (\d+)'
    #pattern_first_chronicles = r'1 Chronicles (\d+)|1 Chr. (\d+)'
    pattern_first_chronicles = r'1 Chr(?:onicles|.) (\d+)'
    #pattern_second_chronicles = r'2 Chronicles (\d+)|2 Chr. (\d+)'
    pattern_second_chronicles = r'2 Chr(?:onicles|.) (\d+)'
    pattern_ezra = r'Ezra (\d+)'
    #pattern_nehemiah = r'Nehemiah (\d+)|Neh. (\d+)'
    pattern_nehemiah = r'Neh(?:emiah|.) (\d+)'
    pattern_esther = r'Esther (\d+)'
    pattern_job = r'Job (\d+)'
    #pattern_psalms = r'Psalms (\d+)|Ps. (\d+)'
    pattern_psalms = r'Ps(?:alms|.) (\d+)'
    #pattern_proverbs = r'Proverbs (\d+)|Prov. (\d+)'
    pattern_proverbs = r'Prov(?:erbs|.) (\d+)'
    pattern_ecclesiastes = r'Ecclesiastes (\d+)'
    #pattern_song_of_solomon = r'Song of Solomon (\d+)|Song. (\d+)'
    pattern_song_of_solomon = r'Song(?: of Solomon|.) (\d+)'
    pattern_isaiah = r'Isa(?:iah|.) (\d+)'
    #pattern_isaiah = r'Isaiah (\d+)|Isa. (\d+)'
    pattern_jeremiah = r'Jer(?:emiah|.) (\d+)'
    #pattern_jeremiah = r'Jeremiah (\d+)|Jer. (\d+)'
    pattern_lamentation = r'Lam(?:entations|.) (\d+)'
    #pattern_lamentation = r'Lamentations (\d+)|Lam. (\d+)'
    pattern_ezekiel = r'Ezek(?:iel|.) (\d+)'
    #pattern_ezekiel = r'Ezekiel (\d+)|Ezek. (\d+)'
    #pattern_daniel = r'Daniel (\d+)|Dan. (\d+)'
    pattern_daniel = r'Dan(?:iel|.) (\d+)'
    pattern_hosea = r'Hosea (\d+)'
    pattern_joel = r'Joel (\d+)'
    pattern_amos = r'Amos (\d+)'
    pattern_jonah = r'Jonah (\d+)'
    pattern_micah = r'Micah (\d+)'
    pattern_nahum = r'Nah(?:um|.) (\d+)'
    #pattern_nahum = r'Nahum (\d+)|Nah. (\d+)'
    pattern_habakkuk = r'Hab(?:akkuk|.) (\d+)'
    #pattern_habakkuk = r'Habakkuk (\d+)|Hab. (\d+)'
    #pattern_zephaniah = r'Zephaniah (\d+)|Zeph. (\d+)'
    pattern_zephaniah = r'Zeph(?:aniah|.) (\d+)'
    #pattern_haggai = r'Haggai (\d+)|Hag. (\d+)'
    pattern_haggai = r'Hag(?:gai|\.) (\d+)'
    #pattern_zechariah = r'Zechariah (\d+)|Zech. (\d+)'
    pattern_zechariah = r'Zech(?:ariah|.) (\d+)'
    #pattern_malachi = r'Malachi (\d+)|Mal. (\d+)'
    pattern_malachi = r'Mal(?:achi|.) (\d+)'
    #pattern_first_nephi = r'1 Nephi (\d+)|1 Ne. (\d+)'
    pattern_first_nephi = r'1 Ne(?:phi|.) (\d+)'
    #pattern_second_nephi = r'2 Nephi (\d+)|2 Ne. (\d+)'
    pattern_second_nephi = r'2 Ne(?:phi|.) (\d+)'
    pattern_jacob = r'Jacob (\d+)'
    #Words of Mormon is one chapter
    #pattern_words_of_mormon = r'Words of Mormon (\d+)|W of M (\d+)'
    pattern_mosiah = r'Mosiah (\d+)'
    pattern_alma = r'Alma (\d+)'
    #pattern_helaman = r'Helaman (\d+)|Hel. (\d+)'
    pattern_helaman = r'Hel(?:aman|.) (\d+)'
    pattern_third_nephi = r'3 Ne(?:phi|.) (\d+)'
    #pattern_third_nephi = r'3 Nephi (\d+)|3 Ne. (\d+)'
    pattern_mormon = r'Morm. (\d+)'
    pattern_ether = r'Ether (\d+)'
    pattern_moroni = r'Moroni (\d+)'
    pattern_matthew = r'Matt(?:hew|.) (\d+)'
    #pattern_matthew = r'Matthew (\d+)|Matt. (\d+)'
    pattern_mark = r'Mark (\d+)'
    pattern_luke = r'Luke (\d+)'
    pattern_john = r'Gospels of John (\d+)|John (\d+)'
    pattern_acts = r'Acts (\d+)'
    pattern_romans = r'Rom(?:ans|.) (\d+)'
    #pattern_romans = r'Romans (\d+)|Rom. (\d+)'
    #pattern_first_corinthians = r'1 Corinthians (\d+)|1 Cor. (\d+)'
    pattern_first_corinthians = r'1 Cor(?:inthians|.) (\d+)'
    pattern_second_corinthians = r'2 Cor(?:inthians|.) (\d+)'
    #pattern_second_corinthians = r'2 Corinthians (\d+)|2 Cor. (\d+)'
    pattern_galatians = r'Gal(?:atians|.) (\d+)'
    #pattern_galatians = r'Galatians (\d+)|Gal. (\d+)'
    pattern_ephesians = r'Eph(?:esians|.) (\d+)'
    #pattern_ephesians = r'Ephesians (\d+)|Eph. (\d+)'
    #pattern_philippians = r'Philippians (\d+)|Philip. (\d+)'
    pattern_philippians = r'Philip(?:pians|.) (\d+)'
    #pattern_colossians = r'Colossians (\d+)|Col. (\d+)'
    pattern_colossians = r'Col(?:ossians|.) (\d+)'
    #pattern_first_thessalonians = r'1 Thessalonians (\d+)|1 Thes. (\d+)'
    pattern_first_thessalonians = r'1 Thes(?:salonians|.) (\d+)'
    #pattern_second_thessalonians = r'2 Thessalonians (\d+)|2 Thes. (\d+)'
    pattern_second_thessalonians = r'2 Thes(?:salonians|.) (\d+)'
    #pattern_first_timothy = r'1 Timothy (\d+)|1 Tim. (\d+)'
    pattern_first_timothy = r'1 Tim(?:othy|.) (\d+)'
    #pattern_second_timothy = r'2 Timothy (\d+)|2 Tim. (\d+)'
    pattern_second_timothy = r'2 Tim(?:othy|.) (\d+)'
    pattern_titus = r'Titus (\d+)'
    #pattern_hebrews = r'Hebrews (\d+)|Heb. (\d+)'
    pattern_hebrews = r'Heb(?:rews|.) (\d+)'
    pattern_james = r'James (\d+)'
    pattern_first_peter = r'1 Pet(?:er|.) (\d+)'
    #pattern_first_peter = r'1 Peter (\d+)|1 Pet. (\d+)'
    #pattern_second_peter = r'2 Peter (\d+)|2 Pet. (\d+)'
    pattern_second_peter = r'2 Pet(?:er|.) (\d+)'
    pattern_first_john = r'1 J(?:ohn|n.) (\d+)'
    #pattern_first_john = r'1 John (\d+)|1 Jn. (\d+)'
    #pattern_first_john = r'2 Pet(?:er|.) (\d+)'
    #pattern_revelation = r'Revelation (\d+)|Rev. (\d+)'
    pattern_revelation = r'Rev(?:elation|.) (\d+)'
    pattern_doctrine_and_covenants = r'D(?:octrine and Covenants|&C) (\d+)'
    #pattern_doctrine_and_covenants = r'Doctrine and Covenants (\d+)|D&C (\d+)'
    pattern_moses = r'Moses (\d+)'
    #pattern_abraham = r'Abraham (\d+)|Abr. (\d+)'
    pattern_abraham = r'Abr(?:aham|.) (\d+)'
    pattern_facsimile = r'Facsimile (\d+)'
    #pattern_joseph_smith_translation = r'Joseph Smith Translation (\d+)|JST (\d+)'
    pattern_joseph_smith_translation = r'J(?:oseph Smith Translation|JST) (\d+)'
    




    i = 0
    together_filtered_lists = []
    
    
    with open('article_remover.csv', mode='r') as csv_file:
        
        csv_reader = csv.DictReader(csv_file)
        #exodus_count_chapters_total = []
        
        for row in csv_reader:
            numbers_value = row.get('numbers', "Unknown numbers")
            #print("numbers value: "+str(numbers_value))
            
            # from 1 to 10
            galatians_chapter_value_list = []
            ephesians_chapter_value_list = []
            philippians_chapter_value_list = []
            colossians_chapter_value_list = []
            first_thessalonians_chapter_value_list = []
            second_thessalonians_chapter_value_list = []
            first_timothy_chapter_value_list = []
            second_timothy_chapter_value_list = []
            titus_chapter_value_list = []
            james_chapter_value_list = []
            first_peter_chapter_value_list = []
            second_peter_chapter_value_list = []
            first_john_chapter_value_list = []
            ruth_chapter_value_list = []
            ezra_chapter_value_list = []
            esther_chapter_value_list = []
            song_of_solomon_chapter_value_list = []
            lamentations_chapter_value_list = []
            joel_chapter_value_list = []
            amos_chapter_value_list = []
            jonah_chapter_value_list = []
            micah_chapter_value_list = []
            nahum_chapter_value_list = []
            habakkuk_chapter_value_list = []
            zephaniah_chapter_value_list = []
            haggai_chapter_value_list = []
            malachi_chapter_value_list = []
            jacob_chapter_value_list = []
            mormon_chapter_value_list = []
            moroni_chapter_value_list = []
            moses_chapter_value_list = []
            abraham_chapter_value_list = []
            facsimile_chapter_value_list = []
            joseph_smith_translation_chapter_value_list = []

            # from 10 to 20
            mark_chapter_value_list = []
            romans_chapter_value_list = []
            first_corinthians_chapter_value_list = []
            second_corinthians_chapter_value_list = []
            hebrews_chapter_value_list = []
            nehemiah_chapter_value_list = []
            ecclesiastes_chapter_value_list = []
            daniel_chapter_value_list = []
            hosea_chapter_value_list = []
            zechariah_chapter_value_list = []
            helaman_chapter_value_list = []
            ether_chapter_value_list = []


            # from 20 to 30
            matthew_chapter_value_list = []
            luke_chapter_value_list = []
            john_chapter_value_list = []
            acts_chapter_value_list = []
            revelation_chapter_value_list = []
            leviticus_chapter_value_list = []
            joshua_chapter_value_list = []
            judges_chapter_value_list = []
            second_samuel_chapter_value_list = []
            first_kings_chapter_value_list = []
            second_kings_chapter_value_list = []
            first_chronicles_chapter_value_list = []
            first_nephi_chapter_value_list = []
            mosiah_chapter_value_list = []
            third_nephi_chapter_value_list = []


            # from 30 to 40
            exodus_chapter_value_list = []
            numbers_chapter_value_list = []
            deuteronomy_chapter_value_list = []
            first_samuel_chapter_value_list = []
            second_chronicles_chapter_value_list = []
            proverbs_chapter_value_list = []
            second_nephi_chapter_value_list = []

            # from 40 to 200
            genesis_chapter_value_list = []
            job_chapter_value_list = []
            psalms_chapter_value_list = []
            isaiah_chapter_value_list = []
            jeremiah_chapter_value_list = []
            ezekiel_chapter_value_list = []
            alma_chapter_value_list = []
            doctrine_and_covenants_chapter_value_list = []



            from_1_to_10_name_list_small = []
            from_10_to_20_name_list_small = []
            from_20_to_30_name_list_small = []
            from_30_to_40_name_list_small = []
            from_40_to_200_name_list_small = []
            
            #print(row)
            matches_list = []
            matches_list = prematch_preparation(row)
            #print("Rows List: " + str(row))
            #print("Matches List: " + str(matches_list))
            #print("")

            #1 to 10 counter chapters row
            galatians_counter_chapters_row = 0
            ephesians_counter_chapters_row = 0
            philippians_counter_chapters_row = 0
            colossians_counter_chapters_row = 0
            first_thessalonians_counter_chapters_row = 0
            second_thessalonians_counter_chapters_row = 0
            first_timothy_counter_chapters_row = 0
            second_timothy_counter_chapters_row = 0
            titus_counter_chapters_row = 0
            james_counter_chapters_row = 0
            first_peter_counter_chapters_row = 0
            second_peter_counter_chapters_row = 0
            first_john_counter_chapters_row = 0
            third_john_counter_chapters_row = 0
            ruth_counter_chapters_row = 0
            ezra_counter_chapters_row = 0
            esther_counter_chapters_row = 0
            song_of_solomon_counter_chapters_row = 0
            lamentations_counter_chapters_row = 0
            joel_counter_chapters_row = 0
            amos_counter_chapters_row = 0
            jonah_counter_chapters_row = 0
            micah_counter_chapters_row = 0
            nahum_counter_chapters_row = 0
            habakkuk_counter_chapters_row = 0
            zephaniah_counter_chapters_row = 0
            haggai_counter_chapters_row = 0
            malachi_counter_chapters_row = 0
            jacob_counter_chapters_row = 0
            mormon_counter_chapters_row = 0
            moroni_counter_chapters_row = 0
            moses_counter_chapters_row = 0
            abraham_counter_chapters_row = 0
            facsimile_counter_chapters_row = 0
            joseph_smith_translation_counter_chapters_row = 0

            #10 to 20 counter chapters row
            mark_counter_chapters_row = 0
            romans_counter_chapters_row = 0
            first_corinthians_counter_chapters_row = 0
            second_corinthians_counter_chapters_row = 0
            second_corinthians_counter_chapters_row = 0
            hebrews_counter_chapters_row = 0
            nehemiah_counter_chapters_row = 0
            ecclesiastes_counter_chapters_row = 0
            daniel_counter_chapters_row = 0
            hosea_counter_chapters_row = 0
            zechariah_counter_chapters_row = 0
            helaman_counter_chapters_row = 0
            ether_counter_chapters_row = 0


            #20 to 30 counter chapters row
            matthew_counter_chapters_row = 0
            luke_counter_chapters_row = 0
            john_counter_chapters_row = 0
            acts_counter_chapters_row = 0
            revelation_counter_chapters_row = 0
            leviticus_counter_chapters_row = 0
            joshua_counter_chapters_row = 0
            judges_counter_chapters_row = 0
            second_samuel_counter_chapters_row = 0
            first_kings_counter_chapters_row = 0
            second_kings_counter_chapters_row = 0
            first_chronicles_counter_chapters_row = 0
            first_nephi_counter_chapters_row = 0
            mosiah_counter_chapters_row = 0
            third_nephi_counter_chapters_row = 0

            
            #30 to 40 counter chapters row
            exodus_counter_chapters_row = 0
            numbers_counter_chapters_row = 0
            deuteronomy_counter_chapters_row = 0
            first_samuel_counter_chapters_row = 0
            second_chronicles_counter_chapters_row = 0
            proverbs_counter_chapters_row = 0
            second_nephi_counter_chapters_row = 0

            #40 to 200 counter chapters row
            genesis_counter_chapters_row = 0
            job_counter_chapters_row = 0
            psalms_counter_chapters_row = 0
            isaiah_counter_chapters_row = 0
            jeremiah_counter_chapters_row = 0
            ezekiel_counter_chapters_row = 0
            alma_counter_chapters_row = 0
            doctrine_and_covenants_counter_chapters_row = 0

            
            for match in matches_list:
                from_1_to_10_name_dictionary = {}
                from_10_to_20_name_dictionary = {}
                from_20_to_30_name_dictionary = {}
                from_30_to_40_name_dictionary = {}
                from_40_to_200_name_dictionary = {}
                #print(match)


                match_genesis = re.fullmatch(pattern_genesis, match)
                match_exodus = re.fullmatch(pattern_exodus, match)
                match_leviticus = re.fullmatch(pattern_leviticus, match)
                match_numbers = re.fullmatch(pattern_numbers, match)
                match_deuteronomy = re.fullmatch(pattern_deuteronomy, match)
                match_joshua = re.fullmatch(pattern_joshua, match)
                match_judges = re.fullmatch(pattern_judges, match)
                match_ruth = re.fullmatch(pattern_ruth, match)
                match_first_samuel = re.fullmatch(pattern_first_samuel, match)
                match_second_samuel = re.fullmatch(pattern_second_samuel, match)
                match_first_kings = re.fullmatch(pattern_first_kings, match)
                match_second_kings = re.fullmatch(pattern_second_kings, match)
                match_first_chronicles = re.fullmatch(pattern_first_chronicles, match)
                match_second_chronicles = re.fullmatch(pattern_second_chronicles, match)
                match_ezra = re.fullmatch(pattern_ezra, match)
                match_nehemiah = re.fullmatch(pattern_nehemiah, match)
                match_esther = re.fullmatch(pattern_esther, match)
                match_job = re.fullmatch(pattern_job, match)
                match_psalms = re.fullmatch(pattern_psalms, match)
                match_proverbs = re.fullmatch(pattern_proverbs, match)
                match_ecclesiastes = re.fullmatch(pattern_ecclesiastes, match)
                match_song_of_solomon = re.fullmatch(pattern_song_of_solomon, match)
                match_isaiah = re.fullmatch(pattern_isaiah, match)
                match_jeremiah = re.fullmatch(pattern_jeremiah, match)
                match_lamentations = re.fullmatch(pattern_lamentation, match)
                match_ezekiel = re.fullmatch(pattern_ezekiel, match)
                match_daniel = re.fullmatch(pattern_daniel, match)
                match_hosea = re.fullmatch(pattern_hosea, match)
                match_joel = re.fullmatch(pattern_joel, match)
                match_amos = re.fullmatch(pattern_amos, match)
                match_jonah = re.fullmatch(pattern_jonah, match)
                match_micah = re.fullmatch(pattern_micah, match)
                match_nahum = re.fullmatch(pattern_nahum, match)
                match_habakkuk = re.fullmatch(pattern_habakkuk, match)
                match_zephaniah = re.fullmatch(pattern_zephaniah, match)
                match_haggai = re.fullmatch(pattern_haggai, match)
                match_zechariah = re.fullmatch(pattern_zechariah, match)
                match_malachi = re.fullmatch(pattern_malachi, match)
                match_first_nephi = re.fullmatch(pattern_first_nephi, match)
                match_second_nephi = re.fullmatch(pattern_second_nephi, match)
                match_jacob = re.fullmatch(pattern_jacob, match)
                #Not needed only one chapter in mormon
                #match_words_of_mormon = re.fullmatch(pattern_words_of_mormon, match)
                match_mosiah = re.fullmatch(pattern_mosiah, match)
                match_alma = re.fullmatch(pattern_alma, match)
                match_helaman = re.fullmatch(pattern_helaman, match)
                match_third_nephi = re.fullmatch(pattern_third_nephi, match)
                match_mormon = re.fullmatch(pattern_mormon, match)
                match_ether = re.fullmatch(pattern_ether, match)
                match_moroni = re.fullmatch(pattern_moroni, match)
                match_matthew = re.fullmatch(pattern_matthew, match)
                match_mark = re.fullmatch(pattern_mark, match)
                match_luke = re.fullmatch(pattern_luke, match)
                match_john = re.fullmatch(pattern_john, match)
                match_acts = re.fullmatch(pattern_acts, match)
                match_romans = re.fullmatch(pattern_romans, match)
                match_first_corinthians = re.fullmatch(pattern_first_corinthians, match)
                match_second_corinthians = re.fullmatch(pattern_second_corinthians, match)
                match_galatians = re.fullmatch(pattern_galatians, match)
                match_ephesians = re.fullmatch(pattern_ephesians, match)
                match_philippians = re.fullmatch(pattern_philippians, match)
                match_colossians = re.fullmatch(pattern_colossians, match)
                match_first_thessalonians = re.fullmatch(pattern_first_thessalonians, match)
                match_second_thessalonians = re.fullmatch(pattern_second_thessalonians, match)
                match_first_timothy = re.fullmatch(pattern_first_timothy, match)
                match_second_timothy = re.fullmatch(pattern_second_timothy, match)
                match_titus = re.fullmatch(pattern_titus, match)
                match_hebrews = re.fullmatch(pattern_hebrews, match)
                match_james = re.fullmatch(pattern_james, match)
                match_first_peter = re.fullmatch(pattern_first_peter, match)
                match_second_peter = re.fullmatch(pattern_second_peter, match)
                match_first_john = re.fullmatch(pattern_first_john, match)
                match_revelation = re.fullmatch(pattern_revelation, match)
                match_doctrine_and_covenants = re.fullmatch(pattern_doctrine_and_covenants, match)
                match_moses = re.fullmatch(pattern_moses, match)
                match_abraham = re.fullmatch(pattern_abraham, match)
                match_facsimile = re.fullmatch(pattern_facsimile, match)
                match_joseph_smith_translation = re.fullmatch(pattern_joseph_smith_translation, match)
 

                #match()
                #print(match)
                #print(counts["ruth_count"])
                if match == "Bible":
                    counts["bible_count"]+=1
                    #print("Bible Counts:"+ str(counts["bible_count"]))
                if match == "Old Testament":
                    counts["old_testament_count"]+=1
                    #print("Old Testament Counts:"+ str(counts["old_testament_count"]))

                #Genesis
                genesis_chapter = ""
                genesis_count_chapters = None
                if match == "Genesis" or match == "Gen.":
                    counts["genesis_count"]+=1
                    genesis_counter_chapters_row += 1
                if match_genesis:
                    counts["genesis_count_"+str(match_genesis.group(1))] = 0
                    if "genesis_count_"+str(match_genesis.group(1)) not in counts:
                        counts["genesis_count_"+str(match_genesis.group(1))] = 1
                        genesis_counter_chapters_row = 1
                    else:
                        counts["genesis_count_"+str(match_genesis.group(1))] += 1
                        genesis_counter_chapters_row += 1
                    genesis_chapter = str(match_genesis.group(1))
                    genesis_count_chapters = counts["genesis_count_"+str(match_genesis.group(1))]
                


                #Exodus
                exodus_chapter = ""
                exodus_count_chapters = None
                if match == "Exodus" or match == "Ex.":
                    counts["exodus_count"]+=1
                    exodus_counter_chapters_row += 1
                if match_exodus:
                    counts["exodus_count_"+str(match_exodus.group(1))] = 0
                    if "exodus_count_"+str(match_exodus.group(1)) not in counts:
                        counts["exodus_count_"+str(match_exodus.group(1))] = 1
                        exodus_counter_chapters_row = 1
                    else:
                        counts["exodus_count_"+str(match_exodus.group(1))] += 1
                        exodus_counter_chapters_row += 1   
                    exodus_chapter = str(match_exodus.group(1))
                    exodus_count_chapters = counts["exodus_count_"+str(match_exodus.group(1))]



                if match_exodus == False:
                    counts["exodus_count_"+str(match_exodus.group(1))] = 0
                
                #Leviticus
                leviticus_chapter = ""
                leviticus_count_chapters = None
                if match == "Leviticus" or match == "Lev.":
                   counts["leviticus_count"]+=1
                   leviticus_counter_chapters_row += 1
                if match_leviticus:
                    if "leviticus_count_"+str(match_leviticus.group(1)) not in counts:
                        counts["leviticus_count_"+str(match_leviticus.group(1))] = 1
                        leviticus_counter_chapters_row = 1
                    else:
                        counts["leviticus_count_"+str(match_leviticus.group(1))] += 1
                        leviticus_counter_chapters_row += 1
                    leviticus_chapter = str(match_leviticus.group(1))
                    leviticus_count_chapters = counts["leviticus_count_"+str(match_leviticus.group(1))]


                #Numbers    
                numbers_chapter = ""
                numbers_count_chapters = None
                if match == "Numbers" or match == "Num.":
                    counts["numbers_count"]+=1
                    numbers_counter_chapters_row += 1
                if match_numbers:
                    if "numbers_count_"+str(match_numbers.group(1)) not in counts:
                        counts["numbers_count_"+str(match_numbers.group(1))] = 1
                        numbers_counter_chapters_row = 1
                    else:
                        counts["numbers_count_"+str(match_numbers.group(1))] += 1
                        numbers_counter_chapters_row += 1
                    numbers_chapter = str(match_numbers.group(1))
                    numbers_count_chapters = counts["numbers_count_"+str(match_numbers.group(1))]

                #Deuteronomy
                deuteronomy_chapter = ""
                deuteronomy_count_chapters = None
                if match == "Deuteronomy":
                    counts["deuteronomy_count"]+=1
                    deuteronomy_counter_chapters_row += 1
                if match_deuteronomy:
                    counts["deuteronomy_count_"+str(match_deuteronomy.group(1))] = 0
                    if "deuteronomy_count_"+str(match_deuteronomy.group(1)) not in counts:
                        counts["deuteronomy_count_"+str(match_deuteronomy.group(1))] = 1
                        deuteronomy_counter_chapters_row = 1
                    else:
                        counts["deuteronomy_count_"+str(match_deuteronomy.group(1))] += 1
                        deuteronomy_counter_chapters_row += 1
                    deuteronomy_chapter = str(match_deuteronomy.group(1))
                    deuteronomy_count_chapters = counts["deuteronomy_count_"+str(match_deuteronomy.group(1))]
                
                
                
                #Joshua
                joshua_chapter = ""
                joshua_count_chapters = None
                if match == "Joshua" or match == "Josh.":
                    counts["joshua_count"]+=1
                    joshua_counter_chapters_row += 1
                if match_joshua:
                    counts["joshua_count_"+str(match_joshua.group(1))] = 0
                    if "joshua_count_"+str(match_joshua.group(1)) not in counts:
                        counts["joshua_count_"+str(match_joshua.group(1))] = 1
                        joshua_counter_chapters_row = 1
                    else:
                        counts["joshua_count_"+str(match_joshua.group(1))] += 1
                        joshua_counter_chapters_row += 1
                    joshua_chapter = str(match_joshua.group(1))
                    joshua_count_chapters = counts["joshua_count_"+str(match_joshua.group(1))]
                    #print("Joshua Counts:"+ str(counts["joshua_count"]))


                #Judges
                judges_chapter = ""
                judges_count_chapters = None
                if match == "Judges" or match == "Judg.":
                    counts["judges_count"]+=1
                    judges_counter_chapters_row += 1
                if match_judges:
                    counts["judges_count_"+str(match_judges.group(1))] = 0
                    if "judges_count_"+str(match_judges.group(1)) not in counts:
                        counts["judges_count_"+str(match_judges.group(1))] = 1
                        judges_counter_chapters_row = 1
                    else:
                        counts["judges_count_"+str(match_judges.group(1))] += 1
                        judges_counter_chapters_row += 1
                    judges_chapter = str(match_judges.group(1))
                    judges_count_chapters = counts["judges_count_"+str(match_judges.group(1))]
                    #print("Judges Counts:"+ str(counts["judges_count"]))



                #Ruth
                ruth_chapter = ""
                ruth_count_chapters = None
                if match == "Ruth" or match == "Rut.":
                    counts["ruth_count"]+=1
                    ruth_counter_chapters_row += 1
                if match_ruth:
                    counts["ruth_count_"+str(match_ruth.group(1))] = 0
                    if "ruth_count_"+str(match_ruth.group(1)) not in counts:
                        counts["ruth_count_"+str(match_ruth.group(1))] = 1
                        ruth_counter_chapters_row = 1
                    else:
                        counts["ruth_count_"+str(match_ruth.group(1))] += 1
                        ruth_counter_chapters_row += 1
                    ruth_chapter = str(match_ruth.group(1))
                    ruth_count_chapters = counts["ruth_count_"+str(match_ruth.group(1))]
                    #print("Ruth Counts:"+ str(counts["ruth_count"]))

                
                #First Samuel
                first_samuel_chapter = ""
                first_samuel_count_chapters = None
                if match == "1 Samuel" or match == "1 Sam.":
                    counts["first_samuel_count"]+=1
                    first_samuel_counter_chapters_row += 1
                if match_first_samuel:
                    if "first_samuel_count_"+str(match_first_samuel.group(1)) not in counts:
                        counts["first_samuel_count_"+str(match_first_samuel.group(1))] = 1
                        first_samuel_counter_chapters_row = 1
                    else:
                        counts["first_samuel_count_"+str(match_first_samuel.group(1))] += 1
                        first_samuel_counter_chapters_row += 1
                    first_samuel_chapter = str(match_first_samuel.group(1))
                    first_samuel_count_chapters = counts["first_samuel_count_"+str(match_first_samuel.group(1))]
                    #print("1 Samuel Counts:"+ str(counts["first_samuel_count"]))
                
                
                #Second Samuel
                second_samuel_chapter = ""
                second_samuel_count_chapters = None
                if match == "2 Samuel" or match == "2 Sam.":
                    counts["second_samuel_count"]+=1
                    second_samuel_counter_chapters_row += 1
                if match_second_samuel:
                    counts["second_samuel_count_"+str(match_second_samuel.group(1))] = 0
                    if "second_samuel_count_"+str(match_second_samuel.group(1)) not in counts:
                        counts["second_samuel_count_"+str(match_second_samuel.group(1))] = 1
                        second_samuel_counter_chapters_row = 1
                    else:
                        counts["second_samuel_count_"+str(match_second_samuel.group(1))] += 1
                        second_samuel_counter_chapters_row += 1
                    second_samuel_chapter = str(match_second_samuel.group(1))
                    second_samuel_count_chapters = counts["second_samuel_count_"+str(match_second_samuel.group(1))]
                    #print("2 Samuel Counts:"+ str(counts["second_samuel_count"]))
                
                
                
                #First Kings
                first_kings_chapter = ""
                first_kings_count_chapters = None
                if match == "1 Kings":
                    counts["first_kings_count"]+=1
                    first_kings_counter_chapters_row += 1
                if match_first_kings:
                    counts["first_kings_count_"+str(match_first_kings.group(1))] = 0
                    if "first_kings_count_"+str(match_first_kings.group(1)) not in counts:
                        counts["first_kings_count_"+str(match_first_kings.group(1))] = 1
                        first_kings_counter_chapters_row = 1
                    else:
                        counts["first_kings_count_"+str(match_first_kings.group(1))] += 1
                        first_kings_counter_chapters_row += 1
                    first_kings_chapter = str(match_first_kings.group(1))
                    first_kings_count_chapters = counts["first_kings_count_"+str(match_first_kings.group(1))]
                    #print("1 Kings Counts:"+ str(counts["first_kings_count"]))


                #Second Kings
                second_kings_chapter = ""
                second_kings_count_chapters = None
                if match == "2 Kings":
                    counts["second_kings_count"]+=1
                    second_kings_counter_chapters_row += 1
                if match_second_kings:
                    if "second_kings_count_"+str(match_second_kings.group(1)) not in counts:
                        counts["second_kings_count_"+str(match_second_kings.group(1))] = 1
                        second_kings_counter_chapters_row = 1
                    else:
                        counts["second_kings_count_"+str(match_second_kings.group(1))] += 1
                        second_kings_counter_chapters_row += 1
                    second_kings_chapter = str(match_second_kings.group(1))
                    second_kings_count_chapters = counts["second_kings_count_"+str(match_second_kings.group(1))]
                    #print("2 Kings Counts:"+ str(counts["second_kings_count"]))
                
                
                #First Chronicles
                first_chronicles_chapter = ""
                first_chronicles_count_chapters = None
                if match == "1 Chronicles" or match == "1 Chr.":
                    counts["first_chronicles_count"]+=1
                    first_chronicles_counter_chapters_row += 1
                if match_first_chronicles:
                    counts["first_chronicles_count_"+str(match_first_chronicles.group(1))] = 0
                    if "first_chronicles_count_"+str(match_first_chronicles.group(1)) not in counts:
                        counts["first_chronicles_count_"+str(match_first_chronicles.group(1))] = 1
                        first_chronicles_counter_chapters_row = 1
                    else:
                        counts["first_chronicles_count_"+str(match_first_chronicles.group(1))] += 1
                        first_chronicles_counter_chapters_row += 1
                    first_chronicles_chapter = str(match_first_chronicles.group(1))
                    first_chronicles_count_chapters = counts["first_chronicles_count_"+str(match_first_chronicles.group(1))]
                    #print("1 Chronicles Counts:"+ str(counts["first_chronicles_count"]))
                
                
                #Second Chronicles
                second_chronicles_chapter = ""
                second_chronicles_count_chapters = None
                if match == "2 Chronicles" or match == "2 Chr.":
                   counts["second_chronicles_count"]+=1
                   second_chronicles_counter_chapters_row += 1
                if match_second_chronicles:
                    counts["second_chronicles_count_"+str(match_second_chronicles.group(1))] = 0
                    if "second_chronicles_count_"+str(match_second_chronicles.group(1)) not in counts:
                        counts["second_chronicles_count_"+str(match_second_chronicles.group(1))] = 1
                        second_chronicles_counter_chapters_row = 1
                    else:
                        counts["second_chronicles_count_"+str(match_second_chronicles.group(1))] += 1
                        second_chronicles_counter_chapters_row += 1
                    second_chronicles_chapter = str(match_second_chronicles.group(1))
                    second_chronicles_count_chapters = counts["second_chronicles_count_"+str(match_second_chronicles.group(1))]
                
                
                #Ezra
                ezra_chapter = ""
                ezra_count_chapters = None
                if match == "Ezra":
                    counts["ezra_count"]+=1
                    ezra_counter_chapters_row += 1
                if match_ezra:
                    counts["ezra_count_"+str(match_ezra.group(1))] = 0
                    if "ezra_count_"+str(match_ezra.group(1)) not in counts:
                        counts["ezra_count_"+str(match_ezra.group(1))] = 1
                        ezra_counter_chapters_row = 1
                    else:
                        counts["ezra_count_"+str(match_ezra.group(1))] += 1
                        ezra_counter_chapters_row += 1
                    ezra_chapter = str(match_ezra.group(1))
                    ezra_count_chapters = counts["ezra_count_"+str(match_ezra.group(1))]
                    #print("Ezra Counts:"+ str(counts["ezra_count"]))

                
                #Nehemiah
                nehemiah_chapter = ""
                nehemiah_count_chapters = None
                if match == "Nehemiah" or match == "Neh.":
                    counts["nehemiah_count"]+=1
                    nehemiah_counter_chapters_row += 1
                if match_nehemiah:
                    counts["nehemiah_count_"+str(match_nehemiah.group(1))] = 0
                    if "nehemiah_count_"+str(match_nehemiah.group(1)) not in counts:
                        counts["nehemiah_count_"+str(match_nehemiah.group(1))] = 1
                        nehemiah_counter_chapters_row = 1
                    else:
                        counts["nehemiah_count_"+str(match_nehemiah.group(1))] += 1
                        nehemiah_counter_chapters_row += 1
                    nehemiah_chapter = str(match_nehemiah.group(1))
                    nehemiah_count_chapters = counts["nehemiah_count_"+str(match_nehemiah.group(1))]
                    #print("Nehemiah Counts:"+str(nehemiah_count_chapters))
                    #print("Nehemiah Counts Rows:"+str(nehemiah_counter_chapters_row))
                

                #Esther
                esther_chapter = ""
                esther_count_chapters = None
                if match == "Esther":
                    counts["esther_count"]+=1
                    esther_counter_chapters_row += 1
                if match_esther:
                    counts["esther_count_"+str(match_esther.group(1))] = 0
                    if "esther_count_"+str(match_esther.group(1)) not in counts:
                        counts["esther_count_"+str(match_esther.group(1))] = 1
                        esther_counter_chapters_row = 1
                    else:
                        counts["esther_count_"+str(match_esther.group(1))] += 1
                        esther_counter_chapters_row += 1
                    esther_chapter = str(match_esther.group(1))
                    esther_count_chapters = counts["esther_count_"+str(match_esther.group(1))]
                    #print("Esther Counts:"+ str(counts["esther_count"]))

                
                #Job
                job_chapter = ""
                job_count_chapters = None
                if match == "Job":
                    counts["job_count"]+=1
                    job_counter_chapters_row += 1
                if match_job:
                    counts["job_count_"+str(match_job.group(1))] = 0
                    if "job_count_"+str(match_job.group(1)) not in counts:
                        counts["job_count_"+str(match_job.group(1))] = 1
                        job_counter_chapters_row = 1
                    else:
                        counts["job_count_"+str(match_job.group(1))] += 1
                        job_counter_chapters_row += 1
                    job_chapter = str(match_job.group(1))
                    job_count_chapters = counts["job_count_"+str(match_job.group(1))]
                    #print("Job Counts:"+ str(counts["job_count"]))
            

                #Psalms
                psalms_chapter = ""
                psalms_count_chapters = None
                if match == "Psalms" or match == "Ps.":
                    counts["psalms_count"]+=1
                    psalms_counter_chapters_row += 1
                if match_psalms:
                    counts["psalms_count_"+str(match_psalms.group(1))] = 0
                    if "psalms_count_"+str(match_psalms.group(1)) not in counts:
                        counts["psalms_count_"+str(match_psalms.group(1))] = 1
                        psalms_counter_chapters_row = 1
                    else:
                        counts["psalms_count_"+str(match_psalms.group(1))] += 1
                        psalms_counter_chapters_row += 1
                    psalms_chapter = str(match_psalms.group(1))
                    psalms_count_chapters = counts["psalms_count_"+str(match_psalms.group(1))]
                    #print("Psalms Counts:"+ str(counts["psalms_count"]))
                
                #Proverbs
                proverbs_chapter = ""
                proverbs_count_chapters = None
                if match == "Proverbs" or match == "Prov.":
                    counts["proverbs_count"]+=1
                    proverbs_counter_chapters_row += 1
                if match_proverbs:
                    counts["proverbs_count_"+str(match_proverbs.group(1))] = 0
                    if "proverbs_count_"+str(match_proverbs.group(1)) not in counts:
                        counts["proverbs_count_"+str(match_proverbs.group(1))] = 1
                        proverbs_counter_chapters_row = 1
                    else:
                        counts["proverbs_count_"+str(match_proverbs.group(1))] += 1
                        proverbs_counter_chapters_row += 1
                    proverbs_chapter = str(match_proverbs.group(1))
                    proverbs_count_chapters = counts["proverbs_count_"+str(match_proverbs.group(1))]

                #Ecclesiastes
                ecclesiastes_chapter = ""
                ecclesiastes_count_chapters = None
                if match == "Ecclesiastes":
                    counts["ecclesiastes_count"]+=1
                    ecclesiastes_counter_chapters_row += 1
                if match_ecclesiastes:
                    counts["ecclesiastes_count_"+str(match_ecclesiastes.group(1))] = 0
                    if "ecclesiastes_count_"+str(match_ecclesiastes.group(1)) not in counts:
                        counts["ecclesiastes_count_"+str(match_ecclesiastes.group(1))] = 1
                        ecclesiastes_counter_chapters_row = 1
                    else:
                        counts["ecclesiastes_count_"+str(match_ecclesiastes.group(1))] += 1
                        ecclesiastes_counter_chapters_row += 1
                    ecclesiastes_count_chapters = counts["ecclesiastes_count_"+str(match_ecclesiastes.group(1))]
                    ecclesiastes_chapter = str(match_ecclesiastes.group(1))
                    #print("Ecclesiastes Counts Rows:"+str(ecclesiastes_counter_chapters_row))


                #Song of Solomon
                song_of_solomon_chapter = ""
                song_of_solomon_count_chapters = None
                if match == "Song of Solomon" or match == "Song.":
                    counts["song_of_solomon_count"]+=1
                    song_of_solomon_counter_chapters_row += 1
                if match_song_of_solomon:
                    counts["song_of_solomon_count_"+str(match_song_of_solomon.group(1))] = 0
                    if "song_of_solomon_count_"+str(match_song_of_solomon.group(1)) not in counts:
                        counts["song_of_solomon_count_"+str(match_song_of_solomon.group(1))] = 1
                        song_of_solomon_counter_chapters_row = 1
                    else:
                        counts["song_of_solomon_count_"+str(match_song_of_solomon.group(1))] += 1
                        song_of_solomon_counter_chapters_row += 1
                    song_of_solomon_chapter = str(match_song_of_solomon.group(1))
                    song_of_solomon_count_chapters = counts["song_of_solomon_count_"+str(match_song_of_solomon.group(1))]
                    #print("Song of Solomon Counts:"+ str(counts["song_of_solomon_count"]))
                
                #Isaiah
                isaiah_chapter = ""
                isaiah_count_chapters = None
                if match == "Isaiah" or match == "Isa.":
                    counts["isaiah_count"]+=1
                    isaiah_counter_chapters_row += 1
                if match_isaiah:
                    counts["isaiah_count_"+str(match_isaiah.group(1))] = 0
                    if "isaiah_count_"+str(match_isaiah.group(1)) not in counts:
                        counts["isaiah_count_"+str(match_isaiah.group(1))] = 1
                        isaiah_counter_chapters_row = 1
                    else:
                        counts["isaiah_count_"+str(match_isaiah.group(1))] += 1
                        isaiah_counter_chapters_row += 1
                    isaiah_chapter = str(match_isaiah.group(1))
                    isaiah_count_chapters = counts["isaiah_count_"+str(match_isaiah.group(1))]
                        
                #Jeremiah
                jeremiah_chapter = ""
                jeremiah_count_chapters = None
                if match == "Jeremiah" or match == "Jer.":
                    counts["jeremiah_count"]+=1
                    jeremiah_counter_chapters_row += 1
                if match_jeremiah:
                    counts["jeremiah_count_"+str(match_jeremiah.group(1))] = 0
                    if "jeremiah_count_"+str(match_jeremiah.group(1)) not in counts:
                        counts["jeremiah_count_"+str(match_jeremiah.group(1))] = 1
                        jeremiah_counter_chapters_row = 1
                    else:
                        counts["jeremiah_count_"+str(match_jeremiah.group(1))] += 1
                        jeremiah_counter_chapters_row += 1
                    jeremiah_chapter = str(match_jeremiah.group(1))
                    jeremiah_count_chapters = counts["jeremiah_count_"+str(match_jeremiah.group(1))]
                        
                #Lamentations
                lamentations_chapter = ""
                lamentations_count_chapters = None
                if match == "Lamentations" or match == "Lam.":
                    counts["lamentations_count"]+=1
                    lamentations_counter_chapters_row += 1
                if match_lamentations:
                    counts["lamentations_count_"+str(match_lamentations.group(1))] = 0
                    if "lamentations_count_"+str(match_lamentations.group(1)) not in counts:
                        counts["lamentations_count_"+str(match_lamentations.group(1))] = 1
                        lamentations_counter_chapters_row = 1
                    else:
                        counts["lamentations_count_"+str(match_lamentations.group(1))] += 1
                        lamentations_counter_chapters_row += 1
                    lamentations_chapter = str(match_lamentations.group(1))
                    lamentations_count_chapters = counts["lamentations_count_"+str(match_lamentations.group(1))]
                
                #Ezekiel
                ezekiel_chapter = ""
                ezekiel_count_chapters = None
                if match == "Ezekiel" or match == "Ezek.":
                    counts["ezekiel_count"]+=1
                    ezekiel_counter_chapters_row += 1
                if match_ezekiel:
                    counts["ezekiel_count_"+str(match_ezekiel.group(1))] = 0
                    if "ezekiel_count_"+str(match_ezekiel.group(1)) not in counts:
                        counts["ezekiel_count_"+str(match_ezekiel.group(1))] = 1
                        ezekiel_counter_chapters_row = 1
                    else:
                        counts["ezekiel_count_"+str(match_ezekiel.group(1))] += 1
                        ezekiel_counter_chapters_row += 1
                    ezekiel_chapter = str(match_ezekiel.group(1))
                    ezekiel_count_chapters = counts["ezekiel_count_"+str(match_ezekiel.group(1))]


                #Daniel
                daniel_chapter = ""
                daniel_count_chapters = None
                if match == "Daniel" or match == "Dan.":
                    counts["daniel_count"]+=1
                    daniel_counter_chapters_row += 1
                if match_daniel:
                    counts["daniel_count_"+str(match_daniel.group(1))] = 0
                    if "daniel_count_"+str(match_daniel.group(1)) not in counts:
                        counts["daniel_count_"+str(match_daniel.group(1))] = 1
                        daniel_counter_chapters_row = 1
                    else:
                        counts["daniel_count_"+str(match_daniel.group(1))] += 1
                        daniel_counter_chapters_row += 1
                    daniel_count_chapters = counts["daniel_count_"+str(match_daniel.group(1))]
                    daniel_chapter = str(match_daniel.group(1))
                    #print("Daniel Counts Rows:"+str(daniel_counter_chapters_row))
                    
                        
                
                #Hosea
                hosea_chapter = ""
                hosea_count_chapters = None
                if match == "Hosea":
                    counts["hosea_count"]+=1
                    hosea_counter_chapters_row += 1
                if match_hosea:
                    counts["hosea_count_"+str(match_hosea.group(1))] = 0
                    if "hosea_count_"+str(match_hosea.group(1)) not in counts:
                        counts["hosea_count_"+str(match_hosea.group(1))] = 1
                        hosea_counter_chapters_row = 1
                    else:
                        counts["hosea_count_"+str(match_hosea.group(1))] += 1
                        hosea_counter_chapters_row += 1
                    hosea_count_chapters = counts["hosea_count_"+str(match_hosea.group(1))]
                    hosea_chapter = str(match_hosea.group(1))
                    #print("Hosea Counts Rows:"+str(hosea_counter_chapters_row))

                #Joel
                joel_chapter = ""
                joel_count_chapters = None
                if match == "Joel":
                    counts["joel_count"]+=1
                    joel_counter_chapters_row += 1
                if match_joel:
                    counts["joel_count_"+str(match_joel.group(1))] = 0
                    if "joel_count_"+str(match_joel.group(1)) not in counts:
                        counts["joel_count_"+str(match_joel.group(1))] = 1
                        joel_counter_chapters_row = 1
                    else:
                        counts["joel_count_"+str(match_joel.group(1))] += 1
                        joel_counter_chapters_row += 1
                    joel_chapter = str(match_joel.group(1))
                    joel_count_chapters = counts["joel_count_"+str(match_joel.group(1))]
                

                #Amos
                amos_chapter = ""
                amos_count_chapters = None
                if match == "Amos":
                    counts["amos_count"]+=1
                    amos_counter_chapters_row += 1
                if match_amos:
                    counts["amos_count_"+str(match_amos.group(1))] = 0
                    if "amos_count_"+str(match_amos.group(1)) not in counts:
                        counts["amos_count_"+str(match_amos.group(1))] = 1
                        amos_counter_chapters_row = 1
                    else:
                        counts["amos_count_"+str(match_amos.group(1))] += 1
                        amos_counter_chapters_row += 1
                    amos_chapter = str(match_amos.group(1))
                    amos_count_chapters = counts["amos_count_"+str(match_amos.group(1))]

                    

                #Obadiah 1
                if match == "Obadiah 1":
                    counts["obadiah_count"]+=1
                    #print("Obadiah 1 Counts:"+ str(counts["obadiah_count"]))


                #Jonah
                jonah_chapter = ""
                jonah_count_chapters = None
                if match == "Jonah":
                    counts["jonah_count"]+=1
                    jonah_counter_chapters_row += 1
                if match_jonah:
                    counts["jonah_count_"+str(match_jonah.group(1))] = 0
                    if "jonah_count_"+str(match_jonah.group(1)) not in counts:
                        counts["jonah_count_"+str(match_jonah.group(1))] = 1
                        jonah_counter_chapters_row = 1
                    else:
                        counts["jonah_count_"+str(match_jonah.group(1))] += 1
                        jonah_counter_chapters_row += 1
                    jonah_chapter = str(match_jonah.group(1))
                    jonah_count_chapters = counts["jonah_count_"+str(match_jonah.group(1))]
                    #print("Jonah Counts:"+ str(counts["jonah_count"]))
                        

                #Micah
                micah_chapter = ""
                micah_count_chapters = None
                if match == "Micah":
                    counts["micah_count"]+=1
                    micah_counter_chapters_row += 1
                if match_micah:
                    counts["micah_count_"+str(match_micah.group(1))] = 0
                    if "micah_count_"+str(match_micah.group(1)) not in counts:
                        counts["micah_count_"+str(match_micah.group(1))] = 1
                        micah_counter_chapters_row = 1
                    else:
                        counts["micah_count_"+str(match_micah.group(1))] += 1
                        micah_counter_chapters_row += 1
                    micah_chapter = str(match_micah.group(1))
                    micah_count_chapters = counts["micah_count_"+str(match_micah.group(1))]
                

                #Nahum
                nahum_chapter = ""
                nahum_count_chapters = None
                if match == "Nahum":    
                    counts["nahum_count"]+=1
                    nahum_counter_chapters_row += 1
                if match_nahum:
                    counts["nahum_count_"+str(match_nahum.group(1))] = 0
                    if "nahum_count_"+str(match_nahum.group(1)) not in counts:
                        counts["nahum_count_"+str(match_nahum.group(1))] = 1
                        nahum_counter_chapters_row = 1
                    else:
                        counts["nahum_count_"+str(match_nahum.group(1))] += 1
                        nahum_counter_chapters_row += 1
                    nahum_chapter = str(match_nahum.group(1))
                    nahum_count_chapters = counts["nahum_count_"+str(match_nahum.group(1))]
                    #print("Nahum Counts:"+ str(counts["nahum_count"]))
                        
                #Habakkuk
                habakkuk_chapter = ""
                habakkuk_count_chapters = None
                if match == "Habakkuk" or match == "Hab.": 
                    counts["habakkuk_count"]+=1
                    habakkuk_counter_chapters_row += 1
                if match_habakkuk:
                    counts["habakkuk_count_"+str(match_habakkuk.group(1))] = 0
                    if "habakkuk_count_"+str(match_habakkuk.group(1)) not in counts:
                        counts["habakkuk_count_"+str(match_habakkuk.group(1))] = 1
                        habakkuk_counter_chapters_row = 1
                    else:
                        counts["habakkuk_count_"+str(match_habakkuk.group(1))] += 1
                        habakkuk_counter_chapters_row += 1
                    habakkuk_chapter = str(match_habakkuk.group(1))
                    habakkuk_count_chapters = counts["habakkuk_count_"+str(match_habakkuk.group(1))]
                    #print("Habakkuk Counts:"+ str(counts["habakkuk_count"]))
                        
                #Zephaniah
                zephaniah_chapter = ""
                zephaniah_count_chapters = None
                if match == "Zephaniah" or match == "Zeph.":
                    counts["zephaniah_count"]+=1
                if match_zephaniah:
                    if "zephaniah_count_"+str(match_zephaniah.group(1)) not in counts:
                        counts["zephaniah_count_"+str(match_zephaniah.group(1))] = 1
                        zephaniah_counter_chapters_row = 1
                    else:
                        counts["zephaniah_count_"+str(match_zephaniah.group(1))] += 1
                        zephaniah_counter_chapters_row += 1
                    zephaniah_chapter = str(match_zephaniah.group(1))
                    zephaniah_count_chapters = counts["zephaniah_count_"+str(match_zephaniah.group(1))]
                    #print("Zephaniah Counts:"+ str(counts["zephaniah_count"]))
                        

                #Haggai
                haggai_chapter = ""
                haggai_count_chapters = None
                if match == "Haggai" or match == "Hag.":
                    counts["haggai_count"]+=1
                    haggai_counter_chapters_row += 1
                if match_haggai:
                    #print(match)
                    #print("matches haggai")
                    #print("matches haggai: "+str(haggai_counter_chapters_row))
                    counts["haggai_count_"+str(match_haggai.group(1))] = 0
                    if "haggai_count_"+str(match_haggai.group(1)) not in counts:
                        counts["haggai_count_"+str(match_haggai.group(1))] = 1
                        haggai_counter_chapters_row = 1
                    else:
                        #print("else runs?")
                        counts["haggai_count_"+str(match_haggai.group(1))] += 1
                        haggai_counter_chapters_row += 1
                    haggai_chapter = str(match_haggai.group(1))
                    haggai_count_chapters = counts["haggai_count_"+str(match_haggai.group(1))]
                    #print("Haggai Counts Rows:"+str(haggai_counter_chapters_row))
                
                #Zechariah
                zechariah_chapter = ""
                zechariah_count_chapters = None
                if match == "Zechariah" or match == "Zech.":
                    counts["zechariah_count"]+=1
                    zechariah_counter_chapters_row += 1
                if match_zechariah:
                    #print("matches zechariah: "+str(zechariah_counter_chapters_row))
                    counts["zechariah_count_"+str(match_zechariah.group(1))] = 0
                    if "zechariah_count_"+str(match_zechariah.group(1)) not in counts:
                        counts["zechariah_count_"+str(match_zechariah.group(1))] = 1
                        zechariah_counter_chapters_row = 1
                    else:
                        counts["zechariah_count_"+str(match_zechariah.group(1))] += 1
                        zechariah_counter_chapters_row += 1
                    zechariah_chapter = str(match_zechariah.group(1))
                    zechariah_count_chapters = counts["zechariah_count_"+str(match_zechariah.group(1))]
                    #print("Zechariah Counts Rows:"+str(zechariah_counter_chapters_row))
                        
                #Malachi
                malachi_chapter = ""
                malachi_count_chapters = None
                if match == "Malachi" or match == "Mal.":
                    counts["malachi_count"]+=1
                    malachi_counter_chapters_row += 1
                if match_malachi:
                    counts["malachi_count_"+str(match_malachi.group(1))] = 0
                    if "malachi_count_"+str(match_malachi.group(1)) not in counts:
                        counts["malachi_count_"+str(match_malachi.group(1))] = 1
                        malachi_counter_chapters_row = 1
                    else:
                        counts["malachi_count_"+str(match_malachi.group(1))] += 1
                        malachi_counter_chapters_row += 1
                    malachi_chapter = str(match_malachi.group(1))
                    malachi_count_chapters = counts["malachi_count_"+str(match_malachi.group(1))]
                    #print("Malachi Counts:"+ str(counts["malachi_count"]))
                
                #First Nephi
                first_nephi_chapter = ""
                first_nephi_count_chapters = None
                if match == "1 Nephi" or match == "1 Ne.":
                    counts["first_nephi_count"]+=1
                    first_nephi_counter_chapters_row += 1
                if match_first_nephi:
                    counts["first_nephi_count_"+str(match_first_nephi.group(1))] = 0
                    if "first_nephi_count_"+str(match_first_nephi.group(1)) not in counts:
                        counts["first_nephi_count_"+str(match_first_nephi.group(1))] = 1
                        first_nephi_counter_chapters_row = 1
                    else:
                        counts["first_nephi_count_"+str(match_first_nephi.group(1))] += 1
                        first_nephi_counter_chapters_row += 1
                    first_nephi_chapter = str(match_first_nephi.group(1))
                    first_nephi_count_chapters = counts["first_nephi_count_"+str(match_first_nephi.group(1))]
                    #print("1 Nephi Counts:"+ str(counts["first_nephi_count"]))
                        
                #Second Nephi
                second_nephi_chapter = ""
                second_nephi_count_chapters = None
                if match == "2 Nephi" or match == "2 Ne.":
                    counts["second_nephi_count"]+=1
                    second_nephi_counter_chapters_row += 1
                if match_second_nephi:
                    counts["second_nephi_count_"+str(match_second_nephi.group(1))] = 0
                    if "second_nephi_count_"+str(match_second_nephi.group(1)) not in counts:
                        counts["second_nephi_count_"+str(match_second_nephi.group(1))] = 1
                    else:
                        counts["second_nephi_count_"+str(match_second_nephi.group(1))] += 1
                        second_nephi_counter_chapters_row += 1
                    second_nephi_chapter = str(match_second_nephi.group(1))
                    second_nephi_count_chapters = counts["second_nephi_count_"+str(match_second_nephi.group(1))]
                    #print("2 Nephi Counts:"+ str(counts["second_nephi_count"]))

                #Jacob
                jacob_chapter = ""
                jacob_count_chapters = None
                if match == "Jacob":
                    counts["jacob_count"]+=1
                    jacob_counter_chapters_row += 1
                if match_jacob:
                    counts["jacob_count_"+str(match_jacob.group(1))] = 0
                    if "jacob_count_"+str(match_jacob.group(1)) not in counts:
                        counts["jacob_count_"+str(match_jacob.group(1))] = 1
                        jacob_counter_chapters_row = 1
                    else:
                        counts["jacob_count_"+str(match_jacob.group(1))] += 1
                        jacob_counter_chapters_row += 1
                    jacob_chapter = str(match_jacob.group(1))
                    jacob_count_chapters = counts["jacob_count_"+str(match_jacob.group(1))]
                    #print("Jacob Counts:"+ str(counts["jacob_count"]))
                        
                #Enos 1
                if match == "Enos 1":
                    counts["enos_count"]+=1
                    #print("Enos 1 Counts:"+ str(counts["enos_count"]))

                #Jarom 1
                if match == "Jarom 1":
                    counts["jarom_count"]+=1
                    #print("Jarom 1 Counts:"+ str(counts["jarom_count"]))

                #Omni 1
                if match == "Omni 1":
                    counts["omni_count"]+=1
                    #print("Omni 1 Counts:"+ str(counts["omni_count"]))
                
                #Words of Mormon
                if match == "Words of Mormon" or match == "W of M":
                    counts["words_of_mormon_count"]+=1
                    #print("Words of Mormon Counts:"+ str(counts["words_of_mormon_count"]))
                        
                
                #Mosiah
                mosiah_chapter = ""
                mosiah_count_chapters = None
                if match == "Mosiah":
                    counts["mosiah_count"]+=1
                    mosiah_counter_chapters_row += 1
                if match_mosiah:
                    counts["mosiah_count_"+str(match_mosiah.group(1))] = 0
                    if "mosiah_count_"+str(match_mosiah.group(1)) not in counts:
                        counts["mosiah_count_"+str(match_mosiah.group(1))] = 1
                        mosiah_counter_chapters_row = 1
                    else:
                        counts["mosiah_count_"+str(match_mosiah.group(1))] += 1
                        mosiah_counter_chapters_row += 1
                    mosiah_chapter = str(match_mosiah.group(1))
                    mosiah_count_chapters = counts["mosiah_count_"+str(match_mosiah.group(1))]
                    #print("Mosiah Counts:"+ str(counts["mosiah_count"]))
                        

                #Alma
                alma_chapter = ""
                alma_count_chapters = None
                if match == "Alma":
                    counts["alma_count"]+=1
                    alma_counter_chapters_row += 1
                if match_alma:
                    counts["alma_count_"+str(match_alma.group(1))] = 0
                    if "alma_count_"+str(match_alma.group(1)) not in counts:
                        counts["alma_count_"+str(match_alma.group(1))] = 1
                        alma_counter_chapters_row = 1
                    else:
                        counts["alma_count_"+str(match_alma.group(1))] += 1
                        alma_counter_chapters_row += 1
                    alma_chapter = str(match_alma.group(1))
                    alma_count_chapters = counts["alma_count_"+str(match_alma.group(1))]
                    #print("Alma Counts:"+ str(counts["alma_count"]))
                
                #Helaman
                helaman_chapter = ""
                helaman_count_chapters = None
                if match == "Helaman" or match == "Hel.":
                    counts["helaman_count"]+=1
                    helaman_counter_chapters_row += 1
                if match_helaman:
                    counts["helaman_count_"+str(match_helaman.group(1))] = 0
                    if "helaman_count_"+str(match_helaman.group(1)) not in counts:
                        counts["helaman_count_"+str(match_helaman.group(1))] = 1
                        helaman_counter_chapters_row = 1
                    else:
                        counts["helaman_count_"+str(match_helaman.group(1))] += 1
                        helaman_counter_chapters_row += 1
                    helaman_count_chapters = counts["helaman_count_"+str(match_helaman.group(1))]
                    helaman_chapter = str(match_helaman.group(1))
                    #print("Helaman Counts Rows:"+str(helaman_counter_chapters_row))

                #3 Nephi
                third_nephi_chapter = ""
                third_nephi_count_chapters = None
                if match == "3 Nephi" or match == "3 Ne.":
                    counts["third_nephi_count"]+=1
                    third_nephi_counter_chapters_row += 1
                if match_third_nephi:
                    counts["third_nephi_count_"+str(match_third_nephi.group(1))] = 0
                    if "third_nephi_count_"+str(match_third_nephi.group(1)) not in counts:
                        counts["third_nephi_count_"+str(match_third_nephi.group(1))] = 1
                        third_nephi_counter_chapters_row = 1
                    else:
                        counts["third_nephi_count_"+str(match_third_nephi.group(1))] += 1
                        third_nephi_counter_chapters_row += 1
                    third_nephi_chapter = str(match_third_nephi.group(1))
                    third_nephi_count_chapters = counts["third_nephi_count_"+str(match_third_nephi.group(1))]
                    #print("3 Nephi Counts:"+ str(counts["third_nephi_count"]))
                        
                #4 Nephi
                if match == "4 Nephi" or match == "4 Ne.":
                    counts["fourth_nephi_count"]+=1
                    #print("4 Nephi Counts:"+ str(counts["fourth_nephi_count"]))

                #4 Nephi
                if match == "Book of Mormon":
                    counts["book_of_mormon_count"]+=1
                    #print("Book of Mormon Counts:"+ str(counts["book_of_mormon_count"]))

                #Mormon
                mormon_chapter = ""
                mormon_count_chapters = None
                if match == "Morm.":
                    counts["mormon_count"]+=1
                    mormon_counter_chapters_row += 1
                if match_mormon:
                    counts["mormon_count_"+str(match_mormon.group(1))] = 0
                    if "mormon_count_"+str(match_mormon.group(1)) not in counts:
                        counts["mormon_count_"+str(match_mormon.group(1))] = 1
                        mormon_counter_chapters_row = 1
                    else:
                        counts["mormon_count_"+str(match_mormon.group(1))] += 1
                        mormon_counter_chapters_row += 1
                    mormon_chapter = str(match_mormon.group(1))
                    mormon_count_chapters = counts["mormon_count_"+str(match_mormon.group(1))]
                    #print("Morm. Counts:"+ str(counts["mormon_count"]))
                        
                #Ether
                ether_chapter = ""
                ether_count_chapters = None
                if match == "Ether":
                    counts["ether_count"]+=1
                    ether_counter_chapters_row += 1
                if match_ether:
                    counts["ether_count_"+str(match_ether.group(1))] = 0
                    if "ether_count_"+str(match_ether.group(1)) not in counts:
                        counts["ether_count_"+str(match_ether.group(1))] = 1
                        ether_counter_chapters_row = 1
                    else:
                        counts["ether_count_"+str(match_ether.group(1))] += 1
                        ether_counter_chapters_row += 1
                    ether_count_chapters = counts["ether_count_"+str(match_ether.group(1))]
                    ether_chapter = str(match_ether.group(1))
                    #print("Ether Counts Rows:"+str(ether_counter_chapters_row))


                #Moroni
                moroni_chapter = ""
                moroni_count_chapters = None
                if match == "Moro." or match == "Moroni":
                    counts["moroni_count"]+=1
                    moroni_counter_chapters_row += 1
                if match_moroni:
                    counts["moroni_count_"+str(match_moroni.group(1))] = 0
                    if "moroni_count_"+str(match_moroni.group(1)) not in counts:
                        counts["moroni_count_"+str(match_moroni.group(1))] = 1
                        moroni_counter_chapters_row = 1
                    else:
                        counts["moroni_count_"+str(match_moroni.group(1))] += 1
                        moroni_counter_chapters_row += 1
                    moroni_chapter = str(match_moroni.group(1))
                    moroni_count_chapters = counts["moroni_count_"+str(match_moroni.group(1))]
                        

                #New Testament
                if match == "New Testament":
                    counts["new_testament_count"]+=1
                    #print("New Testament Counts:"+ str(counts["new_testament_count"]))

                #Matthew
                matthew_chapter = ""
                matthew_count_chapters = None
                if match == "Matthew" or match == "Matt.":
                    counts["matthew_count"]+=1
                    matthew_counter_chapters_row += 1
                if match_matthew:
                    counts["matthew_count_"+str(match_matthew.group(1))] = 0
                    if "matthew_count_"+str(match_matthew.group(1)) not in counts:
                        counts["matthew_count_"+str(match_matthew.group(1))] = 1
                        matthew_counter_chapters_row = 1
                    else:
                        counts["matthew_count_"+str(match_matthew.group(1))] += 1
                        matthew_counter_chapters_row += 1
                    matthew_chapter = str(match_matthew.group(1))
                    matthew_count_chapters = counts["matthew_count_"+str(match_matthew.group(1))]
                        

                #Mark
                mark_chapter = ""
                mark_count_chapters = None
                if match == "Mark":
                    counts["mark_count"]+=1
                    mark_counter_chapters_row += 1
                if match_mark:
                    counts["mark_count_"+str(match_mark.group(1))] = 0
                    if "mark_count_"+str(match_mark.group(1)) not in counts:
                        counts["mark_count_"+str(match_mark.group(1))] = 1
                        mark_counter_chapters_row = 1
                    else:
                        counts["mark_count_"+str(match_mark.group(1))] += 1
                        mark_counter_chapters_row += 1
                    mark_chapter = str(match_mark.group(1))
                    mark_count_chapters = counts["mark_count_"+str(match_mark.group(1))]
                    #print("Mark Counts Rows:"+str(mark_counter_chapters_row))
                        
                #Luke
                luke_chapter = ""
                luke_count_chapters = None
                if match == "Luke":
                    counts["luke_count"]+=1
                    luke_counter_chapters_row += 1
                if match_luke:
                    counts["luke_count_"+str(match_luke.group(1))] = 0
                    if "luke_count_"+str(match_luke.group(1)) not in counts:
                        counts["luke_count_"+str(match_luke.group(1))] = 1
                        luke_counter_chapters_row = 1
                    else:
                        counts["luke_count_"+str(match_luke.group(1))] += 1
                        luke_counter_chapters_row += 1
                    luke_chapter = str(match_luke.group(1))
                    luke_count_chapters = counts["luke_count_"+str(match_luke.group(1))]
                    #print("Luke Counts:"+ str(counts["luke_count"]))
                        

                #John
                john_chapter = ""
                john_count_chapters = None
                if match == "Gospels of John" or match == "John":
                    counts["john_count"]+=1
                    john_counter_chapters_row += 1
                if match_john:
                    counts["john_count_"+str(match_john.group(1))] = 0
                    if "john_count_"+str(match_john.group(1)) not in counts:
                        counts["john_count_"+str(match_john.group(1))] = 1
                        john_counter_chapters_row = 1
                    else:
                        counts["john_count_"+str(match_john.group(1))] += 1
                        john_counter_chapters_row += 1
                    john_chapter = str(match_john.group(1))
                    john_count_chapters = counts["john_count_"+str(match_john.group(1))]
                    #print("John Counts:"+ str(counts["john_count"]))
                # if scripture_names[95] in match or match in scripture_names[96]:
                # #     john_count+=1
                        

                #Acts
                acts_chapter = ""
                acts_count_chapters = None
                if match == "Acts":
                    counts["acts_count"]+=1
                    acts_counter_chapters_row += 1
                if match_acts:
                    counts["acts_count_"+str(match_acts.group(1))] = 0
                    if "acts_count_"+str(match_acts.group(1)) not in counts:
                        counts["acts_count_"+str(match_acts.group(1))] = 1
                        acts_counter_chapters_row = 1
                    else:
                        counts["acts_count_"+str(match_acts.group(1))] += 1
                        acts_counter_chapters_row += 1
                    acts_chapter = str(match_acts.group(1))
                    acts_mark_count_chapters = counts["acts_count_"+str(match_acts.group(1))]
                    #print("Acts Counts:"+ str(counts["acts_count"]))
                        
                #Romans
                romans_chapter = ""
                romans_count_chapters = None
                if match == "Romans" or match == "Rom.":
                    counts["romans_count"]+=1
                    romans_counter_chapters_row += 1
                if match_romans:
                    counts["romans_count_"+str(match_romans.group(1))] = 0
                    if "romans_count_"+str(match_romans.group(1)) not in counts:
                        counts["romans_count_"+str(match_romans.group(1))] = 1
                        romans_counter_chapters_row = 1
                    else:
                        counts["romans_count_"+str(match_romans.group(1))] += 1
                        romans_counter_chapters_row += 1
                    romans_count_chapters = counts["romans_count_"+str(match_romans.group(1))]
                    romans_chapter = str(match_romans.group(1))
                    #print("Romans Counts Rows:"+str(romans_counter_chapters_row))
                        
                #First Corinthians
                first_corinthians_chapter = ""
                first_corinthians_count_chapters = None
                if match == "1 Corinthians" or match == "1 Cor.":
                    counts["first_corinthians_count"]+=1
                    first_corinthians_counter_chapters_row += 1
                if match_first_corinthians:
                    counts["first_corinthians_count_"+str(match_first_corinthians.group(1))] = 0
                    if "first_corinthians_count_"+str(match_first_corinthians.group(1)) not in counts:
                        counts["first_corinthians_count_"+str(match_first_corinthians.group(1))] = 1
                        first_corinthians_counter_chapters_row = 1
                    else:
                        counts["first_corinthians_count_"+str(match_first_corinthians.group(1))] += 1
                        first_corinthians_counter_chapters_row += 1
                    first_corinthians_chapter = str(match_first_corinthians.group(1))
                    first_corinthians_count_chapters = counts["first_corinthians_count_"+str(match_first_corinthians.group(1))]
                    #print("1 Corinthians Chapter: "+str(first_corinthians_chapter))
                    #print("1 Corinthians Counts Rows:"+str(first_corinthians_counter_chapters_row))
                        
                #Second Corinthians
                second_corinthians_chapter = ""
                second_corinthians_count_chapters = None
                if match == "2 Corinthians" or match == "2 Cor.":
                    counts["second_corinthians_count"]+=1
                    second_corinthians_counter_chapters_row += 1
                if match_second_corinthians:
                    counts["second_corinthians_count_"+str(match_second_corinthians.group(1))] = 0
                    if "second_corinthians_count_"+str(match_second_corinthians.group(1)) not in counts:
                        counts["second_corinthians_count_"+str(match_second_corinthians.group(1))] = 1
                        second_corinthians_counter_chapters_row = 1
                    else:
                        counts["second_corinthians_count_"+str(match_second_corinthians.group(1))] += 1
                        second_corinthians_counter_chapters_row += 1
                    second_corinthians_chapter = str(match_second_corinthians.group(1))
                    second_corinthians_count_chapters = counts["second_corinthians_count_"+str(match_second_corinthians.group(1))]
                    #print("2 Corinthians Counts Rows:"+str(second_corinthians_counter_chapters_row))
                        

                #Galatians
                galatians_chapter = ""
                galatians_count_chapters = None
                if match == "Galatians" or match == "Gal.":
                    counts["galatians_count"]+=1
                    galatians_counter_chapters_row += 1
                if match_galatians:
                    counts["galatians_count_"+str(match_galatians.group(1))] = 0
                    if "galatians_count_"+str(match_galatians.group(1)) not in counts:
                        counts["galatians_count_"+str(match_galatians.group(1))] = 1
                        galations_counter_chapters_row = 1
                    else:
                        counts["galatians_count_"+str(match_galatians.group(1))] += 1
                        galatians_counter_chapters_row += 1
                    galatians_chapter = str(match_galatians.group(1))
                    galatians_count_chapters = counts["galatians_count_"+str(match_galatians.group(1))]
                    #print("Galatians Counts:"+ str(counts["galatians_count"]))
                        
                #Ephesians
                ephesians_chapter = ""
                ephesians_count_chapters = None
                if match == "Ephesians" or match == "Eph.":
                    counts["ephesians_count"]+=1
                    ephesians_counter_chapters_row += 1
                if match_ephesians:
                    counts["ephesians_count_"+str(match_ephesians.group(1))] = 0
                    if "ephesians_count_"+str(match_ephesians.group(1)) not in counts:
                        counts["ephesians_count_"+str(match_ephesians.group(1))] = 1
                        ephesians_counter_chapters_row = 1
                    else:
                        counts["ephesians_count_"+str(match_ephesians.group(1))] += 1
                        ephesians_counter_chapters_row += 1
                    ephesians_chapter = str(match_ephesians.group(1))
                    ephesians_count_chapters = counts["ephesians_count_"+str(match_ephesians.group(1))]
                    #print("Ephesians Counts:"+ str(counts["ephesians_count"]))
                        
                #Philippians
                philippians_chapter = ""
                philippians_count_chapters = None
                if match == "Philippians" or match == "Philip.":
                    counts["philippians_count"]+=1
                    philippians_counter_chapters_row += 1
                if match_philippians:
                    counts["philippians_count_"+str(match_philippians.group(1))] = 0
                    if "philippians_count_"+str(match_philippians.group(1)) not in counts:
                        counts["philippians_count_"+str(match_philippians.group(1))] = 1
                        philippians_counter_chapters_row = 1
                    else:
                        counts["philippians_count_"+str(match_philippians.group(1))] += 1
                        philippians_counter_chapters_row += 1
                    philippians_chapter = str(match_philippians.group(1))
                    philippians_count_chapters = counts["philippians_count_"+str(match_philippians.group(1))]
                    #print("Philippians Counts:"+ str(counts["philippians_count"]))
                        
                #Colossians
                colossians_chapter = ""
                colossians_count_chapters = None
                if match == "Colossians" or match == "Col.":
                    counts["colossians_count"]+=1
                    colossians_counter_chapters_row += 1
                if match_colossians:
                    counts["colossians_count_"+str(match_colossians.group(1))] = 0
                    if "colossians_count_"+str(match_colossians.group(1)) not in counts:
                        counts["colossians_count_"+str(match_colossians.group(1))] = 1
                        colossians_counter_chapters_row = 1
                    else:
                        counts["colossians_count_"+str(match_colossians.group(1))] += 1
                        colossians_counter_chapters_row += 1
                    colossians_chapter = str(match_colossians.group(1))
                    colossians_count_chapters = counts["colossians_count_"+str(match_colossians.group(1))]
                    #print("Colossians Counts:"+ str(counts["colossians_count"]))
                        

                #First Thessalonians
                first_thessalonians_chapter = ""
                first_thessalonians_count_chapters = None
                if match == "1 Thessalonians" or match == "1 Thes.":
                    counts["first_thessalonians_count"]+=1
                    first_thessalonians_counter_chapters_row += 1
                if match_first_thessalonians:
                    counts["first_thessalonians_count_"+str(match_first_thessalonians.group(1))] = 0
                    if "first_thessalonians_count_"+str(match_first_thessalonians.group(1)) not in counts:
                        counts["first_thessalonians_count_"+str(match_first_thessalonians.group(1))] = 1
                        first_thessalonians_counter_chapters_row = 1
                    else:
                        counts["first_thessalonians_count_"+str(match_first_thessalonians.group(1))] += 1
                        first_thessalonians_counter_chapters_row += 1
                    first_thessalonians_chapter = str(match_first_thessalonians.group(1))
                    first_thessalonians_count_chapters = counts["first_thessalonians_count_"+str(match_first_thessalonians.group(1))]
                    #print("1 Thessalonians Counts:"+ str(counts["first_thessalonians_count"]))
                        
                #Second Thessalonians
                second_thessalonians_chapter = ""
                second_thessalonians_count_chapters = None
                if match == "2 Thessalonians" or match == "2 Thes.":
                    counts["second_thessalonians_count"]+=1
                    second_counter_chapters_row += 1
                if match_second_thessalonians:
                    counts["second_thessalonians_count_"+str(match_second_thessalonians.group(1))] = 0
                    if "second_thessalonians_count_"+str(match_second_thessalonians.group(1)) not in counts:
                        counts["second_thessalonians_count_"+str(match_second_thessalonians.group(1))] = 1
                        second_thessalonians_counter_chapters_row = 1
                    else:
                        counts["second_thessalonians_count_"+str(match_second_thessalonians.group(1))] += 1
                        second_thessalonians_counter_chapters_row += 1
                    second_thessalonians_chapter = str(match_second_thessalonians.group(1))
                    second_thessalonians_count_chapters = counts["second_thessalonians_count_"+str(match_second_thessalonians.group(1))]
                    #print("2 Thessalonians Counts:"+ str(counts["second_thessalonians_count"]))
                        

                #First Timothy
                first_timothy_chapter = ""
                first_timothy_count_chapters = None
                if match == "1 Timothy" or match == "1 Tim.":
                    counts["first_timothy_count"]+=1
                    first_timothy_counter_chapters_row += 1
                if match_first_timothy:
                    if "first_timothy_count_"+str(match_first_timothy.group(1)) not in counts:
                        counts["first_timothy_count_"+str(match_first_timothy.group(1))] = 1
                        first_timothy_counter_chapters_row = 1
                    else:
                        counts["first_timothy_count_"+str(match_first_timothy.group(1))] += 1
                        first_timothy_counter_chapters_row += 1
                    first_timothy_chapter = str(match_first_timothy.group(1))
                    first_timothy_count_chapters = counts["first_timothy_count_"+str(match_first_timothy.group(1))]
                    #print("1 Timothy Counts:"+ str(counts["first_timothy_count"]))
                        
                
                #Second Timothy
                second_timothy_chapter = ""
                second_timothy_count_chapters = None
                if match == "2 Timothy" or match == "2 Tim.":
                    counts["second_timothy_count"]+=1
                    second_timothy_counter_chapters_row += 1
                if match_second_timothy:
                    counts["second_timothy_count_"+str(match_second_timothy.group(1))] = 0
                    if "second_timothy_count_"+str(match_second_timothy.group(1)) not in counts:
                        counts["second_timothy_count_"+str(match_second_timothy.group(1))] = 1
                        second_timothy_counter_chapters_row = 1
                    else:
                        counts["second_timothy_count_"+str(match_second_timothy.group(1))] += 1
                        second_timothy_counter_chapters_row = 1
                    second_timothy_chapter = str(match_second_timothy.group(1))
                    second_timothy_count_chapters = counts["second_timothy_count_"+str(match_second_timothy.group(1))]
                    #print("2 Timothy Counts:"+ str(counts["second_timothy_count"]))
                        

                #Titus
                titus_chapter = ""
                titus_count_chapters = None
                if match == "Titus":
                    counts["titus_count"]+=1
                    titus_counter_chapters_row += 1
                if match_titus:
                    counts["titus_count_"+str(match_titus.group(1))] = 0
                    if "titus_count_"+str(match_titus.group(1)) not in counts:
                        counts["titus_count_"+str(match_titus.group(1))] = 1
                        titus_counter_chapters_row = 1
                    else:
                        counts["titus_count_"+str(match_titus.group(1))] += 1
                        titus_counter_chapters_row += 1
                    titus_chapter = str(match_titus.group(1))
                    titus_count_chapters = counts["titus_count_"+str(match_titus.group(1))]
                    #print("Titus Counts:"+ str(counts["titus_count"]))
                        
                #Philemon
                if match == "Philemon" or match == "Philem.":
                    counts["philemon_count"]+=1
                    #print("Philemon Counts:"+ str(counts["philemon_count"]))

                #Hebrews
                hebrews_chapter = ""
                hebrews_count_chapters = None
                if match == "Hebrews" or match == "Heb.":
                    counts["hebrews_count"]+=1
                    hebrews_counter_chapters_row += 1
                if match_hebrews:
                    counts["hebrews_count_"+str(match_hebrews.group(1))] = 0
                    if "hebrews_count_"+str(match_hebrews.group(1)) not in counts:
                        counts["hebrews_count_"+str(match_hebrews.group(1))] = 1
                        hebrews_counter_chapters_row = 1
                    else:
                        counts["hebrews_count_"+str(match_hebrews.group(1))] += 1
                        hebrews_counter_chapters_row += 1
                    hebrews_count_chapters = counts["hebrews_count_"+str(match_hebrews.group(1))]
                    hebrews_chapter = str(match_hebrews.group(1))
                    #print("Hebrews Counts Rows:"+str(hebrews_counter_chapters_row))
                        
                
                #James
                # james_chapter = ""
                # james_count_chapters = None
                # if match == "James":
                #     counts["james_count"]+=1
                #     james_counter_chapters_row += 1
                # if match_james:
                #     counts["james_count_"+str(match_james.group(1))] = 0
                #     if "james_count_"+str(match_james.group(1)) not in counts:
                #         counts["james_count_"+str(match_james.group(1))] = 1
                #         james_counter_chapters_row = 1
                #     else:
                #         counts["james_count_"+str(match_james.group(1))] += 1
                #         james_counter_chapters_row += 1
                #     james_count_chapters = counts["james_count_"+str(match_james.group(1))]
                #     james_chapter = str(match_james.group(1))
                #     print(counts)
                #     print("James Counts:"+ str(counts["james_count"]))

                #James
                james_chapter = ""
                james_count_chapters = None
                if match == "James":
                    counts["james_count"]+=1
                    james_counter_chapters_row += 1
                if match_james:
                    counts["james_count_"+str(match_james.group(1))] = 0
                    if "james_count_"+str(match_james.group(1)) not in counts:
                        counts["james_count_"+str(match_james.group(1))] = 1
                        james_counter_chapters_row = 1
                    else:
                        counts["james_count_"+str(match_james.group(1))] += 1
                        james_counter_chapters_row += 1
                    james_chapter = str(match_james.group(1))
                    james_count_chapters = counts["james_count_"+str(match_james.group(1))]
                    #print("James Counts:"+ str(counts["james_count"]))
                        
                #First Peter
                first_peter_chapter = ""
                first_peter_count_chapters = None
                if match == "1 Peter" or match == "1 Pet.":
                    counts["first_peter_count"]+=1
                    first_peter_counter_chapters_row += 1
                if match_first_peter:
                    counts["first_peter_count_"+str(match_first_peter.group(1))] = 0
                    if "first_peter_count_"+str(match_first_peter.group(1)) not in counts:
                        counts["first_peter_count_"+str(match_first_peter.group(1))] = 1
                        first_peter_counter_chapters_row = 1
                    else:
                        counts["first_peter_count_"+str(match_first_peter.group(1))] += 1
                        first_peter_counter_chapters_row += 1
                    first_peter_chapter = str(match_first_peter.group(1))
                    first_peter_count_chapters = counts["first_peter_count_"+str(match_first_peter.group(1))]
                    #print("1 Peter Counts:"+ str(counts["first_peter_count"]))
                        
                #Second Peter
                second_peter_chapter = ""
                second_peter_count_chapters = None
                if match == "2 Peter" or match == "2 Pet.":
                    counts["second_peter_count"]+=1
                    second_peter_counter_chapters_row += 1
                if match_second_peter:
                    counts["second_peter_count_"+str(match_second_peter.group(1))] = 0
                    if "second_peter_count_"+str(match_second_peter.group(1)) not in counts:
                        counts["second_peter_count_"+str(match_second_peter.group(1))] = 1
                        second_peter_counter_chapters_row = 1
                    else:
                        counts["second_peter_count_"+str(match_second_peter.group(1))] += 1
                        second_peter_counter_chapters_row += 1
                    second_peter_chapter = str(match_second_peter.group(1))
                    second_peter_count_chapters = counts["second_peter_count_"+str(match_second_peter.group(1))]
                    #print("2 Peter Counts:"+ str(counts["second_peter_count"]))
                        
                #First John
                first_john_chapter = ""
                first_john_count_chapters = None
                if match == "1 John" or match == "1 Jn.":
                    counts["first_john_count"]+=1
                    first_john_counter_chapters_row += 1
                if match_first_john:
                    counts["first_john_count_"+str(match_first_john.group(1))] = 0
                    if "first_john_count_"+str(match_first_john.group(1)) not in counts:
                        counts["first_john_count_"+str(match_first_john.group(1))] = 1
                        first_john_counter_chapters_row = 1
                    else:
                        counts["first_john_count_"+str(match_first_john.group(1))] += 1
                        first_john_counter_chapters_row += 1
                    first_john_chapter = str(match_first_john.group(1))
                    first_john_count_chapters = counts["first_john_count_"+str(match_first_john.group(1))]
                    #print("1 John Counts:"+ str(counts["first_john_count"]))
                        

                #Second John
                if match == "2 John" or match == "2 Jn.":
                    counts["second_john_count"]+=1
                    #print("2 John Counts:"+ str(counts["second_john_count"]))

                #Third John
                if match == "3 John" or match == "3 Jn.":
                    counts["third_john_count"]+=1
                        
                
                #Jude 1
                if match == "Jude 1":
                    counts["jude_count"]+=1
                    #print("Jude 1:"+ str(counts["jude_count"]))


                #Revelation    
                revelation_chapter = ""
                revelation_count_chapters = None
                if match == "Revelation" or match == "Rev.":
                    counts["revelation_count"]+=1
                    revelation_counter_chapters_row += 1
                if match_revelation:
                    counts["revelation_count_"+str(match_revelation.group(1))] = 0
                    if "revelation_count_"+str(match_revelation.group(1)) not in counts:
                        counts["revelation_count_"+str(match_revelation.group(1))] = 1
                        revelation_counter_chapters_row = 1
                    else:
                        counts["revelation_count_"+str(match_revelation.group(1))] += 1
                        revelation_counter_chapters_row += 1
                    revelation_chapter = str(match_revelation.group(1))
                    revelation_count_chapters = counts["revelation_count_"+str(match_revelation.group(1))]
                    #print("Revelation Counts:"+ str(counts["revelation_count"]))
                        
                #Doctrine and Covenants
                doctrine_and_covenants_chapter = ""
                doctrine_and_covenants_count_chapters = None
                if match == "Doctrine and Covenants" or match == "D&C":
                    counts["doctrine_and_covenants_count"]+=1
                    doctrine_and_covenants_counter_chapters_row += 1
                if match_doctrine_and_covenants:
                    counts["doctrine_and_covenants_count_"+str(match_doctrine_and_covenants.group(1))] = 0
                    if "doctrine_and_covenants_count_"+str(match_doctrine_and_covenants.group(1)) not in counts:
                        counts["doctrine_and_covenants_count_"+str(match_doctrine_and_covenants.group(1))] = 1
                        doctrine_and_covenants_counter_chapters_row = 1
                    else:
                        counts["doctrine_and_covenants_count_"+str(match_doctrine_and_covenants.group(1))] += 1
                        doctrine_and_covenants_counter_chapters_row += 1
                    doctrine_and_covenants_chapter = str(match_doctrine_and_covenants.group(1))
                    doctrine_and_covenants_count_chapters = counts["doctrine_and_covenants_count_"+str(match_doctrine_and_covenants.group(1))]
                    #print("Doctrine and Covenants Counts:"+ str(counts["doctrine_and_covenants_count"]))
                        

                #Moses
                moses_chapter = ""
                moses_count_chapters = None
                if match == "Moses":
                    counts["moses_count"]+=1
                    moses_counter_chapters_row += 1
                if match_moses:
                    counts["moses_count_"+str(match_moses.group(1))] = 0
                    if "moses_count_"+str(match_moses.group(1)) not in counts:
                        counts["moses_count_"+str(match_moses.group(1))] = 1
                        moses_counter_chapters_row = 1
                    else:
                        counts["moses_count_"+str(match_moses.group(1))] += 1
                        moses_counter_chapters_row += 1
                    moses_chapter = str(match_moses.group(1))
                    moses_count_chapters = counts["moses_count_"+str(match_moses.group(1))]
                    
                        

                #Abraham
                abraham_chapter = ""
                abraham_count_chapters = None
                if match == "Abraham" or match == "Abr.":
                    counts["abraham_count"]+=1
                    abraham_counter_chapters_row += 1
                if match_abraham:
                    counts["abraham_count_"+str(match_abraham.group(1))] = 0
                    if "abraham_count_"+str(match_abraham.group(1)) not in counts:
                        counts["abraham_count_"+str(match_abraham.group(1))] = 1
                        abraham_counter_chapters_row = 1
                    else:
                        counts["abraham_count_"+str(match_abraham.group(1))] += 1
                        abraham_counter_chapters_row += 1
                    abraham_chapter = str(match_abraham.group(1))
                    abraham_count_chapters = counts["abraham_count_"+str(match_abraham.group(1))]
                    #print("Abraham:"+ str(counts["abraham_count"]))
                        
                #Facsimile
                facsimile_chapter = ""
                facsimile_count_chapters = None
                if match == "Facsimile":
                    counts["facsimile_count"]+=1
                    facsimile_counter_chapters_row += 1
                if match_facsimile:
                    counts["facsimile_count_"+str(match_facsimile.group(1))] = 0
                    if "facsimile_count_"+str(match_facsimile.group(1)) not in counts:
                        counts["facsimile_count_"+str(match_facsimile.group(1))] = 1
                        facsimile_counter_chapters_row = 1
                    else:
                        counts["facsimile_count_"+str(match_facsimile.group(1))] += 1
                        facsimile_counter_chapters_row += 1
                    facsimile_chapter = str(match_facsimile.group(1))
                    facsimile_count_chapters = counts["facsimile_count_"+str(match_facsimile.group(1))]
                    #print("Facsimile:"+ str(counts["facsimile_count"]))
                        
                #Joseph Smith-Matthew
                if match == "Joseph Smith-Matthew" or match == "JS-M":
                    counts["joseph_smith_matthew_count"]+=1
                    #print("Joseph Smith-Matthew:"+ str(counts["joseph_smith_matthew_count"]))

                
                #Joseph Smith History
                if match == "Joseph Smith History" or match == "Joseph Smith—History":
                    counts["joseph_smith_history_count"]+=1
                    #print("Joseph Smith History:"+ str(counts["joseph_smith_history_count"]))



                #Articles of Faith
                if match == "Articles of Faith" or match == "A of F":
                    counts["articles_of_faith_count"]+=1
                    #print("Articles of Faith:"+ str(counts["articles_of_faith_count"]))


                #Joseph Smith Translation
                # Note: This is broken, but you don't need to fix it. The pattern doesn't seem to match for some strange reason.
                joseph_smith_translation_chapter = ""
                joseph_smith_translation_count_chapters = None
                if match == "Joseph Smith Translation" or match == 'JST':
                    counts["joseph_smith_translation_count"]+=1
                    joseph_smith_translation_counter_chapters_row += 1
                if match_joseph_smith_translation:
                    counts["joseph_smith_translation_count_"+str(match_joseph_smith_translation.group(1))] = 0
                    if "joseph_smith_translation_count_"+str(match_joseph_smith_translation.group(1)) not in counts:
                        counts["joseph_smith_translation_count_"+str(match_joseph_smith_translation.group(1))] = 1
                        joseph_smith_translation_counter_chapters_row = 1
                    else:
                        counts["joseph_smith_translation_"+str(match_joseph_smith_translation.group(1))] += 1
                        joseph_smith_translation_counter_chapters_row += 1
                    joseph_smith_translation_chapter = str(match_joseph_smith_translation.group(1))
                    joseph_smith_translation_count_chapters = counts["joseph_smith_translation_count_"+str(match_joseph_smith_translation.group(1))]
                    #print("Joseph Smith Translation:"+ str(counts["joseph_smith_translation_count"]))
                        

                #Ten Commandments
                if match == "Ten Commandments" or match == "10 Commandments":
                    counts["ten_commandments_count"]+=1
                    #print("Ten Commandments:"+ str(counts["ten_commandments_count"]))


                #Title Page of the Book of Mormon
                if match == "Title Page of the Book of Mormon":
                    counts["title_page_of_the_book_of_mormon_count"]+=1
                    #print("Title Page of the Book of Mormon:"+ str(counts["title_page_of_the_book_of_mormon_count"]))

                #Testimony of the Twelve Apostles from the Book of Mormon
                if match == "Testimony of the Twelve Apostles from the Book of Mormon":
                    counts["testimony_of_the_twelve_apostles_from_the_book_of_mormon_count"]+=1
                    #print("Testimony of the Twelve Apostles from the Book of Mormon:"+ str(counts["testimony_of_the_twelve_apostles_from_the_book_of_mormon_count"]))
                list_for_numbers = counts["numbers_count"]
                #print("List for Numbers" + str(list_for_numbers))
                # if exodus_count_chapters != None:
                #     print(exodus_count_chapters)
                #     print(numbers_count_chapters)
                #     print(deuteronomy_count_chapters)
                #     print(first_samuel_count_chapters)
                #     print(second_chronicles_count_chapters)
                #     print(proverbs_count_chapters)
                #     print(second_nephi_count_chapters)


                    #from_1_to_10_name_list = ['Galatians',"galatians "+str(match_galatians.group(1)),'Ephesians',"ephesians "+str(match_ephesians.group(1)),'Philippians',"philippians "+str(match_philippians.group(1)),'Colossians',"colossians "+str(match_colossians.group(1)),'1 Thessalonians',"first_thessalonians "+str(match_first_thessalonians.group(1)),'2 Thessalonians',"second_thessalonians "+str(match_second_thessalonians.group(1)),'1 Timothy',"first_timothy_"+str(match_first_timothy.group(1)),'2 Timothy',"second_timothy "+str(match_second_timothy.group(1)),'Titus',"titus_"+str(match_titus.group(1)),'Philemon','James',"james "+str(match_james.group(1)),'1 Peter',"first_peter_"+str(match_first_peter.group(1)),'2 Peter',"second_peter_"+str(match_second_peter.group(1)),'1 John',"first_john "+str(match_first_john.group(1)),'2 John','3 John',"third_john "+str(match_third_john.group(1)),'Jude','Ruth',"ruth "+str(match_ruth.group(1)),'Ezra',"ezra "+str(match_ezra.group(1)),'Esther',"esther "+str(match_esther.group(1)),'Song of Solomon',"song_of_solomon "+str(match_song_of_solomon.group(1)),'Lamentations',"lamentations "+str(match_lamentations.group(1)),'Joel',"joel "+str(match_joel.group(1)),'Amos',"amos "+str(match_amos.group(1)),'Obadiah','Jonah',"jonah "+str(match_jonah.group(1)),'Micah',"micah "+str(match_micah.group(1)),'Nahum',"nahum "+str(match_nahum.group(1)),'Habakkuk',"habakkuk "+str(match_habakkuk.group(1)),'Zephaniah',"zephaniah "+str(match_zephaniah.group(1)),'Haggai',"haggai "+str(match_haggai.group(1)),'Malachi',"malachi "+str(match_malachi.group(1)),'Jacob',"jacob "+str(match_jacob.group(1)),'Enos','Jarom','Omni','Words of Mormon','4 Nephi','Mormon',"mormon "+str(match_mormon.group(1)),'Moroni',"moroni "+str(match_moroni.group(1)),'Moses',"moses "+str(match_moses.group(1)),'Abraham',"abraham "+str(match_abraham.group(1)),'Facsimile',"facsimile"+str(match_facsimile.group(1)),'Joseph Smith-Matthew',"Joseph Smith History","Articles of Faith","Joseph Smith Translation","joseph_smith_translation "+str(match_joseph_smith_translation.group(1)),'Ten Commandments','Title Page of the Book of Mormon','Testimony of the Twelve Apostles from the Book of Mormon']
                    #from_10_to_20_name_list = ['Mark',"mark "+str(match_mark.group(1)),'Romans',"romans "+str(match_romans.group(1)),'1 Corinthians',"first_corinthians "+str(match_first_corinthians.group(1)),'2 Corinthians',"second_corinthians "+str(match_second_corinthians.group(1)),'Hebrews',"hebrews "+str(match_hebrews.group(1)),'Nehemiah',"nehemiah"+str(match_nehemiah.group(1)),'Ecclesiastes',"ecclesiastes "+str(match_ecclesiastes.group(1)),'Daniel',"daniel "+str(match_daniel.group(1)),'Hosea',"hosea"+str(match_hosea.group(1)),'Zechariah',"zechariah "+str(match_zechariah.group(1)),'Helaman',"helaman "+str(match_helaman.group(1)),'Ether',"ether "+str(match_ether.group(1))]
                    # from_20_to_30_name_list = ['Matthew',"matthew "+str(match_matthew.group(1)),'Luke',"luke "+str(match_luke.group(1)),'John',"john "+str(match_john.group(1)),'Acts',"acts "+str(match_acts.group(1)),'Revelation',"revelation "+str(match_revelation.group(1)),'Leviticus',"leviticus"+str(match_leviticus.group(1)),'Joshua',"joshua "+str(match_joshua.group(1)),'Judges',"judges "+str(match_judges.group(1)),'2 Samuel',"second_samuel"+str(match_second_samuel.group(1)),'1 Kings',"first_kings "+str(match_first_kings.group(1)),'2 Kings',"second_kings "+str(match_second_kings.group(1)),'1 Chronicles',"first_chronicles "+str(match_first_chronicles.group(1)),'1 Nephi',"first_nephi "+str(match_first_nephi.group(1)),'Mosiah',"mosiah"+str(match_mosiah.group(1)),'3 Nephi',"third_nephi"+str(match_third_nephi.group(1))]
                    #from_30_to_40_name_list = ['Exodus',"exodus"+str(match_exodus.group(1)),'Numbers',"numbers"+str(match_numbers.group(1)),'Deuteronomy',"deuteronomy "+str(match_deuteronomy.group(1)),'1 Samuel',"first_samuel "+str(match_first_samuel.group(1)),'2 Chronicles',"second_chronicles "+str(match_second_chronicles.group(1)),'Proverbs',"proverbs "+str(match_proverbs.group(1)),'2 Nephi',"second_nephi "+str(match_second_nephi.group(1))]
                    # from_40_to_200_name_list = ['Genesis',"genesis "+str(match_genesis.group(1)),'Job',"job "+str(match_job.group(1)),'Psalms',"psalms"+str(match_psalms.group(1)),'Isaiah',"isaiah"+str(match_isaiah.group(1)),'Jeremiah',"jeremiah "+str(match_jeremiah.group(1)),'Ezekiel',"ezekiel"+str(match_ezekiel.group(1)),'Alma',"alma"+str(match_alma.group(1)),"Book of Mormon","Bible","New Testament","Old Testament","Doctrine and Covenants","doctrine_and_covenants "+str(match_doctrine_and_covenants.group(1))]

                # from_1_to_10_name_list_small = ["galatians "+str(galatians_count_chapters),"ephesians "+str(ephesians_count_chapters),"philippians "+str(philippians_count_chapters),"colossians "+str(colossians_count_chapters),"first_thessalonians "+str(first_thessalonians_count_chapters),"second_thessalonians "+str(second_thessalonians_count_chapters),"first_timothy_"+str(first_timothy_count_chapters),"second_timothy "+str(second_timothy_count_chapters),"titus_"+str(titus_count_chapters),"james "+str(james_count_chapters),"first_peter_"+str(first_peter_count_chapters),"second_peter_"+str(second_peter_count_chapters),"first_john "+str(first_john_count_chapters),"ruth "+str(ruth_count_chapters),"ezra "+str(ezra_count_chapters),"esther "+str(esther_count_chapters),"song_of_solomon "+str(song_of_solomon_count_chapters),"lamentations "+str(lamentations_count_chapters),"joel "+str(joel_count_chapters),"amos "+str(amos_count_chapters),"jonah "+str(jonah_count_chapters),"micah "+str(micah_count_chapters),"nahum "+str(nahum_count_chapters),"habakkuk "+str(habakkuk_count_chapters),"zephaniah "+str(zephaniah_count_chapters),"haggai "+str(haggai_count_chapters),"malachi "+str(malachi_count_chapters),"jacob "+str(jacob_count_chapters),"mormon "+str(mormon_count_chapters),"moroni "+str(moroni_count_chapters),"moses "+str(moses_count_chapters),"abraham "+str(abraham_count_chapters),"facsimile"+str(facsimile_count_chapters)]
                

                if galatians_chapter != "":
                    from_1_to_10_name_dictionary["galatians"] = galatians_chapter
                if ephesians_chapter != "":
                    from_1_to_10_name_dictionary["ephesians"] = ephesians_chapter
                if philippians_chapter != "":
                    from_1_to_10_name_dictionary["philippians"] = philippians_chapter
                if colossians_chapter != "":
                    from_1_to_10_name_dictionary["colossians"] = colossians_chapter
                if first_thessalonians_chapter != "":
                    from_1_to_10_name_dictionary["first_thessalonians"] = first_thessalonians_chapter
                if second_thessalonians_chapter != "":
                    from_1_to_10_name_dictionary["second_thessalonians"] = second_thessalonians_chapter
                if first_timothy_chapter != "":
                    from_1_to_10_name_dictionary["first_timothy"] = first_timothy_chapter
                if second_timothy_chapter != "":
                    from_1_to_10_name_dictionary["second_timothy"] = second_timothy_chapter
                if titus_chapter != "":
                    from_1_to_10_name_dictionary["titus"] = titus_chapter
                if james_chapter != "":
                    from_1_to_10_name_dictionary["james"] = james_chapter
                if first_peter_chapter != "":
                    from_1_to_10_name_dictionary["first_peter"] = first_peter_chapter
                if second_peter_chapter != "":
                    from_1_to_10_name_dictionary["second_peter"] = second_peter_chapter
                if first_john_chapter != "":
                    from_1_to_10_name_dictionary["first_john"] = first_john_chapter
                if ruth_chapter != "":
                    from_1_to_10_name_dictionary["ruth"] = ruth_chapter
                if ezra_chapter != "":
                    from_1_to_10_name_dictionary["ezra"] = ezra_chapter
                if esther_chapter != "":
                    from_1_to_10_name_dictionary["esther"] = esther_chapter
                if song_of_solomon_chapter != "":
                    from_1_to_10_name_dictionary["song_of_solomon"] = song_of_solomon_chapter
                if lamentations_chapter != "":
                    from_1_to_10_name_dictionary["lamentations"] = lamentations_chapter
                if joel_chapter != "":
                    from_1_to_10_name_dictionary["joel"] = joel_chapter
                if amos_chapter != "":
                    from_1_to_10_name_dictionary["amos"] = amos_chapter
                if jonah_chapter != "":
                    from_1_to_10_name_dictionary["jonah"] = jonah_chapter
                if micah_chapter != "":
                    from_1_to_10_name_dictionary["micah"] = micah_chapter
                if nahum_chapter != "":
                    from_1_to_10_name_dictionary["nahum"] = nahum_chapter
                if habakkuk_chapter != "":
                    from_1_to_10_name_dictionary["habakkuk"] = habakkuk_chapter
                if zephaniah_chapter != "":
                    from_1_to_10_name_dictionary["zephaniah"] = zephaniah_chapter
                if haggai_chapter != "":
                    from_1_to_10_name_dictionary["haggai"] = haggai_chapter
                if malachi_chapter != "":
                    from_1_to_10_name_dictionary["malachi"] = malachi_chapter
                if jacob_chapter != "":
                    from_1_to_10_name_dictionary["jacob"] = jacob_chapter
                if mormon_chapter != "":
                    from_1_to_10_name_dictionary["mormon"] = mormon_chapter
                if moroni_chapter != "":
                    from_1_to_10_name_dictionary["moroni"] = moroni_chapter
                if moses_chapter != "":
                    from_1_to_10_name_dictionary["moses"] = moses_chapter
                if abraham_chapter != "":
                    from_1_to_10_name_dictionary["abraham"] = abraham_chapter
                if facsimile_chapter != "":
                    from_1_to_10_name_dictionary["facsimile"] = facsimile_chapter
                if joseph_smith_translation_chapter != "":
                    from_1_to_10_name_dictionary["joseph_smith_translation"] = joseph_smith_translation_chapter

                from_1_to_10_name_list_small.append(from_1_to_10_name_dictionary)

                #Scriptures with only one Chapter:
                #philemon
                #second_john
                #third_john
                #jude
                #obadiah
                #enos
                #jarom
                #omni
                #words_of_mormon
                #fourth_nephi
                #joseph_smith_matthew
                # and more...


                #from_10_to_20_name_dictionary = {}

                if mark_chapter != "":
                    from_10_to_20_name_dictionary["mark"] = mark_chapter
                if romans_chapter != "":
                    from_10_to_20_name_dictionary["romans"] = romans_chapter
                if first_corinthians_chapter != "":
                    from_10_to_20_name_dictionary["first_corinthians"] = first_corinthians_chapter
                if second_corinthians_chapter != "":
                    from_10_to_20_name_dictionary["second_corinthians"] = second_corinthians_chapter
                if hebrews_chapter != "":
                    from_10_to_20_name_dictionary["hebrews"] = hebrews_chapter
                if nehemiah_chapter != "":
                    from_10_to_20_name_dictionary["nehemiah"] = nehemiah_chapter
                if ecclesiastes_chapter != "":
                    from_10_to_20_name_dictionary["ecclesiastes"] = ecclesiastes_chapter
                if daniel_chapter != "":
                    from_10_to_20_name_dictionary["daniel"] = daniel_chapter
                if hosea_chapter != "":
                    from_10_to_20_name_dictionary["hosea"] = hosea_chapter
                if zechariah_chapter != "":
                    from_10_to_20_name_dictionary["zechariah"] = zechariah_chapter
                if helaman_chapter != "":
                    from_10_to_20_name_dictionary["helaman"] = helaman_chapter
                if ether_chapter != "":
                    from_10_to_20_name_dictionary["ether"] = ether_chapter
                from_10_to_20_name_list_small.append(from_10_to_20_name_dictionary)
                #print(from_10_to_20_name_list_small)
                

                if matthew_chapter != "":
                    from_20_to_30_name_dictionary["matthew"] = matthew_chapter
                if luke_chapter != "":
                    from_20_to_30_name_dictionary["luke"] = luke_chapter
                if john_chapter != "":
                    from_20_to_30_name_dictionary["john"] = john_chapter
                if acts_chapter != "":
                    from_20_to_30_name_dictionary["acts"] = acts_chapter
                if revelation_chapter != "":
                    from_20_to_30_name_dictionary["revelation"] = revelation_chapter
                if leviticus_chapter != "":
                    from_20_to_30_name_dictionary["leviticus"] = leviticus_chapter
                if joshua_chapter != "":
                    from_20_to_30_name_dictionary["joshua"] = joshua_chapter
                if judges_chapter != "":
                    from_20_to_30_name_dictionary["judges"] = judges_chapter
                if second_samuel_chapter != "":
                    from_20_to_30_name_dictionary["second_samuel"] = second_samuel_chapter
                if first_kings_chapter != "":
                    from_20_to_30_name_dictionary["first_kings"] = first_kings_chapter
                if second_kings_chapter != "":
                    from_20_to_30_name_dictionary["second_kings"] = second_kings_chapter
                if first_chronicles_chapter != "":
                    from_20_to_30_name_dictionary["first_chronicles"] = first_chronicles_chapter
                if first_nephi_chapter != "":
                    from_20_to_30_name_dictionary["first_nephi"] = first_nephi_chapter
                if mosiah_chapter != "":
                    from_20_to_30_name_dictionary["mosiah"] = mosiah_chapter
                if third_nephi_chapter != "":
                    from_20_to_30_name_dictionary["third_nephi"] = third_nephi_chapter
                from_20_to_30_name_list_small.append(from_20_to_30_name_dictionary)

                if exodus_chapter != "":
                    from_30_to_40_name_dictionary["exodus"] = exodus_chapter
                if numbers_chapter != "":
                    from_30_to_40_name_dictionary["numbers"] = numbers_chapter
                if deuteronomy_chapter != "":
                    from_30_to_40_name_dictionary["deuteronomy"] = deuteronomy_chapter
                if first_samuel_chapter != "":
                    from_30_to_40_name_dictionary["first_samuel"] = first_samuel_chapter
                if second_chronicles_chapter != "":
                    from_30_to_40_name_dictionary["second_chronicles"] = second_chronicles_chapter
                if proverbs_chapter != "":
                    from_30_to_40_name_dictionary["proverbs"] = proverbs_chapter
                if second_nephi_chapter != "":
                    from_30_to_40_name_dictionary["second_nephi"] = second_nephi_chapter
                from_30_to_40_name_list_small.append(from_30_to_40_name_dictionary)

                if genesis_chapter != "":
                    from_40_to_200_name_dictionary["genesis"] = genesis_chapter
                if job_chapter != "":
                    from_40_to_200_name_dictionary["job"] = job_chapter
                if psalms_chapter != "":
                    from_40_to_200_name_dictionary["psalms"] = psalms_chapter
                if isaiah_chapter != "":
                    from_40_to_200_name_dictionary["isaiah"] = isaiah_chapter
                if jeremiah_chapter != "":
                    from_40_to_200_name_dictionary["jeremiah"] = jeremiah_chapter
                if ezekiel_chapter != "":
                    from_40_to_200_name_dictionary["ezekiel"] = ezekiel_chapter
                if alma_chapter != "":
                    from_40_to_200_name_dictionary["alma"] = alma_chapter
                if doctrine_and_covenants_chapter != "":
                    from_40_to_200_name_dictionary["doctrine_and_covenants"] = doctrine_and_covenants_chapter
                from_40_to_200_name_list_small.append(from_40_to_200_name_dictionary)









        #Spread 1 to 10
            #Spread Galatians
            unique_spread_galatians_chapters_list = []
            for galatians_dictionary in from_1_to_10_name_list_small:
                if "galatians" in galatians_dictionary:
                    galatians_chapter_value = galatians_dictionary["galatians"]
                    galatians_chapter_value_list.append(int(galatians_chapter_value))
            if galatians_chapter_value_list != []:
                int_set = set(galatians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Galatians "+str(chapter_values) not in unique_spread_galatians_chapters_list:
                            unique_spread_galatians_chapters_list.append("Galatians "+str(chapter_values))
                        if "Galatians "+str(chapter_values+2) not in unique_spread_galatians_chapters_list:
                            unique_spread_galatians_chapters_list.append("Galatians "+str(chapter_values+2))
                if len(unique_spread_galatians_chapters_list) > 1:
                    print("Galatians"+"+"+str(numbers_value))

            #Spread Ephesians
            unique_spread_ephesians_chapters_list = []
            for ephesians_dictionary in from_1_to_10_name_list_small:
                if "ephesians" in ephesians_dictionary:
                    ephesians_chapter_value = ephesians_dictionary["ephesians"]
                    ephesians_chapter_value_list.append(int(ephesians_chapter_value))
            if ephesians_chapter_value_list != []:
                int_set = set(ephesians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Ephesians "+str(chapter_values) not in unique_spread_ephesians_chapters_list:
                            unique_spread_ephesians_chapters_list.append("Ephesians "+str(chapter_values))
                        if "Ephesians "+str(chapter_values+2) not in unique_spread_ephesians_chapters_list:
                            unique_spread_ephesians_chapters_list.append("Ephesians "+str(chapter_values+2))
                if len(unique_spread_ephesians_chapters_list) > 1:
                    print("Ephesians"+"+"+str(numbers_value))
            
            #Spread Philippians
            unique_spread_philippians_chapters_list = []
            for philippians_dictionary in from_1_to_10_name_list_small:
                if "philippians" in philippians_dictionary:
                    philippians_chapter_value = philippians_dictionary["philippians"]
                    philippians_chapter_value_list.append(int(philippians_chapter_value))
            if philippians_chapter_value_list != []:
                int_set = set(philippians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Philippians "+str(chapter_values) not in unique_spread_philippians_chapters_list:
                            unique_spread_philippians_chapters_list.append("Philippians "+str(chapter_values))
                        if "Philippians "+str(chapter_values+2) not in unique_spread_philippians_chapters_list:
                            unique_spread_philippians_chapters_list.append("Philippians "+str(chapter_values+2))
                if len(unique_spread_philippians_chapters_list) > 1:
                    print("Philippians"+"+"+str(numbers_value))
            

            #Spread Colossians
            unique_spread_colossians_chapters_list = []
            for colossians_dictionary in from_1_to_10_name_list_small:
                if "colossians" in colossians_dictionary:
                    colossians_chapter_value = colossians_dictionary["colossians"]
                    colossians_chapter_value_list.append(int(colossians_chapter_value))
            if colossians_chapter_value_list != []:
                int_set = set(colossians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Colossians "+str(chapter_values) not in unique_spread_colossians_chapters_list:
                            unique_spread_colossians_chapters_list.append("Colossians "+str(chapter_values))
                        if "Colossians "+str(chapter_values+2) not in unique_spread_colossians_chapters_list:
                            unique_spread_colossians_chapters_list.append("Colossians "+str(chapter_values+2))
                if len(unique_spread_colossians_chapters_list) > 1:
                    print("Colossians"+"+"+str(numbers_value))

            #Spread First Thessalonians
            unique_spread_first_thessalonians_chapters_list = []
            for first_thessalonians_dictionary in from_1_to_10_name_list_small:
                if "first_thessalonians" in first_thessalonians_dictionary:
                    first_thessalonians_chapter_value = first_thessalonians_dictionary["first_thessalonians"]
                    first_thessalonians_chapter_value_list.append(int(first_thessalonians_chapter_value))
            if first_thessalonians_chapter_value_list != []:
                int_set = set(first_thessalonians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "first_thessalonians "+str(chapter_values) not in unique_spread_first_thessalonians_chapters_list:
                            unique_spread_first_thessalonians_chapters_list.append("first_thessalonians "+str(chapter_values))
                        if "first_thessalonians "+str(chapter_values+2) not in unique_spread_first_thessalonians_chapters_list:
                            unique_spread_first_thessalonians_chapters_list.append("first_thessalonians "+str(chapter_values+2))
                if len(unique_spread_first_thessalonians_chapters_list) > 1:
                    print("first_thessalonians"+"+"+str(numbers_value))

            #Spread Second Thessalonians
            unique_spread_second_thessalonians_chapters_list = []
            for second_thessalonians_dictionary in from_1_to_10_name_list_small:
                if "second_thessalonians" in second_thessalonians_dictionary:
                    second_thessalonians_chapter_value = second_thessalonians_dictionary["second_thessalonians"]
                    second_thessalonians_chapter_value_list.append(int(second_thessalonians_chapter_value))
            if second_thessalonians_chapter_value_list != []:
                int_set = set(second_thessalonians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "second_thessalonians "+str(chapter_values) not in unique_spread_second_thessalonians_chapters_list:
                            unique_spread_second_thessalonians_chapters_list.append("second_thessalonians "+str(chapter_values))
                        if "second_thessalonians "+str(chapter_values+2) not in unique_spread_second_thessalonians_chapters_list:
                            unique_spread_second_thessalonians_chapters_list.append("second_thessalonians "+str(chapter_values+2))
                if len(unique_spread_second_thessalonians_chapters_list) > 1:
                    print("second_thessalonians"+"+"+str(numbers_value))


            #Spread First Timothy
            unique_spread_first_timothy_chapters_list = []
            for first_timothy_dictionary in from_1_to_10_name_list_small:
                if "first_timothy" in first_timothy_dictionary:
                    first_timothy_chapter_value = first_timothy_dictionary["first_timothy"]
                    first_timothy_chapter_value_list.append(int(first_timothy_chapter_value))
            if first_timothy_chapter_value_list != []:
                int_set = set(first_timothy_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "first_timothy "+str(chapter_values) not in unique_spread_first_timothy_chapters_list:
                            unique_spread_first_timothy_chapters_list.append("first_timothy "+str(chapter_values))
                        if "first_timothy "+str(chapter_values+2) not in unique_spread_first_timothy_chapters_list:
                            unique_spread_first_timothy_chapters_list.append("first_timothy "+str(chapter_values+2))
                if len(unique_spread_first_timothy_chapters_list) > 1:
                    print("first_timothy"+"+"+str(numbers_value))
            
            #Spread Second Timothy
            unique_spread_second_timothy_chapters_list = []
            for second_timothy_dictionary in from_1_to_10_name_list_small:
                if "second_timothy" in second_timothy_dictionary:
                    second_timothy_chapter_value = second_timothy_dictionary["second_timothy"]
                    second_timothy_chapter_value_list.append(int(second_timothy_chapter_value))
            if second_timothy_chapter_value_list != []:
                int_set = set(second_timothy_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "second_timothy "+str(chapter_values) not in unique_spread_second_timothy_chapters_list:
                            unique_spread_second_timothy_chapters_list.append("second_timothy "+str(chapter_values))
                        if "second_timothy "+str(chapter_values+2) not in unique_spread_second_timothy_chapters_list:
                            unique_spread_second_timothy_chapters_list.append("second_timothy "+str(chapter_values+2))
                if len(unique_spread_second_timothy_chapters_list) > 1:
                    print("second_timothy"+"+"+str(numbers_value))

            #Spread Titus
            unique_spread_titus_chapters_list = []
            for titus_dictionary in from_1_to_10_name_list_small:
                if "titus" in titus_dictionary:
                    titus_chapter_value = titus_dictionary["titus"]
                    titus_chapter_value_list.append(int(titus_chapter_value))
            if titus_chapter_value_list != []:
                int_set = set(titus_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "titus "+str(chapter_values) not in unique_spread_titus_chapters_list:
                            unique_spread_titus_chapters_list.append("titus "+str(chapter_values))
                        if "titus "+str(chapter_values+2) not in unique_spread_titus_chapters_list:
                            unique_spread_titus_chapters_list.append("titus "+str(chapter_values+2))
                if len(unique_spread_titus_chapters_list) > 1:
                    print("titus"+"+"+str(numbers_value))
            
            #Spread James
            unique_spread_james_chapters_list = []
            for james_dictionary in from_1_to_10_name_list_small:
                if "james" in james_dictionary:
                    james_chapter_value = james_dictionary["james"]
                    james_chapter_value_list.append(int(james_chapter_value))
            if james_chapter_value_list != []:
                int_set = set(james_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "james "+str(chapter_values) not in unique_spread_james_chapters_list:
                            unique_spread_james_chapters_list.append("james "+str(chapter_values))
                        if "james "+str(chapter_values+2) not in unique_spread_james_chapters_list:
                            unique_spread_james_chapters_list.append("james "+str(chapter_values+2))
                if len(unique_spread_james_chapters_list) > 1:
                    print("james"+"+"+str(numbers_value))


            #Spread First Peter
            unique_spread_first_peter_chapters_list = []
            for first_peter_dictionary in from_1_to_10_name_list_small:
                if "first_peter" in first_peter_dictionary:
                    first_peter_chapter_value = first_peter_dictionary["first_peter"]
                    first_peter_chapter_value_list.append(int(first_peter_chapter_value))
            if first_peter_chapter_value_list != []:
                int_set = set(first_peter_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "first_peter "+str(chapter_values) not in unique_spread_first_peter_chapters_list:
                            unique_spread_first_peter_chapters_list.append("first_peter "+str(chapter_values))
                        if "first_peter "+str(chapter_values+2) not in unique_spread_first_peter_chapters_list:
                            unique_spread_first_peter_chapters_list.append("first_peter "+str(chapter_values+2))
                if len(unique_spread_first_peter_chapters_list) > 1:
                    print("first_peter"+"+"+str(numbers_value))

            #Spread Second Peter
            unique_spread_second_peter_chapters_list = []
            for second_peter_dictionary in from_1_to_10_name_list_small:
                if "second_peter" in second_peter_dictionary:
                    second_peter_chapter_value = second_peter_dictionary["second_peter"]
                    second_peter_chapter_value_list.append(int(second_peter_chapter_value))
            if second_peter_chapter_value_list != []:
                int_set = set(second_peter_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "second_peter "+str(chapter_values) not in unique_spread_second_peter_chapters_list:
                            unique_spread_second_peter_chapters_list.append("second_peter "+str(chapter_values))
                        if "second_peter "+str(chapter_values+2) not in unique_spread_second_peter_chapters_list:
                            unique_spread_second_peter_chapters_list.append("second_peter "+str(chapter_values+2))
                if len(unique_spread_second_peter_chapters_list) > 1:
                    print("second_peter"+"+"+str(numbers_value))

            #Spread First John
            unique_spread_first_john_chapters_list = []
            for first_john_dictionary in from_1_to_10_name_list_small:
                if "first_john" in first_john_dictionary:
                    first_john_chapter_value = first_john_dictionary["first_john"]
                    first_john_chapter_value_list.append(int(first_john_chapter_value))
            if first_john_chapter_value_list != []:
                int_set = set(first_john_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "first_john "+str(chapter_values) not in unique_spread_first_john_chapters_list:
                            unique_spread_first_john_chapters_list.append("first_john "+str(chapter_values))
                        if "first_john "+str(chapter_values+2) not in unique_spread_first_john_chapters_list:
                            unique_spread_first_john_chapters_list.append("first_john "+str(chapter_values+2))
                if len(unique_spread_first_john_chapters_list) > 1:
                    print("first_john"+"+"+str(numbers_value))
            # Note: only one chapter in third John
            #Spread Third John
            # unique_spread_third_john_chapters_list = []
            # for third_john_dictionary in from_1_to_10_name_list_small:
            #     if "third_john" in third_john_dictionary:
            #         third_john_chapter_value = third_john_dictionary["third_john"]
            #         third_john_chapter_value_list.append(int(third_john_chapter_value))
            # if third_john_chapter_value_list != []:
            #     int_set = set(third_john_chapter_value_list)
            #     for chapter_values in int_set:
            #         if chapter_values + 2 in int_set:
            #             #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
            #             if "third_john "+str(chapter_values) not in unique_spread_third_john_chapters_list:
            #                 unique_spread_third_john_chapters_list.append("third_john "+str(chapter_values))
            #             if "third_john "+str(chapter_values+2) not in unique_spread_third_john_chapters_list:
            #                 unique_spread_third_john_chapters_list.append("third_john "+str(chapter_values+2))
            #     if len(unique_spread_third_john_chapters_list) > 1:
            #         print("third_john")

            
            #Spread Ruth
            unique_spread_ruth_chapters_list = []
            for ruth_dictionary in from_1_to_10_name_list_small:
                if "ruth" in ruth_dictionary:
                    ruth_chapter_value = ruth_dictionary["ruth"]
                    ruth_chapter_value_list.append(int(ruth_chapter_value))
            if ruth_chapter_value_list != []:
                int_set = set(ruth_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "ruth "+str(chapter_values) not in unique_spread_ruth_chapters_list:
                            unique_spread_ruth_chapters_list.append("ruth "+str(chapter_values))
                        if "ruth "+str(chapter_values+2) not in unique_spread_ruth_chapters_list:
                            unique_spread_ruth_chapters_list.append("ruth "+str(chapter_values+2))
                if len(unique_spread_ruth_chapters_list) > 1:
                    print("ruth"+"+"+str(numbers_value))
            

            #Spread Ezra
            unique_spread_ezra_chapters_list = []
            for ezra_dictionary in from_1_to_10_name_list_small:
                if "ezra" in ezra_dictionary:
                    ezra_chapter_value = ezra_dictionary["ezra"]
                    ezra_chapter_value_list.append(int(ezra_chapter_value))
            if ezra_chapter_value_list != []:
                int_set = set(ezra_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "ezra "+str(chapter_values) not in unique_spread_ezra_chapters_list:
                            unique_spread_ezra_chapters_list.append("ezra "+str(chapter_values))
                        if "ezra "+str(chapter_values+2) not in unique_spread_ezra_chapters_list:
                            unique_spread_ezra_chapters_list.append("ezra "+str(chapter_values+2))
                if len(unique_spread_ezra_chapters_list) > 1:
                    print("ezra"+"+"+str(numbers_value))

            #Spread Esther
            unique_spread_esther_chapters_list = []
            for esther_dictionary in from_1_to_10_name_list_small:
                if "esther" in esther_dictionary:
                    esther_chapter_value = esther_dictionary["esther"]
                    esther_chapter_value_list.append(int(esther_chapter_value))
            if esther_chapter_value_list != []:
                int_set = set(esther_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "esther "+str(chapter_values) not in unique_spread_esther_chapters_list:
                            unique_spread_esther_chapters_list.append("esther "+str(chapter_values))
                        if "esther "+str(chapter_values+2) not in unique_spread_esther_chapters_list:
                            unique_spread_esther_chapters_list.append("esther "+str(chapter_values+2))
                if len(unique_spread_esther_chapters_list) > 1:
                    print("Esther"+"+"+str(numbers_value))
            
            #Spread Song of Solomon
            unique_spread_song_of_solomon_chapters_list = []
            for song_of_solomon_dictionary in from_1_to_10_name_list_small:
                if "song_of_solomon" in song_of_solomon_dictionary:
                    song_of_solomon_chapter_value = song_of_solomon_dictionary["song_of_solomon"]
                    song_of_solomon_chapter_value_list.append(int(song_of_solomon_chapter_value))
            if song_of_solomon_chapter_value_list != []:
                int_set = set(song_of_solomon_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "song_of_solomon "+str(chapter_values) not in unique_spread_song_of_solomon_chapters_list:
                            unique_spread_song_of_solomon_chapters_list.append("song_of_solomon "+str(chapter_values))
                        if "song_of_solomon "+str(chapter_values+2) not in unique_spread_song_of_solomon_chapters_list:
                            unique_spread_song_of_solomon_chapters_list.append("song_of_solomon "+str(chapter_values+2))
                if len(unique_spread_song_of_solomon_chapters_list) > 1:
                    print("Song of solomon"+"+"+str(numbers_value))

            
            #Spread Lamentations
            unique_spread_lamentations_chapters_list = []
            for lamentations_dictionary in from_1_to_10_name_list_small:
                if "lamentations" in lamentations_dictionary:
                    lamentations_chapter_value = lamentations_dictionary["lamentations"]
                    lamentations_chapter_value_list.append(int(lamentations_chapter_value))
            if lamentations_chapter_value_list != []:
                int_set = set(lamentations_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "lamentations "+str(chapter_values) not in unique_spread_lamentations_chapters_list:
                            unique_spread_lamentations_chapters_list.append("lamentations "+str(chapter_values))
                        if "lamentations "+str(chapter_values+2) not in unique_spread_lamentations_chapters_list:
                            unique_spread_lamentations_chapters_list.append("lamentations "+str(chapter_values+2))
                if len(unique_spread_lamentations_chapters_list) > 1:
                    print("Lamentations"+"+"+str(numbers_value))

            #Spread Joel
            unique_spread_joel_chapters_list = []
            for joel_dictionary in from_1_to_10_name_list_small:
                if "joel" in joel_dictionary:
                    joel_chapter_value = joel_dictionary["joel"]
                    joel_chapter_value_list.append(int(joel_chapter_value))
            if joel_chapter_value_list != []:
                int_set = set(joel_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "joel "+str(chapter_values) not in unique_spread_joel_chapters_list:
                            unique_spread_joel_chapters_list.append("joel "+str(chapter_values))
                        if "joel "+str(chapter_values+2) not in unique_spread_joel_chapters_list:
                            unique_spread_joel_chapters_list.append("joel "+str(chapter_values+2))
                if len(unique_spread_joel_chapters_list) > 1:
                    print("Joel"+"+"+str(numbers_value))
            
            #Spread Amos
            unique_spread_amos_chapters_list = []
            for amos_dictionary in from_1_to_10_name_list_small:
                if "amos" in amos_dictionary:
                    amos_chapter_value = amos_dictionary["amos"]
                    amos_chapter_value_list.append(int(amos_chapter_value))
            if amos_chapter_value_list != []:
                int_set = set(amos_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "amos "+str(chapter_values) not in unique_spread_amos_chapters_list:
                            unique_spread_amos_chapters_list.append("amos "+str(chapter_values))
                        if "amos "+str(chapter_values+2) not in unique_spread_amos_chapters_list:
                            unique_spread_amos_chapters_list.append("amos "+str(chapter_values+2))
                if len(unique_spread_amos_chapters_list) > 1:
                    print("Amos"+"+"+str(numbers_value))

            #Spread Jonah
            unique_spread_jonah_chapters_list = []
            for jonah_dictionary in from_1_to_10_name_list_small:
                if "jonah" in jonah_dictionary:
                    jonah_chapter_value = jonah_dictionary["jonah"]
                    jonah_chapter_value_list.append(int(jonah_chapter_value))
            if jonah_chapter_value_list != []:
                int_set = set(jonah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "jonah "+str(chapter_values) not in unique_spread_jonah_chapters_list:
                            unique_spread_jonah_chapters_list.append("jonah "+str(chapter_values))
                        if "jonah "+str(chapter_values+2) not in unique_spread_jonah_chapters_list:
                            unique_spread_jonah_chapters_list.append("jonah "+str(chapter_values+2))
                if len(unique_spread_jonah_chapters_list) > 1:
                    print("Jonah"+"+"+str(numbers_value))
            
            #Spread Micah
            unique_spread_micah_chapters_list = []
            for micah_dictionary in from_1_to_10_name_list_small:
                if "micah" in micah_dictionary:
                    micah_chapter_value = micah_dictionary["micah"]
                    micah_chapter_value_list.append(int(micah_chapter_value))
            if micah_chapter_value_list != []:
                int_set = set(micah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "micah "+str(chapter_values) not in unique_spread_micah_chapters_list:
                            unique_spread_micah_chapters_list.append("micah "+str(chapter_values))
                        if "micah "+str(chapter_values+2) not in unique_spread_micah_chapters_list:
                            unique_spread_micah_chapters_list.append("micah "+str(chapter_values+2))
                if len(unique_spread_micah_chapters_list) > 1:
                    print("Micah"+"+"+str(numbers_value))
            
            #Spread Nahum
            unique_spread_nahum_chapters_list = []
            for nahum_dictionary in from_1_to_10_name_list_small:
                if "nahum" in nahum_dictionary:
                    nahum_chapter_value = nahum_dictionary["nahum"]
                    nahum_chapter_value_list.append(int(nahum_chapter_value))
            if nahum_chapter_value_list != []:
                int_set = set(nahum_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "nahum "+str(chapter_values) not in unique_spread_nahum_chapters_list:
                            unique_spread_nahum_chapters_list.append("nahum "+str(chapter_values))
                        if "nahum "+str(chapter_values+2) not in unique_spread_nahum_chapters_list:
                            unique_spread_nahum_chapters_list.append("nahum "+str(chapter_values+2))
                if len(unique_spread_nahum_chapters_list) > 1:
                    print("Nahum"+"+"+str(numbers_value))

            #Spread Habakkuk
            unique_spread_habakkuk_chapters_list = []
            for habakkuk_dictionary in from_1_to_10_name_list_small:
                if "habakkuk" in habakkuk_dictionary:
                    habakkuk_chapter_value = habakkuk_dictionary["habakkuk"]
                    habakkuk_chapter_value_list.append(int(habakkuk_chapter_value))
            if habakkuk_chapter_value_list != []:
                int_set = set(habakkuk_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "habakkuk "+str(chapter_values) not in unique_spread_habakkuk_chapters_list:
                            unique_spread_habakkuk_chapters_list.append("habakkuk "+str(chapter_values))
                        if "habakkuk "+str(chapter_values+2) not in unique_spread_habakkuk_chapters_list:
                            unique_spread_habakkuk_chapters_list.append("habakkuk "+str(chapter_values+2))
                if len(unique_spread_habakkuk_chapters_list) > 1:
                    print("Habakkuk"+"+"+str(numbers_value))


            #Spread Zephaniah
            unique_spread_zephaniah_chapters_list = []
            for zephaniah_dictionary in from_1_to_10_name_list_small:
                if "zephaniah" in zephaniah_dictionary:
                    zephaniah_chapter_value = zephaniah_dictionary["zephaniah"]
                    zephaniah_chapter_value_list.append(int(zephaniah_chapter_value))
            if zephaniah_chapter_value_list != []:
                int_set = set(zephaniah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "zephaniah "+str(chapter_values) not in unique_spread_zephaniah_chapters_list:
                            unique_spread_zephaniah_chapters_list.append("zephaniah "+str(chapter_values))
                        if "zephaniah "+str(chapter_values+2) not in unique_spread_zephaniah_chapters_list:
                            unique_spread_zephaniah_chapters_list.append("zephaniah "+str(chapter_values+2))
                if len(unique_spread_zephaniah_chapters_list) > 1:
                    print("Zephaniah"+"+"+str(numbers_value))

            #Note: for some reason haggai doesn't appear
            #Spread Haggai
            unique_spread_haggai_chapters_list = []
            for haggai_dictionary in from_1_to_10_name_list_small:
                if "haggai" in haggai_dictionary:
                    haggai_chapter_value = haggai_dictionary["haggai"]
                    #print("haggai running"+str(haggai_chapter_value))
                    haggai_chapter_value_list.append(int(haggai_chapter_value))
            if haggai_chapter_value_list != []:
                int_set = set(haggai_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "haggai "+str(chapter_values) not in unique_spread_haggai_chapters_list:
                            unique_spread_haggai_chapters_list.append("haggai "+str(chapter_values))
                        if "haggai "+str(chapter_values+2) not in unique_spread_haggai_chapters_list:
                            unique_spread_haggai_chapters_list.append("haggai "+str(chapter_values+2))
                if len(unique_spread_haggai_chapters_list) > 1:
                    print("Haggai"+"+"+str(numbers_value))

            #Note: for some reason returns none of malachi?
            #Spread Malachi
            unique_spread_malachi_chapters_list = []
            for malachi_dictionary in from_1_to_10_name_list_small:
                if "malachi" in malachi_dictionary:
                    malachi_chapter_value = malachi_dictionary["malachi"]
                    malachi_chapter_value_list.append(int(malachi_chapter_value))
            if malachi_chapter_value_list != []:
                int_set = set(malachi_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "malachi "+str(chapter_values) not in unique_spread_malachi_chapters_list:
                            unique_spread_malachi_chapters_list.append("malachi "+str(chapter_values))
                        if "malachi "+str(chapter_values+2) not in unique_spread_malachi_chapters_list:
                            unique_spread_malachi_chapters_list.append("malachi "+str(chapter_values+2))
                if len(unique_spread_malachi_chapters_list) > 1:
                    print("Malachi"+"+"+str(numbers_value))

            #Spread Jacob
            unique_spread_jacob_chapters_list = []
            for jacob_dictionary in from_1_to_10_name_list_small:
                if "jacob" in jacob_dictionary:
                    jacob_chapter_value = jacob_dictionary["jacob"]
                    jacob_chapter_value_list.append(int(jacob_chapter_value))
            if jacob_chapter_value_list != []:
                int_set = set(jacob_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "jacob "+str(chapter_values) not in unique_spread_jacob_chapters_list:
                            unique_spread_jacob_chapters_list.append("jacob "+str(chapter_values))
                        if "jacob "+str(chapter_values+2) not in unique_spread_jacob_chapters_list:
                            unique_spread_jacob_chapters_list.append("jacob "+str(chapter_values+2))
                if len(unique_spread_jacob_chapters_list) > 1:
                    print("Jacob"+"+"+str(numbers_value))


            #Spread Mormon
            unique_spread_mormon_chapters_list = []
            for mormon_dictionary in from_1_to_10_name_list_small:
                if "mormon" in mormon_dictionary:
                    mormon_chapter_value = mormon_dictionary["mormon"]
                    mormon_chapter_value_list.append(int(mormon_chapter_value))
            if mormon_chapter_value_list != []:
                int_set = set(mormon_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "mormon "+str(chapter_values) not in unique_spread_mormon_chapters_list:
                            unique_spread_mormon_chapters_list.append("mormon "+str(chapter_values))
                        if "mormon "+str(chapter_values+2) not in unique_spread_mormon_chapters_list:
                            unique_spread_mormon_chapters_list.append("mormon "+str(chapter_values+2))
                if len(unique_spread_mormon_chapters_list) > 1:
                    print("Mormon"+"+"+str(numbers_value))

            #Spread Moroni
            unique_spread_moroni_chapters_list = []
            for moroni_dictionary in from_1_to_10_name_list_small:
                if "moroni" in moroni_dictionary:
                    moroni_chapter_value = moroni_dictionary["moroni"]
                    moroni_chapter_value_list.append(int(moroni_chapter_value))
            if moroni_chapter_value_list != []:
                int_set = set(moroni_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "moroni "+str(chapter_values) not in unique_spread_moroni_chapters_list:
                            unique_spread_moroni_chapters_list.append("moroni "+str(chapter_values))
                        if "moroni "+str(chapter_values+2) not in unique_spread_moroni_chapters_list:
                            unique_spread_moroni_chapters_list.append("moroni "+str(chapter_values+2))
                if len(unique_spread_moroni_chapters_list) > 1:
                    print("Moroni"+"+"+str(numbers_value))

            #Spread Moses
            unique_spread_moses_chapters_list = []
            for moses_dictionary in from_1_to_10_name_list_small:
                if "moses" in moses_dictionary:
                    moses_chapter_value = moses_dictionary["moses"]
                    moses_chapter_value_list.append(int(moses_chapter_value))
            if moses_chapter_value_list != []:
                int_set = set(moses_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "moses "+str(chapter_values) not in unique_spread_moses_chapters_list:
                            unique_spread_moses_chapters_list.append("moses "+str(chapter_values))
                        if "moses "+str(chapter_values+2) not in unique_spread_moses_chapters_list:
                            unique_spread_moses_chapters_list.append("moses "+str(chapter_values+2))
                if len(unique_spread_moses_chapters_list) > 1:
                    print("Moses"+"+"+str(numbers_value))

            #Spread Abraham
            unique_spread_abraham_chapters_list = []
            for abraham_dictionary in from_1_to_10_name_list_small:
                if "abraham" in abraham_dictionary:
                    abraham_chapter_value = abraham_dictionary["abraham"]
                    abraham_chapter_value_list.append(int(abraham_chapter_value))
            if abraham_chapter_value_list != []:
                int_set = set(abraham_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Abraham "+str(chapter_values) not in unique_spread_abraham_chapters_list:
                            unique_spread_abraham_chapters_list.append("Abraham "+str(chapter_values))
                        if "Abraham "+str(chapter_values+2) not in unique_spread_abraham_chapters_list:
                            unique_spread_abraham_chapters_list.append("Abraham "+str(chapter_values+2))
                if len(unique_spread_abraham_chapters_list) > 1:
                    print("Abraham"+"+"+str(numbers_value))

            #Spread Facsimile
            unique_spread_facsimile_chapters_list = []
            for facsimile_dictionary in from_1_to_10_name_list_small:
                if "facsimile" in facsimile_dictionary:
                    facsimile_chapter_value = facsimile_dictionary["facsimile"]
                    facsimile_chapter_value_list.append(int(facsimile_chapter_value))
            if facsimile_chapter_value_list != []:
                int_set = set(facsimile_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "facsimile "+str(chapter_values) not in unique_spread_facsimile_chapters_list:
                            unique_spread_facsimile_chapters_list.append("facsimile "+str(chapter_values))
                        if "facsimile "+str(chapter_values+2) not in unique_spread_facsimile_chapters_list:
                            unique_spread_facsimile_chapters_list.append("facsimile "+str(chapter_values+2))
                if len(unique_spread_facsimile_chapters_list) > 1:
                    print("Facsimile"+"+"+str(numbers_value))

            #Spread Joseph Smith Translation
            unique_spread_joseph_smith_translation_chapters_list = []
            for joseph_smith_translation_dictionary in from_1_to_10_name_list_small:
                if "joseph_smith_translation" in joseph_smith_translation_dictionary:
                    joseph_smith_translation_chapter_value = joseph_smith_translation_dictionary["joseph_smith_translation"]
                    joseph_smith_translation_chapter_value_list.append(int(joseph_smith_translation_chapter_value))
            if joseph_smith_translation_chapter_value_list != []:
                int_set = set(joseph_smith_translation_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "joseph_smith_translation "+str(chapter_values) not in unique_spread_joseph_smith_translation_chapters_list:
                            unique_spread_joseph_smith_translation_chapters_list.append("joseph_smith_translation "+str(chapter_values))
                        if "joseph_smith_translation "+str(chapter_values+2) not in unique_spread_joseph_smith_translation_chapters_list:
                            unique_spread_joseph_smith_translation_chapters_list.append("joseph_smith_translation "+str(chapter_values+2))
                if len(unique_spread_joseph_smith_translation_chapters_list) > 1:
                    print("Joseph Smith Translation"+"+"+str(numbers_value))
            
            
        #Spread 10 to 20
            #Spread Mark
            unique_spread_mark_chapters_list = []
            for mark_dictionary in from_10_to_20_name_list_small:
                if "mark" in mark_dictionary:
                    mark_chapter_value = mark_dictionary["mark"]
                    mark_chapter_value_list.append(int(mark_chapter_value))
            if mark_chapter_value_list != []:
                int_set = set(mark_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Mark "+str(chapter_values) not in unique_spread_mark_chapters_list:
                            unique_spread_mark_chapters_list.append("Mark "+str(chapter_values))
                        if "Mark "+str(chapter_values+2) not in unique_spread_mark_chapters_list:
                            unique_spread_mark_chapters_list.append("Mark "+str(chapter_values+2))
                if len(unique_spread_mark_chapters_list) > 1:
                    print("Mark"+"+"+str(numbers_value))
            

            #Spread Romans
            unique_spread_romans_chapters_list = []
            for romans_dictionary in from_10_to_20_name_list_small:
                if "romans" in romans_dictionary:
                    romans_chapter_value = romans_dictionary["romans"]
                    romans_chapter_value_list.append(int(romans_chapter_value))
            if romans_chapter_value_list != []:
                int_set = set(romans_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Romans "+str(chapter_values) not in unique_spread_romans_chapters_list:
                            unique_spread_romans_chapters_list.append("Romans "+str(chapter_values))
                        if "Romans "+str(chapter_values+2) not in unique_spread_romans_chapters_list:
                            unique_spread_romans_chapters_list.append("Romans "+str(chapter_values+2))
                if len(unique_spread_romans_chapters_list) > 1:
                    print("Romans"+"+"+str(numbers_value))


            #Spread 1 Corinthians
            unique_spread_first_corinthians_chapters_list = []
            for first_corinthians_dictionary in from_10_to_20_name_list_small:
                if "first_corinthians" in first_corinthians_dictionary:
                    first_corinthians_chapter_value = first_corinthians_dictionary["first_corinthians"]
                    first_corinthians_chapter_value_list.append(int(first_corinthians_chapter_value))
            if first_corinthians_chapter_value_list != []:
                int_set = set(first_corinthians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "1 Corinthians "+str(chapter_values) not in unique_spread_first_corinthians_chapters_list:
                            unique_spread_first_corinthians_chapters_list.append("1 Corinthians "+str(chapter_values))
                        if "1 Corinthians "+str(chapter_values+2) not in unique_spread_first_corinthians_chapters_list:
                            unique_spread_first_corinthians_chapters_list.append("1 Corinthians "+str(chapter_values+2))
                if len(unique_spread_first_corinthians_chapters_list) > 1:
                    print("1 Corinthians"+"+"+str(numbers_value))


            #Spread 2 Corinthians
            unique_spread_second_corinthians_chapters_list = []
            for second_corinthians_dictionary in from_10_to_20_name_list_small:
                if "second_corinthians" in second_corinthians_dictionary:
                    second_corinthians_chapter_value = second_corinthians_dictionary["second_corinthians"]
                    second_corinthians_chapter_value_list.append(int(second_corinthians_chapter_value))
            if second_corinthians_chapter_value_list != []:
                int_set = set(second_corinthians_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "2 Corinthians "+str(chapter_values) not in unique_spread_second_corinthians_chapters_list:
                            unique_spread_second_corinthians_chapters_list.append("2 Corinthians "+str(chapter_values))
                        if "2 Corinthians "+str(chapter_values+2) not in unique_spread_second_corinthians_chapters_list:
                            unique_spread_second_corinthians_chapters_list.append("2 Corinthians "+str(chapter_values+2))
                if len(unique_spread_second_corinthians_chapters_list) > 1:
                    print("2 Corinthians"+"+"+str(numbers_value))

            #Spread Hebrews
            unique_spread_hebrews_chapters_list = []
            for hebrews_dictionary in from_10_to_20_name_list_small:
                if "hebrews" in hebrews_dictionary:
                    hebrews_chapter_value = hebrews_dictionary["hebrews"]
                    hebrews_chapter_value_list.append(int(hebrews_chapter_value))
            if hebrews_chapter_value_list != []:
                int_set = set(hebrews_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Hebrews "+str(chapter_values) not in unique_spread_hebrews_chapters_list:
                            unique_spread_hebrews_chapters_list.append("Hebrews "+str(chapter_values))
                        if "Hebrews "+str(chapter_values+2) not in unique_spread_hebrews_chapters_list:
                            unique_spread_hebrews_chapters_list.append("Hebrews "+str(chapter_values+2))
                if len(unique_spread_hebrews_chapters_list) > 1:
                    print("Hebrews"+"+"+str(numbers_value))


            #Spread Nehemiah
            unique_spread_nehemiah_chapters_list = []
            for nehemiah_dictionary in from_10_to_20_name_list_small:
                if "nehemiah" in nehemiah_dictionary:
                    nehemiah_chapter_value = nehemiah_dictionary["nehemiah"]
                    nehemiah_chapter_value_list.append(int(nehemiah_chapter_value))
            if nehemiah_chapter_value_list != []:
                int_set = set(nehemiah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Nehemiah "+str(chapter_values) not in unique_spread_nehemiah_chapters_list:
                            unique_spread_nehemiah_chapters_list.append("Nehemiah "+str(chapter_values))
                        if "Nehemiah "+str(chapter_values+2) not in unique_spread_nehemiah_chapters_list:
                            unique_spread_nehemiah_chapters_list.append("Nehemiah "+str(chapter_values+2))
                if len(unique_spread_nehemiah_chapters_list) > 1:
                    print("Nehemiah"+"+"+str(numbers_value))
            
            #Spread Ecclesiastes
            unique_spread_ecclesiastes_chapters_list = []
            for ecclesiastes_dictionary in from_10_to_20_name_list_small:
                if "ecclesiastes" in ecclesiastes_dictionary:
                    ecclesiastes_chapter_value = ecclesiastes_dictionary["ecclesiastes"]
                    ecclesiastes_chapter_value_list.append(int(ecclesiastes_chapter_value))
            if ecclesiastes_chapter_value_list != []:
                int_set = set(ecclesiastes_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Ecclesiastes "+str(chapter_values) not in unique_spread_ecclesiastes_chapters_list:
                            unique_spread_ecclesiastes_chapters_list.append("Ecclesiastes "+str(chapter_values))
                        if "Ecclesiastes "+str(chapter_values+2) not in unique_spread_ecclesiastes_chapters_list:
                            unique_spread_ecclesiastes_chapters_list.append("Ecclesiastes "+str(chapter_values+2))
                if len(unique_spread_ecclesiastes_chapters_list) > 1:
                    print("Ecclesiastes"+"+"+str(numbers_value))

            #Spread Daniel
            unique_spread_daniel_chapters_list = []
            for daniel_dictionary in from_10_to_20_name_list_small:
                if "daniel" in daniel_dictionary:
                    daniel_chapter_value = daniel_dictionary["daniel"]
                    daniel_chapter_value_list.append(int(daniel_chapter_value))
            if daniel_chapter_value_list != []:
                int_set = set(daniel_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Daniel "+str(chapter_values) not in unique_spread_daniel_chapters_list:
                            unique_spread_daniel_chapters_list.append("Daniel "+str(chapter_values))
                        if "Daniel "+str(chapter_values+2) not in unique_spread_daniel_chapters_list:
                            unique_spread_daniel_chapters_list.append("Daniel "+str(chapter_values+2))
                if len(unique_spread_daniel_chapters_list) > 1:
                    print("Daniel"+"+"+str(numbers_value))


            #Spread Hosea
            unique_spread_hosea_chapters_list = []
            for hosea_dictionary in from_10_to_20_name_list_small:
                if "hosea" in hosea_dictionary:
                    hosea_chapter_value = hosea_dictionary["hosea"]
                    hosea_chapter_value_list.append(int(hosea_chapter_value))
            if hosea_chapter_value_list != []:
                int_set = set(hosea_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Hosea "+str(chapter_values) not in unique_spread_hosea_chapters_list:
                            unique_spread_hosea_chapters_list.append("Hosea "+str(chapter_values))
                        if "Hosea "+str(chapter_values+2) not in unique_spread_hosea_chapters_list:
                            unique_spread_hosea_chapters_list.append("Hosea "+str(chapter_values+2))
                if len(unique_spread_hosea_chapters_list) > 1:
                    print("Hosea"+"+"+str(numbers_value))


            #Spread Zechariah
            unique_spread_zechariah_chapters_list = []
            for zechariah_dictionary in from_10_to_20_name_list_small:
                if "zechariah" in zechariah_dictionary:
                    zechariah_chapter_value = zechariah_dictionary["zechariah"]
                    zechariah_chapter_value_list.append(int(zechariah_chapter_value))
            if zechariah_chapter_value_list != []:
                int_set = set(zechariah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Zechariah "+str(chapter_values) not in unique_spread_zechariah_chapters_list:
                            unique_spread_zechariah_chapters_list.append("Zechariah "+str(chapter_values))
                        if "Zechariah "+str(chapter_values+2) not in unique_spread_zechariah_chapters_list:
                            unique_spread_zechariah_chapters_list.append("Zechariah "+str(chapter_values+2))
                if len(unique_spread_zechariah_chapters_list) > 1:
                    print("Zechariah"+"+"+str(numbers_value))

            #Spread Helaman
            unique_spread_helaman_chapters_list = []
            for helaman_dictionary in from_10_to_20_name_list_small:
                if "helaman" in helaman_dictionary:
                    helaman_chapter_value = helaman_dictionary["helaman"]
                    helaman_chapter_value_list.append(int(helaman_chapter_value))
            if helaman_chapter_value_list != []:
                int_set = set(helaman_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Helaman "+str(chapter_values) not in unique_spread_helaman_chapters_list:
                            unique_spread_helaman_chapters_list.append("Helaman "+str(chapter_values))
                        if "Helaman "+str(chapter_values+2) not in unique_spread_helaman_chapters_list:
                            unique_spread_helaman_chapters_list.append("Helaman "+str(chapter_values+2))
                if len(unique_spread_helaman_chapters_list) > 1:
                    print("Helaman"+"+"+str(numbers_value))

            #Spread Ether
            unique_spread_ether_chapters_list = []
            for ether_dictionary in from_10_to_20_name_list_small:
                if "ether" in ether_dictionary:
                    ether_chapter_value = ether_dictionary["ether"]
                    ether_chapter_value_list.append(int(ether_chapter_value))
            if ether_chapter_value_list != []:
                int_set = set(ether_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Ether "+str(chapter_values) not in unique_spread_ether_chapters_list:
                            unique_spread_ether_chapters_list.append("Ether "+str(chapter_values))
                        if "Ether "+str(chapter_values+2) not in unique_spread_ether_chapters_list:
                            unique_spread_ether_chapters_list.append("Ether "+str(chapter_values+2))
                if len(unique_spread_ether_chapters_list) > 1:
                    print("Ether"+"+"+str(numbers_value))

        #Spread 20 to 30
            #Spread Matthew
            unique_spread_matthew_chapters_list = []
            for matthew_dictionary in from_20_to_30_name_list_small:
                if "matthew" in matthew_dictionary:
                    matthew_chapter_value = matthew_dictionary["matthew"]
                    matthew_chapter_value_list.append(int(matthew_chapter_value))
            if matthew_chapter_value_list != []:
                int_set = set(matthew_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Matthew "+str(chapter_values) not in unique_spread_matthew_chapters_list:
                            unique_spread_matthew_chapters_list.append("Matthew "+str(chapter_values))
                        if "Matthew "+str(chapter_values+2) not in unique_spread_matthew_chapters_list:
                            unique_spread_matthew_chapters_list.append("Matthew "+str(chapter_values+2))
                if len(unique_spread_matthew_chapters_list) > 1:
                    print("Matthew"+"+"+str(numbers_value))

            #Spread Luke
            unique_spread_luke_chapters_list = []
            for luke_dictionary in from_20_to_30_name_list_small:
                if "luke" in luke_dictionary:
                    luke_chapter_value = luke_dictionary["luke"]
                    luke_chapter_value_list.append(int(luke_chapter_value))
            if luke_chapter_value_list != []:
                int_set = set(luke_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Luke "+str(chapter_values) not in unique_spread_luke_chapters_list:
                            unique_spread_luke_chapters_list.append("Luke "+str(chapter_values))
                        if "Luke "+str(chapter_values+2) not in unique_spread_luke_chapters_list:
                            unique_spread_luke_chapters_list.append("Luke "+str(chapter_values+2))
                if len(unique_spread_luke_chapters_list) > 1:
                    print("Luke"+"+"+str(numbers_value))

            #Note: John is still broken
            #Spread John
            # unique_spread_john_chapters_list = []
            # for john_dictionary in from_20_to_30_name_list_small:
            #     if "john" in john_dictionary:
            #         john_chapter_value = john_dictionary["john"]
            #         john_chapter_value_list.append(int(john_chapter_value))
            # if john_chapter_value_list != []:
            #     int_set = set(john_chapter_value_list)
            #     for chapter_values in int_set:
            #         if chapter_values + 2 in int_set:
            #             #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
            #             if "John "+str(chapter_values) not in unique_spread_john_chapters_list:
            #                 unique_spread_john_chapters_list.append("John "+str(chapter_values))
            #             if "John "+str(chapter_values+2) not in unique_spread_john_chapters_list:
            #                 unique_spread_john_chapters_list.append("John "+str(chapter_values+2))
            #     if len(unique_spread_john_chapters_list) > 1:
            #         print("John")

            #Spread Acts
            unique_spread_acts_chapters_list = []
            for acts_dictionary in from_20_to_30_name_list_small:
                if "acts" in acts_dictionary:
                    acts_chapter_value = acts_dictionary["acts"]
                    acts_chapter_value_list.append(int(acts_chapter_value))
            if acts_chapter_value_list != []:
                int_set = set(acts_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Acts "+str(chapter_values) not in unique_spread_acts_chapters_list:
                            unique_spread_acts_chapters_list.append("Acts "+str(chapter_values))
                        if "Acts "+str(chapter_values+2) not in unique_spread_acts_chapters_list:
                            unique_spread_acts_chapters_list.append("Acts "+str(chapter_values+2))
                if len(unique_spread_acts_chapters_list) > 1:
                    print("Acts"+"+"+str(numbers_value))

            #Spread Revelation
            unique_spread_revelation_chapters_list = []
            for revelation_dictionary in from_20_to_30_name_list_small:
                if "revelation" in revelation_dictionary:
                    revelation_chapter_value = revelation_dictionary["revelation"]
                    revelation_chapter_value_list.append(int(revelation_chapter_value))
            if revelation_chapter_value_list != []:
                int_set = set(revelation_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Revelation "+str(chapter_values) not in unique_spread_revelation_chapters_list:
                            unique_spread_revelation_chapters_list.append("Revelation "+str(chapter_values))
                        if "Revelation "+str(chapter_values+2) not in unique_spread_revelation_chapters_list:
                            unique_spread_revelation_chapters_list.append("Revelation "+str(chapter_values+2))
                if len(unique_spread_revelation_chapters_list) > 1:
                    print("Revelation"+"+"+str(numbers_value))


            #Spread Leviticus
            unique_spread_leviticus_chapters_list = []
            for leviticus_dictionary in from_20_to_30_name_list_small:
                if "leviticus" in leviticus_dictionary:
                    leviticus_chapter_value = leviticus_dictionary["leviticus"]
                    leviticus_chapter_value_list.append(int(leviticus_chapter_value))
            if leviticus_chapter_value_list != []:
                int_set = set(leviticus_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Leviticus "+str(chapter_values) not in unique_spread_leviticus_chapters_list:
                            unique_spread_leviticus_chapters_list.append("Leviticus "+str(chapter_values))
                        if "Leviticus "+str(chapter_values+2) not in unique_spread_leviticus_chapters_list:
                            unique_spread_leviticus_chapters_list.append("Leviticus "+str(chapter_values+2))
                if len(unique_spread_leviticus_chapters_list) > 1:
                    print("Leviticus"+"+"+str(numbers_value))

            

            #Spread Joshua
            unique_spread_joshua_chapters_list = []
            for joshua_dictionary in from_20_to_30_name_list_small:
                if "joshua" in joshua_dictionary:
                    joshua_chapter_value = joshua_dictionary["joshua"]
                    joshua_chapter_value_list.append(int(joshua_chapter_value))
            if joshua_chapter_value_list != []:
                int_set = set(joshua_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Joshua "+str(chapter_values) not in unique_spread_joshua_chapters_list:
                            unique_spread_joshua_chapters_list.append("Joshua "+str(chapter_values))
                        if "Joshua "+str(chapter_values+2) not in unique_spread_joshua_chapters_list:
                            unique_spread_joshua_chapters_list.append("Joshua "+str(chapter_values+2))
                if len(unique_spread_joshua_chapters_list) > 1:
                    print("Joshua"+"+"+str(numbers_value))

            #Spread Judges
            unique_spread_judges_chapters_list = []
            for judges_dictionary in from_20_to_30_name_list_small:
                if "judges" in judges_dictionary:
                    judges_chapter_value = judges_dictionary["judges"]
                    judges_chapter_value_list.append(int(judges_chapter_value))
            if judges_chapter_value_list != []:
                int_set = set(judges_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Judges "+str(chapter_values) not in unique_spread_judges_chapters_list:
                            unique_spread_judges_chapters_list.append("Judges "+str(chapter_values))
                        if "Judges "+str(chapter_values+2) not in unique_spread_judges_chapters_list:
                            unique_spread_judges_chapters_list.append("Judges "+str(chapter_values+2))
                if len(unique_spread_judges_chapters_list) > 1:
                    print("Judges"+"+"+str(numbers_value))

            
            #Spread 2 Samuel
            unique_spread_second_samuel_chapters_list = []
            for second_samuel_dictionary in from_20_to_30_name_list_small:
                if "second_samuel" in second_samuel_dictionary:
                    second_samuel_chapter_value = second_samuel_dictionary["second_samuel"]
                    second_samuel_chapter_value_list.append(int(second_samuel_chapter_value))
            if second_samuel_chapter_value_list != []:
                int_set = set(second_samuel_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "2 Samuel "+str(chapter_values) not in unique_spread_second_samuel_chapters_list:
                            unique_spread_second_samuel_chapters_list.append("2 Samuel "+str(chapter_values))
                        if "2 Samuel "+str(chapter_values+2) not in unique_spread_second_samuel_chapters_list:
                            unique_spread_second_samuel_chapters_list.append("2 Samuel "+str(chapter_values+2))
                if len(unique_spread_second_samuel_chapters_list) > 1:
                    print("2 Samuel"+"+"+str(numbers_value))

            #Spread 1 Kings
            unique_spread_first_kings_chapters_list = []
            for first_kings_dictionary in from_20_to_30_name_list_small:
                if "first_kings" in first_kings_dictionary:
                    first_kings_chapter_value = first_kings_dictionary["first_kings"]
                    first_kings_chapter_value_list.append(int(first_kings_chapter_value))
            if first_kings_chapter_value_list != []:
                int_set = set(first_kings_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "1 Kings "+str(chapter_values) not in unique_spread_first_kings_chapters_list:
                            unique_spread_first_kings_chapters_list.append("1 Kings "+str(chapter_values))
                        if "1 Kings"+str(chapter_values+2) not in unique_spread_first_kings_chapters_list:
                            unique_spread_first_kings_chapters_list.append("1 Kings "+str(chapter_values+2))
                if len(unique_spread_first_kings_chapters_list) > 1:
                    print("1 Kings"+"+"+str(numbers_value))

            #Spread 2 Kings
            unique_spread_second_kings_chapters_list = []
            for second_kings_dictionary in from_20_to_30_name_list_small:
                if "second_kings" in second_kings_dictionary:
                    second_kings_chapter_value = second_kings_dictionary["second_kings"]
                    second_kings_chapter_value_list.append(int(second_kings_chapter_value))
            if second_kings_chapter_value_list != []:
                int_set = set(second_kings_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "2 Kings "+str(chapter_values) not in unique_spread_second_kings_chapters_list:
                            unique_spread_second_kings_chapters_list.append("2 Kings "+str(chapter_values))
                        if "2 Kings"+str(chapter_values+2) not in unique_spread_second_kings_chapters_list:
                            unique_spread_second_kings_chapters_list.append("2 Kings "+str(chapter_values+2))
                if len(unique_spread_second_kings_chapters_list) > 1:
                    print("2 Kings"+"+"+str(numbers_value))
            
            #Spread 1 Chronicles
            unique_spread_first_chronicles_chapters_list = []
            for first_chronicles_dictionary in from_20_to_30_name_list_small:
                if "first_chronicles" in first_chronicles_dictionary:
                    first_chronicles_chapter_value = first_chronicles_dictionary["first_chronicles"]
                    first_chronicles_chapter_value_list.append(int(first_chronicles_chapter_value))
            if first_chronicles_chapter_value_list != []:
                int_set = set(first_chronicles_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "1 Chronicles "+str(chapter_values) not in unique_spread_first_chronicles_chapters_list:
                            unique_spread_first_chronicles_chapters_list.append("1 Chronicles "+str(chapter_values))
                        if "1 Chronicles"+str(chapter_values+2) not in unique_spread_first_chronicles_chapters_list:
                            unique_spread_first_chronicles_chapters_list.append("1 Chronicles "+str(chapter_values+2))
                if len(unique_spread_first_chronicles_chapters_list) > 1:
                    print("1 Chronicles"+"+"+str(numbers_value))

            #Spread 1 Nephi
            unique_spread_first_nephi_chapters_list = []
            for first_nephi_dictionary in from_20_to_30_name_list_small:
                if "first_nephi" in first_nephi_dictionary:
                    first_nephi_chapter_value = first_nephi_dictionary["first_nephi"]
                    first_nephi_chapter_value_list.append(int(first_nephi_chapter_value))
            if first_nephi_chapter_value_list != []:
                int_set = set(first_nephi_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "1 Nephi "+str(chapter_values) not in unique_spread_first_nephi_chapters_list:
                            unique_spread_first_nephi_chapters_list.append("1 Nephi "+str(chapter_values))
                        if "1 Nephi"+str(chapter_values+2) not in unique_spread_first_nephi_chapters_list:
                            unique_spread_first_nephi_chapters_list.append("1 Nephi "+str(chapter_values+2))
                if len(unique_spread_first_nephi_chapters_list) > 1:
                    print("1 Nephi"+"+"+str(numbers_value))

            #Spread Mosiah
            unique_spread_mosiah_chapters_list = []
            for mosiah_dictionary in from_20_to_30_name_list_small:
                if "mosiah" in mosiah_dictionary:
                    mosiah_chapter_value = mosiah_dictionary["mosiah"]
                    mosiah_chapter_value_list.append(int(mosiah_chapter_value))
            if mosiah_chapter_value_list != []:
                int_set = set(mosiah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Mosiah "+str(chapter_values) not in unique_spread_mosiah_chapters_list:
                            unique_spread_mosiah_chapters_list.append("Mosiah "+str(chapter_values))
                        if "Mosiah"+str(chapter_values+2) not in unique_spread_mosiah_chapters_list:
                            unique_spread_mosiah_chapters_list.append("Mosiah "+str(chapter_values+2))
                if len(unique_spread_mosiah_chapters_list) > 1:
                    print("Mosiah"+"+"+str(numbers_value))

            #Spread 3 Nephi
            unique_spread_third_nephi_chapters_list = []
            for third_nephi_dictionary in from_20_to_30_name_list_small:
                if "third_nephi" in third_nephi_dictionary:
                    third_nephi_chapter_value = third_nephi_dictionary["third_nephi"]
                    third_nephi_chapter_value_list.append(int(third_nephi_chapter_value))
            if third_nephi_chapter_value_list != []:
                int_set = set(third_nephi_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "3 Nephi "+str(chapter_values) not in unique_spread_third_nephi_chapters_list:
                            unique_spread_third_nephi_chapters_list.append("3 Nephi "+str(chapter_values))
                        if "3 Nephi"+str(chapter_values+2) not in unique_spread_third_nephi_chapters_list:
                            unique_spread_third_nephi_chapters_list.append("3 Nephi "+str(chapter_values+2))
                if len(unique_spread_third_nephi_chapters_list) > 1:
                    print("3 Nephi"+"+"+str(numbers_value))

        #Spread 30 to 40
            #Spread Exodus
            unique_spread_exodus_chapters_list = []
            for exodus_dictionary in from_30_to_40_name_list_small:
                if "exodus" in exodus_dictionary:
                    exodus_chapter_value = exodus_dictionary["exodus"]
                    exodus_chapter_value_list.append(int(exodus_chapter_value))
            if exodus_chapter_value_list != []:
                int_set = set(exodus_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Exodus "+str(chapter_values) not in unique_spread_exodus_chapters_list:
                            unique_spread_exodus_chapters_list.append("Exodus "+str(chapter_values))
                        if "Exodus"+str(chapter_values+2) not in unique_spread_exodus_chapters_list:
                            unique_spread_exodus_chapters_list.append("Exodus "+str(chapter_values+2))
                if len(unique_spread_exodus_chapters_list) > 1:
                    print("Exodus"+"+"+str(numbers_value))

            #Spread Numbers
            unique_spread_numbers_chapters_list = []
            for numbers_dictionary in from_30_to_40_name_list_small:
                if "numbers" in numbers_dictionary:
                    numbers_chapter_value = numbers_dictionary["numbers"]
                    numbers_chapter_value_list.append(int(numbers_chapter_value))
            if numbers_chapter_value_list != []:
                int_set = set(numbers_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Numbers "+str(chapter_values) not in unique_spread_numbers_chapters_list:
                            unique_spread_numbers_chapters_list.append("Numbers "+str(chapter_values))
                        if "Numbers"+str(chapter_values+2) not in unique_spread_numbers_chapters_list:
                            unique_spread_numbers_chapters_list.append("Numbers "+str(chapter_values+2))
                if len(unique_spread_numbers_chapters_list) > 1:
                    print("Numbers"+"+"+str(numbers_value))
            
            #Spread Deuteronomy
            unique_spread_deuteronomy_chapters_list = []
            for deuteronomy_dictionary in from_30_to_40_name_list_small:
                if "deuteronomy" in deuteronomy_dictionary:
                    deuteronomy_chapter_value = deuteronomy_dictionary["deuteronomy"]
                    deuteronomy_chapter_value_list.append(int(deuteronomy_chapter_value))
            if deuteronomy_chapter_value_list != []:
                int_set = set(deuteronomy_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Deuteronomy "+str(chapter_values) not in unique_spread_deuteronomy_chapters_list:
                            unique_spread_deuteronomy_chapters_list.append("Deuteronomy "+str(chapter_values))
                        if "Deuteronomy"+str(chapter_values+2) not in unique_spread_deuteronomy_chapters_list:
                            unique_spread_deuteronomy_chapters_list.append("Deuteronomy "+str(chapter_values+2))
                if len(unique_spread_deuteronomy_chapters_list) > 1:
                    print("Deuteronomy"+"+"+str(numbers_value))

            #Spread 1 Samuel
            unique_spread_first_samuel_chapters_list = []
            for first_samuel_dictionary in from_30_to_40_name_list_small:
                if "first_samuel" in first_samuel_dictionary:
                    first_samuel_chapter_value = first_samuel_dictionary["first_samuel"]
                    first_samuel_chapter_value_list.append(int(first_samuel_chapter_value))
            if first_samuel_chapter_value_list != []:
                int_set = set(first_samuel_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "1 Samuel "+str(chapter_values) not in unique_spread_first_samuel_chapters_list:
                            unique_spread_first_samuel_chapters_list.append("1 Samuel "+str(chapter_values))
                        if "1 Samuel"+str(chapter_values+2) not in unique_spread_first_samuel_chapters_list:
                            unique_spread_first_samuel_chapters_list.append("1 Samuel "+str(chapter_values+2))
                if len(unique_spread_first_samuel_chapters_list) > 1:
                    print("1 Samuel"+"+"+str(numbers_value))

            #Spread 2 Chronicles
            unique_spread_second_chronicles_chapters_list = []
            for second_chronicles_dictionary in from_30_to_40_name_list_small:
                if "second_chronicles" in second_chronicles_dictionary:
                    second_chronicles_chapter_value = second_chronicles_dictionary["second_chronicles"]
                    second_chronicles_chapter_value_list.append(int(second_chronicles_chapter_value))
            if second_chronicles_chapter_value_list != []:
                int_set = set(second_chronicles_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "2 Chronicles "+str(chapter_values) not in unique_spread_second_chronicles_chapters_list:
                            unique_spread_second_chronicles_chapters_list.append("2 Chronicles "+str(chapter_values))
                        if "2 Chronicles"+str(chapter_values+2) not in unique_spread_second_chronicles_chapters_list:
                            unique_spread_second_chronicles_chapters_list.append("2 Chronicles "+str(chapter_values+2))
                if len(unique_spread_second_chronicles_chapters_list) > 1:
                    print("2 Chronicles"+"+"+str(numbers_value))
            
            #Spread Proverbs
            unique_spread_proverbs_chapters_list = []
            for proverbs_dictionary in from_30_to_40_name_list_small:
                if "proverbs" in proverbs_dictionary:
                    proverbs_chapter_value = proverbs_dictionary["proverbs"]
                    proverbs_chapter_value_list.append(int(proverbs_chapter_value))
            if proverbs_chapter_value_list != []:
                int_set = set(proverbs_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Proverbs "+str(chapter_values) not in unique_spread_proverbs_chapters_list:
                            unique_spread_proverbs_chapters_list.append("Proverbs "+str(chapter_values))
                        if "Proverbs"+str(chapter_values+2) not in unique_spread_proverbs_chapters_list:
                            unique_spread_proverbs_chapters_list.append("Proverbs "+str(chapter_values+2))
                if len(unique_spread_proverbs_chapters_list) > 1:
                    print("Proverbs"+"+"+str(numbers_value))

            #Spread 2 Nephi
            unique_spread_second_nephi_chapters_list = []
            for second_nephi_dictionary in from_30_to_40_name_list_small:
                if "second_nephi" in second_nephi_dictionary:
                    second_nephi_chapter_value = second_nephi_dictionary["second_nephi"]
                    second_nephi_chapter_value_list.append(int(second_nephi_chapter_value))
            if second_nephi_chapter_value_list != []:
                int_set = set(second_nephi_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "2 Nephi "+str(chapter_values) not in unique_spread_second_nephi_chapters_list:
                            unique_spread_second_nephi_chapters_list.append("2 Nephi "+str(chapter_values))
                        if "2 Nephi"+str(chapter_values+2) not in unique_spread_second_nephi_chapters_list:
                            unique_spread_second_nephi_chapters_list.append("2 Nephi "+str(chapter_values+2))
                if len(unique_spread_second_nephi_chapters_list) > 1:
                    print("2 Nephi"+"+"+str(numbers_value))
                    
        #Spread 40 to 200
            #Spread Genesis
            unique_spread_genesis_chapters_list = []
            for genesis_dictionary in from_40_to_200_name_list_small:
                if "genesis" in genesis_dictionary:
                    genesis_chapter_value = genesis_dictionary["genesis"]
                    genesis_chapter_value_list.append(int(genesis_chapter_value))
            if genesis_chapter_value_list != []:
                int_set = set(genesis_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Genesis "+str(chapter_values) not in unique_spread_genesis_chapters_list:
                            unique_spread_genesis_chapters_list.append("Genesis "+str(chapter_values))
                        if "Genesis"+str(chapter_values+2) not in unique_spread_genesis_chapters_list:
                            unique_spread_genesis_chapters_list.append("Genesis "+str(chapter_values+2))
                if len(unique_spread_genesis_chapters_list) > 1:
                    print("Genesis"+"+"+str(numbers_value))

            #Spread Job
            unique_spread_job_chapters_list = []
            for job_dictionary in from_40_to_200_name_list_small:
                if "job" in job_dictionary:
                    job_chapter_value = job_dictionary["job"]
                    job_chapter_value_list.append(int(job_chapter_value))
            if job_chapter_value_list != []:
                int_set = set(job_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Job "+str(chapter_values) not in unique_spread_job_chapters_list:
                            unique_spread_job_chapters_list.append("Job "+str(chapter_values))
                        if "Job"+str(chapter_values+2) not in unique_spread_job_chapters_list:
                            unique_spread_job_chapters_list.append("Job "+str(chapter_values+2))
                if len(unique_spread_job_chapters_list) > 1:
                    print("Job"+"+"+str(numbers_value))

            #Spread Psalms
            unique_spread_psalms_chapters_list = []
            for psalms_dictionary in from_40_to_200_name_list_small:
                if "psalms" in psalms_dictionary:
                    psalms_chapter_value = psalms_dictionary["psalms"]
                    psalms_chapter_value_list.append(int(psalms_chapter_value))
            if psalms_chapter_value_list != []:
                int_set = set(psalms_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Psalms "+str(chapter_values) not in unique_spread_psalms_chapters_list:
                            unique_spread_psalms_chapters_list.append("Psalms "+str(chapter_values))
                        if "Psalms"+str(chapter_values+2) not in unique_spread_psalms_chapters_list:
                            unique_spread_psalms_chapters_list.append("Psalms "+str(chapter_values+2))
                if len(unique_spread_psalms_chapters_list) > 1:
                    print("Psalms"+"+"+str(numbers_value))

            #Spread Isaiah
            unique_spread_isaiah_chapters_list = []
            for isaiah_dictionary in from_40_to_200_name_list_small:
                if "isaiah" in isaiah_dictionary:
                    isaiah_chapter_value = isaiah_dictionary["isaiah"]
                    isaiah_chapter_value_list.append(int(isaiah_chapter_value))
            if isaiah_chapter_value_list != []:
                int_set = set(isaiah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Isaiah "+str(chapter_values) not in unique_spread_isaiah_chapters_list:
                            unique_spread_isaiah_chapters_list.append("Isaiah "+str(chapter_values))
                        if "Isaiah"+str(chapter_values+2) not in unique_spread_isaiah_chapters_list:
                            unique_spread_isaiah_chapters_list.append("Isaiah "+str(chapter_values+2))
                if len(unique_spread_isaiah_chapters_list) > 1:
                    print("Isaiah"+"+"+str(numbers_value))
                    
            #Spread Jeremiah
            unique_spread_jeremiah_chapters_list = []
            for jeremiah_dictionary in from_40_to_200_name_list_small:
                if "jeremiah" in jeremiah_dictionary:
                    jeremiah_chapter_value = jeremiah_dictionary["jeremiah"]
                    jeremiah_chapter_value_list.append(int(jeremiah_chapter_value))
            if jeremiah_chapter_value_list != []:
                int_set = set(jeremiah_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Jeremiah "+str(chapter_values) not in unique_spread_jeremiah_chapters_list:
                            unique_spread_jeremiah_chapters_list.append("Jeremiah "+str(chapter_values))
                        if "Jeremiah"+str(chapter_values+2) not in unique_spread_jeremiah_chapters_list:
                            unique_spread_jeremiah_chapters_list.append("Jeremiah "+str(chapter_values+2))
                if len(unique_spread_jeremiah_chapters_list) > 1:
                    print("Jeremiah"+"+"+str(numbers_value))

            #Spread Ezekiel
            unique_spread_ezekiel_chapters_list = []
            for ezekiel_dictionary in from_40_to_200_name_list_small:
                if "ezekiel" in ezekiel_dictionary:
                    ezekiel_chapter_value = ezekiel_dictionary["ezekiel"]
                    ezekiel_chapter_value_list.append(int(ezekiel_chapter_value))
            if ezekiel_chapter_value_list != []:
                int_set = set(ezekiel_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Ezekiel "+str(chapter_values) not in unique_spread_ezekiel_chapters_list:
                            unique_spread_ezekiel_chapters_list.append("Ezekiel "+str(chapter_values))
                        if "Ezekiel"+str(chapter_values+2) not in unique_spread_ezekiel_chapters_list:
                            unique_spread_ezekiel_chapters_list.append("Ezekiel "+str(chapter_values+2))
                if len(unique_spread_ezekiel_chapters_list) > 1:
                    print("Ezekiel"+"+"+str(numbers_value))
            
            
            #Spread Alma
            unique_spread_alma_chapters_list = []
            for alma_dictionary in from_40_to_200_name_list_small:
                if "alma" in alma_dictionary:
                    alma_chapter_value = alma_dictionary["alma"]
                    alma_chapter_value_list.append(int(alma_chapter_value))
            if alma_chapter_value_list != []:
                int_set = set(alma_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Alma "+str(chapter_values) not in unique_spread_alma_chapters_list:
                            unique_spread_alma_chapters_list.append("Alma "+str(chapter_values))
                        if "Alma"+str(chapter_values+2) not in unique_spread_alma_chapters_list:
                            unique_spread_alma_chapters_list.append("Alma "+str(chapter_values+2))
                if len(unique_spread_alma_chapters_list) > 1:
                    print("Alma"+"+"+str(numbers_value))
            

            #Spread Doctrine and Covenants
            unique_spread_doctrine_and_covenants_chapters_list = []
            for doctrine_and_covenants_dictionary in from_40_to_200_name_list_small:
                if "doctrine_and_covenants" in doctrine_and_covenants_dictionary:
                    doctrine_and_covenants_chapter_value = doctrine_and_covenants_dictionary["doctrine_and_covenants"]
                    doctrine_and_covenants_chapter_value_list.append(int(doctrine_and_covenants_chapter_value))
            if doctrine_and_covenants_chapter_value_list != []:
                int_set = set(doctrine_and_covenants_chapter_value_list)
                for chapter_values in int_set:
                    if chapter_values + 2 in int_set:
                        #print(f"Pair found: {chapter_values} and {chapter_values + 2}")
                        if "Doctrine and Covenants "+str(chapter_values) not in unique_spread_doctrine_and_covenants_chapters_list:
                            unique_spread_doctrine_and_covenants_chapters_list.append("Doctrine and Covenants "+str(chapter_values))
                        if "Doctrine and Covenants"+str(chapter_values+2) not in unique_spread_doctrine_and_covenants_chapters_list:
                            unique_spread_doctrine_and_covenants_chapters_list.append("Doctrine and Covenants "+str(chapter_values+2))
                if len(unique_spread_doctrine_and_covenants_chapters_list) > 1:
                    print("Doctrine and Covenants"+"+"+str(numbers_value))
       
            list_of_small_scriptures =["Bible",
"Old Testament",
"Genesis 1",
"Gen. 1",
"Exodus 1",
"Ex. 1",
"Leviticus 1",
"Lev. 1",
"Numbers 1",
"Num. 1",
"Deuteronomy 1",
"Joshua 1",
"Josh. 1",
"Judges 1",
"Judg. 1",
"Ruth 1",
"Rut. 1",
"1 Samuel 1",
"1 Sam. 1",
"2 Samuel 1",
"2 Sam. 1",
"1 Kings 1",
"2 Kings 1",
"1 Chronicles 1",
"1 Chr. 1",
"2 Chronicles 1",
"2 Chr. 1",
"Ezra 1",
"Nehemiah 1",
"Neh. 1",
"Esther 1",
"Job 1",
"Psalms 1",
"Ps. 1",
"Proverbs 1",
"Prov. 1",
"Ecclesiastes 1",
"Song of Solomon 1",
"Song. 1",
"Isaiah 1",
"Isa. 1",
"Jeremiah 1",
"Jer. 1",
"Lamentations 1",
"Lam. 1",
"Ezekiel 1",
"Ezek. 1",
"Daniel 1",
"Dan. 1",
"Hosea 1",
"Joel 1",
"Amos 1",
"Obadiah 1",
"Jonah 1",
"Micah 1",
"Nahum 1",
"Habakkuk 1",
"Hab. 1",
"Zephaniah 1",
"Zeph. 1",
"Haggai 1",
"Hag. 1",
"Zechariah 1",
"Zech. 1",
"Malachi 1",
"Mal. 1",
"1 Nephi 1",
"1 Ne. 1",
"2 Nephi 1",
"2 Ne. 1",
"Jacob 1",
"Enos 1",
"Jarom 1",
"Omni 1",
"Words of Mormon 1",
"W of M 1",
"Mosiah 1",
"Alma 1",
"Helaman 1",
"Hel. 1",
"3 Nephi 1",
"3 Ne. 1",
"4 Nephi",
"4 Ne.",
"Book of Mormon",
"Morm. 1",
"Ether 1",
"Moro. 1",
"Moroni 1",
"New Testament",
"Matthew 1",
"Matt. 1",
"Mark 1",
"Luke 1",
"Gospels of John",
"John 1",
"Acts 1",
"Romans 1",
"Rom. 1",
"1 Corinthians 1",
"1 Cor. 1",
"2 Corinthians 1",
"2 Cor. 1",
"Galatians 1",
"Gal. 1",
"Ephesians 1",
"Eph. 1",
"Philippians 1",
"Philip. 1",
"Colossians 1",
"Col. 1",
"1 Thessalonians 1",
"1 Thes. 1",
"2 Thessalonians 1",
"2 Thes. 1",
"1 Timothy 1",
"1 Tim. 1",
"2 Timothy 1",
"2 Tim. 1",
"Titus 1",
"Philemon",
"Philem. 1",
"Hebrews 1",
"Heb. 1",
"James 1",
"1 Peter 1",
"1 Pet. 1",
"2 Peter 1",
"2 Pet. 1",
"1 John 1",
"1 Jn. 1",
"2 John",
"2 Jn.",
"3 John",
"3 Jn.",
"Jude 1",
"Revelation 1",
"Rev. 1",
"Doctrine and Covenants 1",
"D&C 1",
"Moses 1",
"Abraham 1",
"Abr. 1",
"Facsimile 1",
"Joseph Smith-Matthew",
"JS-M",
"Joseph Smith History",
"Joseph Smith—History",
"Articles of Faith",
"A of F",
"Joseph Smith Translation 1",
"JST 1",
"Ten Commandments",
"10 Commandments",
"Title Page of the Book of Mormon",
"Testimony of the Twelve Apostles from the Book of Mormon",
]

            from_1_to_10_list_saved=[]
            from_10_to_20_list_saved=[]
            from_20_to_30_list_saved=[]
            from_30_to_40_list_saved=[]
            from_40_to_200_list_saved=[]

main_function()
