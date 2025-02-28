def parse_region_statistics(st):
    place_start = 1
    parsed_st = []
    for i in range(len(st)):
        place_finish = place_start
        j = i + 1
        while st[j][1] == st[i][1]:
            place_finish += 1
            j += 1
        for k in range(i, j):
            parsed_st.append((place_start, place_finish, st[k][0], st[k][1]))
        place_start = place_finish + 1
    return parsed_st




