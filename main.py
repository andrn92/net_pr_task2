import csv
import re


class DataReader():
    def __init__(self):
        pass
    def read_csv_file(self, filename:str, lst=[]):
        with open(filename) as f:
            rows = csv.reader(f, delimiter=',')
            for row in rows:
                lst.append(row)
        return lst
        
    def translate_list_to_str(self, lst:list, res_lst=[]):
        for row in lst[1:]:
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = '----'
            new_row = ','.join(row)
            res_lst.append(new_row)
        return res_lst

    def change_str_with_pattern(self, pattern:str, subpat:str, lst:list):
        for i in range(len(lst)):
            res = re.sub(pattern, subpat, lst[i])
            lst[i] = res
        return lst

    def get_list_from_str(self, lst:list):
        for i in range(len(lst)):
            lst[i] = lst[i].split(',')
        return lst

    def change_number_fields(self, lst:list):
        for person in lst:
            if len(person) < 7:
                res = 7 - len(person)
                person += ['----']*(res)
            if len(person) > 7:
                res = len(person) - 7
                while res > 0:
                    if person[-1] == '----':
                        person.remove(person[-1])
                    else:
                        break
                    res -= 1 
        return lst

    def change_and_replace_phone(self, pattern:str, subpat:str, lst:list):
        for person in lst:
            for i in range(len(person)):
                res = re.search(pattern, person[i])
                if res:
                    person[i] = re.sub(pattern, subpat, person[i])
                    person[i], person[5] = person[5], person[i]
        return lst

    def replace_email(self, pattern:str, lst:list):
        for person in lst:
            for i in range(len(person)):
                res = re.search(pattern, person[i])
                if res:
                    person[i], person[6] = person[6], person[i]
        return lst

    def combine_identical_objects(self, lst:list):
        for i in range(len(lst) - 1):
            person = ''
            for j in range(i + 1, len(lst)):
                if lst[i] != [] and lst[j] != [] and lst[i][0] == lst[j][0] and lst[i][1] == lst[j][1]:
                    person = list(zip(lst[i], lst[j]))
                    lst[i] = person
                    lst[j] = []
        return lst

    def delete_unnecessary_records(self, lst:list):
        for person in lst:
            for i in range(len(person)):
                if type(person[i]) == tuple:
                    if person[i][0] == person[i][1] and person[i][0] != '----':
                        person[i] = person[i][0]
                    elif person[i][0] != person[i][1] and person[i][0] == '----':
                        person[i] = person[i][1]
                    elif person[i][0] != person[i][1] and person[i][1] == '----':
                        person[i] = person[i][0]
                    elif person[i][0] == person[i][1] == '----':
                        person[i] = '----'
        for person in lst:
            for i in range(len(person)):
                if person[i] == '----':
                    person[i] = ''
        return lst

    def delete_empty_list(self, lst:list):
        i = 0
        while True:
            if lst[i] == []:
                lst.remove(lst[i])
                if i == len(lst):
                    break
            if lst[i] != [] and i < len(lst) - 1:
                i += 1
            elif i == len(lst) - 1:
                break
        return lst

    def record_csv_file(self, filename:str, lst:list):
        with open(filename, "w") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(lst)

if __name__ == '__main__':
    datareader = DataReader()
    lst = datareader.read_csv_file('phonebook_raw.csv')
    data_str = lst[0]
    res_lst = datareader.translate_list_to_str(lst)

    pat1 = r"^(\w+)\s+(\w+)\s+(\w+),([-]{4}),([-]{4})"
    pat2 = r"^(\w+),\s*(\w+)\s+(\w+),([-]{4})"
    pat3 = r"^(\w+)\s+(\w+),([-]{4})"
    subp1 = r"\1,\2,\3"
    subp2 = r"\1,\2,\3"
    subp3 = r"\1,\2"
    datareader.change_str_with_pattern(pat1, subp1, res_lst)
    datareader.change_str_with_pattern(pat2, subp2, res_lst)
    datareader.change_str_with_pattern(pat3, subp3, res_lst)
    
    datareader.get_list_from_str(res_lst)
    datareader.change_number_fields(res_lst)

    pattern1 = r'(\+7|8)\s*\(?([\d]{3})\)?([\s]*|[-]?)([\d]{3})([-]?|[\s]*)([\d]{2})([-]?|[\s]*)([\d]{2})'
    subpat1 = r'+7(\2)\4-\6-\8'
    pattern2 = r'(\+7|8)\s*\(?([\d]{3})\)?([\s]*|[-]?)([\d]{3})([-]?|[\s]*)([\d]{2})([-]?|[\s]*)([\d]{2})(\s*)\(?(\w*[^()]\s*\w*[^()])\)?'
    subpat2 = r'+7(\2)\4-\6-\8\9\10'
    datareader.change_and_replace_phone(pattern1, subpat1, res_lst)
    datareader.change_and_replace_phone(pattern2, subpat2, res_lst)

    pat_email = r'\w+@\w+\.\w+'
    datareader.replace_email(pat_email, res_lst)
    
    datareader.combine_identical_objects(res_lst)
    datareader.delete_unnecessary_records(res_lst)
    datareader.delete_empty_list(res_lst)
    res_lst = [data_str] + res_lst
    print(res_lst)
    datareader.record_csv_file("phonebook.csv", res_lst)

   