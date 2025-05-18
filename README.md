
# 🏏 IPL Dashboard (2008–2024)

An interactive and visually rich **IPL Dashboard** built with **Streamlit**, offering comprehensive insights into the Indian Premier League (IPL) from 2008 to 2024. Explore season summaries, team performance, player statistics, and historical trends — all in one place!



---

## 🚀 Features

- 📅 **Season Overview**: Visualize total matches, participating teams, champions, and top-performing teams for a selected year.
- 🧢 **Team Analysis**: Deep-dive into a specific team's season performance, banned status, match results, and top players.
- 🧑‍💼 **Player Stats**: View and filter player performance (batting/bowling) with sortable metrics and visual comparisons.
- 📊 **Historical Trends**:
  - Team wins and points across seasons
  - Champions timeline
  - Toss decisions and their success rates
  - Win type distributions (runs vs. wickets)
- 🧠 **Smart UI**: Includes highlights for banned teams, custom metric cards, and fully interactive Plotly charts.
- 🎨 **Custom Styling**: Elegant UI with custom CSS, responsive layout, and color-coded team representations.

---

## 🧾 Tech Stack

- **Frontend/Framework**: [Streamlit](https://streamlit.io/)
- **Data Visualization**:
  - Plotly
  - Seaborn
  - Matplotlib
- **Backend Logic**: Python (Pandas, NumPy)
- **Mock Data**: Generated dynamically (no real `.csv` input required)




## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Dibyanshutest/ipl-dashboard.git
cd ipl-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, manually install:

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly
```

### 3. Run the Dashboard

```bash
streamlit run ipl-dashboard-streamlit.py
```

---

## 🔄 Data Note

This dashboard uses **synthetic/mock IPL data** for demo purposes. In a real-world application, replace the data generation section with actual IPL datasets (e.g., `matches.csv`, `deliveries.csv` from Kaggle).

---

## 📌 Customization

- 🎨 Modify CSS in the `st.markdown(<style>...</style>)` block.
- 🧠 Replace `load_data()` logic to load real CSV data for production use.
- 📅 Update the `winners_by_year` dictionary for future IPL seasons.

---

## 📃 License

MIT License — feel free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📞 Contact

Built by [D.Rath](https://github.com/Dibyanshutest) • For feedback or collaboration, reach out via GitHub or email.
