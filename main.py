import streamlit as st
import pandas as pd
import matplotlib import pyplot as plt
import matplotlib import patches as mpatches
from matplotlib.lines import Line2D
from mplsoccer.pitch import Pitch
from mplsoccer.pitch import VerticalPitch

st.set_page_config(
    page_title="Football Performance Analysis Dashboard",
    page_icon="✅",
    layout="centered",
)

df = pd.read_csv("all_actions.csv")
df = df.drop("Unnamed: 0",axis=1)
df['outcome'] = df['outcome'].astype(str)
df['type_id'] = df['type_id'].astype(str)

st.title("Football Performance Analysis Dashboard")

action_filter = st.selectbox("Select the Displayed Actions", 
                             pd.unique(df["action"]))

team_filter = st.selectbox("Select Team", 
                             pd.unique(df["team"]))
filtered_df = df[df['team'] == team_filter]

match_filter = st.multiselect("Select Match",
                              pd.unique(filtered_df["game"]))

if action_filter == "Passes":
    
    prog_check = st.checkbox("Show Progressive Passes Only")
    xT_slider = st.slider("Minimum xT of Displayed Passes",
                          min_value=0.00,max_value=0.25)
    
    fig,ax = plt.subplots(figsize=(13.5,8))
    fig.set_facecolor('green')
    ax.patch.set_facecolor('green')

    pitch = Pitch(pitch_type='statsbomb', pitch_color='green', line_color='white',
                  figsize=(13.5, 8),constrained_layout=True, tight_layout=False)

    pitch.draw(ax=ax)
    plt.gca().invert_yaxis()
    
    if prog_check == True:
        for x in range(len(df['x_start'])):
            if df['action'].iloc[x] == action_filter:
                if df['team'].iloc[x] == team_filter:
                    if df['game'].iloc[x] in match_filter:
                        if df["outcome"].iloc[x] == '1':
                            if df['progressive'].iloc[x] == True:
                                if df['xT'].iloc[x] >= xT_slider:
                                    plt.plot((df["x_start"].iloc[x],df["x_end"].iloc[x]),
                                             (df["y_start"].iloc[x],df["y_end"].iloc[x]),
                                              color="yellow")
                                    plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                                color='yellow')

    elif prog_check == False:
        for x in range(len(df['x_start'])):
            if df['action'].iloc[x] == action_filter:
                if df['team'].iloc[x] == team_filter:
                    if df['game'].iloc[x] in match_filter:
                        if df["outcome"].iloc[x] == '1':
                            if df['xT'].iloc[x] >= xT_slider:
                                plt.plot((df["x_start"].iloc[x],df["x_end"].iloc[x]),
                                         (df["y_start"].iloc[x],df["y_end"].iloc[x]),
                                          color="yellow")
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='yellow')
   
    legend_elements = [Line2D([0], [0], marker='o', color='yellow', label='Pass Start Location',
                              markerfacecolor='yellow', markersize=10),
                       Line2D([0], [0], color='yellow', lw=5, label='Route of Pass')]
    ax.legend(handles=legend_elements, loc='lower left')
    
    plt.xlim(0,120)
    plt.ylim(0,80);
    st.pyplot(fig)
 
elif action_filter == "Take Ons":
    
    suc_tak = st.checkbox("Show Successful Actions Only")
    
    fig,ax = plt.subplots(figsize=(13.5,8))
    fig.set_facecolor('green')
    ax.patch.set_facecolor('green')

    pitch = Pitch(pitch_type='statsbomb', pitch_color='green', line_color='white',
                  figsize=(13.5, 8),constrained_layout=True, tight_layout=False)    
    
    pitch.draw(ax=ax)
    plt.gca().invert_yaxis()
    
    if suc_tak == True:
        for x in range(len(df['x_start'])):
            if df['action'].iloc[x] == action_filter:
                if df['team'].iloc[x] == team_filter:
                    if df['game'].iloc[x] in match_filter:
                        if df["outcome"].iloc[x] == '1':
                            plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                        color='yellow',marker='v',s=100)
    if suc_tak == False:
        for x in range(len(df['x_start'])):
            if df['action'].iloc[x] == action_filter:
                if df['team'].iloc[x] == team_filter:
                    if df['game'].iloc[x] in match_filter:
                        if df["outcome"].iloc[x] == '1':
                            plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                        color='yellow',marker='v',s=100)
                        elif df["outcome"].iloc[x] == '0':
                            plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                        color='red',marker='v',s=100)
   
    legend_elements = [Line2D([0], [0], marker='v', color='white', label='Successful Take On',
                              markerfacecolor='yellow', markersize=10),
                       Line2D([0], [0], marker='v', color='white', label='Unsuccessful Take On',
                              markerfacecolor='red', markersize=10)]
    ax.legend(handles=legend_elements, loc='lower left')
    
    plt.xlim(0,120)
    plt.ylim(0,80);
    st.pyplot(fig)

elif action_filter == "Shots":
    
    fig,ax = plt.subplots(figsize=(13.5,8))
    fig.set_facecolor('green')
    ax.patch.set_facecolor('green')

    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='green', line_color='white',
                  figsize=(13.5, 8),constrained_layout=True, tight_layout=False, half=True)    
    
    pitch.draw(ax=ax)
    plt.gca().invert_yaxis()
    
    for x in range(len(df['x_start'])):
        if df['action'].iloc[x] == action_filter:
            if df['team'].iloc[x] == team_filter:
                if df['game'].iloc[x] in match_filter:
                    if df["type_shot"].iloc[x] == 'Miss':
                        plt.scatter(df['y_start'].iloc[x],df['x_start'].iloc[x],color='red',s=100)  
                        plt.plot((df['y_start'].iloc[x],df['y_end'].iloc[x]),
                                 (df['x_start'].iloc[x],df['x_end'].iloc[x]),color='red')
                    elif df["type_shot"].iloc[x] == 'Woodwork':
                        plt.scatter(df['y_start'].iloc[x],df['x_start'].iloc[x],color='white',s=100)  
                        plt.plot((df['y_start'].iloc[x],df['y_end'].iloc[x]),
                                 (df['x_start'].iloc[x],df['x_end'].iloc[x]),color='white')
                    elif df["type_shot"].iloc[x] == 'Save':
                        plt.scatter(df['y_start'].iloc[x],df['x_start'].iloc[x],color='blue',s=100)  
                        plt.plot((df['y_start'].iloc[x],df['y_end'].iloc[x]),
                                 (df['x_start'].iloc[x],df['x_end'].iloc[x]),color='blue')
                    elif df["type_shot"].iloc[x] == 'Block':
                        plt.scatter(df['y_start'].iloc[x],df['x_start'].iloc[x],color='purple',s=100)  
                        plt.plot((df['y_start'].iloc[x],df['y_end'].iloc[x]),
                                 (df['x_start'].iloc[x],df['x_end'].iloc[x]),color='purple')
                    elif df["type_shot"].iloc[x] == 'Goal':
                        plt.scatter(df['y_start'].iloc[x],df['x_start'].iloc[x],color='yellow',s=100)  
                        plt.plot((df['y_start'].iloc[x],df['y_end'].iloc[x]),
                                 (df['x_start'].iloc[x],df['x_end'].iloc[x]),color='yellow')
    
    l1 = mpatches.Patch(color='yellow', label='Goal')
    l2 = mpatches.Patch(color='blue', label='Save')
    l3 = mpatches.Patch(color='purple', label='Block')
    l4 = mpatches.Patch(color='white', label='Woodwork')
    l5 = mpatches.Patch(color='red', label='Miss')
    plt.legend(handles=[l1,l2,l3,l4,l5],loc=3)
    
    plt.xlim(80,0)
    plt.ylim(60,120);
    st.pyplot(fig)

elif action_filter == "Defensive Actions":
    
    suc_def = st.checkbox("Show Successful Actions Only")
    
    fig,ax = plt.subplots(figsize=(13.5,8))
    fig.set_facecolor('green')
    ax.patch.set_facecolor('green')

    pitch = Pitch(pitch_type='statsbomb', pitch_color='green', line_color='white',
                  figsize=(13.5, 8),constrained_layout=True, tight_layout=False)    
    
    pitch.draw(ax=ax)
    plt.gca().invert_yaxis()
    
    if suc_def == True:
        for x in range(len(df['x_start'])):
            if df['action'].iloc[x] == action_filter:
                if df['team'].iloc[x] == team_filter:
                    if df['game'].iloc[x] in match_filter:
                        if df['outcome'].iloc[x] == '1':
                            if df["type_def"].iloc[x] == 'Tackle':
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='yellow',marker='s',s=100)
                            if df["type_def"].iloc[x] == 'Interception':
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='yellow',marker='^',s=100)

    if suc_def == False:
        for x in range(len(df['x_start'])):
            if df['action'].iloc[x] == action_filter:
                if df['team'].iloc[x] == team_filter:
                    if df['game'].iloc[x] in match_filter:
                        if df['outcome'].iloc[x] == '1':
                            if df["type_def"].iloc[x] == 'Tackle':
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='yellow',marker='s',s=100)
                            if df["type_def"].iloc[x] == 'Interception':
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='yellow',marker='^',s=100)
                        elif df['outcome'].iloc[x] == '0':
                            if df["type_def"].iloc[x] == 'Tackle':
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='red',marker='s',s=100)
                            if df["type_def"].iloc[x] == 'Interception':
                                plt.scatter(df["x_start"].iloc[x],df['y_start'].iloc[x],
                                            color='red',marker='^',s=100)

    legend_elements = [Line2D([0], [0], marker='s', color='white', label='Successful Tackle',
                              markerfacecolor='yellow', markersize=10),
                       Line2D([0], [0], marker='s', color='white', label='Unsuccessful Tackle',
                              markerfacecolor='red', markersize=10),
                       Line2D([0], [0], marker='^', color='white', label='Successful Interception',
                              markerfacecolor='yellow', markersize=10),
                       Line2D([0], [0], marker='^', color='white', label='Unsuccessful Interception',
                              markerfacecolor='red', markersize=10)]
    ax.legend(handles=legend_elements, loc='lower left')    
    
    plt.xlim(0,120)
    plt.ylim(0,80);
    st.pyplot(fig)