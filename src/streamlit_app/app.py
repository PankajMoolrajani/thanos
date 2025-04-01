import streamlit as st


st.set_page_config(
    layout='centered',
    page_title='Threat Modeling',
    page_icon='🛡️'
)


def nav():
    st.sidebar.page_link('pages/list.py', label='list')
    st.sidebar.page_link('pages/1_create.py', label='Create Threat Model', icon='🛠️')


def main():
    nav()
    st.header('🏡 Welcome to Threat Modeling')


if __name__ == '__main__':
    main()