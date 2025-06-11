zero_symbols = ["\u200b","\u200c","\u200d","\u200e","\u200f"]

def delete_unicode_symbols(text):
    new_text = "".join([char for char in text if char not in zero_symbols])
    return repr(new_text)




# a = input()
# delete_unicode_symbols(a)
