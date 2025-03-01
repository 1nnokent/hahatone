from bs4 import BeautifulSoup

def parse_region_statistics(st):
    place_start = 1
    parsed_st = []
    for i in range(len(st)):
        place_finish = place_start
        j = i + 1
        while j < len(st) and st[j][1] == st[i][1]:
            place_finish += 1
            j += 1
        for k in range(i, j):
            if place_start == place_finish:
                parsed_st.append((str(place_start), st[k][0], st[k][1]))
            else:
                parsed_st.append((str(place_start) + '-' + str(place_finish), st[k][0], st[k][1]))
        place_start = place_finish + 1
    return parsed_st


def parse_students(st):
    place_start = 1
    parsed_st = []
    leng = len(st)
    i = 0
    while i < leng:
        place_finish = place_start
        j = i + 1
        while j < len(st) and st[j][4] == st[i][4]:
            place_finish += 1
            j += 1
        for k in range(i, j):
            if place_start == place_finish:
                parsed_st.append((str(place_start), st[k][0], st[k][1], st[k][2], st[k][4]))
            else:
                parsed_st.append((str(place_start) + '-' + str(place_finish), st[k][0], st[k][1], st[k][2], st[k][4]))
        place_start = place_finish + 1
        i = j
    return parsed_st


def parse_first_tour(html_filename):
    full_path = 'Материалы/Первый тур/' + html_filename
    file = open(full_path, 'r', encoding='utf-8')
    soup = BeautifulSoup(file, 'html.parser')
    result = []

    for table in soup.find_all('table'):
        headers = []
        header_row = table.find('tr')
        if header_row:
            headers = [header.get_text(strip=True) for header in header_row.find_all(['th', 'td'])]

        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            result.append(tuple(row_data))
        return result

    return []


def parse_second_tour(html_filename):
    full_path = 'Материалы/Второй тур/' + html_filename
    file = open(full_path, 'r', encoding='utf-8')
    soup = BeautifulSoup(file, 'html.parser')
    result = []

    for table in soup.find_all('table'):
        headers = []
        header_row = table.find('tr')
        if header_row:
            headers = [header.get_text(strip=True) for header in header_row.find_all(['th', 'td'])]

        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            result.append(tuple(row_data))
        return result

    return []



first_tour_times = [120, 150, 180, 190, 200, 220, 240, 260, 280, 295, 300]
second_tour_times = [30, 45, 75, 90, 95, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 280, 290, 295, 300]
def find_nearest_time(time, tour):
    answ = 0
    if tour == 1:
        for elem in first_tour_times:
            if elem <= time:
                answ = elem
    elif tour == 2:
        for elem in second_tour_times:
            if elem <= time:
                answ = elem
    return answ
