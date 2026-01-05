import requests
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import webbrowser
from PIL import Image, ImageTk
import io
import urllib.request

class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Aggregator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # API key (consider moving this to environment variable in production)
        self.api_key =   # <-- Your API key here
        
        # Variables
        self.news_data = []
        self.current_article_index = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="News Aggregator", font=("Arial", 24, "bold"), 
                              fg="white", bg="#2c3e50")
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="Search News:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.query_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.query_entry.pack(side=tk.LEFT, padx=10)
        self.query_entry.bind("<Return>", lambda e: self.fetch_news())
        
        # Filter frame
        filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        filter_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(filter_frame, text="Sort By:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.sort_var = tk.StringVar(value="publishedAt")
        sort_options = ttk.Combobox(filter_frame, textvariable=self.sort_var, width=15, state="readonly")
        sort_options['values'] = ('publishedAt', 'relevancy', 'popularity')
        sort_options.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="Language:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT, padx=(20, 0))
        
        self.language_var = tk.StringVar(value="en")
        language_options = ttk.Combobox(filter_frame, textvariable=self.language_var, width=10, state="readonly")
        language_options['values'] = ('en', 'es', 'fr', 'de', 'it')
        language_options.pack(side=tk.LEFT, padx=5)
        
        # Date filter
        date_frame = tk.Frame(self.root, bg="#f0f0f0")
        date_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(date_frame, text="From:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.date_var = tk.StringVar(value=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        date_entry = tk.Entry(date_frame, textvariable=self.date_var, width=12)
        date_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(date_frame, text="(YYYY-MM-DD)", font=("Arial", 8), bg="#f0f0f0", fg="gray").pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        search_btn = tk.Button(button_frame, text="Search News", command=self.fetch_news, 
                              bg="#3498db", fg="white", font=("Arial", 12, "bold"), padx=15)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_results, 
                             bg="#e74c3c", fg="white", font=("Arial", 12), padx=15)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = tk.Frame(self.root, bg="#f0f0f0")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Article display
        self.article_frame = tk.Frame(results_frame, bg="white", relief=tk.RAISED, bd=1)
        self.article_frame.pack(fill=tk.BOTH, expand=True)
        
        self.title_label = tk.Label(self.article_frame, text="Welcome to News Aggregator", 
                                   font=("Arial", 16, "bold"), bg="white", wraplength=600)
        self.title_label.pack(pady=10)
        
        self.image_label = tk.Label(self.article_frame, bg="white")
        self.image_label.pack(pady=5)
        
        self.desc_text = scrolledtext.ScrolledText(self.article_frame, wrap=tk.WORD, 
                                                  font=("Arial", 12), height=10, bg="white")
        self.desc_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.desc_text.config(state=tk.DISABLED)
        
        # Article info and navigation
        info_frame = tk.Frame(self.article_frame, bg="white")
        info_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.source_label = tk.Label(info_frame, text="", font=("Arial", 10, "italic"), bg="white", fg="gray")
        self.source_label.pack(side=tk.LEFT)
        
        self.date_label = tk.Label(info_frame, text="", font=("Arial", 10), bg="white", fg="gray")
        self.date_label.pack(side=tk.RIGHT)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.article_frame, bg="white")
        nav_frame.pack(pady=10)
        
        self.prev_btn = tk.Button(nav_frame, text="Previous", command=self.show_previous_article, 
                                 state=tk.DISABLED, bg="#95a5a6", fg="white")
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = tk.Button(nav_frame, text="Next", command=self.show_next_article, 
                                 state=tk.DISABLED, bg="#95a5a6", fg="white")
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        self.read_more_btn = tk.Button(nav_frame, text="Read Full Article", command=self.open_full_article, 
                                      state=tk.DISABLED, bg="#27ae60", fg="white")
        self.read_more_btn.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to search for news")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, 
                             anchor=tk.W, font=("Arial", 10), bg="lightgray")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def fetch_news(self):
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query")
            return
            
        self.status_var.set("Searching for news...")
        self.root.update()
        
        from_date = self.date_var.get()
        sort_by = self.sort_var.get()
        language = self.language_var.get()
        
        url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&sortBy={sort_by}&language={language}&apiKey={self.api_key}"
        
        try:
            response = requests.get(url)
            news_data = json.loads(response.text)
            
            if news_data["status"] == "ok":
                self.news_data = news_data["articles"]
                if self.news_data:
                    self.status_var.set(f"Found {len(self.news_data)} articles. Displaying first result.")
                    self.current_article_index = 0
                    self.display_article()
                    self.update_navigation_buttons()
                else:
                    self.status_var.set("No articles found for your search")
                    messagebox.showinfo("No Results", "No news articles found for your search criteria.")
            else:
                self.status_var.set("Error fetching news")
                messagebox.showerror("API Error", f"Error: {news_data.get('message', 'Unknown error')}")
                
        except Exception as e:
            self.status_var.set("Error fetching news")
            messagebox.showerror("Network Error", f"Failed to fetch news: {str(e)}")
    
    def display_article(self):
        if not self.news_data:
            return
            
        article = self.news_data[self.current_article_index]
        
        # Display title
        self.title_label.config(text=article.get("title", "No title available"))
        
        # Display image if available
        image_url = article.get("urlToImage")
        if image_url:
            try:
                with urllib.request.urlopen(image_url) as url:
                    image_data = url.read()
                    image = Image.open(io.BytesIO(image_data))
                    image.thumbnail((400, 300))
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
            except:
                self.image_label.config(image='')
                self.image_label.image = None
        else:
            self.image_label.config(image='')
            self.image_label.image = None
        
        # Display description
        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        description = article.get("description", "No description available")
        if description:
            self.desc_text.insert(tk.END, description)
        else:
            self.desc_text.insert(tk.END, "No description available for this article.")
        self.desc_text.config(state=tk.DISABLED)
        
        # Display source and date
        source = article.get("source", {}).get("name", "Unknown source")
        published_at = article.get("publishedAt", "")
        if published_at:
            try:
                date_obj = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = date_obj.strftime("%B %d, %Y at %H:%M")
            except:
                formatted_date = published_at
        else:
            formatted_date = "Unknown date"
            
        self.source_label.config(text=f"Source: {source}")
        self.date_label.config(text=f"Published: {formatted_date}")
        
        # Enable read more button if URL available
        if article.get("url"):
            self.read_more_btn.config(state=tk.NORMAL)
        else:
            self.read_more_btn.config(state=tk.DISABLED)
    
    def show_next_article(self):
        if self.current_article_index < len(self.news_data) - 1:
            self.current_article_index += 1
            self.display_article()
            self.update_navigation_buttons()
    
    def show_previous_article(self):
        if self.current_article_index > 0:
            self.current_article_index -= 1
            self.display_article()
            self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        if self.news_data:
            self.prev_btn.config(state=tk.NORMAL if self.current_article_index > 0 else tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL if self.current_article_index < len(self.news_data) - 1 else tk.DISABLED)
        else:
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
    
    def open_full_article(self):
        if self.news_data and self.current_article_index < len(self.news_data):
            article = self.news_data[self.current_article_index]
            url = article.get("url")
            if url:
                webbrowser.open_new_tab(url)
    
    def clear_results(self):
        self.query_entry.delete(0, tk.END)
        self.news_data = []
        self.current_article_index = 0
        
        self.title_label.config(text="Welcome to News Aggregator")
        self.image_label.config(image='')
        self.image_label.image = None
        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.config(state=tk.DISABLED)
        self.source_label.config(text="")
        self.date_label.config(text="")
        
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.read_more_btn.config(state=tk.DISABLED)
        
        self.status_var.set("Ready to search for news")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()