import numpy as np
import math
import sys
np.set_printoptions(threshold=sys.maxsize)

#Generate updated ss array
def edit_ss_array(ss, dotbracket):
    ss_edit = ''
    right_symbols = [")", "]", ">", "}"]
    left_symbols = ["(", "[", "<", "{"]
    for i, s in enumerate(ss):
        if (dotbracket[i] in right_symbols or dotbracket[i].islower()) and s == "S":
            ss_edit += "R"
        elif (dotbracket[i] in left_symbols or dotbracket[i].isupper()) and s == "S":
            ss_edit += "L"
        else:
            ss_edit += s
    return ss_edit

def create_matrix(rows, cols, k, ss_1, ss_2, gap, extend):
    middle_matrix_direction = np.full((rows,cols),"m",  dtype="object")
    X_matrix_direction = np.full((rows,cols), "x", dtype="object")
    Y_matrix_direction = np.full((rows,cols),"y", dtype="object")
    middle_matrix = np.ones((rows, cols))*-1000000
    X_matrix = np.ones((rows, cols))*-1000000
    Y_matrix = np.ones((rows, cols))*-1000000
    count = -1
    for i in range(1, k+1):
        middle_matrix_direction[i,0] = 'y'
        X_matrix_direction[i,0] = 'y'
        Y_matrix_direction[i,0] = 'y'
        X_matrix[i,0] = gap + (i-1)*extend
    for j in range(1, k+1):
        middle_matrix_direction[0,j] = 'x'
        X_matrix_direction[0,j] = 'x'
        Y_matrix_direction[0,j] = 'x'
        Y_matrix[0,j] = gap + (j-1)*extend
    for j in range(1, cols):
        for d in range(-k, k+1):
            i = int(math.ceil(((float(rows)-1)/(cols-1))*j + d))
            if i >= 1 and i < rows:
                score_m, score_x, score_y = calc_score(middle_matrix, X_matrix, Y_matrix, i, j, rows, cols, ss_1, ss_2, extend, k)
                middle_matrix[i][j] = score_m[0]
                X_matrix[i][j] = score_x[0]
                Y_matrix[i][j] = score_y[0]
                middle_matrix_direction[i][j] = score_m[1]
                X_matrix_direction[i][j] = score_x[1]
                Y_matrix_direction[i][j] = score_y[1]
    middle_max = middle_matrix[rows-1][cols-1]
    X_max = X_matrix[rows-1][cols-1]
    Y_max = Y_matrix[rows-1][cols-1]
    max_list = [[X_max, 'x'],[Y_max,'y'], [middle_max, 'm']]
    final_score = -10000000
    max_matrix = 'w'
    for i in max_list:
        value, matrix = i
        if value > final_score:
            final_score = value
            max_matrix = matrix
        elif value == final_score and max_matrix != 'm':
            if  matrix == 'm':
                final_score = value
                max_matrix = matrix
    return middle_matrix, X_matrix, Y_matrix, middle_matrix_direction, X_matrix_direction, Y_matrix_direction, max_matrix, final_score

def calc_score(matrix_m, matrix_x, matrix_y, i, j, rows, cols, ss_1, ss_2, extend, k):
    score = generate_score(i,j, ss_1, ss_2)
    if inside_band(i-1,j, rows, cols, k):
        gap_extend_up = generate_gap_extend_score(i,j, "up", ss_1, ss_2)
        gap_up = generate_gap_score(i,j,"up", ss_1, ss_2)
        score_yy = matrix_y[i-1][j] + gap_extend_up
        score_xy = matrix_x[i-1][j] + gap_up
        score_my = matrix_m[i - 1][j] + gap_up
        score_y = find_max_position(score_my, score_xy, score_yy)
        score_y = find_max_position(score_my, score_xy, score_yy)
    elif not inside_band(i-1,j, rows, cols, k):
        gap_extend_up = generate_gap_extend_score(i,j, "up", ss_1, ss_2)
        score_yy = matrix_y[i-1][j-1] + gap_extend_up
        score_y = [score_yy, 'y']
    if inside_band(i, j-1,rows, cols, k):
        gap_extend_left = generate_gap_extend_score(i,j, "left", ss_1, ss_2)
        gap_left = generate_gap_score(i,j,"left", ss_1, ss_2)
        score_yx = matrix_y[i][j - 1] + gap_left
        score_mx = matrix_m[i][j - 1] + gap_left
        score_xx = matrix_x[i][j - 1] + gap_extend_left
        score_x = find_max_position(score_mx, score_xx, score_yx)
    elif not inside_band(i,j-1, rows, cols,k):
        gap_extend_left = generate_gap_extend_score(i,j, "left", ss_1, ss_2)
        score_xx = matrix_x[i-1][j-1] + gap_extend_left
        score_x = [score_xx, 'x']
    
    score_mm = matrix_m[i - 1][j - 1] + score
    score_xm = matrix_x[i - 1][j - 1] + score
    score_ym = matrix_y[i - 1][j - 1] + score
    score_m = find_max_position(score_mm, score_xm, score_ym)
    return score_m, score_x, score_y

def find_max_position(m, x, y):
    scores = np.array([m,x,y])
    max_score = np.max(scores)
    max_indices = np.where(scores == max_score)
    max_indices = list(max_indices[0])
    if 0 in max_indices:
        return [max_score, 'm']
    elif len(max_indices) >1:
        return [max_score, 'y']
    elif len(max_indices) == 1 and max_indices[0] == 1:
        return [max_score, 'x']
    elif len(max_indices) == 1 and max_indices[0] == 2:
        return [max_score, 'y']
  
        
def traceback(middle_matrix, X_matrix, Y_matrix, middle_matrix_direction, X_matrix_direction, Y_matrix_direction, max_matrix, rows, cols, ss_1, ss_2):
    aligned_seq1 = ''
    aligned_seq2 = ''
    i, j = rows-1, cols-1
    if max_matrix == "m":
        direction = middle_matrix_direction[i][j]
    elif max_matrix == "y":
        direction = Y_matrix_direction[i][j]
    elif max_matrix == "x":
        direction = X_matrix_direction[i][j]
    current_matrix = max_matrix
    while not (i==0 and j == 0):
        if i == 0 and j > 0:
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = ss_2[j-1] + aligned_seq2
        elif j == 0 and i > 0:
            aligned_seq1 = ss_1[i-1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
        elif current_matrix == "m":
            aligned_seq1 = ss_1[i-1] + aligned_seq1
            aligned_seq2 = ss_2[j-1] + aligned_seq2
        elif current_matrix == 'y':
            aligned_seq1 = ss_1[i-1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
        elif current_matrix == 'x':
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = ss_2[j-1] + aligned_seq2
        else:
            print ('Error:')
            break
        current_matrix, direction, i, j = next_move(middle_matrix_direction, X_matrix_direction, Y_matrix_direction, current_matrix, direction, i, j)
    
    return aligned_seq1, aligned_seq2

def get_dist(alignment_1, alignment_2):
    match = 0.0
    for i, feature_1 in enumerate(alignment_1):
        feature_2 = alignment_2[i]
        if feature_1 == feature_2:
            match += 1.0
    ID = match/len(alignment_1)
    dist = 1-ID
    return dist

def next_move (middle_matrix, X_matrix, Y_matrix, current_matrix, direction, i, j):
    if j == 0 and i > 0:
        current_matrix = "y"
        direction = "y"
        i = i -1
        j = j
        direction = "y"
    elif i == 0 and j > 0:
        current_matrix = "x"
        direction = "x"
        i = i
        j = j -1
    elif j > 0 and i > 0: 
        if current_matrix == 'm':
            current_matrix = direction
            i = i-1
            j = j-1
            if direction == "m":
                direction = middle_matrix[i][j]
            elif direction == "y":
                direction = Y_matrix[i][j]
            elif direction == "x":
                direction = X_matrix[i][j]
        elif current_matrix == 'x':
            current_matrix = direction
            j = j-1
            if direction == "m":
                direction = middle_matrix[i][j]
            elif direction == "y":
                direction = Y_matrix[i][j]
            elif direction == "x":
                direction = X_matrix[i][j]
        elif current_matrix == 'y':
            current_matrix = direction
            i = i-1
            if direction == "m":
                direction = middle_matrix[i][j]
            elif direction == "y":
                direction = Y_matrix[i][j]
            elif direction == "x":
                direction = X_matrix[i][j]
    return current_matrix, direction, i, j

def score_alignment(ss_1, ss_2, db_1, db_2, k):
    ss_1 = edit_ss_array(ss_1, db_1)
    ss_2 = edit_ss_array(ss_2, db_2)
    rows = len(ss_1) + 1
    cols = len(ss_2) + 1
    middle_matrix, X_matrix, Y_matrix, middle_matrix_direction, X_matrix_direction, Y_matrix_direction, max_matrix, final_score  = create_matrix(rows, cols, k, ss_1, ss_2, gap, extend)
    aligned_ss_1, aligned_ss_2  = traceback(middle_matrix, X_matrix, Y_matrix, middle_matrix_direction, X_matrix_direction, Y_matrix_direction, max_matrix, rows, cols, ss_1, ss_2)
    dist = get_dist(aligned_ss_1, aligned_ss_2)
    return aligned_ss_1, aligned_ss_2, dist, final_score, X_matrix, Y_matrix, middle_matrix

def generate_gap_score(i, j, direction, ss_1, ss_2):
    if direction == "up":
        a, b = ss_1[i-1], "-"
        if (a,b) in gap_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-2] == ss_2[j-1] and ss_1[i] == ss_2[j-1]:
                return gap_score_dictionary[a,b]
            else:
                return gap
        elif (b,a) in gap_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-2] == ss_2[j-1] and ss_1[i] == ss_2[j-1]:
                return gap_score_dictionary[b,a]
            else:
                return gap
        else:
            return gap

    elif direction == "left":
        a, b = "-", ss_2[j-1]
        if (a,b) in gap_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-1] == ss_2[j-2] and ss_1[i] == ss_2[j-1]:
                return gap_score_dictionary[a,b]
            else:
                return gap
        elif (b,a) in gap_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-1] == ss_2[j-2] and ss_1[i] == ss_2[j-1]:
                return gap_score_dictionary[b,a]
            else:
                return gap
        else:
            return gap

def generate_gap_extend_score(i, j, direction, ss_1, ss_2):
    if direction == "up":
        a, b = ss_1[i-1], "-"
        if (a,b) in extend_score_dictionary and i-2 >= 0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-2] == ss_2[j-1] and ss_1[i] == ss_2[j-1]:
                return extend_score_dictionary[a,b]
            else:
                return extend
        elif (b,a) in extend_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-2] == ss_2[j-1] and ss_1[i] == ss_2[j-1]:
                return extend_score_dictionary[b,a]
            else:
                return extend
        else:
            return extend

    elif direction == "left":
        a, b = "-", ss_2[j-1]
        if (a,b) in extend_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-1] == ss_2[j-2] and ss_1[i] == ss_2[j-1]:
                return extend_score_dictionary[a,b]
            else:
                return extend
        elif (b,a) in extend_score_dictionary and i -2 >=0 and j-2 >=0 and i < len(ss_1) and j < len(ss_2):
            if ss_2[j] == ss_1[i] and ss_1[i-1] == ss_2[j-2] and ss_1[i] == ss_2[j-1]:
                return extend_score_dictionary[b,a]
            else:
                return extend
        else:
            return extend

def generate_score(i,j, ss_1, ss_2):
    a,b = ss_1[i-1], ss_2[j-1]
    if (a,b) in score_dictionary:
        return score_dictionary[a,b]
    else:
        try:
            return score_dictionary[b,a]
        except:
            print ('error')

def inside_band(i,j,rows, cols, k):
    i_diag = int(math.ceil(((float(rows)-1)/(float(cols)-1))*j))
    i_range =  range(i_diag - k, i_diag + k)
    if i in i_range:
        return True
    else:
        return False

########
##MAIN##
########
gap = -3
extend = -6

##GAP_PENALTIES##
gap_score_dictionary = {('-','M'): -2.8, ('-','I'):-2.1 , ('-','R'): -1.4, ('-','L'): -1.4, ('-','B'): -2.3, ('-','E'): -.5,('-','X'): -1.3,('-','H'): -2.2} 
#old {('-','M'): -3.1, ('-','I'):-3.2 , ('-','R'): -3.3, ('-','L'): -3.3, ('-','B'): -3.3, ('-','E'): -2.5,('-','X'): -1.6,('-','H'): -.5} 

extend_score_dictionary = {('-','M'): -5.5, ('-','I'): -4.3, ('-','R'): -2.8, ('-','L'): -2.8, ('-','B'): -4.7, ('-','E'): -1.0,('-','X'): -2.6,('-','H'): -4.3} 
#old {('-','M'): -6.2, ('-','I'): -6.5, ('-','R'): -6.5, ('-','L'): -6.5, ('-','B'): -6.6, ('-','E'): -5,('-','X'): -3.2,('-','H'): -1} 

##SCORING_MATRIX##
score_dictionary = {('M','M'): 4, ('M','I'): -4, ('M','R'): -4, ('M','L'): -4, ('M','B'): -4, ('M','E'): -2,('M','X'): -2,('M','H'): -4, ('I','I'): 2,('I','R'): -4,('I','L'): -4,('I','B'): 0,('I','E'): -2,('I','X'): -2,('I','H'): -4,('R','R'): 6,('R','L'): -8,('R','B'): -4,('R','E'): -4,('R','X'): -2,('R','H'): -4,('L','L'): 6,('L','B'): -4,('L','E'): -4,('L','X'): -2,('L','H'): -4,('B','B'): 2,('B','E'): -2,('B','X'): -2,('B','H'): -4,('E','E'): 2,('E','X'): -2,('E','H'): -4,('X','X'): 2,('X','H'): -4,('H','H'): 4}
# true scoring score_dictionary = {('M','M'): 4, ('M','I'): -4, ('M','R'): -4, ('M','L'): -4, ('M','B'): -4, ('M','E'): -2,('M','X'): -2,('M','H'): -4, ('I','I'): 2,('I','R'): -5,('I','L'): -5,('I','B'): 0,('I','E'): -2,('I','X'): -2,('I','H'): -4,('R','R'): 6,('R','L'): -8,('R','B'): -5,('R','E'): -4,('R','X'): -2,('R','H'): -4,('L','L'): 6,('L','B'): -5,('L','E'): -4,('L','X'): -2,('L','H'): -4,('B','B'): 2,('B','E'): -2,('B','X'): -2,('B','H'): -4,('E','E'): 2,('E','X'): 0,('E','H'): -4,('X','X'): 2,('X','H'): -4,('H','H'): 4}
