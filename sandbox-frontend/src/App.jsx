import { useState, useEffect } from 'react'
import './App.css'

// --- COMPONENTE: TERMINAL SIMULADA (Animación de carga) ---
const TerminalLoader = () => {
  const [logs, setLogs] = useState([])
  
  const fakeLogs = [
    "Initializing secure environment...",
    "Allocating isolated memory blocks...",
    "Injecting payload [sample_artifact]...",
    "Hooking network sockets (syscall trace)...",
    "Monitoring filesystem events (watchdog)...",
    "Capturing TCP/UDP traffic...",
    "Analyzing heuristic behavior patterns...",
    "Detonating malware in sandbox...",
    "Compiling forensic JSON report..."
  ]

  useEffect(() => {
    let delay = 0;
    fakeLogs.forEach((line) => {
      delay += Math.random() * 500 + 200;
      setTimeout(() => {
        setLogs(prev => [...prev, `> ${line}`])
      }, delay);
    });
  }, [])

  return (
    <div className="terminal-loader">
      <div className="terminal-header">SANDBOX EXECUTION LOGS</div>
      <div className="terminal-body">
        {logs.map((log, i) => (
          <div key={i} className="log-line">{log}</div>
        ))}
        <div className="typing-cursor">_</div>
      </div>
    </div>
  )
}

// --- COMPONENTE: CHATBOT DE CIBERSEGURIDAD ---
const ChatComponent = ({ reportData }) => {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Hola. Soy tu Analista de Seguridad. He revisado el reporte. ¿Tienes alguna duda sobre la mitigación o el comportamiento del malware?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return
    
    const userMsg = input
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: userMsg,
          report: reportData 
        })
      })
      
      const data = await response.json()
      setMessages(prev => [...prev, { sender: 'ai', text: data.answer }])
    } catch (e) {
      setMessages(prev => [...prev, { sender: 'ai', text: 'Error al conectar con el analista.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card chat-card" style={{ gridColumn: '1 / -1', marginTop: '20px' }}>
      <h2 style={{color: 'var(--neon-blue)', borderBottom: '1px solid #333', paddingBottom: '10px'}}>
        💬 CHAT TÁCTICO
      </h2>
      
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            <span className="msg-icon">{msg.sender === 'ai' ? '🤖' : '👤'}</span>
            <div className="msg-bubble">
               <span style={{whiteSpace: 'pre-wrap'}}>{msg.text}</span>
            </div>
          </div>
        ))}
        {loading && <div className="message ai"><span className="msg-icon">🤖</span>...Escribiendo...</div>}
      </div>

      <div className="chat-input-area">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ej: ¿Qué IPs debo bloquear en el firewall?"
        />
        <button onClick={handleSend}>ENVIAR</button>
      </div>
    </div>
  )
}

// --- COMPONENTE: VIRUSTOTAL BADGE (NUEVO DISEÑO HUD) ---
const VirusTotalCard = ({ data }) => {
  if (!data) return null;

  if (!data.found) {
    return (
      <div className="card vt-card" style={{ borderColor: '#444' }}>
        <h3 style={{color: '#666'}}>🦠 VIRUSTOTAL</h3>
        <p style={{color: '#888'}}>Archivo no registrado (Zero-day).</p>
      </div>
    );
  }

  // Lógica de Semáforo
  const score = data.malicious_count;
  let riskLevel = "SEGURO";
  let color = "#00ff41"; // Verde Neon

  if (score > 0 && score < 5) {
    riskLevel = "SOSPECHOSO";
    color = "#e3b341"; // Amarillo/Naranja
  } else if (score >= 5) {
    riskLevel = "CRÍTICO";
    color = "#ff003c"; // Rojo Neon
  }

  // Generamos 20 segmentos para la barra visual
  const totalSegments = 20;
  const filledSegments = Math.ceil((data.malicious_count / data.total_engines) * totalSegments);

  return (
    <div className="card vt-card" style={{ borderColor: color, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      
      {/* Encabezado */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <h3 style={{ margin: 0, color: color, fontSize: '0.9rem' }}>🦠 THREAT INTEL</h3>
        <span className={`risk-badge ${riskLevel === 'CRÍTICO' ? 'blink' : ''}`} style={{ backgroundColor: color, color: '#000' }}>
          {riskLevel}
        </span>
      </div>
      
      {/* Score Gigante */}
      <div className="vt-score-container">
        <span className="vt-big-number" style={{ color: color }}>
          {data.malicious_count}
        </span>
        <span className="vt-total">/ {data.total_engines}</span>
      </div>
      
      {/* Barra Segmentada Táctica */}
      <div className="vt-gauge">
        {[...Array(totalSegments)].map((_, i) => (
          <div 
            key={i} 
            className="gauge-segment"
            style={{ 
              backgroundColor: i < filledSegments ? color : '#333',
              boxShadow: i < filledSegments ? `0 0 5px ${color}` : 'none'
            }}
          ></div>
        ))}
      </div>
      
      <p style={{ fontSize: '0.75rem', marginTop: '15px', color: '#888', textAlign: 'center' }}>
        Motores AV Globales
      </p>
    </div>
  );
};

// --- APP PRINCIPAL ---
function App() {
  const [file, setFile] = useState(null)
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setReport(null)
    setError(null)
  }

  const handleScan = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setReport(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/scan', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Error en el análisis del servidor')
      const data = await response.json()
      setReport(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>🛡️ CYBER-SANDBOX</h1>
        <p>Sistema de Detonación y Análisis Forense Automatizado</p>
        <p className="author-credit">Elaborado por: Diego Hernández Vázquez</p>
      </header>

      {/* LÓGICA DE CARGA: Terminal vs Upload */}
      {loading ? (
        <TerminalLoader />
      ) : (
        <div className="upload-section">
          <div className="corner-decoration"></div>
          <input type="file" onChange={handleFileChange} className="file-input" />
          <button onClick={handleScan} disabled={!file} className="scan-button">
            [ INICIAR ANÁLISIS ]
          </button>
        </div>
      )}

      {error && <div className="error-box">ERROR: {error}</div>}

      {/* REPORTE DE RESULTADOS */}
      {report && (
        <div className="report-container">
          
          {/* --- BLOQUE SUPERIOR: INTELIGENCIA COMBINADA --- */}
          {(report.ai_analysis || report.virustotal) && (
            <div className="hero-grid">
              
              {/* COLUMNA IZQUIERDA: SOC VIRTUAL (IA) */}
              {report.ai_analysis && (
                <div className="card ai-card" style={{ margin: 0, height: '100%' }}>
                  <div className="ai-header">
                    <span className="ai-icon">🤖</span>
                    <h2>SOC VIRTUAL ANALYST</h2>
                  </div>
                  <div className="ai-body">
                    {report.ai_analysis}
                  </div>
                </div>
              )}

              {/* COLUMNA DERECHA: VIRUSTOTAL */}
              {report.virustotal && (
                <div className="vt-wrapper">
                  <VirusTotalCard data={report.virustotal} />
                </div>
              )}
              
            </div>
          )}
          
          {/* 1. TARJETA: INTELIGENCIA ESTÁTICA */}
          <div className="card summary">
            <h2>// INTELIGENCIA ESTÁTICA</h2>
            <p><strong>ARCHIVO:</strong> {report.static_analysis.filename}</p>
            <p><strong>SHA256:</strong> <span className="hash">{report.static_analysis.sha256}</span></p>
            <div className="strings-box">
              <h3>Strings Detectados (Preview):</h3>
              <ul>
                {report.static_analysis.interesting_strings.length > 0 ? (
                    report.static_analysis.interesting_strings.slice(0, 5).map((s, i) => (
                    <li key={i}>{s}</li>
                    ))
                ) : (
                    <li>No se encontraron cadenas legibles significativas.</li>
                )}
              </ul>
            </div>
          </div>

          {/* 2. LÓGICA CONDICIONAL: ¿SE EJECUTÓ O SE OMITIÓ? */}
          {report.dynamic_analysis.status === "skipped" ? (
            
            /* CASO A: EJECUCIÓN OMITIDA */
            <div className="card skipped" style={{gridColumn: "1 / -1", borderColor: '#e3b341', borderTop: '3px solid #e3b341'}}>
              <h2 style={{color: '#e3b341'}}>⚠️ EJECUCIÓN OMITIDA</h2>
              <p>{report.dynamic_analysis.reason}</p>
              <p style={{fontSize: '0.9em', color: 'rgba(255,255,255,0.7)', marginTop: '10px'}}>
                Nota: El motor de Sandbox Dinámico actual solo detona scripts ejecutables (.py). 
                Sin embargo, el análisis estático superior (Hash e IOCs) sigue siendo válido.
              </p>
            </div>

          ) : (

            /* CASO B: EJECUCIÓN COMPLETA */
            <>
              {/* Tarjeta de Red */}
              <div className="card network">
                <h2>// TRÁFICO DE RED (DINÁMICO)</h2>
                {!report.dynamic_analysis.network_activity || report.dynamic_analysis.network_activity.length === 0 ? (
                  <p style={{color: 'var(--neon-green)'}}>✅ Sin conexiones sospechosas.</p>
                ) : (
                  <table>
                    <thead>
                      <tr>
                        <th>Proceso</th>
                        <th>Destino</th>
                        <th>Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {report.dynamic_analysis.network_activity.map((conn, i) => (
                        <tr key={i}>
                          <td>{conn.process}</td>
                          <td className="danger-text">{conn.raddr}</td>
                          <td>{conn.status}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
              
              {/* Tarjeta de Archivos */}
              <div className="card files">
                <h2>// CAMBIOS EN DISCO</h2>
                {!report.dynamic_analysis.file_activity || report.dynamic_analysis.file_activity.length === 0 ? (
                    <p>✅ Sin modificaciones en sistema de archivos.</p>
                ) : (
                    <ul>
                    {report.dynamic_analysis.file_activity.map((f, i) => (
                        <li key={i}>
                        <span className={`tag ${f.action}`}>{f.action.toUpperCase()}</span> 
                        {f.path}
                        </li>
                    ))}
                    </ul>
                )}
              </div>
            </>
          )}
          <ChatComponent reportData={report} />
          
        </div>
      )}
    </div>
  )
}

export default App