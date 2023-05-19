import streamlit as st
import pandas as pd
import urllib.request as req

st.set_page_config(page_title="Search Engine")
#css style
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=Open Sans&display=swap'); 

    .title {
        font-family: 'Open Sans', sans-serif;
    }
    .block-container {
            padding-top: 10px !important;
    }
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
    st.markdown("<h1 class='title'>Covid-19 Search Engine</h1>", unsafe_allow_html=True)
    query = st.text_input('Enter search words:')#get the query input

    #show the query result
    if query:
        #create a connection to the solr server
        connect = req.urlopen(f'http://localhost:8983/solr/testing/select?hl.fl=abstract&hl.tag.post=<%2Fb>&hl.tag.pre=<b>&hl=true&indent=true&q.op=OR&q={query}&useParams=&wt=python')
        response = eval(connect.read()) #get the response

        #get and display the total number of results found
        num_found = response['response']['numFound'] 

        if num_found:
            count_str = f'<b style="font-size: 15px; color: gray;">About {num_found} results returned</b>'
            st.markdown(f'{count_str}', unsafe_allow_html=True)

            #display the title, url and short description of results found
            for document in response['response']['docs']:
                id = document['id']
                title = str(document['_title'])[2:-2]
                cite = str(document['url'])[2:-2]
                highlighted_snippets = response['highlighting'][id]
                
                #get the higlighted part
                if highlighted_snippets:
                    description = str(highlighted_snippets['abstract'])[2:-2]
                else:
                    description = str(document['abstract'])[2:-2]

                #draw the card
                st.markdown(f'<h5><a href="{cite}" target="_blank">{title}</a></h5>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:green; margin-bottom:-15px; font-weight: 700;">{cite}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="ellipsis">{description}</p>', unsafe_allow_html=True)
                st.write("---")

        else:
            st.markdown(f'<b style="font-size: 15px; ">There are no results found</b>', unsafe_allow_html=True)

            
if __name__ == '__main__':
    main()