def get_name_and_date(result):
    answer_list = list(result.split(", "))
        
    extracted_names = answer_list[0].rstrip()
    date = answer_list[1].strip()
    title = answer_list[2].strip()

    return extracted_names, date, title
