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

