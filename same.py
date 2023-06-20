

import streamlit as st
import math
import numpy as np
import pandas as pd

############################################################################################

def add_bg_from_url():
    st.set_page_config(layout="wide")
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2019/12/13/09/46/umbrella-4692572__340.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
# this is the main function in which we define our webpage 
#############################################################################################

def slab_all_cal(fc,fy,span,cover,live_load,dead_load,surface_finishing):
    import math
    global effective_depth_span,overall_depth,effective_span,moment,Ast,Ast_min,main_bar_space,dist_bar_space

    mf=1.3#assume mf is 1.3
    dimbar=10#mm
    Tdeff=125## Asumme 
    cc=20#mm

    effective_depth_span=(span*1000)/(26*mf)
    overall_depth=Tdeff+(cc+(dimbar/2))
    effective_span =((span*1000)+(overall_depth))/1000
    total_load=live_load+dead_load+surface_finishing
    fact_load=1.5*total_load
    moment=(fact_load*(effective_span**2))/16
    x=1-math.sqrt(1-((4.6*moment*10**6)/(fc*1000*Tdeff**2)))
    Ast=(0.5*(fc/fy))*x*1000*Tdeff
    Ast_min=0.0012*1000*overall_depth
    
    main_bar_space=min(3*Tdeff,300)
    dist_bar_space=min(5*Tdeff,450)

    return effective_span
    


#************************************************************************************************
#Slab Design 
def slab_design():
      # giving the webpage a title
    #st.set_page_config(layout="wide")

    global Lspan,Mf,dim_bar
    # here we define some of the front end elements of the web page like 
    # the font and background color, the padding and the text to be displayed
    html_temp = """
    <div style ="background-White:LavenderBlush;padding:13px">
    <h1 style ="color:red;">DESIGNING A G+2 STRUCTURE USING PYTHON WITH GUI </h1>
    </div>
    """
    # this line allows us to display the front end aspects we have 
    # defined in the above code
    st.markdown(html_temp, unsafe_allow_html = True)
    st.image(['images.png'])
    # the following lines create text boxes in which the user can enter 
    # the data required to make the prediction
    fc =st.text_input("Enter the concrete grade (in MPa)")
    fy =st.text_input("Enter the steel grade (in MPa):")
    span =st.text_input("Enter the span of the slab (in meters):")
    cover=st.text_input("Enter The cover in mm")
    
    st.title("Inputs For Loads")
    live_load=st.text_input("Enter the live load")
    dead_load=st.text_input("Enter dead_load of the slab in kN/m3: ")
    surface_finishing=st.text_input("Enter The surface_finishing Kn/m2")
    
    if st.button("Result"):
        df=pd.DataFrame({"Span m":span,
                         "cover mm":cover,
                         "effective_span m ":slab_all_cal(float(fc),float(fy),float(span),float(cover),float(live_load),float(dead_load),float(surface_finishing)),
                         "effective depth of span mm":effective_depth_span,
                         "Overall_depth mm":overall_depth,
                         "Bending Moment Mu kn/m":moment,
                         },index=[0])
        
        data2=pd.DataFrame({"Ast mm2":Ast,
                         "Ast_min mm2":Ast_min,
                         "main Bar Spacing mm":main_bar_space,
                         "Dist steel Spacing mm":dist_bar_space},index=[0])
        
        st.table(df)
        st.table(data2)
     
#********************************************************************************************************
#Beam Design 
def beam_cal(fc1,fy1,span1,flange_depth,web_depth,impo_load):
    import math
    global bf1,effective_depth2,effective_span2,ultimate_load,effective_depth_of_span2,ultimate_BM,sf,bf,muf,Ast_for_beam
    effective_depth2=((span1*1000)/15)
    effective_depth_of_span2=(span1+(effective_depth2/1000))
    effective_span2=span1+0.2
    ultimate_load=1.5*(impo_load)
    
    ultimate_BM=((ultimate_load)*(effective_span2**2))/8
    sf=(((ultimate_load)*(effective_span2))/2)*100
    bf=((effective_span2/6)+(web_depth/1000)+6*(flange_depth/1000))*100
    bf1=bf/100
    x1=effective_depth2-(0.416*flange_depth)
    muf=bf1*flange_depth*0.36*fc1*(x1)
    x3=1-math.sqrt(((4.6*ultimate_BM*10**6)/(fc1*1000*effective_depth2**2)))
    Ast_for_beam=(0.5*(fc1/fy1))*x3*1000*effective_depth2
    
    
    return effective_depth2




def beam():
    html_temp = """
    <div style ="background-White:LavenderBlush;padding:13px">
    <h1 style ="color:red;">DESIGNING OF Beam </h1>
    </div>
    """
    # this line allows us to display the front end aspects we have 
    # defined in the above code
    st.markdown(html_temp, unsafe_allow_html = True)
    st.image(['images.png'])
    fc1=st.text_input("Enter The Compressive strength of concrete in MPa")
    fy1=st.text_input("Enter The Yield strength of steel in MPa")
    span1=st.text_input("Enter The Span in m")
    flange_depth=st.text_input("Enter The depth of flange in mm")
    web_depth=st.text_input("Enter The  depth of web in mm")
    impo_Load=st.text_input("Enter the Imposed Load Kn/m2")
    
    ############################
    
    if st.button("Result"):
        df=pd.DataFrame({"Span In m":span1,
                         "Effective Depth":beam_cal(float(fc1),float(fy1),float(span1),float(flange_depth),float(web_depth),float(impo_Load)),
                         "effective_depth of span m":effective_depth_of_span2,
                         "Effective span":effective_span2,
                         "ultimate_load km/m":ultimate_load,
                         
                         },index=[0])
        df2=pd.DataFrame({"Ultimate BM kn/m":ultimate_BM,
                         "Shear Force Kn":sf,
                         "effective_width_of_flange mm":bf1*1000,
                         "moment capacity of flange Kn/m":muf/1000,
                         "Tension Reinforcements mm2":Ast_for_beam/10},index=[0])
        
        st.table(df)
        st.table(df2)
        
        
 
#********************************************************************************************************
def column_cal(column_size,length_col,axial_load,concrete_grade,steel_grade):
    # Define constants for the design
    global effective_length_of_column,pu,slr,slr_text,M,Asc,pc
    column_width,column_depth = [float(i) for i in column_size.split('x')]
    effective_length_of_column=0.65*length_col
    pu=1.5*axial_load
    slr=effective_length_of_column*1000/column_width
    if slr<12:
        slr_text="slenderness ratio is less than 12 ,hence column is designed as short column"
    else:
        slr_text="Use long column"
    
    M=axial_load * length_col
    pc=(0.4 *concrete_grade *(column_width*column_depth ))/1000
    ps=pu-pc
    Asc = -((ps*10**3 )- (0.4*concrete_grade )* (column_width*column_depth)) / (0.67 * steel_grade)
    
    return effective_length_of_column


def column():

    
    st.title("column dimensions")
    column_size=st.text_input("Enter column size (e.g. 300x300) in mm: ")
    length_col=st.text_input("Enter The Length Of Column m")
    
    st.title("Axial load ")
    axial_load=st.text_input("Enter axial load on the column in kN: ")
    
    st.title("Grade of Concrete and Steel")
    concrete_grade=st.text_input("Enter grade of concrete (e.g. 20, 25, 30): ")
    steel_grade=st.text_input("Enter grade of steel (e.g. 250, 415, 500")
    if st.button("Result"):
        df4=pd.DataFrame({"effctive_length of column m":column_cal(column_size,float(length_col),float(axial_load),float(concrete_grade),float(steel_grade)),
                          "Factored Load KN":pu,
                          "slenderness ratio":slr,
                          "":slr_text,
                          "bending moment due to axial load":M,
                          " compressive force KN":pc,
                          "Asc mm2":Asc},index=[0])
        st.table(df4)
    
    
    
    

############################################################################################# 
#Design of Flat footing      
def footing_cal(steel_strength,footing_length,footing_width,total_load,allowable_bearing_pressure):
    global x_reinforcement_size,y_reinforcement_size,footing_area,footing_depth,net_up_pressure
    # Define the safety factor for concrete strength
    concrete_safety_factor = 1.5
    # Define the safety factor for steel strength
    facto_load=total_load*1.5
    footing_area = footing_length * footing_width
    net_up_pressure=facto_load/footing_area
    steel_safety_factor = 1.15
    # Calculate the depth of the footing in meters
    footing_depth = ((total_load * 1000) / (allowable_bearing_pressure * footing_length * footing_width * concrete_safety_factor)) ** 0.5
    # Calculate the x-axis reinforcement size in mm^2
    x_reinforcement_size = (total_load * 1000 * footing_length) / (steel_strength * footing_depth * steel_safety_factor)
    # Calculate the y-axis reinforcement size in mm^2
    y_reinforcement_size = (total_load * 1000 * footing_width) / (steel_strength * footing_depth * steel_safety_factor)
    # Calculate the area of the footing in square meters
    
    return footing_area

def footing_val():
    st.title("Flat Footing ")
    cover=st.text_input("Enter The cover")
    fc=st.text_input("strength of concrete in MPa")
    fy=st.text_input("strength of steel reinforcement in MPa")
    footing_length=st.text_input("length of the footing in meters")
    footing_width=st.text_input("Width of the footing in meters")
    total_load = st.text_input("Enter The Total Load")
    allowable_bearing_pressure =st.text_input("Enter Allowable bearing pressure in kPa")
     
    if st.button("Result"):
        df=pd.DataFrame({"cover":cover,
                         "area of the footing in square meters m2":footing_cal(float(fy),float(footing_length),float(footing_width),float(total_load),float(allowable_bearing_pressure)),
                         "Net Upword Pressure KN/m2":net_up_pressure,
                         "x-axis reinforcement size in mm^2":x_reinforcement_size,
                         "y-axis reinforcement size in mm^2":y_reinforcement_size,
                         "Depth Of Footing":footing_depth},index=[0])
        st.table(df)
    
###############################################################################################
def stair_cal(story_height,stair_hall_height,live_load,supported_width):
    global total_rise,number_of_risers,riser_height,tread_depth,tread_width,run_length,baluster_spacing,minimum_headroom_required,minimum_tread_width
      

    # Constants
    maximum_riser_height = 7.75 # inches
    minimum_tread_depth = 10.0 # inches
    minimum_headroom = 80.0 # inches

    # Calculations
    total_rise = story_height + stair_hall_height
    number_of_risers = int(round(total_rise / maximum_riser_height))
    riser_height = total_rise / number_of_risers
    tread_depth = 0.5 * (supported_width - 8.0) / number_of_risers
    tread_width = supported_width - 8.0
    run_length = (number_of_risers - 1) * tread_depth
    baluster_spacing = tread_width / (number_of_risers - 1)
    minimum_headroom_required = number_of_risers * minimum_headroom
    minimum_tread_width = tread_width / number_of_risers
    return total_rise

# Output
def saire():
    st.title("Stair case ")
    story_height=st.text_input("Enter The story_height in feet ex,9,10,12,20")
    
    stair_hall_height=st.text_input("Enter the stair_hall_height feet Ex:8,7,6")
    
    live_load=st.text_input("Enter The live load pounds per square foot ex:400,450")
    supported_width=st.text_input("Enter The supported_width in inches Ex 40,50")
    
    if st.button("Result"):
        df=pd.DataFrame({"Total Rise feet":stair_cal(float(story_height),float(stair_hall_height),float(live_load),float(supported_width)),
                         "Number of Risers":number_of_risers,
                         "Riser Height inches:":riser_height,
                         "Tread Depth: inches":tread_depth,
                         "Tread Width: inches":tread_width,
                         "Run Length: inches":run_length,
                         "Baluster Spacing inches":baluster_spacing,
                         "Minimum Headroom Required inches:":minimum_headroom_required,
                         "Minimum Tread Width: inches": minimum_tread_width},index=[0])
        st.table(df)

    

pages = {
    "Slab Design":slab_design,
    "Beam Design ":beam,
    "Column": column,
    "Flat_Footing":footing_val,
    "Stair case ":saire
}
page = st.sidebar.selectbox("Select a Validation", tuple(pages.keys()))   
pages[page]()





