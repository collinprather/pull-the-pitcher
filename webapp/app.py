import streamlit as st
from pull_the_pitcher.inference import *
import pickle


db_path = "./data/raw/statcast_pitches.db"
mappers_path = "./data/processed/mappers_2017_2018_2016_2019.pkl"
scaler_path = "./data/processed/scaler_2017_2018_2016_2019.pkl"
model_path = f"./models/07-22-20_DRSA_2016_2017_2018_2019_loss_4.0985.pth"

# loading embedding encoder and scaler
with open("./data/processed/mappers_2017_2018_2016_2019.pkl", "rb") as f:
    mappers = pickle.load(f)
with open("./data/processed/scaler_2017_2018_2016_2019.pkl", "rb") as f:
    scaler = pickle.load(f)

if __name__ == "__main__":
    
    drsa = load_drsa(model_path)
    
    # gathering data for viz
    year = st.text_input("Year.", "2019")
    game_pk = st.text_input("Unique MLBAM game identifier.", "565717")
    pitcher = st.text_input("Unique MLBAM pitcher identifier.", "641745")
    
    # prepping data for model
    game_df = get_game_df(db_path, year=int(year), game_pk=int(game_pk))
    X, pad_diff = game_df2tensor(game_df, int(game_pk), int(pitcher), mappers, scaler)
    
    # loading model
    drsa = load_drsa(model_path)
    drsa.eval() # making sure that no dropout is applied
    preds = drsa(X)
    
    # showing viz
    chart = make_altair_hist(preds, pad_diff)
    st.altair_chart(chart, use_container_width=True)
