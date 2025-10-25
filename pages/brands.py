import streamlit as st
from collections import defaultdict
import math

st.title("Supported Brands")
st.caption("SZTE IMN104L-2025/26/1-IMN104L-2")

st.write("This page shows the brands supported by the brand logo detector.")
st.write("")

classes_file = "resources/classes.txt"

num_cols = 3

@st.cache_resource
def load_and_prepare_classes():
    with open(classes_file, "r") as f:
        classes = [line.strip() for line in f if line.strip()]

    def sort_key(c):
        first = c[0].upper()
        priority = 0 if first.isalpha() else 1
        return (priority, first, c)

    classes = sorted(classes, key=sort_key)

    letter_to_brand = defaultdict(list)
    others = []
    for c in classes:
        first = c[0].upper()
        if first.isalpha():
            letter_to_brand[first].append(c)
        else:
            others.append(c)
            
    groups = []
    for letter in sorted(letter_to_brand.keys()):
        groups.append([letter] + letter_to_brand[letter])
    if others:
        groups.append(["#"] + others)
        
    total_items = sum(len(g) for g in groups)
    approx_col_size = math.ceil(total_items / num_cols)
    
    columns_content = [[] for _ in range(num_cols)]
    current_col = 0
    current_count = 0
    
    for group in groups:
        group_size = len(group)
        if current_count + group_size <= approx_col_size or current_count == 0:
            columns_content[current_col].extend(group)
            current_count += group_size
        else:
            current_col += 1
            if current_col >= num_cols:
                current_col = num_cols - 1
            columns_content[current_col].extend(group)
            current_count = group_size

    return classes, columns_content

classes, columns_content = load_and_prepare_classes()
    
search_text = st.text_input("Search brands")

if search_text:
    filtered = [c for c in classes if search_text.lower() in c.lower()]
    if filtered:
        st.write("Matching brands:")
        for c in filtered:
            st.write(c)
    else:
        st.write("No brands found.")
else:
    st.write("All brands")
    st.write("")

    cols = st.columns(num_cols)
    for col, items in zip(cols, columns_content):
        for item in items:
            if len(item) == 1 and item.isalpha():
                col.markdown(f"<h4>{item}</h4><hr>", unsafe_allow_html=True)
            elif item == "#":
                col.markdown("<h4>#</h4><hr>", unsafe_allow_html=True)
            else:
                col.write(item)