def distribute_in_length(i, total_number, item_length, total_length):
    """Returns position of the i-th item with length item_length, such that it
    is evenly distributed among a total_number number of similar items along
    a length total_length.
    """
    if total_number == 1:
        return float(total_length/2) - item_length/2
    in_between_length = (total_length - total_number*item_length)/(total_number-1)
    pos = i*item_length + i*in_between_length
    return pos
