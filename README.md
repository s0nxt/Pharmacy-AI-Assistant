# Agentic AI Pharmacy System

An autonomous ecosystem for a traditional search-and-click pharmacy, transforming it into an expert-led agentic system.

## Features
- **Conversational Ordering:** Natural interface (text & voice) for extracting medicine, dosage, and quantity.
- **Safety Enforcement:** Autonomous policy checks based on "Medicine Master Data" (Source of Truth).
- **Predictive Intelligence:** Proactive alerts for medicine refills based on patient history.
- **Real-world Tool Use:** Backend stock updates, mock webhook triggers, and order history logging.
- **Observability:** Full Chain of Thought (CoT) tracing integrated with **Langfuse**.
- **Admin View:** Real-time inventory monitoring and proactive refill management.

## Tech Stack
- **Backend:** FastAPI, LangGraph, Google Gemini (Gen AI), Pandas (Mock DB).
- **Frontend:** React, Vite, Framer Motion, Lucide icons.
- **Observability:** Langfuse.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Node.js & npm
- Google Gemini API Key
- Langfuse Account (for Public/Secret keys)

### 2. Backend Setup
1. Navigate to the `backend` folder.
2. Create a `.env` file from the template:
   ```env
   GOOGLE_API_KEY=your_key
   LANGFUSE_PUBLIC_KEY=your_key
   LANGFUSE_SECRET_KEY=your_key
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python main.py`

### 3. Frontend Setup
1. Navigate to the `frontend` folder.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

### 4. Observability
Access the Langfuse dashboard to see the Agentic Trace Logs. Every chat interaction triggers a trace that shows how the agent:
- Checks inventory.
- Checks history.
- Decides whether a prescription is needed.
- Updates the database.

## System Architecture
The system uses a **StateGraph (LangGraph)** where:
- The `agent` node uses Gemini to interpret intent.
- The `tools` node executes actions like `check_inventory` or `place_order`.
- Conditional edges enforce the logical flow (e.g., "Do we have enough stock?" or "Is a prescription required?").
