import streamlit as st
import demo_utils as du
import json
import os
import streamlit_ace as st_ace
from strimlitbook.reader import read_ipynb
from streamlit_card import card
import streamlit_tags as tags


# session related function
def display_gen_nb():
    # # load user's notebook as json
    # byte_nb = st.session_state.gen_uploaded_file
    # json_nb = json.loads(byte_nb)

    # dump it locally 
    # with open('dump_PLBART_documented.ipynb', 'w+', encoding='utf-8-sig') as json_dump:
    #     json.dump(json_nb, json_dump)  


    nb = read_ipynb('dump_PLBART_documented.ipynb')
    nb.display()
    




# '''TODO : 
#  prep help strings 
#  DOM AND TECH INTO SESSION !!!!!
# '''

DUMP_PATH_COM = r'DEMO'
CLASS_RUN_PATH = r'Classification_Task/notebooks/scripts/run.py'
DOCGEN_RUN_PATH = r'DocGen_Task/scripts/terminal_run.py'


# page config
st.set_page_config(
    page_title="Magic notebook",
    page_icon="✨",
)

# sidebar
st.sidebar.markdown("# Upload your notebook Page")


# session state initializing
du.initialize_session(st.session_state)


if st.session_state.uploaded_file == None:
    st.error('No file has been uploaded. Please navigate to the main page and upload a notebook.')
    st.session_state.go_back_main =  st.button('Main page')
    if st.session_state.go_back_main:
        du.switch_page('demo')

else:
    st.write(st.session_state.documented)
    indent, top_class_but, top_doc_but, top_go_but = st.columns([2, 5, 4, 1], gap='small')

    # back button
    with indent:
        st.write(' ')
        st.write(' ')
        st.session_state.go_back_main02 =  st.button('Upload another notebook')
        if st.session_state.go_back_main02:
            du.switch_page('demo')

    # classification
    with top_class_but:
        classify = st.multiselect('Classify the notebook by', ['Domain', 'Technique'], help='help')

    # doc gen
    with top_doc_but:
        gendoc = st.selectbox('Generate documentation using', ('-', 'PLBART'), help='help')

    # go button
    with top_go_but:
        if (len(classify) != 0) | (gendoc != '-'):
            st.write(' ')
            st.write(' ')
            top_go_button = st.button('Go!')
    
  
###### Classification

    # classify by domain
    if ('Domain' in classify) and (len(classify) == 1) and (top_go_button):

        if st.session_state.domain == None:
            os.system('python ' + CLASS_RUN_PATH + ' ' + 'dump.json ' + '--class domain >> file.txt')

            with open('file.txt') as f:
                contents = str(f.readlines()[-1])
            
            st.session_state.domain, st.session_state.technique = du.prep_classification(contents)
        # horizontal divider
        '''
        ---
        '''
        # st.write("Your notebook's domain is : ", dom)
        st.metric(label='Domain', value=st.session_state.domain, delta='Predicted')
        '''
        ---
        '''
        


    # classify by technique
    elif ('Technique' in classify) and (len(classify) == 1) and (top_go_button):

        if st.session_state.technique == None:
            os.system('python ' + CLASS_RUN_PATH + ' ' + 'dump.json ' + '--class technique >> file.txt')
            with open('file.txt') as f:
                contents = str(f.readlines()[-1])

            st.session_state.domain, st.session_state.technique = du.prep_classification(contents)
        # # horizontal divider
        '''
        ---
        '''
        # st.write("Your notebook's technique is : ", tech) 
        st.metric(label='Technique', value=st.session_state.technique, delta='Predicted')
        '''
        ---
        '''
        

    # classify by both
    elif ('Technique' in classify) and ('Domain' in classify) and (top_go_button):
        os.system('python ' + CLASS_RUN_PATH + ' ' + 'dump.json ' + '--class both >> file.txt')
        with open('file.txt') as f:
            contents = str(f.readlines()[-1])

        st.session_state.domain, st.session_state.technique = du.prep_classification(contents)    
        # horizontal divider
        '''
        ---
        '''
        # st.write("Your notebook's domain & technique are : ", dom, ' & ', tech) 
        # st.button(dom, disabled=True)
        l, r = st.columns(2)
        with l:
            st.metric(label='Domain', value=st.session_state.domain, delta='Predicted')
        with r:
            st.metric(label='Technique', value=st.session_state.technique, delta='Predicted')
        
        '''       
        ---
        '''
    
    

    if (gendoc == 'PLBART') and (top_go_button):

        if not(st.session_state.documented):
            os.system('python ' + DOCGEN_RUN_PATH + ' ' + 'dump.json')
        with open('dump_PLBART_documented.ipynb', encoding='utf-8-sig') as doc_nb:
                
            if '.json' in str(st.session_state.uploaded_file_name):
                st.session_state.uploaded_file_name = str(st.session_state.uploaded_file_name).rstrip('.json')
            elif '.ipynb' in str(st.session_state.uploaded_file_name):
                st.session_state.uploaded_file_name = str(st.session_state.uploaded_file_name).rstrip('.ipynb')

            c, o, l = st.columns(3)
            with o:
                st.write('/n')
                btn = st.download_button(
                label="🎉 Download your documented notebook here ! 🎉",
                data=doc_nb,
                file_name=str(st.session_state.uploaded_file_name) + '_PLBART_documented.ipynb',
                mime='application/ipynb+json',
                )
        display_gen_nb()
        st.session_state.documented = True

    if not(st.session_state.documented):
        du.display_nb()
    else:
        with open('dump_PLBART_documented.ipynb', encoding='utf-8-sig') as doc_nb:
                
            if '.json' in str(st.session_state.uploaded_file_name):
                st.session_state.uploaded_file_name = str(st.session_state.uploaded_file_name).rstrip('.json')
            elif '.ipynb' in str(st.session_state.uploaded_file_name):
                st.session_state.uploaded_file_name = str(st.session_state.uploaded_file_name).rstrip('.ipynb')

            c, o, l = st.columns(3)
            with o:
                st.write('/n')
                btn = st.download_button(
                label="🎉 Download your documented notebook here ! 🎉",
                data=doc_nb,
                file_name=str(st.session_state.uploaded_file_name) + '_PLBART_documented.ipynb',
                mime='application/ipynb+json'
                )
        display_gen_nb()
        st.session_state.documented = True

    
        














