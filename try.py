import numpy

def extendChartData(dateStat):
    extendedDates = {'20-05': 63, '19-05': 12, '19-03': 138, '19-02': 44, '19-01': 186, '18-12': 137, '18-11': 33, '18-10': 321, '18-09': 27, '18-07': 2, '18-06': 140, '18-04': 92, '18-03': 138, '18-02': 361, '18-01': 156, '15-07': 380, '15-06': 830}
    print(extendedDates)
    firstDate = min(extendedDates)
    lastDate = max(extendedDates)
    print(firstDate)
    print(lastDate)
    firstYear = int(firstDate.split("-")[0])
    firstMonth = int(firstDate.split("-")[1])
    lastYear = int(lastDate.split("-")[0])
    lastMonth = int(lastDate.split("-")[1])
    months = []

    for x in range(firstYear,lastYear):
        month = ""
        for i in range(1, 13):
            month = ""
            if i < 10:
                month += str(x) + "-" "0"
                month += str(i)
            else:
                month += str(x) + "-" +  str(i)
            #print("month : " + month)
            months.append(month)
            #print(months)
            print("=")

    for month in months:
        print(month)
        if month in extendedDates:
            print(month + " volt")
        else:
            extendedDates[month] = 0




    print(extendedDates)
    # print(firstYear)
    # print(firstMonth)
    # print(lastYear)
    # print(lastMonth)

    # for k in extendedDates:
        #print(i)
        #print()

    exit()
    return extendedDates

extendChartData(1)