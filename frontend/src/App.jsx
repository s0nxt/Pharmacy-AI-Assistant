import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Mic, MicOff, Pill, History, AlertTriangle, RefreshCw, User, Bot, LayoutDashboard } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hello! I am your AI Pharmacist. How can I help you today? I can assist with orders, refills, and medication information.' }
  ]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [inventory, setInventory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  
  const scrollRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const fetchDashboardData = async () => {
    setIsRefreshing(true);
    try {
      const [invRes, alertRes, histRes] = await Promise.all([
        axios.get(`${API_BASE}/inventory`),
        axios.get(`${API_BASE}/alerts`),
        axios.get(`${API_BASE}/history`)
      ]);
      setInventory(invRes.data);
      setAlerts(alertRes.data);
      setHistory(histRes.data);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
    } finally {
      setTimeout(() => setIsRefreshing(false), 500); // Minimum spin time for better feel
    }
  };

  const handleSend = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        message: input,
        history: messages
      });
      const botMsg = { role: 'bot', content: res.data.response };
      setMessages(prev => [...prev, botMsg]);
      
      // Text to Speech
      const utterance = new SpeechSynthesisUtterance(res.data.response);
      window.speechSynthesis.speak(utterance);

      fetchDashboardData(); // Update inventory after potential order
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', content: 'Sorry, I encountered an error. Please try again later.' }]);
    } finally {
      setLoading(false);
    }
  };

  const toggleVoice = () => {
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("Voice recognition not supported in this browser.");
        return;
      }
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
      };
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const clearChat = () => {
    setMessages([{ role: 'bot', content: 'Hello! I am your AI Pharmacist. How can I help you today? I can assist with orders, refills, and medication information.' }]);
  };

  const filteredInventory = inventory.filter(med => 
    med.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const suggestions = [
    "I need a refill for Metformin",
    "What do you have for blood pressure?",
    "Do I need a prescription for Amoxicillin?",
    "Check my order history (John Doe)"
  ];

  return (
    <div className="app-container">
      {/* Sidebar / Admin View */}
      <aside className="sidebar">
        <div className="dashboard-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 className="dashboard-title"><LayoutDashboard size={20} inline /> Admin Panel</h2>
          <button className="btn-icon" onClick={fetchDashboardData} disabled={isRefreshing}>
            <RefreshCw size={18} className={isRefreshing ? 'spin' : ''} />
          </button>
        </div>

        <section style={{ display: 'flex', flexDirection: 'column', maxHeight: '40%', minHeight: '150px' }}>
          <h3 className="section-title"><AlertTriangle size={14} /> Proactive Alerts</h3>
          <div className="alerts-list" style={{ flex: 1, overflowY: 'auto' }}>
            {alerts.length === 0 ? <p style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>No active alerts.</p> : 
              alerts.map((alert, i) => (
                <div key={i} className="card alert-card">
                  <div style={{fontWeight: '600', fontSize: '0.9rem'}}>{alert.customer_name}</div>
                  <div style={{fontSize: '0.8rem'}}>{alert.medicine_name} - {alert.days_remaining} days left</div>
                </div>
              ))
            }
          </div>
        </section>

        <section style={{marginTop: '20px', flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column'}}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <h3 className="section-title" style={{ margin: 0 }}><Pill size={14} /> Inventory</h3>
            <input 
              type="text" 
              placeholder="Search..." 
              className="search-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="inventory-list" style={{flex: 1}}>
            {filteredInventory.length === 0 ? <p style={{fontSize: '0.8rem', color: 'var(--text-muted)', textAlign: 'center', marginTop: '20px'}}>No medicines found.</p> :
              filteredInventory.map((med) => (
                <div key={med.medicine_id} className="card">
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{ fontWeight: '500' }}>{med.name}</span>
                    <span className={med.stock_level < 50 ? 'stock-low' : ''}>{med.stock_level} {med.unit}</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px'}}>
                    <span style={{fontSize: '0.7rem', color: 'var(--text-muted)'}}>
                      {med.prescription_required ? '⚠️ RX Required' : 'OTC'}
                    </span>
                    <span style={{fontSize: '0.8rem', color: 'var(--primary)', fontWeight: '600'}}>${med.price}</span>
                  </div>
                </div>
              ))
            }
          </div>
        </section>
      </aside>

      {/* Main Chat Interface */}
      <main className="main-chat">
        <header style={{padding: '15px 20px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Bot size={24} color="var(--primary)" />
            <div>
              <h1 style={{fontSize: '1.2rem'}}>Pharmacy AI Assistant</h1>
              <p style={{fontSize: '0.8rem', color: 'var(--accent)'}}>● Online & Ready</p>
            </div>
          </div>
          <button className="btn-text" onClick={clearChat} style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Clear Chat
          </button>
        </header>

        <div className="chat-messages" ref={scrollRef}>
          {messages.length === 1 && (
            <div className="suggestions-container">
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '10px' }}>Try asking:</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {suggestions.map((s, i) => (
                  <button key={i} className="suggestion-chip" onClick={() => { setInput(s); }}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`message ${msg.role}`}
              >
                {msg.content}
              </motion.div>
            ))}
          </AnimatePresence>
          {loading && (
            <div className="message bot" style={{opacity: 0.6}}>Assistant is thinking...</div>
          )}
        </div>

        <form className="chat-input-area" onSubmit={handleSend}>
          <button 
            type="button" 
            className={`btn-icon ${isListening ? 'active' : ''}`}
            onClick={toggleVoice}
          >
            {isListening ? <MicOff size={20} /> : <Mic size={20} />}
          </button>
          <input 
            type="text" 
            className="chat-input" 
            placeholder="Type your message or use voice..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" className="btn-icon" style={{color: 'var(--primary)'}}>
            <Send size={20} />
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
