# 🚀 End-to-End Gen AI App 🚀

> **From Prototype to Production.**

### 📝 Project Description
The repository provides a comprehensive template for building advanced generative AI applications, from an initial prototype to a fully functional production solution.

### 🎓 Sources of Inspiration
The project was inspired by the prestigious 5-day Generative AI course run by Google on the Kaggle platform, combining best practices and the latest technological solutions.

### 🧠 Technologies and Components
#### Main Models

* LLM: Llama3 (Groq Tool Use)

    * Engine: Ollama

* Embeddings: Nomic Embed Text

#### Kluczowe Cechy

* Open-source approach
* Flexible architecture
* Scalability of solutions

### 🛠️ Main Functionalities

* Comprehensive management of the AI ​​generation process
* Integration of advanced open-source models
* Efficient implementation of embeddings
* Easy to configure and expand

## What's in this Starter Pack?

### A product-ready FasAPI server

The starter pack includes a production-ready FastAPI server with a real-time chat interface, event streaming, and auto-generated docs. It is designed for scalability and easy integration with monitoring tools.

### Ready to use AI patterns

Start with a variety of common patterns: this repository offers examples including a basic conversational chain, a production-ready RAG (Retrieval-Augmented Generation) chain developed with Python, and a LangGraph agent implementation. Use them in the application by changing one line of code in server.py.

### A comprehensive UI Playground

Experiment with your Generative AI application in a feature-rich playground, including chat curation, ~~user feedback collection,~~ multimodal input, and more!

## Getting Started

### Prerequisites

- Python >=3.10, < 3.13
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Installation

Install required packages using Poetry:

```bash
poetry install --with streamlit,jupyter
```

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make playground`    | Start the backend and frontend for local playground execution                               |
| `make test`          | Run unit and integration tests                                                              |

## Usage

1. **Prototype Your Chain:** Build your Generative AI application using different methodologies and frameworks.
2. **Integrate into the App:** Import your chain into the app. Edit the `app/chain.py` file to add your chain.
3. **Playground Testing:** Explore your chain's functionality using the Streamlit playground. You can run the playground locally with the `make playground` command.
4. **Play with notebook:** You can experiment, for example, with new solutions in Jupyter Notebook.


## 📋 TODO

### 🔜 Planned

- [ ] Integration with Vertex AI Evaluation

- [ ] Integration with OpenTelemetry, Cloud Trace, Cloud Logging

- [ ] Monitoring Responses from the application

## 🚧 In progress

- [ ] Bielik 2.3 model integration
- [ ] Utworzenie aplikacji Advanced RAG z wykorzystaniem modelu Bielik 2.3 

## ✅ Completed

- [x] Basic Project Structure
- [x] Tests
- [x] Llama3 model integration