import { useState } from 'react'
import './App.css'

function App() {
  const [pgn, setPgn] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyzeGame = async () => {
    if (!pgn.trim()) {
      setError('Please enter a PGN.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pgn }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Analysis failed.')
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app">
      <header className="header">
        <div>
          <h1>FORTRESS</h1>
          <p>Chess Anomaly Detection</p>
        </div>
      </header>

      <section className="analysis-card">
        <div className="section-heading">
          <h2>Analyze Game</h2>
          <span>PGN</span>
        </div>

        <textarea
          value={pgn}
          onChange={(event) => setPgn(event.target.value)}
          placeholder="Paste a chess game in PGN format..."
          rows={12}
        />

        <button
          type="button"
          onClick={analyzeGame}
          disabled={loading}
        >
          {loading ? 'Analyzing Game...' : 'Analyze Game'}
        </button>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {result && (
          <section className="results">
            <div className="results-header">
              <div>
                <p className="eyebrow">Analysis Complete</p>
                <h2>Game Assessment</h2>
              </div>

              <div
                className={`status-badge ${
                  result.anomaly_label === 'ANOMALOUS'
                    ? 'anomalous'
                    : 'normal'
                }`}
              >
                {result.anomaly_label}
              </div>
            </div>

            <div className="score-card">
              <p className="score-label">Isolation Score</p>
              <p className="score-value">
                {result.isolation_score.toFixed(4)}
              </p>
              <p className="score-note">
                Lower values indicate greater deviation from the
                model's learned baseline.
              </p>
            </div>

            <div className="feature-grid">
              <div className="feature-card">
                <span>Average CPL</span>
                <strong>
                  {result.features.average_centipawn_loss.toFixed(2)}
                </strong>
              </div>

              <div className="feature-card">
                <span>Median CPL</span>
                <strong>
                  {result.features.median_centipawn_loss.toFixed(2)}
                </strong>
              </div>

              <div className="feature-card">
                <span>Top-1 Agreement</span>
                <strong>
                  {result.features.top1_agreement_percentage.toFixed(1)}%
                </strong>
              </div>

              <div className="feature-card">
                <span>Top-3 Agreement</span>
                <strong>
                  {result.features.top3_agreement_percentage.toFixed(1)}%
                </strong>
              </div>

              <div className="feature-card">
                <span>High CPL Moves</span>
                <strong>
                  {result.features.high_centipawn_loss_percentage.toFixed(1)}%
                </strong>
              </div>

              <div className="feature-card">
                <span>Moves Analyzed</span>
                <strong>
                  {result.features.analyzed_move_count}
                </strong>
              </div>
            </div>

            <div className="disclaimer">
              <strong>Important:</strong> FORTRESS identifies
              statistically unusual game behavior. An anomalous result
              is not proof of cheating.
            </div>
          </section>
        )}
      </section>
    </main>
  )
}

export default App