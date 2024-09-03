import streamlit as st
import json


# Load the data
@st.cache_data
def load_data():
    with open("./demo_result.json", "r") as f:
        return json.load(f)


# Get all unique lv0 values
@st.cache_data
def get_unique_lv0(data):
    lv0_values = set()
    for item in data:
        lv0_values.update(item["keyword"]["lv0"])
    return sorted(list(lv0_values))


def search_page():
    st.title("Search Page")

    data = load_data()
    unique_lv0 = get_unique_lv0(data)

    search_term = st.selectbox("Select a category to search:", unique_lv0)

    if search_term:
        found = False
        for item in data:
            if search_term in item["keyword"]["lv0"]:
                found = True
                st.subheader(item["title"])
                if st.button(f"View Details", key=f"view_{item['index']}"):
                    st.session_state.page = "detail"
                    st.session_state.index = item["index"]
                    st.rerun()
        if not found:
            st.info("No matching categories found.")


def detail_page():
    data = load_data()
    st.title(f"Details for Index {st.session_state.index}")
    item = next(item for item in data if item["index"] == st.session_state.index)

    st.header(item["title"])
    st.write(item["description"])

    st.subheader("Noun Phrases")
    st.write(", ".join(item["keyword"]["noun_phrases"]))

    for level in ["lv0", "lv1", "lv2", "lv3"]:
        st.subheader(f"Level {level}")
        st.write(", ".join(item["keyword"][level]))

    if st.button("Back to Search", key="back_to_search"):
        st.session_state.page = "search"
        st.rerun()


def main():
    if "page" not in st.session_state:
        st.session_state.page = "search"

    if st.session_state.page == "search":
        search_page()
    elif st.session_state.page == "detail":
        detail_page()


if __name__ == "__main__":
    main()
