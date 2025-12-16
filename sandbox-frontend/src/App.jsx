import { useState, useEffect } from 'react'
import './App.css'

// --- COMPONENTE: TERMINAL SIMULADA (Animación de carga) ---
const TerminalLoader = () => {
  const [logs, setLogs] = useState([])
  
  // Lista de mensajes para simular el proceso del backend
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
      delay += Math.random() * 500 + 200; // Retardo aleatorio para realismo
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
      // Conexión a tu API Python
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

      {/* VISUALIZACIÓN DEL REPORTE */}
      {report && (
        <div className="report-container">
          
          {/* 1. TARJETA: INTELIGENCIA ESTÁTICA (Siempre visible) */}
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
            
            /* CASO A: EJECUCIÓN OMITIDA (Imágenes, PDFs, etc) */
            <div className="card skipped" style={{gridColumn: "1 / -1", borderColor: '#e3b341', borderTop: '3px solid #e3b341'}}>
              <h2 style={{color: '#e3b341'}}>⚠️ EJECUCIÓN OMITIDA</h2>
              <p>{report.dynamic_analysis.reason}</p>
              <p style={{fontSize: '0.9em', color: 'rgba(255,255,255,0.7)', marginTop: '10px'}}>
                Nota: El motor de Sandbox Dinámico actual solo detona scripts ejecutables (.py). 
                Sin embargo, el análisis estático superior (Hash e IOCs) sigue siendo válido.
              </p>
            </div>

          ) : (

            /* CASO B: EJECUCIÓN COMPLETA (Python Malware) */
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

        </div>
      )}
    </div>
  )
}

export default App