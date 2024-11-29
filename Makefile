playground:
	poetry run uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload & poetry run streamlit run streamlitapp/streamlit_app.py --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false
