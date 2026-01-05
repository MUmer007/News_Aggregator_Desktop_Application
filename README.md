# 📰 News Aggregator Desktop Application

A Python-based desktop **News Aggregator** application built using **Tkinter** that allows users to search, filter, and browse news articles from around the world using the **NewsAPI**. The app displays article titles, images, descriptions, publication details, and provides easy navigation between articles.

---

## 📌 Features

- 🔍 Search news articles by keyword
- 🗂 Sort results by:
  - Published date
  - Relevancy
  - Popularity
- 🌍 Filter news by language
- 📅 Filter articles by date
- 🖼 Display article images (if available)
- 📖 Read article descriptions inside the app
- ⏮⏭ Navigate between articles
- 🌐 Open full articles in the web browser
- 🧹 Clear search results easily
- ⚠️ Error handling for network/API issues

---

## 🛠 Technologies Used

- **Python 3**
- **Tkinter** – GUI framework
- **NewsAPI** – News data source
- **Requests** – HTTP requests
- **Pillow (PIL)** – Image handling
- **JSON** – API response parsing

---

## 📦 Requirements

Install the required Python libraries:
tkinter, json, and datetime come pre-installed with Python.
🔑 API Key Setup

This project uses NewsAPI.org.

Sign up at 👉 https://newsapi.org

Get your API key

Replace the API key in the code:

self.api_key = "YOUR_API_KEY_HERE"


⚠️ Important:
For production use, store the API key in an environment variable instead of hardcoding it.

▶️ How to Run the Application
python news_app.py


(Replace news_app.py with your actual file name.)

🧭 How to Use

Enter a keyword in the Search News field
(e.g., technology, bitcoin, sports)

Choose:

Sort option

Language

Starting date

Click Search News

Browse articles using Previous and Next

Click Read Full Article to open the article in your browser

Click Clear to reset the app

🖥 Application Layout

Header: Application title

Search Bar: Keyword input

Filters: Sorting, language, date

Main Panel: Article title, image, and description

Navigation Buttons: Browse articles

Status Bar: Displays app status messages

📁 Project Structure
news-aggregator/
│
├── news_app.py       # Main application file
├── README.md         # Project documentation

⚠️ Known Limitations

API request limits depend on your NewsAPI plan

Image loading may be slow on low internet connections

No offline support

🚀 Future Improvements

🔒 Secure API key using environment variables

⚡ Load images asynchronously (threading)

🗃 Save favorite articles

📄 Pagination support

🌙 Dark mode

📱 Convert to PyQt or Web App

📜 License

This project is for educational purposes.
Please follow NewsAPI’s terms of service when using their data.

🙌 Acknowledgements

NewsAPI
 for providing the news data

Python and Tkinter community

💡 Author

Developed by Muhammad Umer
Feel free to modify and extend this project.

```bash
pip install requests pillow
