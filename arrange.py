from functools import cmp_to_key
def sortbyCond_ar_dc(a, b):
    if (a[0] != b[0]):
        return (a[0] - b[0]) # -
    else:
        return b[1] - a[1] # +
def sortbyCond_dr_ac(a, b):
    if (a[0] != b[0]):
        return b[0] - a[0] # -
    else:
        return b[1] - a[1] # +
stack = [(3, 9), (3, 10), (4,8), (5, 6), (2, 10), (2, 30)]
stack.sort(key = cmp_to_key(sortbyCond_ar_dc))  # Hàng tăng cột giảm
print (stack)
stack.sort(key = cmp_to_key(sortbyCond_ar_dc), reverse=True) # hàng giảm cột tăng
print (stack)
stack.sort(key = cmp_to_key(sortbyCond_dr_ac)) # Hàng giảm cột giảm
print (stack)
stack.sort(key = cmp_to_key(sortbyCond_dr_ac), reverse=True) # Hàng tăng cột tăng
print (stack)

# [(2, 30), (2, 10), (3, 10), (3, 9), (4, 8), (5, 6)]
# [(5, 6), (4, 8), (3, 9), (3, 10), (2, 10), (2, 30)]
# [(5, 6), (4, 8), (3, 10), (3, 9), (2, 30), (2, 10)]
# [(2, 10), (2, 30), (3, 9), (3, 10), (4, 8), (5, 6)]
# Ascending row - Ascending column
# Descending row - Ascending column
# Ascending row - Descending column .
# Descending row - Descending column