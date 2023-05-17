import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
    .ellipsis {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 3;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: -15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    df = pd.read_csv('covid_abstracts.csv', nrows=10)
    st.title('Search Engine')
    query = st.text_input('Enter search words:')

    # st.write(df)  # visualize my dataframe in the Streamlit app

    m1 = df["title"].str.contains(query)
    df_search = df[m1]
    # Another way to show the filtered results
    # Show the cards
    if query:
        count_str = f'<b style="font-size: 15px; ">About {len(df_search)} results returned</b>'
        st.markdown(f'{count_str}', unsafe_allow_html=True)
        for n_row, col in df_search.reset_index().iterrows():
            title = col['title'].strip()
            cite = col['url'].strip()
            description = col['abstract'].strip()
            # draw the card
            st.markdown(f'<h5><a href="{cite}" target="_blank">{title}</a></h5>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:green; margin-bottom:-15px; font-weight: 700;">{cite}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="ellipsis">{description}</p>', unsafe_allow_html=True)
            st.write("---")
            
if __name__ == '__main__':
    main()