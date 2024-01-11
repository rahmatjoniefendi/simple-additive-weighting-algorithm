import numpy as np
import matplotlib.pyplot as plt;

CATEGORY_BENEFIT = 1
CATEGORY_COST = 2

def rumus_benefit(column, index, digits=2):
    ri = column[index] / max(column)
    result = round(ri, digits)

    return result

def rumus_cost(column, index, digits=2):
    ri = min(column) / column[index]
    result = round(ri, digits)

    return result

def normalisasi_row(column, category, digits=2):
    ci = []

    for i in range(len(column)):
        if(category == CATEGORY_BENEFIT):
            ci.append(rumus_benefit(column, i, digits))
        elif(category == CATEGORY_COST):
            ci.append(rumus_cost(column, i, digits))
        
    return ci

def normalisasi(columns, categories, digits=2):
    r = []
    
    column_size = len(columns)
    
    for i in range(column_size):
        r.append(normalisasi_row(columns[i], categories[i], digits))

    return r

def rank_i(columns, categories, weigths, row_index, digits=2):
    vi = []
    
    for ri, wi in zip(to_rows(normalisasi(columns, categories, digits))[row_index], weigths):
        vi.append(ri * wi)
        
    return vi

def rank(matrix, categories, weigths, digits=2):
    v = []

    column_size = len(matrix[0])
    
    for i in range(column_size):
        vi = sum(rank_i(matrix, categories, weigths, i, digits))
        v.append(vi)

# Utility
def to_row(matrix, index):
    ci = []
    
    for row in matrix:
        ci.append(row[index])

    return ci

def to_rows(matrix):
    ci = []
    
    for i in range(len(matrix[0])):
        ci.append(to_row(matrix, i))

    return ci

def print_rumus_benefit_proses(column, index, digits=2):
    print('\t'+ str(column[index]).rjust(32) + str(column[index]).rjust(56))
    print('\t---------------------------------------------------------------------------' + 
            ' = ------------------ = ' +
          str(rumus_benefit(column, index, digits)))
    print('\t'+ str('max({})          {}'.format(column, max(column))).rjust(8))
    print()


def print_rumus_cost_proses(column, index, digits=2):
    print(str('\tmin({})          {}'.format(column, min(column))).rjust(8))
    print('\t---------------------------------------------------------------------- = ' + 
          '------------------ = ' +
          str(rumus_cost(column, index, digits)))
    print('\t'+ str(column[index]).rjust(32) + str(column[index]).rjust(51))
    print()
    

def print_normalisasi_row_proses(column, category, digits=2):
    for i in range(len(column)):
        if(category == CATEGORY_BENEFIT):
            print_rumus_benefit_proses(column, i, digits)
        elif(category == CATEGORY_COST):
            print_rumus_cost_proses(column, i, digits)
    
def print_normalisasi_proses(columns, categories, digits=2):
    column_size = len(columns)
    
    for i in range(column_size):
        print('+----------------------------------------------------------------+')
        print('|C{}'.rjust(32).format(i+1) + '|')
        print('+----------------------------------------------------------------+\n')
        
        print_normalisasi_row_proses(columns[i], categories[i], digits)

def print_normalisasi(columns, categories, digits=2):
    for ri in to_rows(normalisasi(columns, categories, digits)):
        print('\t' + str(ri))
        print()

def print_rank(matrix, categories, weigths, digits=2):
    print('\n\tW = {' + str(weigths) + '}\n')
    
    for i in range(len(matrix[0])):
        print('\tV{} = '.format(i+1), end='')
        j = 0
        for ri, wi in zip(to_rows(normalisasi(matrix, categories, digits))[i], weigths):
            print('\t({}).({})'.format(wi, ri), end=' ')
            if j != len(matrix)-1:
                print(' + ', end='')
            else:
                vi = sum(rank_i(matrix, categories, weigths, i, digits))
                print(' = ' + str(round(vi, digits+1)))
            j += 1
        print()


def create_rank(matrix, categories, weigths, digits=2, labels=None):
    ordered_index = {}
    for i in range(len(matrix[0])):
        vi = sum(rank_i(matrix, categories, weigths, i, digits))
        if labels is None:
            ordered_index["V"+str(i+1)] = round(vi, digits+1)
        else:
            ordered_index[(labels[i] + " (V"+str(i+1) +")").rjust(18)] = round(vi, digits+1)
    
    i = 0

    [print('\t' + str(key) + '   |   ' + 
        str(value)) for (key, value) in sorted(ordered_index.items(), 
                                               key=lambda x: x[1], 
                                               reverse=True)]

def print_all(matrix, categories, weigths, digits=2, labels=None):
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+')
    print('|NORMALISASI'.rjust(32) + '|')
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')
    print_normalisasi_proses(matrix, categories, digits)
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+')
    print('|HASIL NORMALISASI - R'.rjust(32) + '|')
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')
    print_normalisasi(matrix, categories, digits)
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+')
    print('|NILAI PREFERENSI - PERANGKINGAN'.rjust(32) + '|')
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+')
    print_rank(matrix, categories, weigths, digits)
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+')
    print('|TABEL PERANGKINGAN'.rjust(32) + '|')
    print('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')
    create_rank(matrix, categories, weigths, digits, labels)

def demo_1():
    matrix = [
        [70, 50, 85, 82, 75, 62], #C1
        [50, 60, 55, 70, 75, 50], #C2 
        [80, 82, 80, 65, 85, 75], #C3
        [60, 70, 75, 85, 74, 80]  #C4
    ]

    w = [0.35, 0.25, 0.25, 0.15]
    categories = [CATEGORY_BENEFIT, CATEGORY_BENEFIT, CATEGORY_BENEFIT, CATEGORY_BENEFIT]
    print_all(matrix, categories, w)


def demo_2():
    matrix = [
        [70, 50, 85, 82, 75, 62], #C1
        [50, 60, 55, 70, 75, 50], #C2 
        [80, 82, 80, 65, 85, 75], #C3
        [60, 70, 75, 85, 74, 80]  #C4
    ]

    w = [0.50, 0.10, 0.25, 0.15]

    categories = [
        CATEGORY_BENEFIT,
        CATEGORY_BENEFIT,
        CATEGORY_BENEFIT,
        CATEGORY_BENEFIT
    ]

    print_all(matrix, categories, w)


def demo_3():
    
    matrix_before_converted = [                                                    # ALTERNATIF (KANDIDAT)
        
        #BUDI(V1)         ANI(V2)          SARI(V3)        FITRI(V4)        PUTRI(V5)        ANGEL(V6)        RAHMAN(V7)        YUDI(V8)         INDRA(V9)        CAHYO(V10)        MISEL(V11)       BUNGA(V12)
        [5000000,        15000000,         2000000,         1500000,         2500000,         1100000,         6500000,         8900000,          7600000,         11000000,         980000,         1450000],      #C1 ( Jumlah Penghasilan Orangtua )
        [13,                   14,              13,              15,              14,              12,              13,              13,               13,               14,             15,              13],      #C2 ( Usia )
        [1,                     2,               1,               3,               1,               1,               1,               1,                1,                2,              3,               2],      #C3 ( Kelas )
        [2,                     3,               1,               4,               3,               6,               4,               2,                4,                2,              1,               5],      #C4 ( Jumlah Tanggungan Orangtua )
        [95,                   70,              96,              85,              65,              80,              80,              82,               80,               98,             85,              75]       #C5 ( RATA-RATA NILAI SEMESTER 1 dan SEMESTER 2 )

    ]

    # NOTE :
    # C1 ( Jumlah Penghasilan Orangtua )
    # C2 ( Usia )
    # C3 ( Kelas )
    # C4 ( Jumlah Tanggungan Orangtua )
    # C5 ( Rata-rata Nilai Semester Ganjil dan SEMESTER Genap )
    
    #     C1             C2              C3              C4              C5
    
    w = [0.25,          0.05,           0.15,           0.20,           0.35]


    # Kriteria : Selain C5
    #w = [0.25,          0.05,           0.15,           0.20,           0]

    # Kriteria : Selain C1, C4
    # w = [0.0,          0.05,           0.15,           0.0,           0.35]

    # Kriteria : Hanya C1, C4
    # w = [0.25,          0.0,           0.0,           0.20,           0.0]

    # Kriteria : Hanya C5
    #w = [0.0,          0.0,           0.0,           0.0,           0.35]

    # Kriteria : Tidak Ada  
    # w = [0.0,          0.0,           0.0,           0.0,           0.0]

    categories = [
        CATEGORY_COST,
        CATEGORY_BENEFIT,
        CATEGORY_BENEFIT,
        CATEGORY_BENEFIT,
        CATEGORY_BENEFIT
    ]

    matrix = get_matrix_based_on_subcriteria(matrix_before_converted)

    alternatif_label = ['BUDI','ANI','SARI','FITRI','PUTRI' ,'ANGEL',
                        'RAHMAN','YUDI','INDRA','CAHYO','MISEL','BUNGA']

    print_all(matrix, categories, w, digits=10, labels=alternatif_label)

    show_bar_diagram(alternatif_label, matrix, categories, w, digits=2)


# HELPER FUNCTION FOR FINDING VALUE OF EACH SUBCRITERIA

def cari_nilai_penghasilan_orangtua(penghasilan):
    if penghasilan > 10000000:
        return 1.0
    elif penghasilan > 5000000 and penghasilan <= 10000000:
        return 0.75
    elif penghasilan > 1000000 and penghasilan <= 5000000:
        return 0.5
    elif penghasilan <= 1000000:
        return 0.25

def cari_nilai_usia(usia):
    if usia <= 13:
        return 0.25
    elif usia == 14:
        return 0.5
    elif usia == 15:
        return 0.75
    elif usia > 15:
        return 1.0

def cari_nilai_kelas(kelas):
    if kelas == 1:
        return 0.33
    elif kelas == 2:
        return 0.66
    elif kelas == 3:
        return 0.99

def cari_nilai_jumlah_tanggungan_orangtua(jumlah_tanggungan):
    if jumlah_tanggungan == 1:
        return 0
    elif jumlah_tanggungan == 2:
        return 0.25
    elif jumlah_tanggungan == 3:
        return 0.5
    elif jumlah_tanggungan == 4:
        return 0.75
    elif jumlah_tanggungan >= 5:
        return 1.0

def cari_nilai_rata_rata_semester(rata_rata_semester_1_2):
    if rata_rata_semester_1_2 <= 65:
        return 0
    elif rata_rata_semester_1_2 > 65 and rata_rata_semester_1_2 <= 70:
        return 0.25
    elif rata_rata_semester_1_2 > 70 and rata_rata_semester_1_2 <= 80:
        return 0.5
    elif rata_rata_semester_1_2 > 80 and rata_rata_semester_1_2 <= 90:
        return 0.75
    elif rata_rata_semester_1_2 > 90 and rata_rata_semester_1_2 <= 100:
        return 1.0

def get_matrix_based_on_subcriteria(matrix_before_converted):
    matrix_after_converted = []

    for i in to_rows(matrix_before_converted):
        matrix_after_converted.append([
            cari_nilai_penghasilan_orangtua(i[0]),
            cari_nilai_usia(i[1]),
            cari_nilai_kelas(i[2]),
            cari_nilai_jumlah_tanggungan_orangtua(i[3]),
            cari_nilai_rata_rata_semester(i[4])
        ])

    matrix = to_rows(matrix_after_converted)

    return matrix

def show_bar_diagram(labels, matrix, categories, weigths, digits=2):
    ordered_index = {}
    
    for i in range(len(matrix[0])):
        vi = sum(rank_i(matrix, categories, weigths, i, digits))
        ordered_index[labels[i]] = round(vi, digits+1)
    
    bar_colors = ['cyan', 'teal', 'crimson', 'deeppink', 'blue', 'orangered',
                  'yellow', 'lime', 'navy', 'turquoise', 'slategray', 'olive']

    alternatif = [alt for alt in ordered_index.keys()]
    preference_value = [value for value in ordered_index.values()]
    y_pos = np.arange(len(alternatif))
    
    plt.rcdefaults()
    
    plt.figure(figsize=(9, 5))
    plt.bar(y_pos, preference_value, align='center', alpha=0.5, color=bar_colors)
    plt.xticks(y_pos, alternatif)
    plt.ylabel('Nilai Preferensi')
    plt.title('Kandidat Penerima Beasiswa Berdasarkan Prestasi dan Perekonomian Keluarga Siswa')

    plt.show()


if __name__ == '__main__':
    demo_3()
