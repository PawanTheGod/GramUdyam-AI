import React from 'react';

interface ScoreRingProps {
  score: number;
  size?: number;
  label?: string;
}

const ScoreRing: React.FC<ScoreRingProps> = ({ score, size = 100, label }) => {
  const radius = (size - 10) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = score >= 70 ? '#16a34a' : score >= 45 ? '#f59e0b' : '#dc2626';

  return (
    <div className="score-ring" style={{ width: size, height: size }}>
      <svg width={size} height={size}>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="6" />
        <circle
          cx={size / 2} cy={size / 2} r={radius}
          fill="none" stroke={color} strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.8s ease' }}
        />
      </svg>
      <div className="score-value" style={{ color }}>
        {score.toFixed(0)}
        {label && <span className="score-label">{label}</span>}
      </div>
    </div>
  );
};

export default ScoreRing;
